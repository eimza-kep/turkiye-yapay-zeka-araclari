#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
09_ictihat_ozetleyici_ai.py
---------------------------
Yargıtay ve Danıştay içtihatlarını 4 başlık altında özetleyen
ve davada lehe/aleyhe kullanım stratejisi üreten yapay zeka aracı.
UYAP .udf ve XML dava kararlarını tek tıkla otomatik içe aktarma desteği içerir.
"""

import os
import sys
import argparse

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from core.ai_client import AIClient
from core.prompt_templates import PROMPT_TEMPLATES
from core.udf_parser import read_udf_or_text

TOOL_KEY = "09_ictihat_ozetleyici_ai"

def run_tool(input_text=None, mock=False, api_key=None, provider=None):
    tool_info = PROMPT_TEMPLATES[TOOL_KEY]
    content = input_text if input_text else tool_info["sample_input"]

    print(f"\n===============================================================================")
    print(f"  {tool_info['title']}")
    print(f"===============================================================================\n")
    print(f"📥 Karar Metni:\n{content[:500]}...\n" if len(content) > 500 else f"📥 Karar Metni:\n{content}\n")
    print(f"🤖 Yapay Zeka Kararı Analiz Ediyor ve Dava Stratejisi Üretiyor...\n")

    client = AIClient(api_key=api_key, provider=provider, mock=mock)
    response = client.generate(tool_info["system_prompt"], content)

    print("📤 Yapay Zeka Çıktısı:")
    print("-------------------------------------------------------------------------------")
    print(response)
    print("-------------------------------------------------------------------------------\n")
    return response

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=PROMPT_TEMPLATES[TOOL_KEY]["title"])
    parser.add_argument("input", nargs="?", default=None, help="Yargıtay/Danıştay kararı, UDF dosya yolu (.udf) veya metin")
    parser.add_argument("--udf", default=None, help="UYAP UDF dosya yolu (.udf)")
    parser.add_argument("--test", "--mock", action="store_true", help="API anahtarsız test modu")
    parser.add_argument("--api-key", default=None, help="OpenAI, Gemini API Anahtarı veya 'local'")
    parser.add_argument("--provider", default=None, help="gemini, openai, anthropic veya ollama/local")
    args = parser.parse_args()

    target_file = args.udf or args.input
    user_input = read_udf_or_text(target_file) if target_file else None

    run_tool(user_input, mock=args.test, api_key=args.api_key, provider=args.provider)
