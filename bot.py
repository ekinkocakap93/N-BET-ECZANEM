import json
import time
import random
import requests
from bs4 import BeautifulSoup

# Çekilecek tüm şehirlerin listesi (Burayı 81 il ve KKTC olarak tamamlayabilirsin)
SEHIRLER = ["adana", "diyarbakir", "istanbul", "kktc"]

# Anti-Ban Zırhı: Her istekte farklı bir bilgisayarmış gibi görünmemizi sağlar
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2.1 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
]

def eczaneleri_getir(sehir):
    """
    KENDİ KODUNU BURAYA EKLEYECEKSİN:
    Daha önce yazdığın, siteye bağlanıp eczane isimlerini ve adreslerini
    ayıklayan o BeautifulSoup (veya kullandığın kütüphane) kodlarını bu bloğun içine yerleştir.
    """
    headers = {"User-Agent": random.choice(USER_AGENTS)}
    
    try:
        # ÖRNEK MANTIK: url = f"https://hedef-eczane-sitesi.com/{sehir}"
        # response = requests.get(url, headers=headers, timeout=10)
        # soup = BeautifulSoup(response.content, 'html.parser')
        # ... verileri ayıkla ...
        
        # Fonksiyon en son o şehre ait şu tarz bir liste döndürmeli:
        return [
            {"isim": f"{sehir.upper()} Örnek Eczanesi", "adres": "Örnek Mah.", "telefon": "0000"}
        ]
    except Exception as e:
        print(f"HATA: {sehir} çekilirken sorun oluştu -> {e}")
        return [] # Sunucu çökmüşse boş liste dön ki diğer şehirler patlamasın

def ana_motor():
    tum_eczaneler = []
    
    print("🤖 Nöbetçi Bot Çalışmaya Başladı...")
    for sehir in SEHIRLER:
        print(f"Hedef: {sehir.upper()} taranıyor...")
        sehir_verisi = eczaneleri_getir(sehir)
        tum_eczaneler.extend(sehir_verisi)
        
        # İnsan Taklidi: Siteleri yormamak ve engellenmemek için 2 ile 5 saniye arası rastgele bekle
        bekleme_suresi = random.uniform(2.0, 5.0)
        time.sleep(bekleme_suresi)
        
    # Tüm şehirler bittikten sonra veriyi GitHub'daki mevcut dosyaya kaydet
    with open("eczaneler.json", "w", encoding="utf-8") as f:
        json.dump({"eczaneler": tum_eczaneler}, f, ensure_ascii=False, indent=4)
        
    print("✅ Tüm veriler başarıyla eczaneler.json dosyasına yazıldı!")

if __name__ == "__main__":
    ana_motor()
