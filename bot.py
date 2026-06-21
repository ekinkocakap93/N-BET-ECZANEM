import json
import time
import random
import requests
from bs4 import BeautifulSoup

SEHIRLER = [
    "istanbul",
    "diyarbakir",
    "kibris-lefkosa"
]

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4.1 Safari/605.1.15"
]

def eczaneleri_getir(sehir_eki):
    url = f"https://www.eczaneler.gen.tr/nobetci-{sehir_eki}"
    headers = {
        "User-Agent": random.choice(USER_AGENTS),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "tr-TR,tr;q=0.9,en-US;q=0.8,en;q=0.7"
    }
    sehir_eczaneleri = []

    try:
        print(f"📡 BASTILIYOR: {url}")
        response = requests.get(url, headers=headers, timeout=15)
        response.encoding = 'utf-8'
        
        # Sitenin bize ne cevap verdiğini ekrana yazdırıyoruz (Çok Kritik!)
        print(f"🚦 SİTE CEVAP KODU: {response.status_code}")
        
        if response.status_code != 200:
            print("❌ SİTE BİZİ ENGELLEDİ (Cloudflare veya Güvenlik Duvarı)")
            return []

        soup = BeautifulSoup(response.text, 'html.parser')
        
        # En kaba kuvvet (Brute-Force) arama yöntemi:
        # İsimlerin genellikle bulunduğu büyük başlıkları (h2, span, a) ve class'ı "isim" veya "title" olanları ara
        isim_etiketleri = soup.find_all(class_=['isim', 'title', 'eczane-adi'])
        
        for etiket in isim_etiketleri:
            isim = etiket.text.strip()
            # Eğer isim boşsa atla
            if not isim: continue
                
            # Ebeveyn kutuyu bul (kartın tamamı)
            kart = etiket.find_parent('div', class_=['row', 'panel', 'card']) or etiket.find_parent('tr')
            if kart:
                adres_etiket = kart.find(class_=['adres', 'text-muted', 'address'])
                tel_etiket = kart.find(class_=['telefon', 'tel', 'phone'])
                
                adres = adres_etiket.text.strip() if adres_etiket else "Adres çekilemedi"
                telefon = tel_etiket.text.strip() if tel_etiket else "Telefon çekilemedi"
                
                # Sadece gerçekten isim gibi duranları ekle (en az 3 harf)
                if len(isim) > 3:
                    sehir_eczaneleri.append({
                        "isim": isim,
                        "adres": f"{adres} ({sehir_eki.upper()})",
                        "telefon": telefon
                    })
        
        # Eğer div'lerden bulamadıysa, klasik tablo (table) avına çık:
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
    print("🚀 Nöbetçi Cepte Teşhis Motoru Başlatıldı...\n")
    
    for sehir in SEHIRLER:
        veriler = eczaneleri_getir(sehir)
        if veriler:
            tum_eczaneler.extend(veriler)
        time.sleep(random.uniform(2.0, 4.0))
        
    with open("eczaneler.json", "w", encoding="utf-8") as f:
        json.dump({"eczaneler": tum_eczaneler}, f, ensure_ascii=False, indent=4)
        
    print(f"\n🎯 İŞLEM BİTTİ! TOPLAM {len(tum_eczaneler)} ECZANE KAYDEDİLDİ.")

if __name__ == "__main__":
    ana_motor()
