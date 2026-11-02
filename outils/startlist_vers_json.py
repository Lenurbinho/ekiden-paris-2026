"""Transforme le fichier d'engagés de l'organisateur (Excel) en data/startlist.json pour le site.

Gère les deux cas :
  - RELAIS : dossard « 310.2 » (équipe 310, relayeur 2), ou colonnes séparées Dossard + Ordre ;
  - COURSE INDIVIDUELLE (cross, route) : dossard simple « 1542 » → une « équipe » d'un seul coureur.
Les inscrits sans dossard sont rangés dans « sansDossard », rattachés à leur équipe si son nom
est unique.

Colonnes reconnues (insensible à la casse/aux accents) : prénom, nom, sexe, âge OU année de
naissance, équipe/club, dossard, ordre, compétition/catégorie.

Usage :
  python outils/startlist_vers_json.py engages.xlsx data/startlist.json --maj "Startlist du 31/10/2026"
  (option --cat "Libellé=CODE" répétable pour raccourcir les catégories affichées)
"""
import argparse
import datetime
import json
import math
import re
import unicodedata

from openpyxl import load_workbook

CAT_DEFAUT = {"grand public": "GP", "entreprises formule classique": "EC",
              "entreprises formule privilege": "EP", "clubs ffa": "FFA"}
ALIAS = {
    "prenom": ["prenom", "prenoms", "first name", "firstname"],
    "nom": ["nom", "nom de famille", "last name", "lastname", "surname"],
    "sexe": ["sexe", "genre", "sex", "s"],
    "age": ["age", "age a la date de l'edition", "age a la date de l edition"],
    "annee": ["annee", "annee de naissance", "naissance", "ne en", "date de naissance", "ddn"],
    "equipe": ["equipe", "club", "team", "nom equipe", "structure"],
    "dossard": ["dossard", "dos", "bib", "dossard equipe", "n dossard", "no dossard"],
    "ordre": ["ordre", "relais", "relayeur", "ordre de passage"],
    "competition": ["competition", "categorie", "course", "epreuve", "formule"],
}


def norm(s):
    s = unicodedata.normalize("NFKD", str(s or "")).encode("ascii", "ignore").decode().lower()
    return re.sub(r"\s+", " ", re.sub(r"[^a-z0-9' ]", " ", s)).strip()


def vide(v):
    return v is None or (isinstance(v, float) and math.isnan(v)) or str(v).strip() in ("", "nan", "None")


def age_de(ligne, col, annee_course):
    if col.get("age") is not None and not vide(ligne[col["age"]]):
        try:
            a = int(float(str(ligne[col["age"]]).strip()))
            return a if 5 <= a <= 110 else None
        except ValueError:
            pass
    if col.get("annee") is not None and not vide(ligne[col["annee"]]):
        v = ligne[col["annee"]]
        if isinstance(v, (datetime.date, datetime.datetime)):
            return annee_course - v.year
        m = re.search(r"(19|20)\d\d", str(v))
        if m:
            return annee_course - int(m.group(0))
    return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("entree")
    ap.add_argument("sortie")
    ap.add_argument("--maj", default="")
    ap.add_argument("--annee", type=int, default=datetime.date.today().year)
    ap.add_argument("--cat", action="append", default=[], help='"Libellé=CODE"')
    a = ap.parse_args()
    cats = dict(CAT_DEFAUT)
    for c in a.cat:
        k, v = c.split("=", 1)
        cats[norm(k)] = v

    wb = load_workbook(a.entree, read_only=True, data_only=True)
    ws = wb.worksheets[0]
    lignes = list(ws.iter_rows(values_only=True))
    entete = [norm(x) for x in lignes[0]]
    col = {}
    for cle, alias in ALIAS.items():
        for i, h in enumerate(entete):
            if h in alias and cle not in col:
                col[cle] = i
    manque = [k for k in ("prenom", "nom", "dossard") if k not in col]
    if manque:
        raise SystemExit(f"Colonnes introuvables : {manque}. En-têtes lus : {lignes[0]}")

    equipes, sans = {}, []
    for L in lignes[1:]:
        if all(vide(x) for x in L):
            continue
        prenom = str(L[col["prenom"]] or "").strip()
        nom = str(L[col["nom"]] or "").strip()
        sexe = norm(L[col["sexe"]])[:1].upper() if "sexe" in col else ""
        sexe = {"H": "M"}.get(sexe, sexe)
        age = age_de(L, col, a.annee)
        eq = str(L[col["equipe"]] or "").strip() if "equipe" in col else ""
        cat_lib = str(L[col["competition"]] or "").strip() if "competition" in col else ""
        cat = cats.get(norm(cat_lib), cat_lib)
        dos = str(L[col["dossard"]] or "").strip().replace(",", ".")
        ordre = None
        m = re.fullmatch(r"(\d+)(?:\.0)?(?:[.\-/ ](\d+))?", dos)
        if m and m.group(2):
            num, ordre = int(m.group(1)), int(m.group(2))
        elif m:
            num = int(m.group(1))
            if "ordre" in col and not vide(L[col["ordre"]]):
                ordre = int(float(L[col["ordre"]]))
        else:
            sans.append([None, prenom, nom, sexe, age, eq, cat])
            continue
        t = equipes.setdefault(num, {"d": num, "e": eq or f"{prenom} {nom}", "c": cat, "r": {}})
        t["r"][ordre or 1] = [prenom, nom, sexe, age]

    sortie = []
    for num in sorted(equipes):
        t = equipes[num]
        r = [t["r"][k] for k in sorted(t["r"])]
        sx = {x[2] for x in r}
        t2 = {"d": num, "e": t["e"], "c": t["c"], "t": "X" if len(sx) > 1 else (next(iter(sx)) or "X").replace("M", "H"), "r": r}
        sortie.append(t2)
    par_nom = {}
    for t in sortie:
        par_nom.setdefault(norm(t["e"]), []).append(t["d"])
    for s in sans:
        ds = par_nom.get(norm(s[5]), [])
        s[0] = ds[0] if len(ds) == 1 else None
    data = {"maj": a.maj or f"Startlist importée le {datetime.date.today():%d/%m/%Y}",
            "teams": sortie, "sansDossard": [x[:6] for x in sans]}
    txt = json.dumps(data, ensure_ascii=False, separators=(",", ":"), allow_nan=False)
    open(a.sortie, "w", encoding="utf-8").write(txt)
    nb = sum(len(t["r"]) for t in sortie)
    print(f"{len(sortie)} dossards/équipes, {nb} coureurs, {len(sans)} sans dossard → {a.sortie}")


if __name__ == "__main__":
    main()
