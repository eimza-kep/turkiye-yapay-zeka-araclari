#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
12_hukuk_whisper_noteri_ai.py
-----------------------------
Müvekkil ses kayıt deşifrelerinden olay kronolojisi,
tazminat talepleri ve delil listesi çıkaran yapay zeka hukuk noteri.
"""

import os
import sys
import argparse

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from core.ai_client import AIClient
from core.prompt_templates import PROMPT_TEMPLATES

TOOL_KEY = "12_hukuk_whisper_noteri_ai"

def run_tool(input_text=None, mock=False, api_key=None, provider=None):
    tool_info = PROMPT_TEMPLATES[TOOL_KEY]
    content = input_text if input_text else tool_info["sample_input"]

    print(f"\n===============================================================================")
    print(f"  {tool_info['title']}")
    print(f"===============================================================================\n")
    print(f"📥 Ses Kaydı Deşifre Metni:\n{content}\n")
    print(f"🤖 Yapay Zeka Hukuki Görüşme Tutanağını Hazırlıyor...\n")

    client = AIClient(api_key=api_key, provider=provider, mock=mock)
    response = client.generate(tool_info["system_prompt"], content)

    print("📤 Yapay Zeka Çıktısı:")
    print("-------------------------------------------------------------------------------")
    print(response)
    print("-------------------------------------------------------------------------------\n")
    return response

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=PROMPT_TEMPLATES[TOOL_KEY]["title"])
    parser.add_argument("input", nargs="?", default=None, help="Ses deşifre metni veya dosya yolu")
    parser.add_argument("--test", "--mock", action="store_true", help="API anahtarsız test modu")
    parser.add_argument("--api-key", default=None, help="OpenAI veya Gemini API Anahtarı")
    parser.add_argument("--provider", default=None, help="openai veya gemini")
    args = parser.parse_args()

    user_input = args.input
    if user_input and os.path.isfile(user_input):
        with open(user_input, "r", encoding="utf-8", errors="ignore") as f:
            user_input = f.read()

    run_tool(user_input, mock=args.test, api_key=args.api_key, provider=args.provider)
