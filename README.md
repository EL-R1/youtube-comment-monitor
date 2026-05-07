# youtube-comment-tracker

Surveille les commentaires de vidéos YouTube et notifie sur Discord les **suppressions** et **modifications**.

## Fonctionnement

1. **Récupération** : via `yt-dlp` (pas de clé API YouTube nécessaire)
2. **Snapshot** : un snapshot par vidéo dans chaque environnement (`data/{environment}/{video_id}.json`, cache GitHub Actions)
3. **Diff** : à chaque exécution, comparaison avec le snapshot précédent
4. **Notification** : seuls les commentaires supprimés et modifiés sont envoyés sur Discord

## Architecture

- Les **environnements GitHub** isolent les configurations par projet
- Chaque environnement a ses propres `VIDEO_IDS`, `DISCORD_WEBHOOK_URL`, `YOUTUBE_COOKIES`
- Le workflow détecte automatiquement tous les environnements du repo
- Un job parallèle par environnement, une boucle séquentielle par vidéo

## Prérequis

- Python 3.10+
- Cookies YouTube exportés

## Installation locale

```bash
pip install -r requirements.txt
```

## Utilisation

```bash
COOKIES_FILE=cookies.txt \
VIDEO_ID=tsvRQc8GsDE \
SNAPSHOT_PATH=data/snapshot.json \
python -m src.main
```

## Configuration GitHub Actions

### Dans chaque environnement GitHub

| Type | Nom | Description |
|---|---|---|
| Variable | `VIDEO_IDS` | `["abc123","def456"]` |
| Variable | `NOTIFY_MODIFIED` | `"true"` ou `"false"` (optionnel) |
| Secret | `DISCORD_WEBHOOK_URL` | Webhook Discord |
| Secret | `YOUTUBE_COOKIES` | Cookies YouTube |

### Exporter les cookies

```bash
# Depuis votre navigateur, exporter les cookies au format Netscape
# Extension : "Get cookies.txt LOCALLY" (Chrome) ou "cookies.txt" (Firefox)
# Coller le contenu dans le secret YOUTUBE_COOKIES
```

Le workflow s'exécute toutes les 6h. Déclenchement manuel depuis l'onglet Actions.
