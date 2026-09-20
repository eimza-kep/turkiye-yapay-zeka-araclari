#!/usr/bin/env bash
cd "$(dirname "$0")"

echo "======================================================================"
echo "   🇹🇷 Türkiye Yapay Zeka Araçları - Kolay Başlatıcı"
echo "======================================================================"

if command -v python3 &>/dev/null; then
    python3 baslat.py
elif command -v python &>/dev/null; then
    python baslat.py
else
    echo "[BİLGİ] Python bulunamadı. Web portalı açılıyor..."
    xdg-open web/index.html 2>/dev/null || open web/index.html 2>/dev/null
fi
