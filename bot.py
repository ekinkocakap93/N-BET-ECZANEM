import json
import time
import random
import cloudscraper
from bs4 import BeautifulSoup
import re

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

        soup = BeautifulSoup(response.text, 'html.parser')

        isim_etiketleri = soup.find_all(['span', 'div', 'a', 'h2'], class_=['isim', 'eczane-adi', 'title'])

        for etiket in isim_etiketleri:
            isim = etiket.text.strip()
            if len(isim) < 3: continue

            # Kartın tamamını kapsayan ebeveyni bul
            kart = etiket.find_parent('tr')
            if not kart:
                kart = etiket.find_parent('div', class_=lambda c: c and any(x in c.lower() for x in ['col-', 'panel', 'card', 'row']))

            adres = "Adres bulunamadı"
            telefon = "Telefon bulunamadı"

            if kart:
                # 📞 TELEFONU BUL (Regex Avcısı veya Tıklanabilir Link)
                tel_link = kart.find('a', href=re.compile(r'tel:'))
                if tel_link:
                    telefon = tel_link.text.strip()
                else:
                    # Link yoksa tüm metnin içinde 10-11 haneli numara şablonu ara
                    metin = kart.get_text(" ")
                    tel_match = re.search(r'0\s?\d{3}\s?\d{3}\s?\d{2}\s?\d{2}|0\d{10}', metin)
                    if tel_match:
                        telefon = tel_match.group(0)

                # 📍 ADRESİ BUL (Tablo ise 2. sütun, değilse kart içindeki en uzun anlamlı metin)
                tdler = kart.find_all('td')
                if tdler and len(tdler) >= 3:
                    adres = tdler[1].text.strip()
                else:
                    olasi_adresler = []
                    # Sadece temiz metin parçalarını al
                    for parca in kart.stripped_strings:
                        parca = parca.strip()
                        # İsim, telefon veya buton yazısı olmayan uzun metinleri topla
                        if len(parca) > 15 and parca != isim and parca != telefon and "Yol" not in parca and "Harita" not in parca and "Konum" not in parca:
                            olasi_adresler.append(parca)
                    
                    if olasi_adresler:
                        # En uzun cümle %99 ihtimalle adrestir
                        adres = max(olasi_adresler, key=len)

            # Eczane sitede iki kere basıldıysa (mobil/masaüstü çiftlemesi) sadece birini al
            if any(e['isim'] == isim for e in sehir_eczaneleri):
                continue

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
    print("🚀 Nöbetçi Cepte V6 (Regex Avcısı) Motoru Başlatıldı...\n")

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
