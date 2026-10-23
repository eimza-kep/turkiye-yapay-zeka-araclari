#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
10_dava_hafizasi_ai.py
----------------------
Dava dosyası, duruşma tutanakları ve tanık beyanları arasındaki
çelişkileri ve yerine getirilmemiş ara kararları sorgulayan yapay zeka.
UYAP .udf duruşma zabıtlarını tek tıkla otomatik RAG hattına aktarır.
"""

import os
import sys
import argparse

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from core.ai_client import AIClient
from core.prompt_templates import PROMPT_TEMPLATES
from core.udf_parser import read_udf_or_text

TOOL_KEY = "10_dava_hafizasi_ai"

def run_tool(input_text=None, mock=False, api_key=None, provider=None):
    tool_info = PROMPT_TEMPLATES[TOOL_KEY]
    content = input_text if input_text else tool_info["sample_input"]

    print(f"\n===============================================================================")
    print(f"  {tool_info['title']}")
    print(f"===============================================================================\n")
    print(f"📥 Duruşma / Dosya Tutanakları:\n{content[:500]}...\n" if len(content) > 500 else f"📥 Duruşma / Dosya Tutanakları:\n{content}\n")
    print(f"🤖 Yapay Zeka Çelişkileri ve Kritik Beyanları İnceliyor...\n")

    client = AIClient(api_key=api_key, provider=provider, mock=mock)
    response = client.generate(tool_info["system_prompt"], content)

    print("📤 Yapay Zeka Çıktısı:")
    print("-------------------------------------------------------------------------------")
    print(response)
    print("-------------------------------------------------------------------------------\n")
    return response

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=PROMPT_TEMPLATES[TOOL_KEY]["title"])
    parser.add_argument("input", nargs="?", default=None, help="Duruşma zaptı metni, UYAP UDF dosyası (.udf) veya dosya yolu")
    parser.add_argument("--udf", default=None, help="UYAP duruşma zaptı UDF dosya yolu (.udf)")
    parser.add_argument("--test", "--mock", action="store_true", help="API anahtarsız test modu")
    parser.add_argument("--api-key", default=None, help="OpenAI, Gemini API Anahtarı veya 'local'")
    parser.add_argument("--provider", default=None, help="gemini, openai, anthropic veya ollama/local")
    args = parser.parse_args()

    target_file = args.udf or args.input
    user_input = read_udf_or_text(target_file) if target_file else None

    run_tool(user_input, mock=args.test, api_key=args.api_key, provider=args.provider)
