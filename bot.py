import json
import time
import random
import cloudscraper
from bs4 import BeautifulSoup

SEHIRLER = [
    "istanbul",
    "diyarbakir",
    "kibris-lefkosa"
]

def eczaneleri_getir(sehir_eki):
    url = f"https://www.eczaneler.gen.tr/nobetci-{sehir_eki}"
    sehir_eczaneleri = []

    try:
        print(f"📡 BASTILIYOR: {url}")
        
        # Cloudflare'i aşmak için özel tarayıcı taklidi yapan kazıyıcıyı oluşturuyoruz
        scraper = cloudscraper.create_scraper(browser={
            'browser': 'chrome',
            'platform': 'windows',
            'desktop': True
        })
        
        response = scraper.get(url, timeout=20)
        response.encoding = 'utf-8'
        
        print(f"🚦 SİTE CEVAP KODU: {response.status_code}")
        
        if response.status_code != 200:
            print("❌ ENGEL AŞILAMADI.")
            return []

        soup = BeautifulSoup(response.text, 'html.parser')
        isim_etiketleri = soup.find_all(class_=['isim', 'title', 'eczane-adi'])
        
        for etiket in isim_etiketleri:
            isim = etiket.text.strip()
            if not isim: continue
                
            kart = etiket.find_parent('div', class_=['row', 'panel', 'card']) or etiket.find_parent('tr')
            if kart:
                adres_etiket = kart.find(class_=['adres', 'text-muted', 'address'])
                tel_etiket = kart.find(class_=['telefon', 'tel', 'phone'])
                
                adres = adres_etiket.text.strip() if adres_etiket else "Adres çekilemedi"
                telefon = tel_etiket.text.strip() if tel_etiket else "Telefon çekilemedi"
                
                if len(isim) > 3:
                    sehir_eczaneleri.append({
                        "isim": isim,
                        "adres": f"{adres} ({sehir_eki.upper()})",
                        "telefon": telefon
                    })
        
        if not sehir_eczaneleri:
            tablolar = soup.find_all("table")
            for tablo in tablolar:
                satirlar = tablo.find_all("tr")
                for satir in satirlar:
                    sutunlar = satir.find_all("td")
                    if len(sutunlar) >= 3:
                        sehir_eczaneleri.append({
                            "isim": sutunlar[0].text.strip(),
                            "adres": f"{sutunlar[1].text.strip()} ({sehir_eki.upper()})",
                            "telefon": sutunlar[2].text.strip()
                        })

        print(f"✅ BULUNAN ECZANE SAYISI: {len(sehir_eczaneleri)}")

    except Exception as e:
        print(f"🚨 KRİTİK HATA: {e}")
        
    return sehir_eczaneleri

def ana_motor():
    tum_eczaneler = []
    print("🚀 Nöbetçi Cepte V2 Motoru Başlatıldı...\n")
    
    for sehir in SEHIRLER:
        veriler = eczaneleri_getir(sehir)
        if veriler:
            tum_eczaneler.extend(veriler)
        time.sleep(random.uniform(3.0, 6.0))
        
    with open("eczaneler.json", "w", encoding="utf-8") as f:
        json.dump({"eczaneler": tum_eczaneler}, f, ensure_ascii=False, indent=4)
        
    print(f"\n🎯 İŞLEM BİTTİ! TOPLAM {len(tum_eczaneler)} ECZANE KAYDEDİLDİ.")

if __name__ == "__main__":
    ana_motor()
