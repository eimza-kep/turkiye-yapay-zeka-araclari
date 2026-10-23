# -*- coding: utf-8 -*-
"""
ai_client.py
------------
OpenAI, Google Gemini, Anthropic ve Yerel LLM'ler (Ollama, LM Studio, Llama.cpp)
için sıfır bağımlılıklı, hafif ve evrensel Python istemcisi. Python standart kütüphanesini
(urllib.request, json) kullanır; harici paket (pip install) gerektirmez.

Avukatlar ve mali müşavirler için KVKK ve gizlilik uyumlu %100 yerel çevrimdışı
(Ollama / LM Studio) model desteği ve yerleşik .env okuyucu içerir.
"""

import os
import sys
import json
import urllib.request
import urllib.error

# Windows console UTF-8 desteği
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

LOCAL_PROVIDERS = ("ollama", "lmstudio", "llamacpp", "local")

def load_dotenv():
    """
    Harici python-dotenv kütüphanesine ihtiyaç duymadan
    proje kök dizinindeki veya çalışma dizinindeki .env dosyasını okur.
    """
    candidates = [
        os.path.join(os.getcwd(), ".env"),
        os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), ".env"),
    ]
    for path in candidates:
        if os.path.isfile(path):
            try:
                with open(path, "r", encoding="utf-8") as f:
                    for line in f:
                        line = line.strip()
                        if line and not line.startswith("#") and "=" in line:
                            k, v = line.split("=", 1)
                            k = k.strip()
                            v = v.strip().strip("'\"")
                            if k and k not in os.environ:
                                os.environ[k] = v
            except Exception:
                pass
            break

# Modül yüklendiğinde otomatik .env oku
load_dotenv()

