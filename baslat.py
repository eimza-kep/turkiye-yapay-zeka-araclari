# -*- coding: utf-8 -*-
"""
baslat.py
---------
Türkiye Yapay Zeka Araçları - İnteraktif Başlatıcı ve Kurulum Sihirbazı.
Web portalını tek tuşla açar, API anahtarlarını kolayca ayarlar ve 20 yapay zeka
aracını menüden anında çalıştırmanızı sağlar.
"""

import os
import sys
import time
import webbrowser
import threading
from http.server import SimpleHTTPRequestHandler
import socketserver

# Proje kök dizinini sys.path'e ekle
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from core.ai_client import AIClient, load_dotenv
from core.prompt_templates import PROMPT_TEMPLATES

# Windows UTF-8 desteği
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ENV_PATH = os.path.join(ROOT_DIR, ".env")

def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

def print_banner():
    print("=" * 70)
    print("   🇹🇷 TÜRKİYE YAPAY ZEKA ARAÇLARI - KOLAY BAŞLATICI & SİHİRBAZ   ")
    print("   (Mali Müşavirler, Avukatlar ve KOBİ'ler İçin 20 AI Aracı)     ")
    print("=" * 70)

def get_current_keys():
    load_dotenv()
    gemini = os.environ.get("GEMINI_API_KEY", "").strip()
    openai = os.environ.get("OPENAI_API_KEY", "").strip()
    provider = os.environ.get("DEFAULT_AI_PROVIDER", "gemini").strip()
    return gemini, openai, provider

def mask_key(key):
    if not key:
        return "❌ Tanımlı Değil"
    if len(key) <= 8:
        return "****"
    return f"✅ {key[:6]}...{key[-4:]}"

def save_to_env(gemini_key=None, openai_key=None, default_provider=None, ollama_model=None):
    """
    Anahtarları ve model tercihlerini .env dosyasına güvenle kaydeder.
    """
    env_data = {}
    if os.path.exists(ENV_PATH):
        try:
            with open(ENV_PATH, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith("#") and "=" in line:
                        k, v = line.split("=", 1)
                        env_data[k.strip()] = v.strip().strip("'\"")
        except Exception:
            pass

    if gemini_key is not None:
        env_data["GEMINI_API_KEY"] = gemini_key.strip()
        os.environ["GEMINI_API_KEY"] = gemini_key.strip()
    if openai_key is not None:
        env_data["OPENAI_API_KEY"] = openai_key.strip()
        os.environ["OPENAI_API_KEY"] = openai_key.strip()
    if default_provider is not None:
        env_data["DEFAULT_AI_PROVIDER"] = default_provider.strip()
        os.environ["DEFAULT_AI_PROVIDER"] = default_provider.strip()
    if ollama_model is not None:
        env_data["OLLAMA_MODEL"] = ollama_model.strip()
        os.environ["OLLAMA_MODEL"] = ollama_model.strip()

    if "DEFAULT_AI_PROVIDER" not in env_data:
        env_data["DEFAULT_AI_PROVIDER"] = "gemini"

    try:
        with open(ENV_PATH, "w", encoding="utf-8") as f:
            f.write("# Türkiye Yapay Zeka Araçları - API ve Model Yapılandırması\n")
            for k, v in env_data.items():
                f.write(f"{k}={v}\n")
        return True
    except Exception as e:
        print(f"❌ .env dosyasına yazılamadı: {e}")
        return False

def run_local_server(port=8000):
    web_dir = os.path.join(ROOT_DIR, "web")
    class Handler(SimpleHTTPRequestHandler):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, directory=web_dir, **kwargs)
        def log_message(self, format, *args):
            pass # Sessiz mod

    try:
        with socketserver.TCPServer(("", port), Handler) as httpd:
            httpd.serve_forever()
    except Exception:
        pass

def launch_web_portal():
    print("\n🌐 Web Portalı Başlatılıyor...")
    port = 8000
    server_thread = threading.Thread(target=run_local_server, args=(port,), daemon=True)
    server_thread.start()
    time.sleep(0.5)
    
    url = f"http://localhost:{port}/index.html"
    print(f"✅ Yerel sunucu aktif: {url}")
    print("🚀 Tarayıcınızda açılıyor...")
    webbrowser.open(url)
    input("\nAna menüye dönmek için [Enter] tuşuna basınız...")

