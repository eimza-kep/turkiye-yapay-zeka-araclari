# -*- coding: utf-8 -*-
"""
udf_parser.py
--------------
UYAP UDF (.udf) ve XML dava evrakları için sıfır bağımlılıklı Python ayrıştırıcısı.
Python standart kütüphanesini (zipfile, xml.etree.ElementTree, io, re) kullanır.
UDF içerisindeki 'content.xml' dosyasını açar, metni ve e-imza metaverilerini çıkarır.
"""

import os
import sys
import re
import io
import zipfile
import xml.etree.ElementTree as ET

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

def clean_xml_tags(xml_content: str) -> str:
    """
    XML etiketlerini temizleyerek okunabilir düz metin ve Markdown üretir.
    """
    if not xml_content:
        return ""

    # CDATA bloklarını aç
    xml_content = re.sub(r"<!\[CDATA\[(.*?)\]\]>", r"\1", xml_content, flags=re.DOTALL)

    # Paragraf sonları ve satır sonu etiketleri
    xml_content = re.sub(r"<(?:p|paragraph|br|div|tr)[^>]*>", "\n", xml_content, flags=re.IGNORECASE)
    xml_content = re.sub(r"</(?:p|paragraph|div|tr)>", "\n", xml_content, flags=re.IGNORECASE)

    # XML taglerini temizle
    text = re.sub(r"<[^>]+>", "", xml_content)

    # HTML/XML entity çözümleme
    text = text.replace("&nbsp;", " ") \
               .replace("&amp;", "&") \
               .replace("&lt;", "<") \
               .replace("&gt;", ">") \
               .replace("&quot;", '"') \
               .replace("&#39;", "'")

    # Fazla boşluk ve satırları düzenle
    lines = [line.strip() for line in text.split("\n")]
    clean_lines = []
    empty_count = 0
    for line in lines:
        if not line:
            empty_count += 1
            if empty_count <= 1:
                clean_lines.append("")
        else:
            empty_count = 0
            clean_lines.append(line)

    return "\n".join(clean_lines).strip()

def extract_udf_signers(xml_content: str) -> list:
    """
    UDF içerisindeki elektronik imza (E-İmza) sahiplerini tespit eder.
    """
    signers = []
    if not xml_content:
        return signers

    # 1. <signer name="..." date="..." role="..." issuer="...">
    for m in re.finditer(r'<signer\b([^>]*)>', xml_content, re.IGNORECASE):
        attrs = m.group(1)
        name_m = re.search(r'name=["\']([^"\']+)["\']', attrs, re.IGNORECASE)
        date_m = re.search(r'date=["\']([^"\']+)["\']', attrs, re.IGNORECASE)
        role_m = re.search(r'role=["\']([^"\']+)["\']', attrs, re.IGNORECASE)
        if name_m:
            name = name_m.group(1).strip()
            if not any(s["ad"] == name for s in signers):
                signers.append({
                    "ad": name,
                    "tarih": date_m.group(1).strip() if date_m else None,
                    "gorev": role_m.group(1).strip() if role_m else "İmza Sahibi"
                })

    # 2. <imzaci adSoyad="..." tarih="..." unvan="...">
    for m in re.finditer(r'<imzaci\b([^>]*)>', xml_content, re.IGNORECASE):
        attrs = m.group(1)
        name_m = re.search(r'(?:adSoyad|ad|name)=["\']([^"\']+)["\']', attrs, re.IGNORECASE)
        date_m = re.search(r'(?:tarih|date)=["\']([^"\']+)["\']', attrs, re.IGNORECASE)
        role_m = re.search(r'(?:unvan|gorev|role)=["\']([^"\']+)["\']', attrs, re.IGNORECASE)
        if name_m:
            name = name_m.group(1).strip()
            if not any(s["ad"] == name for s in signers):
                signers.append({
                    "ad": name,
                    "tarih": date_m.group(1).strip() if date_m else None,
                    "gorev": role_m.group(1).strip() if role_m else "İmza Sahibi"
                })

    # 3. XML-DSIG X509SubjectName CN=
    for m in re.finditer(r'CN=([^,\/<>"\n\r]+)', xml_content, re.IGNORECASE):
        cn = m.group(1).strip()
        if cn and not any(s["ad"] == cn for s in signers):
            signers.append({
                "ad": cn,
                "tarih": None,
                "gorev": "Elektronik İmza Sahibi"
            })

    return signers

