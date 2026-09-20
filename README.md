# 🇹🇷 Türkiye Yapay Zeka Araçları (Mali Müşavir, Avukat ve KOBİ'ler İçin)

[![CI & Test Suite](https://github.com/eimza-kep/turkiye-yapay-zeka-araclari/actions/workflows/ci.yml/badge.svg)](https://github.com/eimza-kep/turkiye-yapay-zeka-araclari/actions/workflows/ci.yml)
[![Python Version](https://img.shields.io/badge/python-3.10%20%7C%203.11%20%7C%203.12-blue)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Dependencies](https://img.shields.io/badge/dependencies-0%20external%20(stdlib%20only)-brightgreen)](#)
[![BYOK Architecture](https://img.shields.io/badge/Privacy-BYOK%20(100%25%20Local)-orange)](#)

Türkiye'de mali müşavirler, serbest muhasebeciler, avukatlar, hukuk büroları ve KOBİ'lerin günlük operasyonlarını yapay zeka ile hızlandırmak için geliştirilmiş **20 adet açık kaynaklı yapay zeka aracı ve etkileşimli web portalı**.

Bu proje; ağır kütüphanelere (LangChain, LlamaIndex, ChromaDB vb.) gerek duymadan, doğrudan **OpenAI** (`gpt-4o-mini`, `gpt-4o`) ve **Google Gemini** (`gemini-1.5-flash`, `gemini-1.5-pro`) REST API'lerini kullanan **sıfır bağımlılıklı (zero-dependency)** saf Python mimarisine ve **tarayıcı üzerinde çalışan modern BYOK web arayüzüne** sahiptir.

---

## 🌟 Öne Çıkan Özellikler

1. **Sıfır Dış Bağımlılık (Pure Python Stdlib):**
   - Kodları çalıştırmak için `pip install` yapmanıza gerek yoktur. Python 3'ün yerleşik `urllib.request` ve `json` kütüphaneleriyle çalışır.
2. **BYOK (Bring Your Own Key) & %100 Gizlilik:**
   - Verileriniz ve API anahtarlarınız hiçbir üçüncü taraf sunucuya veya veritabanına kaydedilmez.
   - Web arayüzü doğrudan istemci tarafında (tarayıcınızda) çalışır; API çağrıları doğrudan OpenAI / Google uç noktalarına gider.
3. **Çift Model Sağlayıcı Desteği (OpenAI & Google Gemini):**
   - İster OpenAI API anahtarınızla (`sk-...`), ister Google AI Studio'dan aldığınız ücretsiz Gemini anahtarınızla (`AIzaSy...`) çalışabilirsiniz.
4. **Kapsamlı Türkiye Mevzuat & Vergi Bilgi Tabanı:**
   - Sistem istemleri (prompt templates); VUK, TDHP (Tekdüzen Hesap Planı), GİB e-Defter şemaları, HMK, İİK 89/1, 6698 sayılı KVKK, KOSGEB ve EKAP mevzuatlarına tam uyumlu olarak tasarlanmıştır.
5. **Dahili Test & Simülasyon Modu (`--test`):**
   - API anahtarınız olmadan da araçların nasıl çalıştığını, girdi-çıktı formatlarını ve mantığını test edebileceğiniz yerleşik deterministik simülasyon modu.

---

## 🗂️ 20 Yapay Zeka Aracı Kataloğu

### 📊 1. Mali Müşavir ve Muhasebe Araçları (1 - 7)

| No | Modül | Dosya | Açıklama |
|---|---|---|---|
| **01** | **Fişmatik AI** | [`muhasebe/01_fismatik_ai.py`](muhasebe/01_fismatik_ai.py) | Fiş ve fatura metinlerinden KDV oranlarını (%1, %10, %20) ayıklar, VUK ve Tekdüzen Hesap Planı (TDHP 191/391/770) uyumlu yevmiye maddesi üretir. |
| **02** | **e-Defter Debugger AI** | [`muhasebe/02_edefter_debugger_ai.py`](muhasebe/02_edefter_debugger_ai.py) | GİB e-Defter berat yükleme hatalarını, XML şema uyumsuzluklarını ve imza tutarsızlıklarını adım adım çözüm reçetelerine dönüştürür. |
| **03** | **Mevzuat & Özelge AI** | [`muhasebe/03_mevzuat_ozelge_ai.py`](muhasebe/03_mevzuat_ozelge_ai.py) | Vergi uyuşmazlıkları ve özellikli işlemlerde GİB özelgeleri ve VUK/KDV kanun maddeleri ışığında gerekçeli mali görüş raporu hazırlar. |
| **04** | **Banka Ekstresi AI** | [`muhasebe/04_banka_ekstresi_ai.py`](muhasebe/04_banka_ekstresi_ai.py) | Karışık banka hesap hareketlerini analiz eder; POS, EFT, kredi taksiti ve vergi ödemelerini TDHP muavin hesap kodlarıyla (102, 108, 300, 360) eşler. |
| **05** | **Mizan CFO Raporu AI** | [`muhasebe/05_mizan_cfo_raporu_ai.py`](muhasebe/05_mizan_cfo_raporu_ai.py) | Borç/Alacak mizan tablosundan şirket sahibinin veya genel müdürün tek bakışta anlayacağı likidite, kârlılık ve risk analiz raporu çıkarır. |
| **06** | **Beyanname Ön Denetim AI** | [`muhasebe/06_beyanname_on_denetim_ai.py`](muhasebe/06_beyanname_on_denetim_ai.py) | KDV-1, Muhtasar ve Geçici Vergi beyannameleri arasındaki kümülatif matrah, tevkifat ve devreden KDV tutarsızlıklarını denetler. |
| **07** | **Bordro & Vergi Dilimi AI** | [`muhasebe/07_bordro_vergi_asistani_ai.py`](muhasebe/07_bordro_vergi_asistani_ai.py) | Asgari ücret istisnası, SGK tavanı ve kümülatif gelir vergisi dilim geçişlerini brüt-net simülasyonu ile çalışanlara anlaşılır dilde açıklar. |

---

### ⚖️ 2. Avukat ve Hukuk Bürosu Araçları (8 - 14)

| No | Modül | Dosya | Açıklama |
|---|---|---|---|
| **08** | **Sözleşme Denetleyici AI** | [`hukuk/08_sozlesme_denetleyici_ai.py`](hukuk/08_sozlesme_denetleyici_ai.py) | Ticari sözleşmelerdeki tek taraflı cezai şartları, fahiş tazminat maddelerini ve yetki şartlarını tespit eder, revize madde (redline) önerir. |
| **09** | **İçtihat Özetleyici AI** | [`hukuk/09_ictihat_ozetleyici_ai.py`](hukuk/09_ictihat_ozetleyici_ai.py) | 30 sayfalık Yargıtay Hukuk Genel Kurulu veya BAM kararlarını; Uyuşmazlık, Hukuki Gerekçe, Hüküm Özeti ve Emsal Değeri başlıklarında özetler. |
| **10** | **Dava Hafızası AI** | [`hukuk/10_dava_hafizasi_ai.py`](hukuk/10_dava_hafizasi_ai.py) | Duruşma tutanakları ile tanık/davalı beyanlarını karşılaştırarak zamansal ve olgusal çelişkileri tablo halinde tespit eder. |
| **11** | **HMK Dilekçe Mimarı AI** | [`hukuk/11_dilekce_mimari_ai.py`](hukuk/11_dilekce_mimari_ai.py) | Olay örgüsü ve delil listesinden HMK Madde 119 standartlarına tam uyumlu dava/cevap dilekçesi taslağı inşa eder. |
| **12** | **Hukuk Noteri AI** | [`hukuk/12_hukuk_whisper_noteri_ai.py`](hukuk/12_hukuk_whisper_noteri_ai.py) | Müvekkil görüşmesi veya duruşma ses deşifresini kronolojik olay sırasına ve hukuki delil envanterine dönüştürür. |
| **13** | **KVKK Uyum AI** | [`hukuk/13_kvkk_uyum_denetleyici_ai.py`](hukuk/13_kvkk_uyum_denetleyici_ai.py) | Web siteleri ve İK süreçlerindeki Aydınlatma Metni ile Açık Rıza formlarını 6698 sayılı Kanun ve Kurul ilke kararlarına göre denetler. |
| **14** | **e-İhtarname & KEP AI** | [`hukuk/14_e_ihtarname_ai.py`](hukuk/14_e_ihtarname_ai.py) | Kira tahliyesi, ödenmeyen fatura veya sözleşme feshi durumlarında Türk Borçlar Kanunu'na uygun KEP ihtarname metni oluşturur. |

---

### 🏢 3. KOBİ ve E-Dönüşüm Araçları (15 - 20)

| No | Modül | Dosya | Açıklama |
|---|---|---|---|
| **15** | **Fatura Anomali AI** | [`kobi/15_fatura_anomali_ai.py`](kobi/15_fatura_anomali_ai.py) | Tedarikçi e-faturalarını geçmiş birim fiyatlarla karşılaştırarak gizli fiyat artışlarını ve mükerrer faturalandırmaları anında yakalar. |
| **16** | **KEP Nöbetçisi AI** | [`kobi/16_kep_nobetci_ai.py`](kobi/16_kep_nobetci_ai.py) | Gelen KEP iletisini tarar; İİK 89/1 haciz ihbarnamesi veya fesih ihtarı olup olmadığını anlar, 7 günlük itiraz takvimini hesaplar. |
| **17** | **EKAP İhale Asistanı AI** | [`kobi/17_ihale_asistan_ai.py`](kobi/17_ihale_asistan_ai.py) | 80 sayfalık kamu ihale idari/teknik şartnamelerini tarayarak KOBİ için elenme risklerini, iş bitirme şartlarını ve maliyet tuzaklarını raporlar. |
| **18** | **Satış & Teklif Botu AI** | [`kobi/18_satis_teklif_botu_ai.py`](kobi/18_satis_teklif_botu_ai.py) | Müşterinin WhatsApp veya e-posta mesajındaki talepleri profesyonel proforma teklife ve nezih bir satış metnine çevirir. |
| **19** | **Teşvik Radarı AI** | [`kobi/19_tesvik_radar_ai.py`](kobi/19_tesvik_radar_ai.py) | Firmanın NACE kodu, cirosu ve yatırım planına göre KOSGEB, TÜBİTAK ve Sanayi Bakanlığı teşvik paketlerini eşleştirir. |
| **20** | **Reklam Uyum AI** | [`kobi/20_reklam_uyum_ai.py`](kobi/20_reklam_uyum_ai.py) | E-ticaret ürün açıklamaları ve sosyal medya reklamlarını Ticaret Bakanlığı Reklam Kurulu mevzuatına göre denetler, idari para cezalarını önler. |

---

## 🚀 Süper Kolay Başlangıç & Kurulum

Bu projeyi kullanmak için terminal komutları bilmenize gerek yoktur. İster tek tıkla web arayüzünü açabilir, ister interaktif sihirbazı çalıştırabilirsiniz:

---

### 1️⃣ Yöntem 1: Windows'ta Tek Tıkla Başlatma (En Kolay)

Depo klasöründeki dosyalarla doğrudan başlayabilirsiniz:
- **`Baslat.bat`** : Çift tıklayın; sisteminizdeki Python'u otomatik bulur ve interaktif Türkçe menüyü açar. (Python yoksa doğrudan Web Portalını tarayıcınızda açar).
- **`Web-Portali.bat`** : Çift tıklayın; 20 AI aracının bulunduğu görsel web arayüzünü doğrudan varsayılan internet tarayıcınızda açar.
- **`baslat.sh`** (Mac & Linux): Terminalde `./baslat.sh` çalıştırarak sihirbazı veya web portalını açabilirsiniz.

---

### 2️⃣ Yöntem 2: İnteraktif Terminal Sihirbazı (`python baslat.py`)

Terminal veya komut satırında tek bir komutla tüm ekosistemi yönetebilirsiniz:

```bash
python baslat.py
```

Açılan renkli Türkçe menüde:
* **`[1] 🌐 Web Portalını Aç`** : Yerel sunucuyu ayağa kaldırır ve tarayıcınızı otomatik açar.
* **`[2] 🔑 API Anahtarlarını Ayarla`** : Gemini veya OpenAI anahtarınızı yapıştırın; sistem anahtarın çalışıp çalışmadığını **canlı test eder** ve otomatik `.env` dosyası oluşturur!
* **`[3] 🤖 20 Yapay Zeka Aracını Çalıştır`** : Menüden dilediğiniz aracı seçip hazır örnekle veya kendi metninizle anında çalıştırabilirsiniz.
* **`[4] 🧪 Tüm Araçları Test Et`** : 20 aracın entegrasyon testini koşar.
* **`[5] 📖 Ücretsiz API Anahtarı Alma Rehberi`** : Kredi kartsız 30 saniyede ücretsiz Gemini anahtarı alma rehberi.

---

### 3️⃣ Yöntem 3: Görsel Web Portalı (`web/index.html`)

Doğrudan `web/index.html` dosyasına çift tıklayarak tarayıcınızda açabilirsiniz:
1. **Demo / Test Modu (Anahtarsız):** Hiçbir API anahtarı girmeden de sol menüden istediğiniz aracı seçip **"✨ Hazır Örnek Yükle"** ve **"🚀 Yapay Zeka ile Analiz Et"** diyerek çıktısını inceleyebilirsiniz.
2. **Canlı Yapay Zeka Modu:** Sağ üstteki **"⚙️ Ayarla"** butonuna basarak Google Gemini veya OpenAI anahtarınızı yapıştırıp **"🔍 Doğrula & Kaydet"** butonuna tıklayın. Anahtarınız doğrudan tarayıcı üzerinden canlı test edilir ve onaylanır!

---

## 🔑 30 Saniyede Ücretsiz API Anahtarı Nasıl Alınır?

Yapay zeka araçlarını canlı kullanmak için en kolay yol **Google Gemini** kullanmaktır:

1. [Google AI Studio API Key](https://aistudio.google.com/app/apikey) sayfasına gidin.
2. Google (Gmail) hesabınızla giriş yapın (*Kredi kartı, telefon onayı veya ödeme bilgisi gerekmez*).
3. Mavi renkli **"Create API Key"** butonuna tıklayın.
4. Çıkan `AIzaSy...` ile başlayan anahtarı kopyalayın.
5. Web portalında veya `python baslat.py` sihirbazında yapıştırıp kaydedin!

> 💡 *Not: Dilerseniz [OpenAI Platform](https://platform.openai.com/api-keys) üzerinden aldığınız `sk-...` anahtarınızı da aynı şekilde tanımlayabilirsiniz.*

---

### 💻 Komut Satırından (CLI) Bağımsız Araç Çağırma

Her araç doğrudan bağımsız bir komut satırı betiği olarak da çalıştırılabilir:

```bash
# Otomatik .env dosyasından okuyarak:
python muhasebe/01_fismatik_ai.py

# Simülasyon / Test modunda (API anahtarsız deneme):
python hukuk/08_sozlesme_denetleyici_ai.py --test

# Farklı sağlayıcı belirterek:
python kobi/16_kep_nobetci_ai.py --provider gemini
```

---

## 🧪 Entegrasyon Testleri

Tüm 20 aracın girdi formatlarını, prompt şablonlarını ve JSON serialization yapılarını test etmek için:

```bash
python scripts/test_all_ai_tools.py
```

Çıktı Özeti:
```
======================================================================
  TURKIYE YAPAY ZEKA ARACLARI - ENTEGRASYON TESTI (20 ARAC)
======================================================================
[01/20] [PASS] FismatikAi
[02/20] [PASS] EdefterDebuggerAi
[03/20] [PASS] MevzuatOzelgeAi
[04/20] [PASS] BankaEkstresiAi
[05/20] [PASS] MizanCfoRaporuAi
[06/20] [PASS] BeyannameOnDenetimAi
[07/20] [PASS] BordroVergiAsistaniAi
[08/20] [PASS] SozlesmeDenetleyiciAi
[09/20] [PASS] IctihatOzetleyiciAi
[10/20] [PASS] DavaHafizasiAi
[11/20] [PASS] DilekceMimariAi
[12/20] [PASS] HukukWhisperNoteriAi
[13/20] [PASS] KvkkUyumDenetleyiciAi
[14/20] [PASS] EIhtarnameAi
[15/20] [PASS] FaturaAnomaliAi
[16/20] [PASS] KepNobetciAi
[17/20] [PASS] IhaleAsistanAi
[18/20] [PASS] SatisTeklifBotuAi
[19/20] [PASS] TesvikRadarAi
[20/20] [PASS] ReklamUyumAi
======================================================================
TEST SONUCU: 20/20 Basarili (0 Hata) - Tum araclar sorunsuz calisiyor!
======================================================================
```

---

## 🔒 Güvenlik, Gizlilik ve KVKK Taahhüdü

- **Veri Tutmama İlkesi (Zero Retention):** Bu kütüphane hiçbir kullanıcı girdisini, müşteri faturasını, mizan verisini veya dava evrakını kendi sunucularına iletmez.
- **Doğrudan İstemci-API İletişimi:** Çağrılar istemci makinesinden doğrudan resmi API sağlayıcılarına (`api.openai.com` veya `generativelanguage.googleapis.com`) HTTPS üzerinden şifreli iletilir.
- **BYOK (Kendi Anahtarını Getir):** API anahtarınız tarayıcınızın yerel hafızasında (`localStorage`) saklanır, çerezlere veya harici servislere aktarılmaz.

---

## 🤝 Katkıda Bulunma

1. Bu depoyu Fork'layın (`gh repo fork eimza-kep/turkiye-yapay-zeka-araclari`).
2. Yeni bir özellik dalı oluşturun (`git checkout -b feature/yeni-arac`).
3. Değişikliklerinizi commit edin (`git commit -m 'feat: Yeni mevzuat kontrol aracı eklendi'`).
4. Dalınıza push yapın (`git push origin feature/yeni-arac`).
5. Bir Pull Request açın.

---

## 📜 Lisans

Bu proje [MIT Lisansı](LICENSE) altında lisanslanmıştır. Ticari ve bireysel kullanım için tamamen serbesttir.
