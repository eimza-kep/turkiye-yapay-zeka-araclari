# 🇹🇷 Türkiye Yapay Zeka Araçları (Mali Müşavir, Avukat ve KOBİ'ler İçin)

[![CI & Test Suite](https://github.com/eimza-kep/turkiye-yapay-zeka-araclari/actions/workflows/ci.yml/badge.svg)](https://github.com/eimza-kep/turkiye-yapay-zeka-araclari/actions/workflows/ci.yml)
[![Canlı Web Portalı](https://img.shields.io/badge/Demo-Canl%C4%B1%20Web%20Portal%C4%B1-brightgreen.svg)](https://eimza-kep.github.io/turkiye-yapay-zeka-araclari/)
[![Python Version](https://img.shields.io/badge/python-3.10%20%7C%203.11%20%7C%203.12-blue)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Dependencies](https://img.shields.io/badge/dependencies-0%20external%20(stdlib%20only)-brightgreen)](#)
[![Privacy: 100% Offline KVKK](https://img.shields.io/badge/Privacy-100%25%20Offline%20KVKK-blueviolet)](#)
[![Local LLM: Ollama & LM Studio](https://img.shields.io/badge/Local%20LLM-Ollama%20%7C%20LM%20Studio-orange)](#)
[![UYAP UDF Parser](https://img.shields.io/badge/UYAP-UDF%20%26%20XML%20Parser-red)](#)

Türkiye'de mali müşavirler, serbest muhasebeciler, avukatlar, hukuk büroları ve KOBİ'lerin günlük operasyonlarını yapay zeka ile hızlandırmak için geliştirilmiş **20 adet açık kaynaklı yapay zeka aracı, sıfır bağımlılıklı UYAP UDF ayrıştırıcısı ve modern web portalı**.

Bu proje; ağır kütüphanelere (LangChain, LlamaIndex, ChromaDB vb.) gerek duymadan, doğrudan **Yerel LLM'ler (Ollama, LM Studio, Llama.cpp)**, **Google Gemini** (`gemini-1.5-flash`) ve **OpenAI** (`gpt-4o-mini`) REST API'lerini kullanan **sıfır bağımlılıklı (zero-dependency)** saf Python mimarisine ve **tarayıcı üzerinde çalışan modern BYOK web arayüzüne** sahiptir.

---

## 🌟 Öne Çıkan Özellikler

1. **Sıfır Dış Bağımlılık (Pure Python Stdlib):**
   - Kodları çalıştırmak için `pip install` yapmanıza gerek yoktur. Python 3'ün yerleşik standart kütüphaneleri (`urllib.request`, `json`, `zipfile`, `re`) ile çalışır.
2. **%100 Yerel LLM & KVKK Uyumu (Ollama / LM Studio):**
   - Gizli dava dosyaları, ticari sırlar veya müşteri mizanları buluta çıkmadan, yerel makinenizde çalışan Llama 3, Qwen 2.5 veya Mistral modelleriyle **çevrimdışı (offline)** işlenir.
3. **Yerleşik UYAP UDF / XML Dava Evrakı Ayrıştırıcı (`core/udf_parser.py`):**
   - UYAP sisteminden indirilen `.udf` ve `.xml` uzantılı dava dosyalarını sıfır kütüphane ile açar; elektronik imza (E-İmza) sahiplerini, tarih ve görev bilgilerini ayıklar ve temiz Markdown metnine çevirir.
4. **BYOK (Bring Your Own Key) & Çift Bulut Sağlayıcı (Gemini & OpenAI):**
   - Google AI Studio'dan alınan ücretsiz Gemini anahtarı (`AIzaSy...`) veya OpenAI anahtarı (`sk-...`) doğrudan istemcide (localStorage) saklanır.
5. **Kapsamlı Türkiye Mevzuat & Vergi Bilgi Tabanı:**
   - Sistem istemleri (prompt templates); VUK, TDHP (Tekdüzen Hesap Planı), GİB e-Defter şemaları, HMK 119, İİK 89/1, 6698 sayılı KVKK, KOSGEB ve EKAP mevzuatlarına tam uyumludur.
6. **Dahili Test & Simülasyon Modu (`--test`):**
   - API anahtarınız veya yerel sunucunuz olmadan da araçların nasıl çalıştığını, girdi-çıktı formatlarını ve mantığını test edebileceğiniz deterministik simülasyon motoru.

---

## 🗂️ 20 Yapay Zeka Aracı Kataloğu

### 📊 1. Mali Müşavir ve Muhasebe Araçları (01 - 07)

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

### ⚖️ 2. Avukat ve Hukuk Bürosu Araçları (08 - 14)

*(Tüm hukuk araçları doğrudan `.udf` UYAP dava dosyası kabul eder)*

| No | Modül | Dosya | Açıklama |
|---|---|---|---|
| **08** | **Sözleşme Denetleyici AI** | [`hukuk/08_sozlesme_denetleyici_ai.py`](hukuk/08_sozlesme_denetleyici_ai.py) | Ticari sözleşmelerdeki tek taraflı cezai şartları, fahiş tazminat maddelerini ve yetki şartlarını tespit eder, revize madde (redline) önerir. (.udf / metin) |
| **09** | **İçtihat Özetleyici AI** | [`hukuk/09_ictihat_ozetleyici_ai.py`](hukuk/09_ictihat_ozetleyici_ai.py) | 30 sayfalık Yargıtay Hukuk Genel Kurulu veya BAM kararlarını; Uyuşmazlık, Hukuki Gerekçe, Hüküm Özeti ve Emsal Değeri başlıklarında özetler. (.udf / metin) |
| **10** | **Dava Hafızası AI** | [`hukuk/10_dava_hafizasi_ai.py`](hukuk/10_dava_hafizasi_ai.py) | Duruşma tutanakları ile tanık/davalı beyanlarını karşılaştırarak zamansal ve olgusal çelişkileri tablo halinde tespit eder. (.udf / metin) |
| **11** | **HMK Dilekçe Mimarı AI** | [`hukuk/11_dilekce_mimari_ai.py`](hukuk/11_dilekce_mimari_ai.py) | Olay örgüsü ve delil listesinden HMK Madde 119 standartlarına tam uyumlu dava/cevap dilekçesi taslağı inşa eder. (.udf / metin) |
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

## 🦙 Yerel LLM Kurulum Rehberi (Ollama / LM Studio)

Avukatlar, mali müşavirler ve kurumsal firmalar için **KVKK ve gizlilik gereği hiçbir verinin buluta gitmediği %100 yerel çalışma**:

### 1. Ollama ile Çevrimdışı Çalışma

1. [ollama.com](https://ollama.com) adresinden Ollama'yı indirip kurun.
2. Türkçe başarısı yüksek bir model indirin:
   ```bash
   ollama pull llama3.2
   # veya
   ollama pull qwen2.5:7b
   ```
3. Web portalından (tarayıcıdan) erişim sağlamak için Ollama'yı CORS izniyle başlatın:
   ```bash
   # Windows PowerShell:
   $env:OLLAMA_ORIGINS="*" ; ollama serve

   # Linux / macOS:
   OLLAMA_ORIGINS="*" ollama serve
   ```
4. `.env` dosyanıza şu satırı ekleyin veya `python baslat.py` içinden seçin:
   ```env
   DEFAULT_AI_PROVIDER=ollama
   OLLAMA_HOST=http://localhost:11434
   OLLAMA_MODEL=llama3.2
   ```

### 2. LM Studio ile Çalışma

1. [lmstudio.ai](https://lmstudio.ai) uygulamasını açın ve istediğiniz modeli (örneğin Qwen 2.5 veya Mistral) indirin.
2. Sol menüden **"Local Server"** sekmesine gelin.
3. Modeli seçip yeşil renkli **"Start Server"** butonuna tıklayın (`http://localhost:1234`).
4. Web portalında veya `.env` dosyasında sağlayıcıyı `lmstudio` olarak seçin.

---

## ⚖️ UYAP UDF / XML Dava Evrakı Entegrasyonu

UYAP formatındaki dava evrakları (`.udf`), sıkıştırılmış bir ZIP arşivi içinde `content.xml` dosyasını barındırır. Bu depoda yer alan yerleşik `core/udf_parser.py` modülü:
* Harici bir paket yüklemeden dosya içeriğini çözer.
* Evrakın kaç kelime ve karakter olduğunu hesaplar.
* Belgeye atılmış tüm **Elektronik İmza (E-İmza)** sahiplerini, imza tarihlerini ve unvanlarını tespit eder.
* Yapay zeka RAG boru hatlarına doğrudan verilebilecek YAML ön bilgili Markdown formatı üretir.

### Python Koduyla Kullanım:
```python
from core.udf_parser import parse_udf, read_udf_or_text

# 1. Doğrudan UDF dosyasını ayrıştırıp metaverileri alma:
sonuc = parse_udf("dava_dilekcesi.udf")
print("Belge Metni:", sonuc["text"])
print("E-İmza Sahipleri:", sonuc["signers"])

# 2. Hukuk araçlarına dosya yolunu doğrudan parametre geçme:
metin = read_udf_or_text("dava_dilekcesi.udf")
```

### CLI Üzerinden Kullanım:
```bash
python hukuk/08_sozlesme_denetleyici_ai.py "ornek_sozlesme.udf"
python hukuk/09_ictihat_ozetleyici_ai.py "yargitay_karari.udf"
python hukuk/10_dava_hafizasi_ai.py "durusma_tutanagi.udf"
python hukuk/11_dilekce_mimari_ai.py "olay_ve_deliller.udf"
```

### Web Portalında Kullanım:
Web arayüzünde **"⚖️ UYAP UDF / Belge Yükle"** butonuna basarak `.udf` dosyanızı seçtiğinizde, tarayıcınız dosyayı doğrudan yerel hafızada ayrıştırır ve metin alanına aktarır.

---

## 🚀 Başlangıç & Kurulum Yöntemleri

### 1️⃣ Yöntem 1: Windows'ta Tek Tıkla Başlatma (En Kolay)

Depo kök dizinindeki başlatıcılara çift tıklayabilirsiniz:
- **`Baslat.bat`** : Python'u bulur ve interaktif Türkçe menüyü açar.
- **`Web-Portali.bat`** : 20 AI aracının bulunduğu görsel web arayüzünü tarayıcınızda açar.
- **`baslat.sh`** (Mac & Linux): Terminalde `./baslat.sh` ile çalıştırılır.

---

### 2️⃣ Yöntem 2: İnteraktif Terminal Sihirbazı (`python baslat.py`)

```bash
python baslat.py
```

Açılan renkli Türkçe menüde:
* **`[1] 🌐 Web Portalını Aç`** : Yerel sunucuyu açar ve web portalını tarayıcıda başlatır.
* **`[2] 🔑 API / Model Yapılandırması`** : Ollama, LM Studio, Gemini veya OpenAI seçimi yapıp tek tuşla doğrular.
* **`[3] 🤖 20 Yapay Zeka Aracından Birini Çalıştır`** : İster hazır örnekle, ister kendi metninizle, ister `.udf` dosyanızla çalıştırın.
* **`[4] 🧪 Tüm Araçları Test Et`** : 20 aracın entegrasyon ve UDF testlerini koşar.
* **`[5] 📖 Ücretsiz API Rehberi`** : Kredi kartsız Gemini anahtarı alma kılavuzu.

---

### 3️⃣ Yöntem 3: Görsel Web Portalı (`web/index.html`)

Doğrudan `web/index.html` dosyasına çift tıklayarak tarayıcınızda açabilirsiniz:
1. **Demo / Test Modu (Anahtarsız):** Hiçbir API anahtarı girmeden de sol menüden istediğiniz aracı seçip **"✨ Hazır Örnek Yükle"** ve **"🚀 Yapay Zeka ile Analiz Et"** diyerek simülasyon çıktısını inceleyebilirsiniz.
2. **Canlı / Çevrimdışı Mod:** Sağ üstteki **"⚙️ Ayarla"** butonuna basarak:
   - **Google Gemini** (Ücretsiz kota)
   - **OpenAI** (GPT-4o-mini)
   - **Ollama** (Yerel & KVKK Güvenli)
   - **LM Studio** (Offline Local Server)
   seçeneklerinden birini kaydedebilirsiniz.

---

## 🔑 30 Saniyede Ücretsiz API Anahtarı Nasıl Alınır?

Bulut yapay zeka modellerini ücretsiz kullanmak için Google Gemini:

1. [Google AI Studio API Key](https://aistudio.google.com/app/apikey) sayfasına gidin.
2. Google hesabınızla giriş yapın (*Kredi kartı veya ödeme bilgisi gerekmez*).
3. Mavi renkli **"Create API Key"** butonuna tıklayın.
4. Çıkan `AIzaSy...` ile başlayan anahtarı kopyalayın.
5. Web portalında veya `python baslat.py` sihirbazında kaydedin!

---

## 🧪 Entegrasyon Testleri

Tüm 20 aracın prompt şablonlarını, UDF ayrıştırıcısını ve yerel LLM modüllerini denetlemek için:

```bash
python scripts/test_all_ai_tools.py
```

Çıktı Özeti:
```
===============================================================================
      TÜRKİYE YAPAY ZEKA ARAÇLARI - 20 ARAÇLIK ENTEGRASYON TESTİ
===============================================================================
  [01/20] ✓ FişMatik AI: Fiş/Fatura OCR ve Tekdüzen Yevmiye Üretici (MUHASEBE) - OK
  ...
  [20/20] ✓ Reklam-Uyum AI: Reklam Kurulu Ceza Önleyici Denetçi (KOBI) - OK
-------------------------------------------------------------------------------
📊 Test Sonucu: 20/20 Araç Başarıyla Doğrulandı.
-------------------------------------------------------------------------------
⚖️ UYAP UDF & XML Dava Evrakı Ayrıştırıcı Testleri
  [01/03] ✓ clean_xml_tags (XML etiket temizleme) - OK
  [02/03] ✓ extract_udf_signers (Elektronik imza tespiti) - OK
  [03/03] ✓ parse_udf (Zero-dependency UDF ZIP/XML motoru) - OK
-------------------------------------------------------------------------------
🦙 Yerel LLM (Ollama, LM Studio, Llama.cpp) Desteği Testleri
  ✓ AIClient yerel sağlayıcı: ollama (Mock & Model: llama3) - OK
  ✓ AIClient yerel sağlayıcı: lmstudio (Mock & Model: local-model) - OK
  ✓ AIClient yerel sağlayıcı: llamacpp (Mock & Model: local-model) - OK
  ✓ AIClient yerel sağlayıcı: local (Mock & Model: local-model) - OK
  ✓ AIClient.validate_key yerel teşhis motoru - OK

🎉 Tüm 20 yapay zeka aracı, UYAP UDF motoru ve Yerel LLM testleri eksiksiz geçti!
```

---

## 🔒 Güvenlik, Gizlilik ve KVKK Taahhüdü

- **Veri Tutmama İlkesi (Zero Retention):** Bu kütüphane hiçbir kullanıcı girdisini, müşteri faturasını, mizan verisini veya dava evrakını harici sunuculara iletmez.
- **Doğrudan İstemci-Model İletişimi:** Çağrılar istemci makinesinden doğrudan resmi API sağlayıcılarına HTTPS şifreli iletilir veya yerel sunucuya (`localhost`) iletilir.
- **BYOK (Kendi Anahtarını Getir):** API anahtarınız tarayıcınızın yerel hafızasında (`localStorage`) saklanır, üçüncü taraflarla paylaşılmaz.
- **Yerel LLM (Ollama / LM Studio):** KVKK ve ticari sır gerekçesiyle verilerin internete çıkmasını istemiyorsanız, yerel modeller ile tam çevrimdışı çalışabilirsiniz.

---

## 🌐 E-Dönüşüm & LegalTech Açık Kaynak Ekosistemi

Bu depo, [@eimza-kep](https://github.com/eimza-kep) açık kaynak ekosisteminin yapay zeka omurgasıdır. İlgili diğer açık kaynak projelerimiz:

* 📄 [udf2md](https://github.com/eimza-kep/udf2md) - UYAP `.udf` dosyalarını Markdown ve JSON'a çeviren LegalTech CLI ve kütüphane (Yapay zeka RAG boru hatları için ideal).
* 📝 [javascript-udf-editor](https://github.com/eimza-kep/uyap-web-udf-editor) - Tarayıcı tabanlı modern web UDF belge görüntüleyici ve düzenleyici.
* ⚖️ [avukat-hukuk-excel-hesaplamalari](https://github.com/eimza-kep/avukat-hukuk-excel-hesaplamalari) - Hukuk büroları için AAÜT, arabuluculuk ve icra hesaplama araçları.
* 📊 [muhasebe-excel-sablonlari](https://github.com/eimza-kep/muhasebe-excel-sablonlari) - e-SMM, Tevkifat ve vergi kontrol motoru.
* 🏢 [kobi-finans-yonetim-excel-sablonlari](https://github.com/eimza-kep/kobi-finans-yonetim-excel-sablonlari) - Nakit akış, başabaş ve stok takip tabloları.
* 🌟 [awesome-turkiye-e-donusum](https://github.com/eimza-kep/awesome-turkiye-e-donusum) - Türkiye e-Dönüşüm açık kaynak araçları ve kütüphaneleri kürasyonu.

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
