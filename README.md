# 🔍 LAOTH Pastebin Leak Scanner

Selam dostlar! 👋

Bu tool, Pastebin üzerinde sızan hesapları bulmak için geliştirdiğim bir araç. Özellikle güvenlik araştırmacıları ve kendi hesaplarının güvenliğini kontrol etmek isteyenler için tasarlandı.

## 🚀 Özellikler

- 🎯 Akıllı arama algoritması
- 🔑 Birden fazla kimlik bilgisi formatını destekler
- 📊 Detaylı sonuç raporlama
- 🛡️ Anti-ban koruması
- 🎨 Renkli ve kullanıcı dostu arayüz

## 📦 Kurulum

Hey! Kurulum oldukça basit. Hadi başlayalım:

1. İlk olarak, Python 3.x sürümünün yüklü olduğundan emin ol. Terminalden kontrol edebilirsin:
```bash
python3 --version
```

2. Eğer Python yüklü değilse:
```bash
sudo apt update
sudo apt install python3 python3-pip python3-venv
```

3. Şimdi projeyi klonla veya ZIP olarak indir ve klasöre git:
```bash
cd /klasörün/yolu
```

4. Virtual environment oluştur ve aktif et:
```bash
python3 -m venv venv
source venv/bin/activate  # Linux/Mac için
# Windows için: venv\Scripts\activate
```

5. Gerekli paketleri yükle:
```bash
pip install -r requirements.txt
```

## 🎮 Kullanım

Tool'u çalıştırmak süper kolay! İşte birkaç örnek:

### 👉 Temel Kullanım
```bash
python pastebin_scanner.py -find spotify
```

### 🔄 Daha Fazla Sayfa Tarama
```bash
python pastebin_scanner.py -find spotify -p 10
```

### 💾 Özel Dosyaya Kaydetme
```bash
python pastebin_scanner.py -find spotify -o spotify_leaks.txt
```

## 🎯 Parametreler

- `-find`: Aranacak servis adı (örn: spotify, riot, steam)
- `-p` veya `--pages`: Taranacak sayfa sayısı (varsayılan: 5)
- `-o` veya `--output`: Sonuçların kaydedileceği dosya (varsayılan: sonuclar.txt)

## 💡 İpuçları

1. Çok sık tarama yapmaktan kaçın, IP'niz engellenebilir
2. VPN kullanmak iyi bir fikir olabilir
3. Sonuçları hemen kaydetmeyi unutmayın
4. Şüpheli bir durumla karşılaşırsanız ilgili servisi bilgilendirin

## ⚠️ Yasal Uyarı

Bu tool'u sadece:
- Kendi hesaplarınızı kontrol etmek için
- Güvenlik araştırmaları için
- Yasal ve etik sınırlar içinde kullanın

## 🐛 Sorun mu var?

Bir bug bulduysan veya özellik önerisi yapmak istiyorsan bana ulaşmaktan çekinme!

## 🙏 Teşekkürler

Bu tool'u geliştirirken yardımcı olan herkese teşekkürler! Güvenli taramalar! 🚀

---
Made with ❤️ by LAOTH 