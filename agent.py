import os
import requests
import xml.etree.ElementTree as ET

# 🔐 Segreti dal server
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

# 🔵 Feed stabile tramite RSSHub
RSS_URL = "https://rsshub.app/youtube/channel/UCf8fVtX8Hk2YtYtq8uQfV0xA"

def manda_telegram(testo):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    params = {"chat_id": CHAT_ID, "text": testo}
    requests.get(url, params=params)

def prendi_ultimo_video():
    r = requests.get(RSS_URL)

    # Controllo XML
    if not r.text.strip().startswith("<?xml"):
        raise Exception("Il feed non è XML. Il server RSS potrebbe essere temporaneamente non disponibile.")

    root = ET.fromstring(r.text)

    entry = root.find("channel/item")
    titolo = entry.find("title").text
    link = entry.find("link").text

    # Estrarre ID dal link
    video_id = link.split("v=")[-1]

    return {"id": video_id, "titolo": titolo, "url": link}

def main():
    video = prendi_ultimo_video()

    messaggio = (
        f"📢 Nuovo video di Lopsvito!\n\n"
        f"🎬 Titolo: {video['titolo']}\n"
        f"🔗 Link: {video['url']}\n\n"
        f"📝 (La parte di trascrizione e riassunto verrà aggiunta dopo)"
    )

    manda_telegram(messaggio)

if __name__ == "__main__":
    main()
