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
        scraper = cloudscraper.create_scraper(browser={'browser': 'chrome', 'platform': 'windows', 'desktop': True})
        response = scraper.get(url, timeout=20)
        response.encoding = 'utf-8'
        
        if response.status_code != 200:
            print("❌ ENGEL AŞILAMADI.")
            return []

        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Sitenin kalbi olan tablo satırlarını (tr) buluyoruz
        satirlar = soup.find_all("tr")
        
        for satir in satirlar:
            sutunlar = satir.find_all("td")
            
            # Eczane tablosunda genelde en az 3 sütun olur: İsim, Adres, Telefon
            if len(sutunlar) >= 3:
                # Tablonun en üstündeki başlık ("Eczane Adı") satırını atla
                if "Eczane Adı" in sutunlar[0].text:
                    continue
                    
                # 1. SÜTUN: İSİM (İsim etiketini bul, bulamazsa düz metni al)
                isim_span = sutunlar[0].find(class_=['isim', 'title'])
                if isim_span:
                    isim = isim_span.text.strip()
                else:
                    isim = sutunlar[0].text.strip().split('\n')[0]
                    
                # 2. SÜTUN: ADRES
                adres = sutunlar[1].text.strip()
                
                # 3. SÜTUN: TELEFON
                telefon = sutunlar[2].text.strip()
                
                # Sadece gerçekçi verileri listeye ekle
                if len(isim) > 2:
                    sehir_eczaneleri.append({
                        "isim": isim,
                        "adres": f"{adres} ({sehir_eki.upper()})",
                        "telefon": telefon
                    })
        
        print(f"✅ BULUNAN ECZANE SAYISI: {len(sehir_eczaneleri)}")

    except Exception as e:
        print(f"🚨 KRİTİK HATA: {e}")
        
    return sehir_eczaneleri

def ana_motor():
    tum_eczaneler = []
    print("🚀 Nöbetçi Cepte V3 (Keskin Nişancı) Motoru Başlatıldı...\n")
    
    for sehir in SEHIRLER:
        veriler = eczaneleri_getir(sehir)
        if veriler:
            tum_eczaneler.extend(veriler)
        time.sleep(random.uniform(3.0, 5.0))
        
    with open("eczaneler.json", "w", encoding="utf-8") as f:
        json.dump({"eczaneler": tum_eczaneler}, f, ensure_ascii=False, indent=4)
        
    print(f"\n🎯 İŞLEM BİTTİ! TOPLAM {len(tum_eczaneler)} ECZANE KAYDEDİLDİ.")

if __name__ == "__main__":
    ana_motor()
