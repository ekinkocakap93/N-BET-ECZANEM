import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime

def eczaneleri_topla_ve_kaydet():
    print("⏳ Aşama 1: Sistem başlatılıyor. Tüm Türkiye ve KKTC verileri hedefleniyor...")
    
    # 81 İl ve KKTC için tüm bağlantıların ekleneceği merkez havuz
    sehirler = [
        "Adana", "Adıyaman", "Afyonkarahisar", "Ağrı", "Amasya", "Ankara", "Antalya", "Artvin", 
        "Aydın", "Balıkesir", "Bilecik", "Bingöl", "Bitlis", "Bolu", "Burdur", "Bursa", "Çanakkale", 
        "Çankırı", "Çorum", "Denizli", "Diyarbakır", "Edirne", "Elazığ", "Erzincan", "Erzurum", 
        "Eskişehir", "Gaziantep", "Giresun", "Gümüşhane", "Hakkari", "Hatay", "Isparta", "Mersin", 
        "İstanbul", "İzmir", "Kars", "Kastamonu", "Kayseri", "Kırklareli", "Kırşehir", "Kocaeli", 
        "Konya", "Kütahya", "Malatya", "Manisa", "Kahramanmaraş", "Mardin", "Muğla", "Muş", 
        "Nevşehir", "Niğde", "Ordu", "Rize", "Sakarya", "Samsun", "Siirt", "Sinop", "Sivas", 
        "Tekirdağ", "Tokat", "Trabzon", "Tunceli", "Şanlıurfa", "Uşak", "Van", "Yozgat", 
        "Zonguldak", "Aksaray", "Bayburt", "Karaman", "Kırıkkale", "Batman", "Şırnak", "Bartın", 
        "Ardahan", "Iğdır", "Yalova", "Karabük", "Kilis", "Osmaniye", "Düzce", "KKTC"
    ]
    
    try:
        print(f"🔍 Aşama 2: Toplam {len(sehirler)} bölge için altyapı hazırlanıyor...")
        
        # Şimdilik sistemin hatasız çalıştığını test etmek için örnek bir yapı oluşturuyoruz.
        # İleride her ilin verisi ilgili sitelerden buraya otomatik akacak.
        ham_kazilan_veriler = [
            {
                "koordinat_var_mi": True,
                "koordinatlar": {"lat": 41.0082, "lng": 28.9784},
                "detay": "İSTANBUL MERKEZ ECZANESİ - Tel: 0212 111 22 33 - Kadıköy / İstanbul"
            },
            {
                "koordinat_var_mi": True,
                "koordinatlar": {"lat": 37.9144, "lng": 40.2306},
                "detay": "DİYARBAKIR UMUT ECZANESİ - Tel: 0412 224 55 66 - Yenişehir Mah. Ekinciler Caddesi No:12 Yenişehir / Diyarbakır"
            },
            {
                "koordinat_var_mi": True,
                "koordinatlar": {"lat": 35.2104, "lng": 33.3262},
                "detay": "LEFKOŞA ŞİFA ECZANESİ - Tel: 0392 228 33 44 - Bedrettin Demirel Caddesi No:88 Gönyeli / Lefkoşa"
            }
        ]
        
        # 3. Aşama: Veritabanı paketini hazırlama
        guncel_zaman = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        yayinlanacak_api_verisi = {
            "son_guncelleme": guncel_zaman,
            "hedef_kapsam": "Tüm Türkiye ve KKTC",
            "eczaneler": ham_kazilan_veriler
        }
        
        # 4. Aşama: Fiziki dosya üretimi
        with open('eczaneler.json', 'w', encoding='utf-8') as json_dosyasi:
            json.dump(yayinlanacak_api_verisi, json_dosyasi, ensure_ascii=False, indent=4)
            
        print("✅ Aşama 3: Başarılı! 'eczaneler.json' veritabanı dosyası oluşturuldu.")
        
    except Exception as hata:
        print(f"❌ Hata Oluştu! İşlem durduruldu: {str(hata)}")

if __name__ == "__main__":
    eczaneleri_topla_ve_kaydet()