# -*- coding: utf-8 -*-
"""
ai_client.py
------------
OpenAI ve Google Gemini REST API'leri için sıfır bağımlılıklı,
hafif ve evrensel Python istemcisi. Python standart kütüphanesini
(urllib.request, json) kullanır; ek paket gerektirmez.
"""

import os
import sys
import json
import urllib.request
import urllib.error

# Windows console UTF-8 desteği
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

class AIClient:
    def __init__(self, api_key=None, provider=None, model=None, mock=False):
        self.mock = mock
        self.api_key = api_key or os.environ.get("OPENAI_API_KEY") or os.environ.get("GEMINI_API_KEY")

        # Sağlayıcı tespiti
        if provider:
            self.provider = provider.lower()
        elif self.api_key and self.api_key.startswith("AIza"):
            self.provider = "gemini"
        elif self.api_key and self.api_key.startswith("sk-"):
            self.provider = "openai"
        elif os.environ.get("GEMINI_API_KEY"):
            self.provider = "gemini"
            self.api_key = os.environ.get("GEMINI_API_KEY")
        else:
            self.provider = "openai"

        # Model seçimi
        if model:
            self.model = model
        elif self.provider == "gemini":
            self.model = "gemini-1.5-flash"
        else:
            self.model = "gpt-4o-mini"

    def generate(self, system_prompt, user_content, response_format=None):
        """
        Modelden metin veya JSON yanıt üretir.
        """
        if self.mock or not self.api_key:
            return self._generate_mock(system_prompt, user_content, response_format)

        try:
            if self.provider == "gemini":
                return self._call_gemini(system_prompt, user_content, response_format)
            else:
                return self._call_openai(system_prompt, user_content, response_format)
        except Exception as e:
            # Gerçek API çağrısında internet/kota hatası olursa anlaşılır hata döndür
            return f"❌ API Bağlantı Hatası ({self.provider.upper()} - {self.model}): {e}\n(Not: Test amacıyla çalıştırmak için --mock parametresini kullanabilirsiniz.)"

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

    def _generate_mock(self, system_prompt, user_content, response_format):
        """
        API anahtarı bulunmadığında veya CI testlerinde deterministik simülasyon yanıtı döner.
        """
        return f"""[SİMÜLASYON / TEST ÇIKTISI - API Anahtarsız Mod]
Model: {self.model} ({self.provider.upper()})
Analiz Özeti:
Kullanıcı girdisi başarıyla ayrıştırıldı ({len(user_content)} karakter). Sistem promptu kuralları başarıyla işletildi.

✅ İşlem Sonucu: Başarılı
📌 Girdi Özeti: {user_content[:120]}...
💡 Not: Gerçek yapay zeka yanıtı almak için OPENAI_API_KEY veya GEMINI_API_KEY tanımlayınız."""

def generate_response(system_prompt, user_content, response_format=None, mock=False):
    client = AIClient(mock=mock)
    return client.generate(system_prompt, user_content, response_format)
