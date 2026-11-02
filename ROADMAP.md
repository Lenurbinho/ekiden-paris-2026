# Pistes d'amélioration et version piste / salle

## A. Saisie des dossards (retours de l'Ekiden 2026)

1. ✅ **Pavé numérique intégré** : grosses touches 0-9, « . » et OK en bas d'écran, sans le clavier
   Android. Plus rapide, utilisable d'une main, sans que le clavier cache la fiche.
2. ✅ **Bouton « Effacer »** (✕) dans la case, et effacement automatique quand on recommence à taper
   après avoir consulté une fiche.
3. ✅ **Dictée vocale** : bouton micro → « trois cent dix point deux » → 310.2. Possible avec la
   reconnaissance vocale de Chrome sur Android, mais **elle demande du réseau** : prévoir le pavé en secours.
4. ✅ **Historique** des 10 derniers dossards consultés, en pastilles à toucher.
5. **Relais suivant / précédent** d'un geste (balayage) sur la fiche équipe.

## B. Pendant la course

6. **« Équipes à suivre »** : épingler 5 à 10 équipes (favoris, VIP) en haut de l'écran.
7. **Chrono enrichi** : temps de passage théoriques aux allures record, écart à annoncer.
8. **Résultats en direct** : lien profond vers le live du chronométreur pour un dossard
   (à étudier selon le chronométreur).
9. **Notes partagées entre les deux speakers** : nécessite un petit espace de stockage en ligne
   commun ; aujourd'hui chaque téléphone garde ses notes.

## C. Préparation plus rapide

10. **Fichier de réglages `course.json`** (titre, date, distances, catégories, records, couleurs,
    lien live) : on ne toucherait plus à `index.html` d'une course à l'autre.
11. **Onglet « Chiffres clés » généré automatiquement** : nombre d'équipes, % de femmes, doyen et
    benjamin, plus grosse entreprise, clubs les plus représentés, noms d'équipe insolites.
12. **Import Media Sheet sans ordinateur** : déposer le fichier `.json` directement dans le site.
13. **Dépôt modèle** : un dépôt GitHub « outil-speaker-modele » à copier pour chaque nouvelle course.

## D. Version piste / salle — à étudier

La différence de fond : sur route, l'entrée est **le dossard** ; sur piste, c'est **l'épreuve**,
avec plusieurs épreuves en même temps (une course + deux ou trois concours).

**Ce qui change :**
- **Onglet « Maintenant »** : les épreuves en cours et à venir dans les 30 minutes, côte à côte
  (ex. 400 m haies série 2 · perche F · triple saut H), à partir de l'horaire.
- **Fiche épreuve** : liste de départ avec couloirs ou ordre de passage, records (meeting, France,
  catégorie), minima, meilleures perfs de la saison, favoris. **Media Sheet calcule déjà tout cela**
  par épreuve : le site pourrait lire directement son fichier de meeting.
- **Concours** : suivi essai par essai (barre en cours, classement provisoire), au moins en saisie
  rapide manuelle ; à défaut, lien vers les résultats en direct.
- **Séries → finales** : qualifiés (Q/q) et nouvelle composition, que Media Sheet sait réarranger.
- **Recherche par dossard conservée** : un athlète engagé sur plusieurs épreuves affiche toutes
  ses épreuves et horaires.
- **Salle** : épreuves courtes (60 m, 60 m haies), records salle, enchaînements serrés.
- **Deux speakers** : répartition piste / concours, avec un filtre « mes épreuves ».

**Questions à trancher avant de construire :**
- La source des horaires et startlists (Direct FFA `athle.fr/direct`, logiciel de l'organisateur ?).
- Les résultats en direct sont-ils accessibles pendant la réunion ?
- Téléphone, tablette ou ordinateur au micro ? (une tablette permet deux colonnes : course + concours)
- Le stade a-t-il du réseau fiable ? (sinon tout doit être chargé avant)
