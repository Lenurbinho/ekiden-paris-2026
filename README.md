# Ekiden Paris 2026 · outil speaker

Site mobile pour les speakers du MAIF Ekiden de Paris (1er novembre 2026).

- **Dossard** : taper `310` (équipe) ou `310.2` (équipe 310, relais 2).
- **Recherche** : par nom, prénom ou équipe ; filtres ★ Repérés, Équipes notées, Sans dossard.
- **Dossier** : essentiel, horaires, records, histoire, plateau, parcours, mémo terrain.
- **Micro** : messages partenaires de l'organisation.
- **Live** : lien Breizh Chrono, temps de course et notes perso.

## Ajouter ou corriger un athlète repéré
Modifier `data/reperes.json` directement sur GitHub (crayon ✎), puis « Commit changes ».
Le site se met à jour en 1 à 2 minutes. Format d'un bloc :

```json
{"dossard": "310.2", "titre": "International · 800 m", "texte": "Ce qu'il faut dire au micro."},
```

Les notes ajoutées depuis le téléphone (bouton « + note ») restent sur ce téléphone.
