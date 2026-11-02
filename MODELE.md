# Socle « outil speaker » — mode d'emploi pour une nouvelle course

Ce dépôt a servi au MAIF Ekiden de Paris 2026. Il sert maintenant de **modèle** pour d'autres
courses sur route ou de cross. Ce document résume la méthode, les fichiers à demander, les outils
fournis et les pièges à éviter.

## 1. Ce que contient le socle

| Élément | Rôle |
|---|---|
| `index.html` | Le site (une seule page, sans installation) : onglets Dossard, Recherche, Repérés, Dossier, Micro, Live. Fonctionne hors connexion une fois ouvert. |
| `data/startlist.json` | Tous les engagés (produit par `outils/startlist_vers_json.py`). |
| `data/reperes.json` | Athlètes et équipes repérés, rédigés à la main (modifiable directement sur GitHub). |
| `data/ffa.json` | Liens FFA, palmarès, SB/PB (produit depuis Media Sheet par `outils/import_media_sheet.py`). |
| `docs/` | PDF téléchargeables depuis le site (fiche une page, texte d'avant-départ). |
| `outils/startlist_vers_json.py` | Excel d'engagés de l'organisateur → `data/startlist.json` (relais ou course individuelle). |
| `outils/excel_media_sheet.py` | Engagés → Excel directement importable dans Media Sheet (onglets « épreuve Hommes / Femmes »). |
| `outils/import_media_sheet.py` | Fichier `.json` de meeting Media Sheet → `data/ffa.json`, avec contrôle nom + âge. |
| `outils/fiche_1page/` | Fiche speaker A4 paysage d'une page (favoris + repérés dans l'ordre des dossards). |

## 2. À demander à l'organisateur

1. **La liste des engagés en Excel** : prénom, nom, sexe, âge ou année de naissance, dossard,
   équipe/club, catégorie. Pour un relais : dossard au format « équipe.relayeur » (310.2) ou
   colonnes Dossard + Ordre.
2. **Le roadbook / programme** : horaires, distances, parcours (image du plan), animations.
3. **Les messages partenaires** à lire au micro.
4. **Les records de l'épreuve** et le palmarès des éditions précédentes.
5. **Le lien du live** (chronométreur) et l'affiche / les visuels pour reprendre la charte.
6. **Les VIP attendus** : élus, dirigeants des sponsors, personnalités, équipes « à signaler ».

## 3. Déroulé (de J-7 à J)

1. **Engagés** : `python outils/startlist_vers_json.py engages.xlsx data/startlist.json --maj "Startlist du JJ/MM/AAAA"`.
2. **Repérage** :
   - internationaux : croisement nom + prénom + âge (±1 an) avec la base des biographies FFA
     (athle.fr, rubrique biographies), puis vérification de chaque fiche ;
   - personnalités : croisement avec Wikidata (personnalités françaises nées depuis 1946, ~65 métiers,
     en gardant le nombre d'articles Wikipédia pour écarter les homonymes d'élus locaux) ;
   - recherche ciblée sur les équipes au nom évocateur (médias, sponsors, institutions, police, armée…) ;
   - tout profil non certain est marqué « À VÉRIFIER » dans `data/reperes.json`.
3. **Stats FFA de masse** (Media Sheet) :
   - `python outils/excel_media_sheet.py --categorie FFA --club clubs.xlsx` (colonne Club seulement si
     le nom d'équipe est un vrai club), et sans `--club` pour les entreprises ;
   - nommer l'épreuve comme la FFA : `--epreuve "Cross long"`, `"10 Km Route"`, `"1/2 Marathon"`…
   - lancer Media Sheet (bios IA désactivées), **confirmer les homonymes**, récupérer le fichier
     `store/meetings/<id>.json` ;
   - `python outils/import_media_sheet.py meeting1.json meeting2.json data/ffa.json`.
4. **Adapter le site** (`index.html`) : titre et bandeau, distances des relais (`DIST`), catégories
   (`CAT`), records et allures du chrono (onglet Live), contenu des onglets Dossier et Micro, lien live,
   image de l'affiche (`img/`), couleurs (variables en haut du fichier).
5. **Publier** : pousser sur GitHub, Settings → Pages → branche `main`, dossier racine.
   Augmenter la version dans `sw.js` (`ekiden26-vN`) à chaque mise à jour.
6. **Documents papier** : fiche une page (`outils/fiche_1page/`) et texte d'avant-départ à deux voix.
7. **La veille** : ouvrir le site en ligne sur chaque téléphone (copie hors connexion).

## 4. Pièges rencontrés (à ne pas refaire)

- Les tableurs contiennent des cellules « NaN » : un navigateur refuse alors tout le fichier JSON.
  Les outils écrivent avec `allow_nan=False`.
- **Homonymes** : Media Sheet (surtout via World Athletics) peut se tromper de personne
  (« Lucien … Massong » pris pour Lucie Jean-Charles). `import_media_sheet.py` rejette tout profil
  dont prénom, nom ou âge ne collent pas ; la liste des rejets est écrite à côté.
- Le nom d'équipe en colonne Club n'aide que si c'est un vrai club, et sans mots vagues
  (« athlétisme », « club »…), sinon il fait choisir le mauvais homonyme.
- Les inscrits sans dossard (remplaçants) cachent parfois des têtes d'affiche (Navarro en 2026).
- Les notes ajoutées sur le téléphone restent sur ce téléphone (bouton « Copier mes notes »).
- Données personnelles : le dépôt est public. Ne publier que ce qui figurera dans les résultats
  officiels, et seulement avec l'accord de l'organisateur.

## 5. Adapter à une course individuelle (route, cross)

`startlist_vers_json.py` transforme un dossard simple en « équipe » d'un seul coureur : la recherche
et l'onglet Repérés fonctionnent tels quels. À adapter dans `index.html` : `DIST` (une seule distance),
l'affichage « R1 », les catégories (souvent des catégories d'âge : SE, M0…). Voir `ROADMAP.md`.
