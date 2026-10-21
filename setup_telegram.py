#!/usr/bin/env python3
"""
Richtet Telegram als Push-Kanal ein – einmalig auf dem Mac ausführen:

  1. In Telegram @BotFather öffnen, /newbot senden, Namen vergeben, Token kopieren (⌘C)
  2. python3 setup_telegram.py

Das Skript liest den Token aus der Zwischenablage (er wird nirgends angezeigt),
wartet, bis du deinem Bot "Start" schickst, speichert Token + Chat-ID als
GitHub-Secrets und schickt eine Test-Nachricht.
"""

import json
import os
import re
import subprocess
import sys
import time
import urllib.request

REPO = "maxbaumgart17-afk/trump-invest-alert"
GH = os.path.expanduser("~/.local/gh-cli/gh_2.102.1_macOS_arm64/bin/gh")


def api(token, method, **params):
    req = urllib.request.Request(
        f"https://api.telegram.org/bot{token}/{method}",
        data=json.dumps(params).encode(),
        headers={"Content-Type": "application/json"},
    )
    try:
        with urllib.request.urlopen(req, timeout=40) as r:
            return json.loads(r.read())["result"]
    except urllib.error.HTTPError as e:
        sys.exit(f"✗ Telegram lehnt ab ({e.code}). Ist der Token vollständig kopiert?")


def set_secret(name, value):
    subprocess.run([GH, "secret", "set", name, "--repo", REPO], input=value, text=True, check=True,
                   capture_output=True)


def main():
    token = re.sub(r"\s", "", subprocess.run(["pbpaste"], capture_output=True, text=True).stdout)
    if not re.fullmatch(r"\d{6,}:[A-Za-z0-9_-]{30,}", token):
        sys.exit("✗ In der Zwischenablage ist kein Bot-Token. In Telegram bei @BotFather den Token kopieren und erneut starten.")

    bot = api(token, "getMe")
    print(f"✓ Bot gefunden: @{bot['username']}")
    print(f"\n👉 Öffne jetzt auf dem Handy diesen Link und tippe auf START:\n   https://t.me/{bot['username']}\n")
    print("   Ich warte (max. 5 Minuten) …")

    chat_id, deadline, offset = None, time.time() + 300, None
    while not chat_id and time.time() < deadline:
        params = {"timeout": 25, "allowed_updates": ["message"]}
        if offset:
            params["offset"] = offset
        for upd in api(token, "getUpdates", **params):
            offset = upd["update_id"] + 1
            msg = upd.get("message") or {}
            if msg.get("chat", {}).get("type") == "private":
                chat_id = str(msg["chat"]["id"])
                name = msg["chat"].get("first_name", "")
    if not chat_id:
        sys.exit("✗ Keine Nachricht erhalten. Bitte den Link öffnen, START tippen und das Skript erneut starten.")
    print(f"✓ Chat mit {name} verbunden")

    set_secret("TELEGRAM_BOT_TOKEN", token)
    set_secret("TELEGRAM_CHAT_ID", chat_id)
    print("✓ Bei GitHub gespeichert")

    api(token, "sendMessage", chat_id=chat_id, parse_mode="HTML",
        text="<b>✅ Trump Invest Alert ist verbunden!</b>\n\nAb jetzt bekommst du hier eine Nachricht, "
             "sobald Trump etwas Investment-Relevantes postet.")
    print("✓ Test-Nachricht an dein Handy geschickt. Fertig! 🎉")


if __name__ == "__main__":
    main()
