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

## D. Version piste / salle : un « CIS hybride »

Principe : pas de suivi live branché, mais un écran de type CIS (système d'information de
compétition) qui suit l'horaire, avec la **possibilité d'entrer les perfs à la main** au fil de la
réunion, par le speaker ou par une deuxième personne pendant que le speaker parle.

### Données préparées avant la réunion
- Horaire complet : épreuve, catégorie, tour (série / finale / qualif), heure, lieu (piste, sautoir…),
  mode de qualification (ex. « 3Q + 2q »).
- Listes de départ par série (couloirs) ou ordre de passage (concours).
- Stats par athlète : SB, PB, records, palmarès, minima. **Media Sheet calcule déjà tout cela** :
  le site lirait directement son fichier de meeting.

### Écrans
1. **Bandeau horaire** affichable / masquable à la demande : liste des épreuves avec l'heure,
   ligne « maintenant », statut (à venir, en cours, terminée), bouton **« +5 min »** pour décaler
   la suite quand la réunion prend du retard.
2. **Vue « Maintenant »** : épreuves proposées selon l'heure ; on en épingle 2 à 4, affichées côte à côte
   (tablette) ou en onglets à balayer (téléphone). Choix de la série (S1, S2… finale).
3. **Fiche course** : couloir, nom, club, SB/PB, records à battre en tête.
   - Saisie des temps couloir par couloir avec le pavé intégré (format automatique 10"52, 1'52"30).
   - Classement de la série calculé aussitôt ; **Q et q calculés automatiquement** série après série
     selon la règle (places puis meilleurs temps), corrigeables d'un tap.
   - Vue « bilan des séries » et composition de la finale.
4. **Concours horizontaux** (longueur, triple, lancers) : grille d'essais (perf, X, –), meilleure marque,
   **classement qui se met à jour à chaque essai** ; après 3 essais, les 8 meilleurs continuent :
   les autres sont masqués (option) et l'ordre de passage est inversé.
5. **Concours verticaux** (hauteur, perche) : barres successives, O / X / –, **éliminé après 3 échecs
   consécutifs** (masqué automatiquement), classement selon la règle (barre franchie, échecs à cette
   barre, total des échecs).
6. **Alertes speaker** : quand une perf saisie bat le SB, le PB, la meilleure perf de l'engagement,
   le record du meeting ou un minima → pastille « PB ! », « Record du meeting »…
7. **Recherche par dossard** : toutes les épreuves d'un athlète, avec horaires et perfs déjà saisies.

### Point technique décisif : la saisie par une deuxième personne
Pour qu'une personne entre les perfs sur son téléphone et que le speaker les voie sur le sien,
il faut un **petit espace de stockage en ligne partagé** (le site actuel, hébergé sur GitHub Pages,
ne garde rien en ligne). Sans réseau, chaque appareil continue en local.

### Décisions (2 novembre 2026)
- **Tablette en priorité**, téléphone en secours (affichage côte à côte sur tablette, onglets sur téléphone).
- **Saisie partagée : idée gardée, pas dans la première version.** Les modifications devront
  apparaître à l'identique chez tous les utilisateurs. Piste retenue : une **feuille Google Sheets
  + un petit script Google (Apps Script)** servant de relais gratuit, dans le Drive d'Alexandre
  (synchronisation en quelques secondes ; repli local sans réseau). GitHub écarté pour le direct.
- **Projet dédié** : nouveau dépôt GitHub et projet Claude séparés de l'Ekiden.
- Données test : fichier de meeting Media Sheet + horaire, à fournir.