def parse_udf(file_path_or_bytes, filename="evrak.udf") -> dict:
    """
    UYAP .udf dosyasını (veya ham byte dizisini) açarak metin ve meta verileri çıkarır.
    Döner:
    {
        "success": bool,
        "filename": str,
        "text": str,
        "signers": list,
        "word_count": int,
        "char_count": int,
        "markdown": str
    }
    """
    raw_bytes = None
    fname = filename

    if isinstance(file_path_or_bytes, str):
        if os.path.isfile(file_path_or_bytes):
            fname = os.path.basename(file_path_or_bytes)
            with open(file_path_or_bytes, "rb") as f:
                raw_bytes = f.read()
        else:
            # Doğrudan XML veya metin string'i
            raw_bytes = file_path_or_bytes.encode("utf-8", errors="replace")
    elif isinstance(file_path_or_bytes, (bytes, bytearray)):
        raw_bytes = bytes(file_path_or_bytes)
    else:
        return {"success": False, "error": "Geçersiz girdi tipi."}

    xml_text = None

    # 1. ZIP olup olmadığını kontrol et (UDF dosyaları tipik olarak ZIP arşividir)
    if raw_bytes[:4] == b"PK\x03\x04" or fname.lower().endswith(".udf"):
        try:
            with zipfile.ZipFile(io.BytesIO(raw_bytes)) as zf:
                content_filename = None
                for name in zf.namelist():
                    if name.lower() == "content.xml" or name.lower().endswith("/content.xml"):
                        content_filename = name
                        break

                if content_filename:
                    xml_text = zf.read(content_filename).decode("utf-8", errors="replace")
                else:
                    # Başka bir XML bulmaya çalış
                    xml_files = [n for n in zf.namelist() if n.lower().endswith(".xml")]
                    if xml_files:
                        xml_text = zf.read(xml_files[0]).decode("utf-8", errors="replace")
        except Exception:
            pass

    # 2. Eğer ZIP değilse doğrudan XML olarak dene
    if not xml_text:
        try:
            xml_text = raw_bytes.decode("utf-8", errors="replace")
        except Exception:
            return {"success": False, "error": "Dosya içeriği çözümlenemedi."}

    clean_text = clean_xml_tags(xml_text)
    signers = extract_udf_signers(xml_text)

    words = len(clean_text.split())
    chars = len(clean_text)

    # YAML Frontmatter ve Markdown çıktısı oluştur
    md = f"---\nbelge_adi: \"{fname}\"\nkelime_sayisi: {words}\nkarakter_sayisi: {chars}\n"
    if signers:
        md += "e_imza_sahipleri:\n"
        for s in signers:
            md += f"  - ad: \"{s['ad']}\"\n    gorev: \"{s.get('gorev') or ''}\"\n"
    md += "---\n\n" + clean_text

    return {
        "success": True,
        "filename": fname,
        "text": clean_text,
        "metin": clean_text,
        "signers": signers,
        "imzacilar": signers,
        "word_count": words,
        "char_count": chars,
        "markdown": md
    }

def read_udf_or_text(input_val: str) -> str:
    """
    Kullanıcı girdi parametresini denetler.
    Eğer dosya yolu bir .udf veya .xml ise otomatik parse edip metnini döner,
    aksi halde dosya içeriğini veya metnin kendisini döner.
    """
    if not input_val:
        return ""

    if os.path.isfile(input_val):
        lower_name = input_val.lower()
        if lower_name.endswith(".udf") or lower_name.endswith(".xml"):
            res = parse_udf(input_val)
            if res.get("success") and res.get("text"):
                return res["text"]
        with open(input_val, "r", encoding="utf-8", errors="ignore") as f:
            return f.read()

    return input_val