def api_key_wizard():
    while True:
        clear_screen()
        print_banner()
        gemini, openai, prov = get_current_keys()
        print("\n🔑 MEVCUT MODEL VE SAĞLAYICI YAPILANDIRMASI:")
        print(f"  • Aktif Sağlayıcı: {prov.upper()}")
        print(f"  • Google Gemini  : {mask_key(gemini)}")
        print(f"  • OpenAI         : {mask_key(openai)}")
        print(f"  • Yerel LLM      : Ollama / LM Studio (KVKK Çevrimdışı)")
        print("-" * 70)
        print("1. Google Gemini API Anahtarı Gir / Güncelle (ÖNERİLEN - ÜCRETSİZ)")
        print("2. OpenAI API Anahtarı Gir / Güncelle")
        print("3. Ollama Yerel LLM'e Geç (%100 Çevrimdışı & KVKK Uyumlu)")
        print("4. LM Studio Yerel Sunucuya Geç (http://localhost:1234)")
        print("5. Mevcut Bağlantıları Test Et & Doğrula")
        print("6. Anahtarları Temizle (Test / Demo Moduna Dön)")
        print("7. Ücretsiz Gemini Anahtarı Nasıl Alınır? (Rehber)")
        print("0. Ana Menüye Dön")
        print("-" * 70)

        choice = input("Seçiminiz [0-7]: ").strip()

        if choice == "1":
            print("\n💡 İpucu: Google AI Studio'dan aldığınız 'AIzaSy...' ile başlayan anahtarı yapıştırın.")
            print("   (Ücretsiz almak için: https://aistudio.google.com/app/apikey)")
            key = input("Gemini API Anahtarı: ").strip()
            if key:
                print("⏳ Anahtar test ediliyor...")
                ok, msg = AIClient.validate_key(key, "gemini")
                print(msg)
                if ok or "429" in msg:
                    save_to_env(gemini_key=key, default_provider="gemini")
                    print("💾 Anahtar .env dosyasına başarıyla kaydedildi!")
                else:
                    save_choice = input("Anahtar doğrulanamadı, yine de kaydetmek ister misiniz? (e/h): ").lower()
                    if save_choice == "e":
                        save_to_env(gemini_key=key, default_provider="gemini")
            input("\nDevam etmek için [Enter] tuşuna basınız...")

        elif choice == "2":
            print("\n💡 OpenAI platformundan aldığınız 'sk-...' ile başlayan anahtarı yapıştırın.")
            print("   (Almak için: https://platform.openai.com/api-keys)")
            key = input("OpenAI API Anahtarı: ").strip()
            if key:
                print("⏳ Anahtar test ediliyor...")
                ok, msg = AIClient.validate_key(key, "openai")
                print(msg)
                if ok or "429" in msg:
                    save_to_env(openai_key=key, default_provider="openai")
                    print("💾 Anahtar .env dosyasına başarıyla kaydedildi!")
                else:
                    save_choice = input("Anahtar doğrulanamadı, yine de kaydetmek ister misiniz? (e/h): ").lower()
                    if save_choice == "e":
                        save_to_env(openai_key=key, default_provider="openai")
            input("\nDevam etmek için [Enter] tuşuna basınız...")

        elif choice == "3":
            model_name = input("Ollama model adı (Varsayılan: llama3.2 veya qwen2.5): ").strip() or "llama3.2"
            print("⏳ Yerel Ollama sunucusu (http://localhost:11434) kontrol ediliyor...")
            ok, msg = AIClient.validate_key("", "ollama")
            print(msg)
            save_to_env(default_provider="ollama", ollama_model=model_name)
            print("✅ Aktif sağlayıcı Ollama olarak ayarlandı (%100 KVKK Güvenli).")
            input("\nDevam etmek için [Enter] tuşuna basınız...")

        elif choice == "4":
            print("⏳ LM Studio yerel sunucusu (http://localhost:1234) kontrol ediliyor...")
            ok, msg = AIClient.validate_key("", "lmstudio")
            print(msg)
            save_to_env(default_provider="lmstudio")
            print("✅ Aktif sağlayıcı LM Studio olarak ayarlandı.")
            input("\nDevam etmek için [Enter] tuşuna basınız...")

        elif choice == "5":
            print("\n🧪 Sağlayıcı Bağlantıları Test Ediliyor...")
            if gemini:
                ok, msg = AIClient.validate_key(gemini, "gemini")
                print(f"Google Gemini : {msg}")
            else:
                print("Google Gemini : Tanımlı değil.")

            if openai:
                ok, msg = AIClient.validate_key(openai, "openai")
                print(f"OpenAI        : {msg}")
            else:
                print("OpenAI        : Tanımlı değil.")

            ok_ol, msg_ol = AIClient.validate_key("", "ollama")
            print(f"Yerel Ollama  : {msg_ol}")
            input("\nDevam etmek için [Enter] tuşuna basınız...")

        elif choice == "6":
            save_to_env(gemini_key="", openai_key="", default_provider="demo")
            print("\n🗑️ Tüm API anahtarları temizlendi. Sistem artık Demo / Test modunda çalışacak.")
            input("\nDevam etmek için [Enter] tuşuna basınız...")

        elif choice == "7":
            show_key_guide()

        elif choice == "0":
            break

