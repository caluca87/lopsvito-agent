import requests
import xml.etree.ElementTree as ET
import time

# 🔐 INSERISCI QUI I TUOI DATI
TELEGRAM_TOKEN = "8602600167:AAG59w8TdCoDKoLIr_M1Rj67fBVz10lCrSM"
CHAT_ID = "24993178"

# 🔵 ID del canale Lopsvito (già inserito)
RSS_URL = "https://www.youtube.com/feeds/videos.xml?channel_id=UCf8fVtX8Hk2YtYtq8uQfV0xA"

def manda_telegram(testo):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    params = {"chat_id": CHAT_ID, "text": testo}
    requests.get(url, params=params)

def prendi_ultimo_video():
    r = requests.get(RSS_URL)
    root = ET.fromstring(r.text)

    entry = root.find("{http://www.w3.org/2005/Atom}entry")
    titolo = entry.find("{http://www.w3.org/2005/Atom}title").text
    link = entry.find("{http://www.w3.org/2005/Atom}link").attrib["href"]
    video_id = entry.find("{http://www.youtube.com/xml/schemas/2015}videoId").text

    return {"id": video_id, "titolo": titolo, "url": link}

def main():
    ultimo_id = None

    while True:
        video = prendi_ultimo_video()

        if video["id"] != ultimo_id:
            ultimo_id = video["id"]

            messaggio = (
                f"📢 Nuovo video di Lopsvito!\n\n"
                f"🎬 Titolo: {video['titolo']}\n"
                f"🔗 Link: {video['url']}\n\n"
                f"📝 (La parte di trascrizione e riassunto verrà aggiunta dopo)"
            )

            manda_telegram(messaggio)

        time.sleep(24 * 60 * 60)

if __name__ == "__main__":
    main()
