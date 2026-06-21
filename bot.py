import json
import time
import random
import requests
from bs4 import BeautifulSoup
import os

# Sistemin hedef uzantıları: Hem iller hem de demin bulduğun KKTC bölgeleri
# Şimdilik testi hızlı yapmak için birkaç bölge koydum, sonradan 81 ili buraya dizeceksin.
SEHIRLER = [
    "istanbul",
    "diyarbakir",
    "kibris-lefkosa",
    "kibris-girne",
    "kibris-gazimagusa"
]

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2.1 Safari/605.1.15"
]

def eczaneleri_getir(sehir_eki):
    url = f"https://www.eczaneler.gen.tr/nobetci-{sehir_eki}"
    headers = {"User-Agent": random.choice(USER_AGENTS)}
    sehir_eczaneleri = []

    try:
        # Siteye bağlan ve veriyi çek
        response = requests.get(url, headers=headers, timeout=15)
        response.encoding = 'utf-8' # Türkçe karakterleri bozmaması için
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Site tasarımında eczane isimleri genelde 'isim' veya 'title' class'lı div'lerde veya tablolarda yer alır.
        # En yaygın CSS seçicilerini kullanarak verileri avlıyoruz:
        isim_divleri = soup.find_all('span', class_='isim')
        
        # Eğer span olarak bulamazsa tablo içinden çekmeye çalışır (Yedekleme planı)
        if not isim_divleri:
            tablo_satirlari = soup.select("table.table-bordered tbody tr")
            for satir in tablo_satirlari:
                sutunlar = satir.find_all('td')
                if len(sutunlar) >= 3:
                    isim = sutunlar[0].text.strip()
                    adres = sutunlar[1].text.strip()
                    telefon = sutunlar[2].text.strip()
                    
                    sehir_adi = "Lefkoşa" if "lefkosa" in sehir_eki else sehir_eki.capitalize()
                    
                    sehir_eczaneleri.append({
                        "isim": isim,
                        "adres": f"{adres} - {sehir_adi}",
                        "telefon": telefon
                    })
            return sehir_eczaneleri

        # Eğer div sistemiyle yapılmışsa:
        for div in soup.select('.eczane-karti, .panel, .box'):
            try:
                isim = div.find(['div', 'span', 'h2'], class_='isim').text.strip()
                adres = div.find(['div', 'span'], class_='adres').text.strip()
                telefon = div.find(['div', 'span'], class_='telefon').text.strip()
                
                sehir_eczaneleri.append({
                    "isim": isim,
                    "adres": adres,
                    "telefon": telefon
                })
            except AttributeError:
                continue

    except Exception as e:
        print(f"HATA: {sehir_eki} verisi çekilemedi -> {e}")
        
    return sehir_eczaneleri

def ana_motor():
    tum_eczaneler = []
    print("🚀 Nöbetçi Cepte Ana Motoru Başlatıldı...")
    
    for sehir in SEHIRLER:
        print(f"Hedef Taranıyor: {sehir.upper()}...")
        veriler = eczaneleri_getir(sehir)
        tum_eczaneler.extend(veriler)
        
        # Anti-Ban Zırhı: Her il arasında 2-4 saniye rastgele bekle
        time.sleep(random.uniform(2.0, 4.0))
        
    # Verileri dosyaya yazma işlemi
    with open("eczaneler.json", "w", encoding="utf-8") as f:
        json.dump({"eczaneler": tum_eczaneler}, f, ensure_ascii=False, indent=4)
        
    print(f"✅ Görev Tamamlandı! Toplam {len(tum_eczaneler)} eczane kaydedildi.")

if __name__ == "__main__":
    ana_motor()