class AIClient:
    def __init__(self, api_key=None, provider=None, model=None, mock=False):
        self.mock = mock
        load_dotenv()

        # Doğrudan girilen veya ortam değişkeninden okunan anahtar
        self.api_key = api_key or os.environ.get("GEMINI_API_KEY") or os.environ.get("OPENAI_API_KEY")

        # Sağlayıcı tespiti
        if provider:
            self.provider = provider.lower()
        elif os.environ.get("USE_OLLAMA", "").lower() in ("true", "1") or os.environ.get("DEFAULT_AI_PROVIDER", "").lower() == "ollama":
            self.provider = "ollama"
        elif os.environ.get("USE_LMSTUDIO", "").lower() in ("true", "1") or os.environ.get("DEFAULT_AI_PROVIDER", "").lower() == "lmstudio":
            self.provider = "lmstudio"
        elif self.api_key and self.api_key.startswith("AIza"):
            self.provider = "gemini"
        elif self.api_key and self.api_key.startswith("sk-ant-"):
            self.provider = "anthropic"
        elif self.api_key and self.api_key.startswith("sk-"):
            self.provider = "openai"
        elif os.environ.get("GEMINI_API_KEY"):
            self.provider = "gemini"
            self.api_key = os.environ.get("GEMINI_API_KEY")
        elif os.environ.get("ANTHROPIC_API_KEY"):
            self.provider = "anthropic"
            self.api_key = os.environ.get("ANTHROPIC_API_KEY")
        elif os.environ.get("OPENAI_API_KEY"):
            self.provider = "openai"
            self.api_key = os.environ.get("OPENAI_API_KEY")
        else:
            self.provider = os.environ.get("DEFAULT_AI_PROVIDER", "gemini").lower()

        # Model seçimi
        if model:
            self.model = model
        elif self.provider == "gemini":
            self.model = "gemini-1.5-flash"
        elif self.provider == "anthropic":
            self.model = "claude-3-5-sonnet-20241022"
        elif self.provider == "ollama":
            self.model = os.environ.get("OLLAMA_MODEL", "llama3")
        elif self.provider in ("lmstudio", "llamacpp", "local"):
            self.model = os.environ.get("LOCAL_MODEL", "local-model")
        else:
            self.model = "gpt-4o-mini"

    def generate(self, system_prompt, user_content, response_format=None):
        """
        Modelden metin veya JSON yanıt üretir.
        """
        if self.mock or (not self.api_key and self.provider not in LOCAL_PROVIDERS):
            return self._generate_mock(system_prompt, user_content, response_format)

        try:
            if self.provider == "gemini":
                return self._call_gemini(system_prompt, user_content, response_format)
            elif self.provider == "anthropic":
                return self._call_anthropic(system_prompt, user_content, response_format)
            elif self.provider == "ollama":
                return self._call_ollama(system_prompt, user_content, response_format)
            elif self.provider == "lmstudio":
                return self._call_lmstudio(system_prompt, user_content, response_format)
            elif self.provider == "llamacpp":
                return self._call_llamacpp(system_prompt, user_content, response_format)
            elif self.provider == "local":
                return self._call_auto_local(system_prompt, user_content, response_format)
            else:
                return self._call_openai(system_prompt, user_content, response_format)
        except urllib.error.HTTPError as e:
            err_body = ""
            try:
                err_body = e.read().decode("utf-8")
            except Exception:
                pass
            return f"❌ API Hatası (HTTP {e.code} - {self.provider.upper()}):\n{err_body or str(e)}\n\n💡 İpucu: Anahtarınızı kontrol ediniz veya simülasyon modu için --mock kullanınız."
        except Exception as e:
            return f"❌ Bağlantı Hatası ({self.provider.upper()}): {e}"

    def _call_openai(self, system_prompt, user_content, response_format):
        url = "https://api.openai.com/v1/chat/completions"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }

        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_content}
            ],
            "temperature": 0.2
        }

        if response_format == "json":
            payload["response_format"] = {"type": "json_object"}

        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(url, data=data, headers=headers, method="POST")

        with urllib.request.urlopen(req, timeout=45) as resp:
            res_body = resp.read().decode("utf-8")
            res_json = json.loads(res_body)
            return res_json["choices"][0]["message"]["content"]

    def _call_gemini(self, system_prompt, user_content, response_format):
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{self.model}:generateContent?key={self.api_key}"
        headers = {"Content-Type": "application/json"}

        combined_prompt = f"{system_prompt}\n\nKULLANICI GİRDİSİ:\n{user_content}"
        payload = {
            "contents": [
                {
                    "parts": [{"text": combined_prompt}]
                }
            ],
            "generationConfig": {
                "temperature": 0.2
            }
        }

        if response_format == "json":
            payload["generationConfig"]["responseMimeType"] = "application/json"

        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(url, data=data, headers=headers, method="POST")

        with urllib.request.urlopen(req, timeout=45) as resp:
            res_body = resp.read().decode("utf-8")
            res_json = json.loads(res_body)
            candidates = res_json.get("candidates", [])
            if candidates:
                parts = candidates[0].get("content", {}).get("parts", [])
                if parts:
                    return parts[0].get("text", "")
            return "Yanıt alınamadı."

    def _call_anthropic(self, system_prompt, user_content, response_format):
        url = "https://api.anthropic.com/v1/messages"
        headers = {
            "Content-Type": "application/json",
            "x-api-key": self.api_key,
            "anthropic-version": "2023-06-01"
        }
        payload = {
            "model": self.model if self.model.startswith("claude") else "claude-3-5-sonnet-20241022",
            "system": system_prompt,
            "messages": [
                {"role": "user", "content": user_content}
            ],
            "max_tokens": 4096,
            "temperature": 0.2
        }
        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(url, data=data, headers=headers, method="POST")

        with urllib.request.urlopen(req, timeout=60) as resp:
            res_body = resp.read().decode("utf-8")
            res_json = json.loads(res_body)
            content = res_json.get("content", [])
            if content and isinstance(content, list):
                return content[0].get("text", "")
            return "Anthropic yanıtı alınamadı."

    def _call_ollama(self, system_prompt, user_content, response_format):
        host = os.environ.get("OLLAMA_HOST", "http://localhost:11434")
        url = f"{host.rstrip('/')}/api/generate"
        headers = {"Content-Type": "application/json"}
        payload = {
            "model": self.model,
            "system": system_prompt,
            "prompt": user_content,
            "stream": False
        }
        if response_format == "json":
            payload["format"] = "json"

        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(url, data=data, headers=headers, method="POST")

        with urllib.request.urlopen(req, timeout=120) as resp:
            res_body = resp.read().decode("utf-8")
            res_json = json.loads(res_body)
            return res_json.get("response", "Ollama yanıtı alınamadı.")

    def _call_lmstudio(self, system_prompt, user_content, response_format):
        host = os.environ.get("LMSTUDIO_HOST", "http://localhost:1234")
        url = f"{host.rstrip('/')}/v1/chat/completions"
        headers = {"Content-Type": "application/json"}
        payload = {
            "model": self.model if self.model != "local-model" else "local",
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_content}
            ],
            "temperature": 0.2
        }
        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(url, data=data, headers=headers, method="POST")

        with urllib.request.urlopen(req, timeout=120) as resp:
            res_body = resp.read().decode("utf-8")
            res_json = json.loads(res_body)
            return res_json["choices"][0]["message"]["content"]

    def _call_llamacpp(self, system_prompt, user_content, response_format):
        host = os.environ.get("LLAMACPP_HOST", "http://localhost:8080")
        url = f"{host.rstrip('/')}/v1/chat/completions"
        headers = {"Content-Type": "application/json"}
        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_content}
            ],
            "temperature": 0.2
        }
        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(url, data=data, headers=headers, method="POST")

        with urllib.request.urlopen(req, timeout=120) as resp:
            res_body = resp.read().decode("utf-8")
            res_json = json.loads(res_body)
            return res_json["choices"][0]["message"]["content"]

    def _call_auto_local(self, system_prompt, user_content, response_format):
        """
        Yerel sunucuları otomatik algılar: Önce Ollama (11434), sonra LM Studio (1234), sonra Llama.cpp (8080).
        """
        # 1. Ollama dene
        try:
            return self._call_ollama(system_prompt, user_content, response_format)
        except Exception:
            pass

        # 2. LM Studio dene
        try:
            return self._call_lmstudio(system_prompt, user_content, response_format)
        except Exception:
            pass

        # 3. Llama.cpp dene
        try:
            return self._call_llamacpp(system_prompt, user_content, response_format)
        except Exception as e:
            return f"❌ Yerel LLM Sunucusuna (Ollama 11434 / LM Studio 1234) bağlanılamadı. Lütfen yerel model sunucunuzu başlatınız: {e}"

    def _generate_mock(self, system_prompt, user_content, response_format):
        """
        API anahtarı bulunmadığında veya CI testlerinde deterministik simülasyon yanıtı döner.
        """
        is_local = self.provider in LOCAL_PROVIDERS
        mode_str = "YEREL LLM MODU (KVKK & Gizlilik Uyumlu)" if is_local else "API Anahtarsız Mod"
        return f"""[SİMÜLASYON / TEST ÇIKTISI - {mode_str}]
Model: {self.model} ({self.provider.upper()})
Analiz Özeti:
Kullanıcı girdisi başarıyla ayrıştırıldı ({len(user_content)} karakter). Sistem promptu kuralları başarıyla işletildi.

✅ İşlem Sonucu: Başarılı
📌 Girdi Özeti: {user_content[:120]}...
💡 Not: Canlı yapay zeka çıktısı almak için 'python baslat.py' çalıştırıp API anahtarınızı veya yerel LLM sunucunuzu seçebilirsiniz."""

    @staticmethod
    def validate_key(api_key, provider="gemini"):
        """
        Verilen API anahtarının veya yerel sunucunun geçerliliğini test eder.
        Döner: (bool, str) -> (Başarılı mı, Mesaj)
        """
        prov = provider.lower()
        if prov == "ollama":
            try:
                host = os.environ.get("OLLAMA_HOST", "http://localhost:11434")
                url = f"{host.rstrip('/')}/api/tags"
                req = urllib.request.Request(url, method="GET")
                with urllib.request.urlopen(req, timeout=5) as resp:
                    if resp.status == 200:
                        return True, "✅ Yerel Ollama sunucusuna bağlanıldı ve aktif (KVKK Güvenli)!"
            except Exception as e:
                return False, f"❌ Ollama sunucusuna erişilemedi ({e}). Ollama'nın (http://localhost:11434) çalıştığından emin olun."

        elif prov in ("lmstudio", "llamacpp", "local"):
            host = os.environ.get("LMSTUDIO_HOST", "http://localhost:1234")
            try:
                url = f"{host.rstrip('/')}/v1/models"
                req = urllib.request.Request(url, method="GET")
                with urllib.request.urlopen(req, timeout=5) as resp:
                    if resp.status == 200:
                        return True, f"✅ Yerel {prov.upper()} OpenAI-uyumlu sunucuya bağlanıldı!"
            except Exception as e:
                return False, f"❌ Yerel sunucuya erişilemedi ({host}): {e}"

        elif prov == "gemini":
            try:
                url = f"https://generativelanguage.googleapis.com/v1beta/models?key={api_key}"
                req = urllib.request.Request(url, method="GET")
                with urllib.request.urlopen(req, timeout=7) as resp:
                    if resp.status == 200:
                        return True, "✅ Google Gemini API anahtarı başarıyla doğrulandı!"
            except urllib.error.HTTPError as e:
                return False, f"❌ Gemini API Hatası (HTTP {e.code})"
            except Exception as e:
                return False, f"❌ Bağlantı hatası: {e}"

        elif prov == "openai":
            try:
                url = "https://api.openai.com/v1/models"
                headers = {"Authorization": f"Bearer {api_key}"}
                req = urllib.request.Request(url, headers=headers, method="GET")
                with urllib.request.urlopen(req, timeout=7) as resp:
                    if resp.status == 200:
                        return True, "✅ OpenAI API anahtarı başarıyla doğrulandı!"
            except urllib.error.HTTPError as e:
                return False, f"❌ OpenAI API Hatası (HTTP {e.code})"
            except Exception as e:
                return False, f"❌ Bağlantı hatası: {e}"

        return False, "Bilinmeyen sağlayıcı."

def generate_response(system_prompt, user_content, response_format=None, mock=False, provider=None, model=None):
    """
    Hızlı kullanım için yardımcı fonksiyon.
    """
    client = AIClient(provider=provider, model=model, mock=mock)
    return client.generate(system_prompt, user_content, response_format)

