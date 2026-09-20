#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
07_bordro_vergi_asistani_ai.py
------------------------------
Çalışanların maaş kesintileri, gelir vergisi dilimleri (%15, %20, %27)
ve net maaş değişimleri hakkında şeffaf ve hesaplamalı yanıt veren AI.
"""

import os
import sys
import argparse

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from core.ai_client import AIClient
from core.prompt_templates import PROMPT_TEMPLATES

TOOL_KEY = "07_bordro_vergi_asistani_ai"

def run_tool(input_text=None, mock=False, api_key=None, provider=None):
    tool_info = PROMPT_TEMPLATES[TOOL_KEY]
    content = input_text if input_text else tool_info["sample_input"]

    print(f"\n===============================================================================")
    print(f"  {tool_info['title']}")
    print(f"===============================================================================\n")
    print(f"📥 Çalışan Sorusu:\n{content}\n")
    print(f"🤖 Yapay Zeka Bordro ve Vergi Dilimi Açıklamasını Hazırlıyor...\n")

    client = AIClient(api_key=api_key, provider=provider, mock=mock)
    response = client.generate(tool_info["system_prompt"], content)

    print("📤 Yapay Zeka Çıktısı:")
    print("-------------------------------------------------------------------------------")
    print(response)
    print("-------------------------------------------------------------------------------\n")
    return response

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=PROMPT_TEMPLATES[TOOL_KEY]["title"])
    parser.add_argument("input", nargs="?", default=None, help="Maaş veya bordro sorusu")
    parser.add_argument("--test", "--mock", action="store_true", help="API anahtarsız test modu")
    parser.add_argument("--api-key", default=None, help="OpenAI veya Gemini API Anahtarı")
    parser.add_argument("--provider", default=None, help="openai veya gemini")
    args = parser.parse_args()

    user_input = args.input
    if user_input and os.path.isfile(user_input):
        with open(user_input, "r", encoding="utf-8", errors="ignore") as f:
            user_input = f.read()

    run_tool(user_input, mock=args.test, api_key=args.api_key, provider=args.provider)
