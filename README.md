# 🇺🇸📈 Trump Invest Alert

Überwacht Donald Trumps Truth-Social-Posts. Claude (KI) prüft jeden neuen Post darauf, ob er für
Investments relevant ist (Zölle, Fed/Zinsen, Krypto, einzelne Firmen, Öl, „Buy …“ usw.).
Bei einem Treffer bekommst du **sofort eine Push-Nachricht aufs Handy**, mit dem Post-Text,
einer deutschen KI-Zusammenfassung, den betroffenen Branchen/Tickern und einem Link zum Original.

```
Truth Social ──► trumpstruth.org-Feed ──► Claude-Bewertung (1–10) ──► ntfy ──► 📱 Push
                    (alle 5 Min, in der GitHub-Cloud, kostenlos – dein Mac kann aus sein)
```

## Einrichtung (ca. 10 Minuten)

### 1. Push-App aufs Handy
1. **ntfy** installieren ([iPhone](https://apps.apple.com/app/ntfy/id1625396347) / [Android](https://play.google.com/store/apps/details?id=io.heckel.ntfy)).
2. In der App **„+“ → Thema abonnieren** und einen geheimen Namen eintragen, z. B.
   einen langen, zufälligen Namen wie `trump-invest-k3x9q7mw2p` (der Name ist wie ein Passwort: wer ihn kennt, kann mitlesen – nirgends öffentlich posten).
3. iPhone: Mitteilungen für ntfy erlauben.

### 2. Claude-Zugang über dein Abo (kostenlos)
Die App nutzt **Claude Code mit deinem Claude-Abo (Pro/Max)**. Es entstehen keine Extrakosten, die paar
Bewertungen pro Tag zählen nur minimal gegen dein normales Nutzungslimit.
Im Terminal ausführen, im Browser mit deinem Claude-Konto bestätigen und den angezeigten Token kopieren:
```bash
claude setup-token
```
Der Token ist ein Jahr gültig und wie ein Passwort zu behandeln.
*(Alternative ohne Abo: API-Key von console.anthropic.com als Secret `ANTHROPIC_API_KEY`, Prepaid, ca. 0,20 $/Monat.)*

### 3. In die Cloud bringen (GitHub, kostenlos)
1. Auf [github.com](https://github.com) ein neues **öffentliches** Repository anlegen (bei öffentlichen Repos sind die Läufe unbegrenzt kostenlos; Key und Thema liegen trotzdem geheim in den *Secrets*), z. B. `trump-invest-alert`.
2. Diesen Ordner hochladen (*Add file → Upload files*, inkl. Ordner `.github`) – oder im Terminal:
   ```bash
   cd ~/Documents/AI/trump-invest-alert && git init && git add . && git commit -m "start" && git branch -M main && git remote add origin https://github.com/DEIN-NAME/trump-invest-alert.git && git push -u origin main
   ```
3. Im Repo: **Settings → Secrets and variables → Actions → New repository secret**
   - `CLAUDE_CODE_OAUTH_TOKEN` = der Token aus Schritt 2
   - `NTFY_TOPIC` = der Themenname aus Schritt 1
4. **Actions**-Tab → „Trump Invest Alert“ → **Run workflow**. Der erste Lauf merkt sich nur die
   bisherigen Posts (damit du nicht 100 alte Nachrichten bekommst). Danach läuft es alle 5 Minuten automatisch.

Fertig ✅

## Ausprobieren auf dem Mac (optional)
```bash
cd ~/Documents/AI/trump-invest-alert
```
```bash
export CLAUDE_CODE_OAUTH_TOKEN=sk-ant-oat01-... NTFY_TOPIC=dein-geheimes-thema
```
```bash
python3 trump_watch.py --test
```
```bash
python3 trump_watch.py --backfill 10
```
`--test` schickt eine Test-Push, `--backfill 10` analysiert die letzten 10 Posts und pusht die relevanten
(ideal, um zu sehen, wie die KI urteilt). `--loop 60` lässt es dauerhaft auf dem Mac laufen (jede Minute).

## Einstellungen
| Was | Wo | Standard |
|---|---|---|
| Ab welcher Relevanz gepusht wird (1–10) | GitHub → Settings → Variables → `MIN_RELEVANCE` | `6` |
| KI-Modell | GitHub → Settings → Variables → `CLAUDE_MODEL` (z. B. `claude-sonnet-5-5`, genauer, verbraucht mehr vom Abo-Limit) | `claude-haiku-5-5` |
| Was als „Investment-relevant“ gilt | `SYSTEM_PROMPT` in `trump_watch.py` | Zölle, Fed, Krypto, Firmen, … |

Relevanz ≥ 9 kommt als **dringende** Mitteilung, alles andere als hohe Priorität.

## Gut zu wissen
- **Quelle:** Truth Social selbst blockiert automatische Abrufe, daher wird das öffentliche Archiv
  [trumpstruth.org](https://www.trumpstruth.org) genutzt, das jeden Post innerhalb weniger Minuten spiegelt.
- **Verzögerung:** typischerweise 2–10 Minuten nach dem Original-Post (GitHub-Zeitpläne laufen nicht
  sekundengenau). Wer es schneller will, lässt `--loop 60` auf einem immer laufenden Rechner laufen.
- **Keine Anlageberatung:** Die KI beschreibt nur, welche Bereiche betroffen sein könnten – Kauf- und
  Verkaufsentscheidungen triffst du selbst.
