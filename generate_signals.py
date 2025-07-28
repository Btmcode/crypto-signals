import requests, json
from datetime import datetime

API_KEY = "YOUR_API_KEY"
HEADERS = {"Accepts":"application/json","X-CMC_PRO_API_KEY":API_KEY}
COIN_SYMBOLS = ["YFI","SHIB","ALP","ZIL","BNB","NOT","BTTC","XRP","MEME","ETC"]

def fetch_data():
    url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest"
    params = {"symbol":",".join(COIN_SYMBOLS),"convert":"USD"}
    return requests.get(url, headers=HEADERS, params=params).json()

def generate_signals():
    data = fetch_data()
    cards = []
    for s in COIN_SYMBOLS:
        c = data["data"][s]["quote"]["USD"]
        change = c["percent_change_24h"]
        rsi = 70 if change>1.5 else (30 if change<-1.5 else 50)
        signal = "SAT" if rsi>=70 else ("AL" if rsi<=30 else "TUT")
        cards.append({
            "coin": s,
            "price": round(c["price"],4),
            "rsi": rsi,
            "macd": "pozitif" if change>0 else "negatif",
            "volume": int(c["volume_24h"]),
            "signal": signal
        })
    with open("signals.json","w") as f:
        json.dump(cards, f, indent=2)
    print(f"[{datetime.now()}] {len(cards)} sinyal oluşturuldu.")

if __name__=="__main__":
    generate_signals()
