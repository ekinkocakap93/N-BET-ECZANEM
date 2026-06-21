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

        # Sadece eczane isimlerini bularak başla
        isim_etiketleri = soup.find_all(class_=['isim', 'title', 'eczane-adi'])

        for etiket in isim_etiketleri:
            isim = etiket.text.strip()
            if len(isim) < 3: continue

            # Eczanenin bilgilerini kapsayan en dış kutuyu (container) bul
            kart = etiket.find_parent(['div', 'li', 'tr'], class_=['row', 'panel', 'card', 'eczane-karti']) or etiket.find_parent('tr')

            adres = "Adres bulunamadı"
            telefon = "Telefon bulunamadı"

            if kart:
                # 🧠 METİN ANALİZ MANTIĞI: Kutunun içindeki tüm metinleri sırayla al
                tum_metinler = list(kart.stripped_strings)
                
                # 1. Telefonu Bul (İçinde 10 ile 15 arası rakam olan metin)
                for metin in reversed(tum_metinler):
                    rakam_sayisi = sum(c.isdigit() for c in metin)
                    if 10 <= rakam_sayisi <= 15:
                        telefon = metin
                        break
                
                # 2. Adresi Bul (İsim, Telefon ve Butonlar hariç kalan metinleri birleştir)
                adres_parcalari = []
                yasakli_kelimeler = ['yol tarifi', 'harita', 'konum', 'ara', 'detay', 'açık', 'kapalı', 'nöbetçi']
                
                for metin in tum_metinler:
                    if metin == isim or metin == telefon: 
                        continue
                    if metin.lower() in yasakli_kelimeler: 
                        continue
                    # Sadece tek harflik gereksiz işaretleri atla, gerisini adrese ekle
                    if len(metin) > 3: 
                        adres_parcalari.append(metin)
                
                if adres_parcalari:
                    adres = " ".join(adres_parcalari)

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
    print("🚀 Nöbetçi Cepte V5 (Metin Analizi) Motoru Başlatıldı...\n")

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
