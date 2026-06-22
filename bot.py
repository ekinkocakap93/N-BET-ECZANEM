import json
import time
import random
import cloudscraper
from bs4 import BeautifulSoup
import re
import urllib.parse

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

            kart = etiket.find_parent('tr')
            if not kart:
                kart = etiket.find_parent('div', class_=lambda c: c and any(x in c.lower() for x in ['col-', 'panel', 'card', 'row', 'my-2']))

            adres = "Adres bulunamadı"
            telefon = "Telefon bulunamadı"
            harita_linki = ""

            if kart:
                # 📞 TELEFON
                tel_link = kart.find('a', href=re.compile(r'tel:'))
                if tel_link:
                    telefon = tel_link.get('href').replace('tel:', '').strip()
                else:
                    metin = kart.get_text(" ")
                    tel_match = re.search(r'\(?\d{3}\)?[\s\-]?\d{3}[\s\-]?\d{2}[\s\-]?\d{2}', metin)
                    if tel_match:
                        telefon = tel_match.group(0).strip()

                # 📍 ADRES
                tdler = kart.find_all('td')
                if tdler and len(tdler) >= 3:
                    adres = tdler[1].text.strip()
                else:
                    olasi_adresler = []
                    for parca in kart.stripped_strings:
                        parca = parca.strip()
                        if len(parca) > 15 and parca != isim and parca not in telefon and "Yol" not in parca and "Harita" not in parca:
                            olasi_adresler.append(parca)
                    if olasi_adresler:
                        adres = max(olasi_adresler, key=len)

                # 🗺️ HARİTA
                map_link = kart.find('a', href=re.compile(r'maps\.google|google\.com/maps'))
                if map_link:
                    harita_linki = map_link.get('href')
                else:
                    arama_metni = f"{isim} {sehir_eki.upper().replace('KIBRIS-', '')}"
                    harita_linki = f"https://www.google.com/maps/search/?api=1&query={urllib.parse.quote(arama_metni)}"

            # 🛑 HAYALET KART FİLTRELERİ 🛑
            # 1. İsmin içinde "eczane" geçmiyorsa ve tek kelimeyse (örn: Arnavutköy) bunu atla
            if "eczane" not in isim.lower() and len(isim.split()) == 1:
                continue
            
            # 2. Aynı telefon numarasına sahip başka bir kart daha önce eklendiyse (ve telefon boş değilse) bunu atla
            if telefon != "Telefon bulunamadı" and any(e['telefon'] == telefon for e in sehir_eczaneleri):
                continue
                
            # 3. İsim birebir aynıysa atla
            if any(e['isim'] == isim for e in sehir_eczaneleri):
                continue

            sehir_eczaneleri.append({
                "isim": isim,
                "adres": f"{adres} ({sehir_eki.upper()})",
                "telefon": telefon,
                "harita_linki": harita_linki
            })

        print(f"✅ BULUNAN ECZANE SAYISI: {len(sehir_eczaneleri)}")

    except Exception as e:
        print(f"🚨 KRİTİK HATA: {e}")

    return sehir_eczaneleri

def ana_motor():
    tum_eczaneler = []
    print("🚀 Nöbetçi Cepte V8 (Anti-Hayalet) Motoru Başlatıldı...\n")

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
