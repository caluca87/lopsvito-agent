import os
import requests
import xml.etree.ElementTree as ET

# 🔐 PRENDIAMO I DATI DAI SEGRETI DEL SERVER
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

# 🔵 FEED STABILE (non bloccato da YouTube)
RSS_URL = "https://feed.yt/UCf8fVtX8Hk2YtYtq8uQfV0xA"

def manda_telegram(testo):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    params = {"chat_id": CHAT_ID, "text": testo}
    requests.get(url, params=params)

def prendi_ultimo_video():
    r = requests.get(RSS_URL)

    # Se la risposta NON è XML → YouTube ha restituito HTML
    if not r.text.strip().startswith("<?xml"):
        raise Exception("Feed YouTube non disponibile (YouTube ha restituito HTML).")

    root = ET.fromstring(r.text)

    entry = root.find("{http://www.w3.org/2005/Atom}entry")
    titolo = entry.find("{http://www.w3.org/2005/Atom}title").text
    link = entry.find("{http://www.w3.org/2005/Atom}link").attrib["href"]
    video_id = entry.find("{http://www.youtube.com/xml/schemas/2015}videoId").text

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
