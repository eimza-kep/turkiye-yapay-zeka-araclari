#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
test_all_ai_tools.py
--------------------
20 yapay zeka aracının tamamını sırayla test eder.
Mock/Test modunda her aracın prompt şablonunu, girdi doğrulamasını
ve çıktı üretimini denetler.
"""

import os
import sys
import importlib

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_DIR)

from core.prompt_templates import PROMPT_TEMPLATES

MODULE_MAP = {
    # Muhasebe
    "01_fismatik_ai": "muhasebe.01_fismatik_ai",
    "02_edefter_debugger_ai": "muhasebe.02_edefter_debugger_ai",
    "03_mevzuat_ozelge_ai": "muhasebe.03_mevzuat_ozelge_ai",
    "04_banka_ekstresi_ai": "muhasebe.04_banka_ekstresi_ai",
    "05_mizan_cfo_raporu_ai": "muhasebe.05_mizan_cfo_raporu_ai",
    "06_beyanname_on_denetim_ai": "muhasebe.06_beyanname_on_denetim_ai",
    "07_bordro_vergi_asistani_ai": "muhasebe.07_bordro_vergi_asistani_ai",
    # Hukuk
    "08_sozlesme_denetleyici_ai": "hukuk.08_sozlesme_denetleyici_ai",
    "09_ictihat_ozetleyici_ai": "hukuk.09_ictihat_ozetleyici_ai",
    "10_dava_hafizasi_ai": "hukuk.10_dava_hafizasi_ai",
    "11_dilekce_mimari_ai": "hukuk.11_dilekce_mimari_ai",
    "12_hukuk_whisper_noteri_ai": "hukuk.12_hukuk_whisper_noteri_ai",
    "13_kvkk_uyum_denetleyici_ai": "hukuk.13_kvkk_uyum_denetleyici_ai",
    "14_e_ihtarname_ai": "hukuk.14_e_ihtarname_ai",
    # KOBİ
    "15_fatura_anomali_ai": "kobi.15_fatura_anomali_ai",
    "16_kep_nobetci_ai": "kobi.16_kep_nobetci_ai",
    "17_ihale_asistan_ai": "kobi.17_ihale_asistan_ai",
    "18_satis_teklif_botu_ai": "kobi.18_satis_teklif_botu_ai",
    "19_tesvik_radar_ai": "kobi.19_tesvik_radar_ai",
    "20_reklam_uyum_ai": "kobi.20_reklam_uyum_ai",
}

def main():
    print("===============================================================================")
    print("      TÜRKİYE YAPAY ZEKA ARAÇLARI - 20 ARAÇLIK ENTEGRASYON TESTİ")
    print("===============================================================================\n")

    print(f"📋 Doğrulanacak Araç Sayısı: {len(MODULE_MAP)}")
    errors = []
    passed = 0

    for idx, (tool_key, module_path) in enumerate(MODULE_MAP.items(), 1):
        try:
            # 1. Şablon kontrolü
            if tool_key not in PROMPT_TEMPLATES:
                errors.append(f"[{tool_key}] PROMPT_TEMPLATES içinde tanımsız!")
                continue

            tool_info = PROMPT_TEMPLATES[tool_key]
            title = tool_info.get("title", tool_key)
            category = tool_info.get("category", "")
            system_prompt = tool_info.get("system_prompt", "")
            sample_input = tool_info.get("sample_input", "")

            if not system_prompt or len(system_prompt) < 30:
                errors.append(f"[{tool_key}] Yetersiz veya boş sistem promptu!")
                continue

            if not sample_input:
                errors.append(f"[{tool_key}] Örnek girdi verisi eksik!")
                continue

            # 2. Modülü dinamik yükle ve çalıştır
            mod = importlib.import_module(module_path)
            if not hasattr(mod, "run_tool"):
                errors.append(f"[{tool_key}] Modülde run_tool fonksiyonu bulunamadı!")
                continue

            # Mock modunda çalıştır
            output = mod.run_tool(sample_input, mock=True)
            if not output or len(output) < 20:
                errors.append(f"[{tool_key}] Boş veya yetersiz yanıt üretildi!")
                continue

            passed += 1
            print(f"  [{idx:02d}/20] ✓ {title} ({category.upper()}) - OK")
        except Exception as e:
            errors.append(f"[{tool_key}] Çalıştırma hatası: {e}")

    print("\n-------------------------------------------------------------------------------")
    print(f"📊 Test Sonucu: {passed}/{len(MODULE_MAP)} Araç Başarıyla Doğrulandı.")
    print("-------------------------------------------------------------------------------")

    if errors:
        print("\n⚠️ Tespit Edilen Hatalar:")
        for err in errors:
            print(f"  - {err}")
        return 1

    print("\n🎉 Tüm 20 yapay zeka aracı testleri eksiksiz geçti! Sistem canlıya hazır.")
    return 0

if __name__ == "__main__":
    sys.exit(main())