def show_key_guide():
    clear_screen()
    print_banner()
    print("""
📖 30 SANİYEDE ÜCRETSİZ GOOGLE GEMINI API ANAHTARI ALMA:
-------------------------------------------------------
1. Tarayıcınızda Google AI Studio'yu açın:
   👉 https://aistudio.google.com/app/apikey

2. Google hesabınızla giriş yapın.
   (Herhangi bir kredi kartı veya ödeme bilgisi İSTEMEZ).

3. Mavi renkli "Create API key" butonuna basın.

4. Üretilen 'AIzaSy...' ile başlayan kodu kopyalayıp buraya yapıştırın.

✅ Bu anahtar günlük yüzlerce ücretsiz analiz yapmanızı sağlar!
    """)
    open_now = input("Tarayıcıda Google AI Studio sayfasını açmak ister misiniz? (e/h): ").lower()
    if open_now == "e":
        webbrowser.open("https://aistudio.google.com/app/apikey")
    input("\nMenüye dönmek için [Enter] tuşuna basınız...")

def run_cli_tool():
    tools_list = list(PROMPT_TEMPLATES.items())
    while True:
        clear_screen()
        print_banner()
        print("\n🤖 20 YAPAY ZEKA ARACI LİSTESİ:\n")
        for i, (tool_id, data) in enumerate(tools_list, 1):
            cat_icon = "📊" if data["category"] == "muhasebe" else ("⚖️" if data["category"] == "hukuk" else "🏢")
            print(f"  [{i:02d}] {cat_icon} {data['title']}")

        print("\n  [00] Ana Menüye Dön")
        print("-" * 70)
        choice = input("Çalıştırmak istediğiniz araç numarasını giriniz [0-20]: ").strip()

        if choice in ["0", "00"]:
            break

        try:
            idx = int(choice) - 1
            if 0 <= idx < len(tools_list):
                tool_id, data = tools_list[idx]
                execute_single_tool(tool_id, data)
            else:
                print("Geçersiz numara!")
                time.sleep(1)
        except ValueError:
            print("Lütfen bir sayı giriniz!")
            time.sleep(1)

