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

        soup = BeautifulSoup(response.text, 'html.parser')

        # 🕵️ DEDEKTİF MODU: Sayfanın başlığını yazdırarak Cloudflare tuzağına düşüp düşmediğimizi anlıyoruz
        sayfa_basligi = soup.title.text.strip() if soup.title else "Başlık Yok"
        print(f"🔍 SAYFA BAŞLIĞI: {sayfa_basligi}")

        if "Just a moment" in sayfa_basligi or "Cloudflare" in sayfa_basligi:
            print("❌ DİKKAT: SİTE BİZE SAHTE 200 KODU VERİP ROBOT DOĞRULAMASI SUNDU!")
            return []

        # 🕸️ GENİŞ AĞ MODU: Hem tabloları hem de div kartlarını aynı anda esnekçe tarar
        isim_etiketleri = soup.find_all(class_=['isim', 'title', 'eczane-adi'])

        for etiket in isim_etiketleri:
            isim = etiket.text.strip()
            if len(isim) < 3: continue

            # Eczanenin içinde bulunduğu ana kutuyu bul
            kart = etiket.find_parent(['tr', 'div', 'li'], class_=['row', 'panel', 'card']) or etiket.find_parent('tr')

            adres = "Adres bulunamadı"
            telefon = "Telefon bulunamadı"

            if kart:
                sutunlar = kart.find_all("td")
                if len(sutunlar) >= 3:
                    # Tablo yapısındaysa
                    adres = sutunlar[1].text.strip()
                    telefon = sutunlar[2].text.strip()
                else:
                    # Kutu (div) yapısındaysa
                    adres_etiket = kart.find(class_=['adres', 'text-muted', 'address'])
                    tel_etiket = kart.find(class_=['telefon', 'tel', 'phone'])
                    if adres_etiket: adres = adres_etiket.text.strip()
                    if tel_etiket: telefon = tel_etiket.text.strip()

            # Temizlenmiş veriyi listeye ekle
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
    print("🚀 Nöbetçi Cepte V4 (Dedektif + Geniş Ağ) Motoru Başlatıldı...\n")

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
