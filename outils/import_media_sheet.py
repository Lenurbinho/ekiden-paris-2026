"""Convertit un ou plusieurs meetings Media Sheet (store/meetings/<id>.json) en data/ffa.json pour le site Ekiden.

- Tous les athlètes résolus (avec lien de fiche) : lien FFA.
- Palmarès national / international / records : affichés, et l'athlète entre dans « Repérés ».
- Ligne demi-fond : « épreuve SB / PB (année) », du 800 m au marathon, route comprise.

Usage : python import_media_sheet.py meeting.json [autre.json ...] sortie_ffa.json
"""
import json
import re
import sys

import os

# Réutilise les règles de Media Sheet si son dossier est disponible (variable MEDIA_SHEET),
# sinon une version simplifiée intégrée.
sys.path.insert(0, os.environ.get("MEDIA_SHEET", "../alex-brunel-media-sheet"))
try:
    from core.cross import _libelle_court, est_demi_fond  # noqa: E402
except ImportError:
    def _libelle_court(ep):
        s = re.sub(r"(?i)\s*-?\s*(salle|piste courte)", "", ep).strip()
        s = re.sub(r"(\d) (\d{3})", r"\1\2", s)
        s = re.sub(r"(?i)\bkm route\b", "km route", s)
        if re.fullmatch(r"(?i)1/2 marathon|semi-marathon", s):
            return "semi-marathon"
        s = s.replace("Steeple", "steeple").replace("Marathon", "marathon")
        return re.sub(r"(?i)(\d+) km route", r"\1 km route", s)

    def est_demi_fond(ep):
        c = _libelle_court(ep).lower()
        m = re.match(r"(\d+)m", c)
        if "haies" in c or "marche" in c:
            return False
        if m and not c.endswith("route"):
            return int(m.group(1)) >= 800
        return bool(re.search(r"km route|marathon|mile", c))

ORDRE = ["800m", "1000m", "1500m", "mile", "2000m", "3000m", "3000m steeple", "5000m", "10000m",
         "5 km route", "10 km route", "15 km route", "20 km route", "semi-marathon", "marathon"]
MAX_EPREUVES = 7
PRIORITE = ["10 km route", "5 km route", "5000m", "10000m", "semi-marathon", "1500m", "marathon", "3000m",
            "800m", "3000m steeple", "20 km route", "15 km route", "mile", "1000m", "2000m"]
VIDE = {"", "aucun", "none", "-", "nan"}


def vide(s):
    return str(s or "").strip().lower() in VIDE


def perf_jolie(p):
    p = re.sub(r"\s*\((\d{2})\)\s*$", "", p).strip()
    p = re.sub(r"\s*\([A-Za-z]{1,3}\)\s*$", "", p).strip()       # marqueurs du type « (F) »
    return p.replace("''", '"')


def parse(liste):
    """'ep : perf (aa) | …' → {libellé : (perf, annee)} sur le demi-fond.
    Le plein air prime ; la salle (« Piste Courte ») n'est gardée que s'il n'y a rien dehors."""
    out, salle = {}, {}
    for e in str(liste or "").split("|"):
        if " : " not in e:
            continue
        ep, perf = (x.strip() for x in e.split(" : ", 1))
        if re.search(r"\(\d", ep) or not est_demi_fond(ep):    # ex. steeple cadets « (91) »
            continue
        est_salle = bool(re.search(r"(?i)piste courte|salle", ep))
        lib = _libelle_court(ep)
        if lib in out and not (salle.get(lib) and not est_salle):
            continue
        m = re.search(r"\((\d{2})\)", perf)
        out[lib] = (perf_jolie(perf) + (" (salle)" if est_salle else ""), m.group(1) if m else "")
        salle[lib] = est_salle
    return out


def autres_pb(pb, n=3):
    """PB hors demi-fond (sprint, sauts…) pour ceux qui n'ont rien en demi-fond."""
    res = []
    for e in str(pb or "").split("|"):
        if " : " in e and not re.search(r"(?i)piste courte|salle", e):
            ep, perf = (x.strip() for x in e.split(" : ", 1))
            res.append(f"{ep} {perf_jolie(perf)}")
    return " · ".join(res[:n])


def ligne_df(pb, sb):
    pbs, sbs = parse(pb), parse(sb)
    tous = set(pbs) | set(sbs)
    choisis = sorted(tous, key=lambda l: (PRIORITE.index(l) if l in PRIORITE else 99, l))[:MAX_EPREUVES]
    libs = sorted(choisis, key=lambda l: (ORDRE.index(l) if l in ORDRE else 99, l))
    morceaux = []
    for lib in libs:
        p, a = pbs.get(lib, ("", ""))
        s = sbs.get(lib, ("", ""))[0]
        if s and p and s == p:
            morceaux.append(f"{lib}\t{p} (PB {a})" if a else f"{lib}\t{p} (PB)")
        elif s and not p:
            morceaux.append(f"{lib}\t{s} (SB)")
        else:
            morceaux.append(f"{lib}\t{s or '-'} / {p or '-'}" + (f" ({a})" if a and p else ""))
    return " · ".join(morceaux)


