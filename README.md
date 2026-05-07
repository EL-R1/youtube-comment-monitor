# youtube-comment-tracker

Surveille les commentaires de vidéos YouTube et notifie sur Discord les **suppressions** et **modifications**.

## Fonctionnement

1. **Récupération** : via `yt-dlp` (pas de clé API YouTube nécessaire)
2. **Snapshot** : l'état des commentaires est stocké dans `data/snapshot.json` (cache GitHub Actions, pas dans git)
3. **Diff** : à chaque exécution, comparaison avec le snapshot précédent
4. **Notification** : seuls les commentaires supprimés et modifiés sont envoyés sur Discord

## Prérequis

- Python 3.10+
- Cookies YouTube exportés (pour les vidéos qui le nécessitent)

## Installation locale

```bash
pip install -r requirements.txt
```

## Utilisation

```bash
COOKIES_FILE=cookies.txt VIDEO_ID=tsvRQc8GsDE python -m src.main
```

## Déploiement GitHub Actions

### Variables à configurer

| Variable | Description |
|---|---|
| `VIDEO_IDS` | Tableau JSON des IDs YouTube, ex: `["abc123","def456"]` |
| `NOTIFY_MODIFIED` | `"true"` (défaut) ou `"false"` |

### Secrets à configurer

| Secret | Description |
|---|---|
| `DISCORD_WEBHOOK_URL` | URL du webhook Discord |
| `YOUTUBE_COOKIES` | Contenu du fichier `cookies.txt` (optionnel) |

### Exporter les cookies YouTube

```bash
# Depuis votre navigateur, exporter les cookies au format Netscape
# Extension recommandée : "Get cookies.txt LOCALLY"
# Coller le contenu dans le secret GitHub YOUTUBE_COOKIES
```

Le workflow s'exécute automatiquement toutes les 6h pour chaque vidéo, et peut être déclenché manuellement depuis l'onglet Actions.
