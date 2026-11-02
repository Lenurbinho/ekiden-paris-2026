"""Prépare un fichier Excel d'engagés directement importable dans Media Sheet.

Lit data/startlist.json (format du site) et écrit un classeur à deux onglets
« <épreuve> Hommes » / « <épreuve> Femmes » : Media Sheet déduit l'épreuve ET le sexe du nom
de l'onglet. Dossard au format équipe.ordre (relais) ou numéro simple (course individuelle).

Exemples :
  python outils/excel_media_sheet.py --categorie FFA --club sortie.xlsx
  python outils/excel_media_sheet.py --categorie EP sortie.xlsx
  python outils/excel_media_sheet.py --epreuve "Cross long" sortie.xlsx

Options :
  --categorie X   ne garder que les équipes de cette catégorie (FFA, EP, EC, GP…) ; défaut : toutes
  --club          recopier le nom d'équipe (nettoyé) en colonne Club. À n'utiliser QUE si le nom
                  d'équipe est vraiment un club : Media Sheet s'en sert pour départager les homonymes.
  --epreuve NOM   nom d'épreuve FFA (défaut « 10 Km Route ») : « Cross long », « 5 Km Route »,
                  « 1/2 Marathon », « Marathon »… (une distance en km = route, jamais piste).
"""
import argparse
import json
import os
import re
import unicodedata

from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill

ICI = os.path.dirname(os.path.abspath(__file__))
FAUX = set("X XX XXX Z ZZ DOE RELAIS CHRONO DEPART SPRINT TURBO TROIS CINQ SIX QUATRE".split())
GENERIQUES = set("ATHLETISME ATHLETIC ATHLETICS ATHLE CLUB TEAM EQUIPE RUNNING RUNNERS RUN COURSE SPORT "
                 "SPORTS ASSOCIATION ENTENTE UNION AMICALE OLYMPIQUE STADE HOMMES FEMMES MIXTE DAMES "
                 "MASTERS MASTER EQ DE DU DES LA LE LES ET POUR CLUBS ELITE".split())


def sans_accent(s):
    return unicodedata.normalize("NFKD", s or "").encode("ascii", "ignore").decode()


def club_propre(nom_equipe):
    """« AS CHELLES ATHLETISME N°2 » → « AS CHELLES » : on retire les mots trop vagues, qui
    feraient choisir le mauvais homonyme, et les numéros d'équipe."""
    t = [m for m in re.split(r"[^A-Za-z0-9]+", sans_accent(nom_equipe)) if m]
    garde = [m for m in t if m.upper() not in GENERIQUES and not m.isdigit() and len(m) > 1
             and not re.fullmatch(r"(?i)n\d+|[IVX]+", m)]
    return " ".join(garde)


def bidon(prenom, nom):
    a = f"{prenom or ''} {nom or ''}".strip()
    if re.search(r"\d", a):
        return True
    toks = re.sub(r"[^A-Za-zÀ-ÿ ]", " ", a).upper().split()
    if len(toks) < 2 or any(len(x) <= 1 for x in toks) or set(toks) & FAUX:
        return True
    return (prenom or "").strip().upper() == (nom or "").strip().upper()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("sortie")
    ap.add_argument("--categorie")
    ap.add_argument("--club", action="store_true")
    ap.add_argument("--epreuve", default="10 Km Route")
    ap.add_argument("--startlist", default=os.path.join(ICI, "..", "data", "startlist.json"))
    a = ap.parse_args()

    S = json.load(open(a.startlist, encoding="utf-8"))
    equipes = [t for t in S["teams"] if not a.categorie or t["c"] == a.categorie]
    ids = {t["d"]: t for t in equipes}
    lignes, titulaires = {"M": [], "F": []}, set()
    for t in equipes:
        for i, r in enumerate(t["r"]):
            dos = f"{t['d']}.{i + 1}" if len(t["r"]) > 1 else str(t["d"])
            lignes[r[2]].append((t["d"], i + 1, [dos, i + 1, r[1].strip(), r[0].strip(),
                                                 club_propre(t["e"]) if a.club else "", r[3], t["e"], ""]))
            titulaires.add((r[1].strip().upper(), r[0].strip().upper()))
    vus = set()
    for d, p, n, sx, age, eq in S.get("sansDossard", []):
        if d not in ids or bidon(p, n):
            continue
        k = ((n or "").strip().upper(), (p or "").strip().upper())
        if k in titulaires or k in vus:
            continue
        vus.add(k)
        lignes[sx if sx in ("M", "F") else "M"].append(
            (d, 9, [f"{d}.R", "R", n.strip(), p.strip(), club_propre(ids[d]["e"]) if a.club else "", age,
                    ids[d]["e"], "Remplaçant sans dossard"]))

    wb = Workbook()
    wb.remove(wb.active)
    entete = ["Dossard", "Ordre", "Nom", "Prénom", "Club", "Age", "Nom équipe", "Remarque"]
    for sx, suffixe in (("M", "Hommes"), ("F", "Femmes")):
        ws = wb.create_sheet(f"{a.epreuve} {suffixe}"[:31])
        ws.append(entete)
        for c in ws[1]:
            c.font = Font(bold=True, color="FFFFFF")
            c.fill = PatternFill("solid", fgColor="001D46")
        for r in sorted(lignes[sx], key=lambda r: (r[0], r[1])):
            ws.append(r[2])
        for col, w in zip("ABCDEFGH", (10, 7, 24, 18, 26, 6, 36, 24)):
            ws.column_dimensions[col].width = w
        ws.freeze_panes = "A2"
        print(ws.title, len(lignes[sx]))
    wb.save(a.sortie)


if __name__ == "__main__":
    main()