def execute_single_tool(tool_id, data):
    clear_screen()
    print_banner()
    print(f"\n🚀 SEÇİLEN ARAÇ: {data['title']}\n")
    print("1. Hazır Gerçekçi Örnek Senaryo ile Çalıştır")
    print("2. Kendi Metnimi / Verimi Girerek Çalıştır")
    print("3. UYAP UDF (.udf) veya XML Belgesi Dosyadan Yükle")
    print("0. Geri Dön")
    
    sub = input("\nSeçiminiz [1/2/3/0]: ").strip()
    if sub == "1":
        content = data["sample_input"]
        print("\n📥 KULLANILAN ÖRNEK GİRDİ:")
        print("-" * 50)
        print(content)
        print("-" * 50)
    elif sub == "2":
        print("\n📥 Lütfen incelenecek metni yapıştırın ve ardından boş bir satırda 'TAMAM' yazıp Enter'a basın:")
        lines = []
        while True:
            line = input()
            if line.strip().upper() == "TAMAM":
                break
            lines.append(line)
        content = "\n".join(lines).strip()
        if not content:
            print("Girdi boş olduğu için işlem iptal edildi.")
            input("\nDevam etmek için [Enter]...")
            return
    elif sub == "3":
        file_path = input("\n📁 UYAP UDF veya metin/xml dosya yolunu girin: ").strip().strip('"\'')
        if not file_path or not os.path.exists(file_path):
            print("❌ Dosya bulunamadı!")
            input("\nDevam etmek için [Enter]...")
            return
        from core.udf_parser import read_udf_or_text
        try:
            content = read_udf_or_text(file_path)
            print(f"✅ Dosya başarıyla okundu ({len(content)} karakter).")
        except Exception as e:
            print(f"❌ Dosya okuma hatası: {e}")
            input("\nDevam etmek için [Enter]...")
            return
    else:
        return

    print("\n⏳ Yapay Zeka Analizi Yapılıyor, Lütfen Bekleyiniz...\n")
    client = AIClient()
    response = client.generate(data["system_prompt"], content)
    
    print("=" * 70)
    print("📤 YAPAY ZEKA YANITI:")
    print("=" * 70)
    print(response)
    print("=" * 70)
    input("\nDevam etmek için [Enter] tuşuna basınız...")

def run_integration_tests():
    clear_screen()
    print_banner()
    print("\n🧪 20 Yapay Zeka Aracının Entegrasyon Testi Koşuluyor...\n")
    test_script = os.path.join(ROOT_DIR, "scripts", "test_all_ai_tools.py")
    if os.path.exists(test_script):
        cmd = f'"{sys.executable}" "{test_script}"'
        os.system(cmd)
    else:
        print("❌ Test betiği bulunamadı!")
    input("\nAna menüye dönmek için [Enter] tuşuna basınız...")

def main_menu():
    while True:
        clear_screen()
        print_banner()
        gemini, openai, prov = get_current_keys()
        
        if prov in ("ollama", "lmstudio", "llamacpp", "local"):
            mode_text = f"🟢 Yerel AI Modu ({prov.upper()} - %100 KVKK Güvenli)"
            active_prov = prov.upper()
        elif gemini or openai:
            mode_text = "🟢 Canlı Bulut AI Modu"
            active_prov = "Gemini" if gemini else "OpenAI"
        else:
            mode_text = "🧪 Demo / Simülasyon Modu (Anahtarsız)"
            active_prov = "Demo Motoru"

        print(f"\n📌 ÇALIŞMA DURUMU: {mode_text} (Aktif: {active_prov})")
        print("-" * 70)
        print("  [1] 🌐 Web Portalını Aç (Görsel Arayüz - Tek Tıkla Tarayıcıda)")
        print("  [2] 🔑 API Anahtarlarını / Yerel Modeli Ayarla (Ollama/LM Studio/Gemini)")
        print("  [3] 🤖 20 Yapay Zeka Aracından Birini Çalıştır (Terminal)")
        print("  [4] 🧪 Tüm Araçları Test Et (20/20 Doğrulama)")
        print("  [5] 📖 Ücretsiz API Anahtarı Nasıl Alınır? (Rehber)")
        print("  [0] 🚪 Çıkış")
        print("-" * 70)

        choice = input("Lütfen bir seçenek seçin [0-5]: ").strip()

        if choice == "1":
            launch_web_portal()
        elif choice == "2":
            api_key_wizard()
        elif choice == "3":
            run_cli_tool()
        elif choice == "4":
            run_integration_tests()
        elif choice == "5":
            show_key_guide()
        elif choice == "0":
            print("\n👋 Görüşmek üzere! Başarılar dileriz.\n")
            break

if __name__ == "__main__":
    main_menu()