def court(txt, n=6):
    """Garde les n premières lignes de palmarès (séparées par ' / ', ';' ou retours)."""
    parts = [p.strip() for p in re.split(r"\s+/\s+|\s*;\s*|\n", str(txt or "")) if p.strip()]
    return " / ".join(parts[:n]) + (" …" if len(parts) > n else "")


import unicodedata

STARTLIST = os.environ.get("STARTLIST", os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data", "startlist.json"))


def toks(s):
    s = unicodedata.normalize("NFKD", str(s or "")).encode("ascii", "ignore").decode().upper()
    s = re.sub(r"\(.*?\)", " ", s)
    return set(t for t in re.split(r"[^A-Z]+", s) if len(t) > 1)


def coherent(nom_ms, prenom, nom, age, annee, rejets, cle):
    """Le profil trouvé doit porter les mêmes prénom et nom, et l'âge doit coller (±1 an)."""
    a, b = toks(nom_ms), toks(f"{prenom} {nom}")
    if not a or not b or not (a <= b or b <= a):
        rejets.append(f"{cle} : {prenom} {nom} ≠ {nom_ms}")
        return False
    try:
        if age and annee and abs((2026 - int(age)) - int(str(annee)[:4])) > 1:
            rejets.append(f"{cle} : {prenom} {nom} ({age} ans) ≠ né en {annee}")
            return False
    except ValueError:
        pass
    return True


def main(entrees, sortie):
    S = json.load(open(STARTLIST, encoding="utf-8"))
    T = {t["d"]: t for t in S["teams"]}
    SD = S["sansDossard"]
    rejets = []
    res, remp, stats = {}, [], {"athletes": 0, "liens": 0, "palmares": 0, "a_confirmer": 0}
    for chemin in entrees:
        d = json.load(open(chemin, encoding="utf-8"))
        meeting = d.get("meeting", d)
        for ep in meeting.get("epreuves", []):
            for a in ep.get("startlist", []):
                stats["athletes"] += 1
                if a.get("a_confirmer"):
                    stats["a_confirmer"] += 1
                url = a.get("url", "")
                if not url:
                    continue
                f = {"u": url, "nom": a.get("nom", "")}
                if not vide(a.get("palmares_international")):
                    f["int"] = court(a["palmares_international"])
                if not vide(a.get("palmares_national")):
                    f["nat"] = court(a["palmares_national"])
                if not vide(a.get("records")):
                    f["rec"] = a["records"]
                df = ligne_df(a.get("pb"), a.get("sb"))
                if df:
                    f["df"] = df
                else:
                    ap = autres_pb(a.get("pb"))
                    if ap:
                        f["pbx"] = ap
                dos0 = str(a.get("dossard", "")).strip()
                m0 = re.fullmatch(r"(\d+)\.(\d)", dos0)
                annee = a.get("annee", "")
                if m0:
                    t = T.get(int(m0.group(1)))
                    r = t["r"][int(m0.group(2)) - 1] if t else None
                    if not r or not coherent(a.get("nom"), r[0], r[1], r[3], annee, rejets, dos0):
                        continue
                elif re.fullmatch(r"(\d+)\.R", dos0):
                    eq = int(dos0.split(".")[0])
                    cands = [x for x in SD if x[0] == eq and toks(f"{x[1]} {x[2]}") and
                             (toks(f"{x[1]} {x[2]}") <= toks(a.get("nom")) or toks(a.get("nom")) <= toks(f"{x[1]} {x[2]}"))]
                    if not cands or not coherent(a.get("nom"), cands[0][1], cands[0][2], cands[0][4], annee, rejets, dos0):
                        if not cands:
                            rejets.append(f"{dos0} : {a.get('nom')} introuvable chez les remplaçants")
                        continue
                stats["liens"] += 1
                stats["palmares"] += bool(f.get("int") or f.get("nat") or f.get("rec"))
                dos = str(a.get("dossard", "")).strip()
                m = re.fullmatch(r"(\d+)\.(\d)", dos)
                if m:
                    res[dos] = f
                elif re.fullmatch(r"(\d+)\.R", dos):
                    f["equipe"] = dos.split(".")[0]
                    remp.append(f)
    json.dump({"maj": "Media Sheet", "a": res, "remplacants": remp}, open(sortie, "w", encoding="utf-8"),
              ensure_ascii=False, separators=(",", ":"))
    print(stats, "remplaçants:", len(remp), "rejetés:", len(rejets))
    open(sortie + ".rejets.txt", "w", encoding="utf-8").write("\n".join(rejets))


if __name__ == "__main__":
    main(sys.argv[1:-1], sys.argv[-1])
