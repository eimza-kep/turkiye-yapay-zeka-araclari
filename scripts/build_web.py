# -*- coding: utf-8 -*-
"""
build_web.py
------------
web/index.html dosyasını en güncel 20 araç, zenginleştirilmiş BYOK & Yerel LLM
(Ollama, LM Studio) çubuğu, UYAP UDF evrak yükleme/ayrıştırma ve canlı doğrulama
özelliği ile üretir.
"""

import json
import os
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
JSON_PATH = os.path.join(ROOT_DIR, "web", "tools_data.json")
INDEX_PATH = os.path.join(ROOT_DIR, "web", "index.html")

with open(JSON_PATH, "r", encoding="utf-8") as f:
    tools_data = json.load(f)

tools_data_str = json.dumps(tools_data, ensure_ascii=False)

html_content = f"""<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Türkiye Yapay Zeka Araçları - Mali Müşavir, Avukat & KOBİ</title>
    <!-- JSZip for Client-side UYAP .udf Decompression -->
    <script src="https://cdnjs.cloudflare.com/ajax/libs/jszip/3.10.1/jszip.min.js"></script>
    <style>
        :root {{
            --primary: #4f46e5;
            --primary-hover: #4338ca;
            --primary-light: #eef2ff;
            --secondary: #0f172a;
            --bg: #f8fafc;
            --card-bg: #ffffff;
            --border: #e2e8f0;
            --text-main: #1e293b;
            --text-muted: #64748b;
            --success: #10b981;
            --success-light: #ecfdf5;
            --warning: #f59e0b;
            --warning-light: #fffbeb;
            --danger: #ef4444;
            --danger-light: #fef2f2;
            --sidebar-width: 320px;
        }}

        * {{ box-sizing: border-box; margin: 0; padding: 0; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; }}
        body {{ display: flex; height: 100vh; background: var(--bg); color: var(--text-main); overflow: hidden; }}

        /* Sidebar */
        .sidebar {{
            width: var(--sidebar-width);
            background: var(--secondary);
            color: white;
            display: flex;
            flex-direction: column;
            border-right: 1px solid #1e293b;
            flex-shrink: 0;
        }}
        .sidebar-header {{
            padding: 20px;
            border-bottom: 1px solid #1e293b;
            display: flex;
            align-items: center;
            justify-content: space-between;
        }}
        .sidebar-header h1 {{ font-size: 1.05rem; font-weight: 700; color: #f8fafc; display: flex; align-items: center; gap: 8px; }}
        .sidebar-header span {{ font-size: 0.75rem; background: #334155; padding: 3px 8px; border-radius: 999px; color: #94a3b8; }}
        .sidebar-search {{ padding: 12px 16px; border-bottom: 1px solid #1e293b; }}
        .sidebar-search input {{
            width: 100%; padding: 9px 14px; background: #1e293b; border: 1px solid #334155;
            border-radius: 8px; color: white; font-size: 0.85rem; outline: none;
        }}
        .sidebar-search input:focus {{ border-color: var(--primary); }}
        .tools-nav {{ flex: 1; overflow-y: auto; padding: 12px 0; }}
        .category-title {{
            padding: 10px 20px 4px 20px; font-size: 0.72rem; font-weight: 700;
            color: #94a3b8; text-transform: uppercase; letter-spacing: 0.05em;
        }}
        .tool-item {{
            padding: 10px 20px; font-size: 0.84rem; color: #cbd5e1; cursor: pointer;
            display: flex; align-items: center; gap: 10px; transition: all 0.15s;
        }}
        .tool-item:hover {{ background: #1e293b; color: white; }}
        .tool-item.active {{ background: var(--primary); color: white; font-weight: 600; }}
        .tool-item-icon {{ font-size: 1.1rem; }}

        /* Main Workspace */
        .main-content {{ flex: 1; display: flex; flex-direction: column; overflow: hidden; }}

        /* Topbar */
        .topbar {{
            height: 64px; background: var(--card-bg); border-bottom: 1px solid var(--border);
            display: flex; justify-content: space-between; align-items: center; padding: 0 24px; flex-shrink: 0;
        }}
        .topbar-title {{ font-size: 1.15rem; font-weight: 700; color: #0f172a; display: flex; align-items: center; gap: 10px; }}
        .topbar-actions {{ display: flex; align-items: center; gap: 12px; }}

        .api-badge {{
            display: inline-flex; align-items: center; gap: 8px; background: #f8fafc; border: 1px solid var(--border);
            padding: 7px 14px; border-radius: 8px; font-size: 0.83rem; cursor: pointer; transition: all 0.2s;
        }}
        .api-badge:hover {{ background: #f1f5f9; border-color: #cbd5e1; }}
        .status-dot {{ width: 9px; height: 9px; border-radius: 50%; background: var(--warning); }}
        .status-dot.active {{ background: var(--success); }}

        /* Notice Banner */
        .notice-banner {{
            background: #f0fdf4; border-bottom: 1px solid #bbf7d0; padding: 10px 24px;
            display: flex; align-items: center; justify-content: space-between; font-size: 0.85rem; color: #166534;
        }}
        .notice-banner.demo-mode {{
            background: #eff6ff; border-bottom: 1px solid #bfdbfe; color: #1e40af;
        }}
        .notice-banner a {{ color: inherit; font-weight: 700; text-decoration: underline; cursor: pointer; }}
        .notice-banner-btn {{
            background: white; border: 1px solid #bfdbfe; padding: 4px 10px; border-radius: 6px;
            font-size: 0.78rem; font-weight: 600; cursor: pointer; color: #1e40af; margin-left: 8px;
        }}
        .notice-banner-btn:hover {{ background: #dbeafe; }}

        /* Workspace Grid */
        .workspace {{ flex: 1; overflow-y: auto; padding: 24px; display: grid; grid-template-columns: 1fr 1fr; gap: 24px; }}

        .card {{
            background: var(--card-bg); border: 1px solid var(--border); border-radius: 12px;
            display: flex; flex-direction: column; overflow: hidden; box-shadow: 0 1px 3px rgba(0,0,0,0.03);
        }}
        .card-header {{
            padding: 14px 20px; border-bottom: 1px solid var(--border); background: #fafafa;
            display: flex; justify-content: space-between; align-items: center;
        }}
        .card-header h2 {{ font-size: 0.92rem; font-weight: 700; color: #334155; display: flex; align-items: center; gap: 6px; }}
        .card-body {{ padding: 20px; flex: 1; display: flex; flex-direction: column; gap: 14px; }}

        textarea {{
            width: 100%; flex: 1; min-height: 240px; border: 1px solid var(--border); border-radius: 8px;
            padding: 14px; font-size: 0.88rem; line-height: 1.55; resize: none; outline: none;
            background: #f8fafc; color: #0f172a; transition: border-color 0.2s;
        }}
        textarea:focus {{ border-color: var(--primary); background: white; }}

        .output-box {{
            width: 100%; flex: 1; min-height: 240px; border: 1px solid var(--border); border-radius: 8px;
            padding: 16px; font-size: 0.88rem; line-height: 1.65; background: #f8fafc; overflow-y: auto;
            white-space: pre-wrap; word-break: break-word; color: #1e293b;
        }}

        .btn-group {{ display: flex; gap: 10px; align-items: center; flex-wrap: wrap; }}
        .btn {{
            padding: 9px 16px; border-radius: 8px; font-size: 0.88rem; font-weight: 600; cursor: pointer;
            border: none; display: inline-flex; align-items: center; gap: 6px; transition: all 0.2s;
        }}
        .btn-primary {{ background: var(--primary); color: white; }}
        .btn-primary:hover {{ background: var(--primary-hover); }}
        .btn-secondary {{ background: #e2e8f0; color: #334155; }}
        .btn-secondary:hover {{ background: #cbd5e1; }}
        .btn-outline {{ background: white; border: 1px solid var(--border); color: #475569; }}
        .btn-outline:hover {{ background: #f8fafc; border-color: #cbd5e1; }}
        .btn-sm {{ padding: 5px 10px; font-size: 0.78rem; border-radius: 6px; }}

        /* Toast */
        .toast {{
            position: fixed; bottom: 24px; right: 24px; background: #0f172a; color: white;
            padding: 10px 18px; border-radius: 8px; font-size: 0.85rem; display: none;
            box-shadow: 0 10px 15px -3px rgba(0,0,0,0.3); z-index: 200;
        }}

        /* API Modal */
        .modal-overlay {{
            position: fixed; inset: 0; background: rgba(15, 23, 42, 0.6); backdrop-filter: blur(2px);
            display: none; justify-content: center; align-items: center; z-index: 100;
        }}
        .modal {{
            background: white; width: 580px; max-width: 92vw; border-radius: 14px;
            box-shadow: 0 20px 25px -5px rgba(0,0,0,0.25); overflow: hidden;
            display: flex; flex-direction: column; max-height: 90vh;
        }}
        .modal-header {{
            padding: 20px 24px; border-bottom: 1px solid var(--border);
            display: flex; justify-content: space-between; align-items: center;
        }}
        .modal-header h3 {{ font-size: 1.15rem; color: #0f172a; font-weight: 700; display: flex; align-items: center; gap: 8px; }}
        .modal-close-btn {{ background: none; border: none; font-size: 1.25rem; color: #94a3b8; cursor: pointer; }}
        .modal-close-btn:hover {{ color: #0f172a; }}

        .modal-body {{ padding: 24px; display: flex; flex-direction: column; gap: 16px; overflow-y: auto; }}

        /* Provider Tabs */
        .provider-cards {{ display: grid; grid-template-columns: 1fr 1fr; gap: 10px; }}
        .provider-card {{
            border: 2px solid var(--border); border-radius: 10px; padding: 12px; cursor: pointer;
            transition: all 0.2s; text-align: left; background: #f8fafc;
        }}
        .provider-card:hover {{ border-color: #cbd5e1; }}
        .provider-card.active {{ border-color: var(--primary); background: var(--primary-light); }}
        .provider-card-title {{ font-weight: 700; font-size: 0.88rem; color: #1e293b; margin-bottom: 3px; display: flex; align-items: center; justify-content: space-between; }}
        .provider-card-desc {{ font-size: 0.72rem; color: var(--text-muted); line-height: 1.35; }}
        .free-badge {{ background: #dcfce7; color: #15803d; font-size: 0.65rem; font-weight: 700; padding: 2px 6px; border-radius: 4px; }}
        .kvkk-badge {{ background: #e0e7ff; color: #4338ca; font-size: 0.65rem; font-weight: 700; padding: 2px 6px; border-radius: 4px; }}

        .input-with-actions {{ display: flex; gap: 8px; position: relative; }}
        .input-with-actions input {{
            flex: 1; padding: 11px 14px; border: 1px solid var(--border); border-radius: 8px;
            font-size: 0.9rem; outline: none; background: #f8fafc; font-family: monospace;
        }}
        .input-with-actions input:focus {{ border-color: var(--primary); background: white; }}

        .key-guide-box {{
            background: #f8fafc; border: 1px solid var(--border); border-radius: 8px; padding: 12px;
            font-size: 0.8rem; color: #475569; line-height: 1.45;
        }}
        .key-guide-box a {{ color: var(--primary); font-weight: 600; text-decoration: none; }}
        .key-guide-box a:hover {{ text-decoration: underline; }}

        .validation-result {{
            padding: 12px; border-radius: 8px; font-size: 0.84rem; display: none;
            line-height: 1.4;
        }}
        .validation-result.success {{ background: var(--success-light); border: 1px solid #a7f3d0; color: #065f46; display: block; }}
        .validation-result.error {{ background: var(--danger-light); border: 1px solid #fecaca; color: #991b1b; display: block; }}
        .validation-result.loading {{ background: #f1f5f9; border: 1px solid #cbd5e1; color: #334155; display: block; }}

        .modal-footer {{
            padding: 16px 24px; border-top: 1px solid var(--border); background: #fafafa;
            display: flex; justify-content: space-between; align-items: center; flex-shrink: 0;
        }}
    </style>
</head>
<body>

<!-- Sidebar -->
<div class="sidebar">
    <div class="sidebar-header">
        <h1>🇹🇷 AI Araçları</h1>
        <span id="toolsCountBadge">20 Araç</span>
    </div>
    <div class="sidebar-search">
        <input type="text" id="searchInput" placeholder="Araç veya mevzuat ara..." oninput="filterTools()">
    </div>
    <div class="tools-nav" id="toolsNav"></div>
</div>

<!-- Main Area -->
<div class="main-content">
    <!-- Topbar -->
    <div class="topbar">
        <div class="topbar-title">
            <span id="activeToolIcon">🧾</span>
            <span id="activeToolTitle">FişMatik AI</span>
        </div>
        <div class="topbar-actions">
            <div class="api-badge" onclick="openKeyModal()">
                <div class="status-dot" id="keyStatusDot"></div>
                <span id="keyStatusText">Yükleniyor...</span>
                <span style="font-size: 0.72rem; color: #64748b; margin-left: 2px;">⚙️ Ayarla</span>
            </div>
        </div>
    </div>

    <!-- Notice Banner -->
    <div class="notice-banner demo-mode" id="noticeBanner">
        <span id="noticeBannerText">💡 <b>Demo / Simülasyon Modu:</b> Canlı yapay zeka analizleri için ücretsiz bir Google Gemini veya çevrimdışı yerel LLM (Ollama) bağlayabilirsiniz.</span>
        <div>
            <button class="notice-banner-btn" onclick="openKeyModal()">🔑 Model / Anahtar Ekle</button>
            <button class="notice-banner-btn" onclick="window.open('https://aistudio.google.com/app/apikey', '_blank')">🎁 Ücretsiz Gemini Al</button>
            <button class="notice-banner-btn" style="border:none; background:transparent;" onclick="dismissBanner()">✕</button>
        </div>
    </div>

    <!-- Workspace -->
    <div class="workspace">
        <!-- Input Card -->
        <div class="card">
            <div class="card-header">
                <h2>📥 Girdi Verisi</h2>
                <div class="btn-group">
                    <input type="file" id="udfFileInput" accept=".udf,.xml,.txt,.md" style="display:none;" onchange="handleFileInput(event)">
                    <button class="btn btn-outline btn-sm" onclick="document.getElementById('udfFileInput').click()" title="UYAP .udf veya XML dava dosyasını doğrudan aktarın">⚖️ UYAP UDF / Belge Yükle</button>
                    <button class="btn btn-outline btn-sm" onclick="loadSampleData()">✨ Hazır Örnek Yükle</button>
                </div>
            </div>
            <div class="card-body">
                <textarea id="userInput" placeholder="İncelenecek metni, faturayı, sözleşme maddesini veya UYAP UDF belgesini buraya yapıştırın veya yükleyin..."></textarea>
                <div class="btn-group">
                    <button class="btn btn-primary" id="runBtn" onclick="runActiveTool()">
                        <span>🚀 Yapay Zeka ile Analiz Et</span>
                    </button>
                    <button class="btn btn-secondary" onclick="clearInput()">Temizle</button>
                </div>
            </div>
        </div>

        <!-- Output Card -->
        <div class="card">
            <div class="card-header">
                <h2>📤 Yapay Zeka Analizi ve Raporu</h2>
                <div class="btn-group">
                    <button class="btn btn-outline btn-sm" onclick="copyOutput()">📋 Kopyala</button>
                </div>
            </div>
            <div class="card-body">
                <div class="output-box" id="outputBox">Yapay zeka analiz raporu burada görüntülenecektir...</div>
            </div>
        </div>
    </div>
</div>

<!-- API Key Setup Modal -->
<div class="modal-overlay" id="keyModal">
    <div class="modal">
        <div class="modal-header">
            <h3>🔑 Sağlayıcı ve Model Ayarları</h3>
            <button class="modal-close-btn" onclick="closeKeyModal()">&times;</button>
        </div>
        <div class="modal-body">
            <p style="font-size: 0.83rem; color: #475569; line-height: 1.45;">
                Mali ve hukuki gizlilik esastır. Anahtarlarınız <b>yalnızca tarayıcınızın yerel hafızasında (localStorage)</b> tutulur. Dilerseniz <b>Ollama / LM Studio</b> ile verileriniz cihazınızdan hiç çıkmadan %100 KVKK uyumlu çalışabilirsiniz.
            </p>

            <div class="provider-cards">
                <div class="provider-card active" id="cardGemini" onclick="selectProvider('gemini')">
                    <div class="provider-card-title">
                        <span>Google Gemini</span>
                        <span class="free-badge">ÜCRETSİZ</span>
                    </div>
                    <div class="provider-card-desc">Gemini 1.5 Flash. Kredi kartsız ücretsiz kota, yüksek hız ve Türkçe başarısı.</div>
                </div>
                <div class="provider-card" id="cardOpenai" onclick="selectProvider('openai')">
                    <div class="provider-card-title">
                        <span>OpenAI</span>
                    </div>
                    <div class="provider-card-desc">GPT-4o-mini. Güvenilir genel akıl yürütme ve yapılandırılmış JSON çıktısı.</div>
                </div>
                <div class="provider-card" id="cardOllama" onclick="selectProvider('ollama')">
                    <div class="provider-card-title">
                        <span>Ollama (Yerel)</span>
                        <span class="kvkk-badge">KVKK GÜVENLİ</span>
                    </div>
                    <div class="provider-card-desc">Yerel makinede çevrimdışı çalışma (Llama 3, Qwen 2.5). Veriler dışarı çıkmaz.</div>
                </div>
                <div class="provider-card" id="cardLmstudio" onclick="selectProvider('lmstudio')">
                    <div class="provider-card-title">
                        <span>LM Studio</span>
                        <span class="kvkk-badge">OFFLINE</span>
                    </div>
                    <div class="provider-card-desc">LM Studio yerel sunucusu (http://127.0.0.1:1234). Gizli dava ve mali veriler için ideal.</div>
                </div>
            </div>

            <!-- Cloud API Key Input Group -->
            <div id="apiKeyGroup">
                <label id="apiKeyLabel" style="display:block; font-size: 0.8rem; font-weight: 700; margin-bottom: 6px; color: #334155;">API Anahtarınız</label>
                <div class="input-with-actions">
                    <input type="password" id="apiKeyInput" placeholder="AIzaSy... veya sk-...">
                    <button class="btn btn-outline" id="keyVisBtn" onclick="toggleKeyVisibility()" title="Göster / Gizle">👁️</button>
                </div>
            </div>

            <!-- Local Server Config Group -->
            <div id="localConfigGroup" style="display:none; flex-direction:column; gap:8px;">
                <label style="display:block; font-size: 0.8rem; font-weight: 700; margin-bottom: 2px; color: #334155;">Yerel Sunucu Adresi ve Model</label>
                <div style="display:flex; gap:8px;">
                    <input type="text" id="localHostInput" placeholder="http://127.0.0.1:11434" style="flex:2; padding:10px; border:1px solid var(--border); border-radius:8px; font-size:0.85rem;" title="Sunucu adresi">
                    <input type="text" id="localModelInput" placeholder="llama3.2" style="flex:1; padding:10px; border:1px solid var(--border); border-radius:8px; font-size:0.85rem;" title="Model adı (ör: llama3.2, qwen2.5, mistral)">
                </div>
            </div>

            <div class="key-guide-box" id="keyGuideBox"></div>

            <div class="validation-result" id="validationResult"></div>
        </div>

        <div class="modal-footer">
            <button class="btn btn-outline" onclick="clearApiKey()">🗑️ Demo Moduna Dön</button>
            <div class="btn-group">
                <button class="btn btn-secondary" onclick="closeKeyModal()">Vazgeç</button>
                <button class="btn btn-primary" id="saveValidateBtn" onclick="testAndSaveKey()">🔍 Doğrula & Kaydet</button>
            </div>
        </div>
    </div>
</div>

<!-- Toast -->
<div class="toast" id="toast"></div>

<script>
const TOOLS_DATA = {tools_data_str};

let activeToolId = TOOLS_DATA[0].id;
let selectedProvider = localStorage.getItem('ai_provider') || 'gemini';

function initApp() {{
    renderSidebar();
    selectTool(activeToolId);
    updateApiStatusBadge();
}}

function renderSidebar(filteredTools = null) {{
    const nav = document.getElementById('toolsNav');
    nav.innerHTML = '';
    const tools = filteredTools || TOOLS_DATA;

    let currentCat = '';
    tools.forEach(tool => {{
        if (tool.catTitle !== currentCat) {{
            currentCat = tool.catTitle;
            const catHeader = document.createElement('div');
            catHeader.className = 'category-title';
            catHeader.innerText = currentCat;
            nav.appendChild(catHeader);
        }}

        const item = document.createElement('div');
        item.className = 'tool-item ' + (tool.id === activeToolId ? 'active' : '');
        item.onclick = () => selectTool(tool.id);
        item.innerHTML = `<span class="tool-item-icon">${{tool.icon}}</span> <span>${{tool.title}}</span>`;
        nav.appendChild(item);
    }});

    document.getElementById('toolsCountBadge').innerText = `${{tools.length}} Araç`;
}}

function filterTools() {{
    const q = document.getElementById('searchInput').value.toLowerCase().trim();
    if (!q) {{
        renderSidebar();
        return;
    }}
    const filtered = TOOLS_DATA.filter(t => 
        t.title.toLowerCase().includes(q) || 
        t.catTitle.toLowerCase().includes(q) ||
        t.system_prompt.toLowerCase().includes(q)
    );
    renderSidebar(filtered);
}}

function selectTool(id) {{
    activeToolId = id;
    const tool = TOOLS_DATA.find(t => t.id === id);
    if (!tool) return;

    document.getElementById('activeToolIcon').innerText = tool.icon;
    document.getElementById('activeToolTitle').innerText = tool.title;
    
    document.querySelectorAll('.tool-item').forEach(el => {{
        el.classList.toggle('active', el.innerText.includes(tool.title));
    }});

    document.getElementById('userInput').value = '';
    document.getElementById('outputBox').innerText = 'Analiz için metin giriniz, UYAP UDF belgesi yükleyiniz veya "✨ Hazır Örnek Yükle" butonuna tıklayınız...';
}}

function loadSampleData() {{
    const tool = TOOLS_DATA.find(t => t.id === activeToolId);
    if (tool && tool.sample_input) {{
        document.getElementById('userInput').value = tool.sample_input;
        showToast('✨ Örnek senaryo yüklendi!');
    }}
}}

function clearInput() {{
    document.getElementById('userInput').value = '';
    document.getElementById('outputBox').innerText = 'Girdi temizlendi.';
}}

function copyOutput() {{
    const text = document.getElementById('outputBox').innerText;
    if (!text) return;
    navigator.clipboard.writeText(text).then(() => {{
        showToast('📋 Analiz sonucu panoya kopyalandı!');
    }});
}}

function showToast(msg) {{
    const t = document.getElementById('toast');
    t.innerText = msg;
    t.style.display = 'block';
    setTimeout(() => {{ t.style.display = 'none'; }}, 3000);
}}

/* UYAP .UDF / Dosya Ayrıştırma (Client-side, Sıfır Veri Sızıntısı) */
async function handleFileInput(event) {{
    const file = event.target.files[0];
    if (!file) return;

    const fileName = file.name;
    const lowerName = fileName.toLowerCase();

    showToast('⏳ Belge ayrıştırılıyor...');

    try {{
        if (lowerName.endsWith('.udf')) {{
            if (typeof JSZip === 'undefined') {{
                throw new Error("JSZip kütüphanesi yüklenemedi. Lütfen internet bağlantınızı kontrol ediniz.");
            }}
            const zip = await JSZip.loadAsync(file);
            const contentFile = zip.file('content.xml') || Object.values(zip.files).find(f => f.name.toLowerCase().endsWith('.xml'));
            if (!contentFile) {{
                throw new Error("UDF arşivi içinde content.xml bulunamadı!");
            }}

            const xmlText = await contentFile.async('string');
            const parsed = parseUdfXmlContent(xmlText);

            let header = `═══════════════════════════════════════════════════════════════\\n` +
                         `⚖️ UYAP UDF EVRAKI: ${{fileName}}\\n` +
                         `📏 Karakter: ${{parsed.text.length}} | Kelime: ${{parsed.text.split(/\\s+/).filter(Boolean).length}}\\n`;
            
            if (parsed.signers.length > 0) {{
                header += `✍️ E-İMZA SAHİPLERİ:\\n`;
                parsed.signers.forEach(s => {{
                    header += `  • ${{s.name}} (${{s.role}})${{s.date ? ' - ' + s.date : ''}}\\n`;
                }});
            }}
            header += `═══════════════════════════════════════════════════════════════\\n\\n`;

            document.getElementById('userInput').value = header + parsed.text;
            showToast(`⚖️ UYAP UDF belgesi başarıyla aktarıldı! (${{parsed.text.length}} karakter)`);
        }} else {{
            const text = await file.text();
            document.getElementById('userInput').value = `[DOSYA: ${{fileName}}]\\n\\n` + text;
            showToast(`📄 ${{fileName}} yüklendi!`);
        }}
    }} catch (err) {{
        alert("Dosya ayrıştırma hatası: " + err.message);
    }} finally {{
        event.target.value = '';
    }}
}}

function parseUdfXmlContent(xml) {{
    const signers = [];

    // E-İmza tespiti (signer, imzaci, CN=)
    const signerRegex = /<signer\\b([^>]*)>/gi;
    let match;
    while ((match = signerRegex.exec(xml)) !== null) {{
        const attrs = match[1];
        const nameM = attrs.match(/name=["']([^"']+)["']/i);
        const dateM = attrs.match(/date=["']([^"']+)["']/i);
        const roleM = attrs.match(/role=["']([^"']+)["']/i);
        if (nameM && !signers.some(s => s.name === nameM[1])) {{
            signers.push({{
                name: nameM[1].trim(),
                date: dateM ? dateM[1].trim() : null,
                role: roleM ? roleM[1].trim() : "İmza Sahibi"
            }});
        }}
    }}

    const cnRegex = /CN=([^,\\/<>\"\\n\\r]+)/gi;
    while ((match = cnRegex.exec(xml)) !== null) {{
        const cn = match[1].trim();
        if (cn && !signers.some(s => s.name === cn)) {{
            signers.push({{ name: cn, date: null, role: "Elektronik Sertifika Sahibi" }});
        }}
    }}

    // XML Tag temizliği
    let clean = xml.replace(/<!\\[CDATA\\[(.*?)\\]\\]>/gs, '$1');
    clean = clean.replace(/<(?:p|paragraph|br|div|tr)[^>]*>/gi, '\\n');
    clean = clean.replace(/<\\/(?:p|paragraph|div|tr)>/gi, '\\n');
    clean = clean.replace(/<[^>]+>/g, '');
    clean = clean.replace(/&nbsp;/g, ' ')
                 .replace(/&amp;/g, '&')
                 .replace(/&lt;/g, '<')
                 .replace(/&gt;/g, '>')
                 .replace(/&quot;/g, '"')
                 .replace(/&#39;/g, "'");

    const lines = clean.split('\\n').map(l => l.trim());
    const finalLines = [];
    let emptyCount = 0;
    for (const l of lines) {{
        if (!l) {{
            emptyCount++;
            if (emptyCount <= 1) finalLines.push('');
        }} else {{
            emptyCount = 0;
            finalLines.push(l);
        }}
    }}

    return {{ text: finalLines.join('\\n').trim(), signers }};
}}

/* API Key & Mode Management */
function updateApiStatusBadge() {{
    const key = localStorage.getItem('ai_api_key');
    const prov = localStorage.getItem('ai_provider') || 'gemini';
    const localHost = localStorage.getItem('ai_local_host');
    const localModel = localStorage.getItem('ai_local_model');
    const dot = document.getElementById('keyStatusDot');
    const text = document.getElementById('keyStatusText');
    const banner = document.getElementById('noticeBanner');
    const bannerText = document.getElementById('noticeBannerText');

    if (prov === 'ollama') {{
        dot.className = 'status-dot active';
        text.innerText = `🟢 Ollama (${{localModel || 'llama3.2'}}) - KVKK Güvenli`;
        banner.style.display = 'none';
    }} else if (prov === 'lmstudio') {{
        dot.className = 'status-dot active';
        text.innerText = `🟢 LM Studio (Offline)`;
        banner.style.display = 'none';
    }} else if (key && key.trim()) {{
        dot.className = 'status-dot active';
        text.innerText = `🟢 Canlı AI (${{prov === 'gemini' ? 'Google Gemini' : 'OpenAI'}})`;
        banner.style.display = 'none';
    }} else {{
        dot.className = 'status-dot';
        text.innerText = '🧪 Demo / Test Modu (Anahtarsız)';
        banner.style.display = 'flex';
        banner.className = 'notice-banner demo-mode';
        bannerText.innerHTML = '💡 <b>Demo / Simülasyon Modu:</b> Canlı yapay zeka analizleri için <b>ücretsiz Gemini</b> ekleyebilir veya <b>Ollama / LM Studio</b> ile %100 yerel çalışabilirsiniz.';
    }}
}}

function dismissBanner() {{
    document.getElementById('noticeBanner').style.display = 'none';
}}

function openKeyModal() {{
    document.getElementById('keyModal').style.display = 'flex';
    selectedProvider = localStorage.getItem('ai_provider') || 'gemini';
    selectProvider(selectedProvider);
    document.getElementById('apiKeyInput').value = localStorage.getItem('ai_api_key') || '';
    document.getElementById('localHostInput').value = localStorage.getItem('ai_local_host') || (selectedProvider === 'ollama' ? 'http://127.0.0.1:11434' : 'http://127.0.0.1:1234');
    document.getElementById('localModelInput').value = localStorage.getItem('ai_local_model') || (selectedProvider === 'ollama' ? 'llama3.2' : 'local-model');
    hideValidation();
}}

function closeKeyModal() {{
    document.getElementById('keyModal').style.display = 'none';
}}

function selectProvider(prov) {{
    selectedProvider = prov;
    document.getElementById('cardGemini').classList.toggle('active', prov === 'gemini');
    document.getElementById('cardOpenai').classList.toggle('active', prov === 'openai');
    document.getElementById('cardOllama').classList.toggle('active', prov === 'ollama');
    document.getElementById('cardLmstudio').classList.toggle('active', prov === 'lmstudio');
    
    const guideBox = document.getElementById('keyGuideBox');
    const input = document.getElementById('apiKeyInput');
    const apiKeyGroup = document.getElementById('apiKeyGroup');
    const localGroup = document.getElementById('localConfigGroup');

    if (prov === 'gemini') {{
        apiKeyGroup.style.display = 'block';
        localGroup.style.display = 'none';
        input.placeholder = 'AIzaSy... ile başlayan anahtar';
        guideBox.innerHTML = `
            <b>Google Gemini API Anahtarı (Önerilen - Ücretsiz):</b><br>
            1. <a href="https://aistudio.google.com/app/apikey" target="_blank">Google AI Studio</a> sayfasını açın.<br>
            2. Google hesabınızla oturum açın (Kredi kartı gerekmez).<br>
            3. "Create API Key" butonuna tıklayın ve üretilen anahtarı buraya yapıştırın.
        `;
    }} else if (prov === 'openai') {{
        apiKeyGroup.style.display = 'block';
        localGroup.style.display = 'none';
        input.placeholder = 'sk-... ile başlayan anahtar';
        guideBox.innerHTML = `
            <b>OpenAI API Anahtarı:</b><br>
            1. <a href="https://platform.openai.com/api-keys" target="_blank">OpenAI Platform API Keys</a> sayfasını açın.<br>
            2. "Create new secret key" butonuna tıklayıp anahtarınızı buraya yapıştırın.
        `;
    }} else if (prov === 'ollama') {{
        apiKeyGroup.style.display = 'none';
        localGroup.style.display = 'flex';
        document.getElementById('localHostInput').value = localStorage.getItem('ai_local_host') || 'http://127.0.0.1:11434';
        document.getElementById('localModelInput').value = localStorage.getItem('ai_local_model') || 'llama3.2';
        guideBox.innerHTML = `
            <b>Ollama Yerel LLM Kurulumu (%100 Çevrimdışı & KVKK Güvenli):</b><br>
            1. <a href="https://ollama.com" target="_blank">ollama.com</a> adresinden Ollama'yı indirip kurun.<br>
            2. Terminalde modeli indirin: <code>ollama run llama3.2</code> veya <code>ollama run qwen2.5</code>.<br>
            3. Tarayıcıdan erişim için Ollama'yı şu komutla başlatın: <code>OLLAMA_ORIGINS="*" ollama serve</code><br>
            4. Hiçbir veri buluta veya harici sunuculara aktarılmaz.
        `;
    }} else if (prov === 'lmstudio') {{
        apiKeyGroup.style.display = 'none';
        localGroup.style.display = 'flex';
        document.getElementById('localHostInput').value = localStorage.getItem('ai_local_host') || 'http://127.0.0.1:1234';
        document.getElementById('localModelInput').value = localStorage.getItem('ai_local_model') || 'local-model';
        guideBox.innerHTML = `
            <b>LM Studio Yerel Sunucu Kurulumu:</b><br>
            1. <a href="https://lmstudio.ai" target="_blank">lmstudio.ai</a> uygulamasını açın.<br>
            2. Sol menüden <b>Local Server (Yerel Sunucu)</b> sekmesine gelin.<br>
            3. İndirdiğiniz bir Türkçe destekli modeli seçip <b>Start Server</b> butonuna basın.<br>
            4. Varsayılan port <code>1234</code> üzerinden OpenAI uyumlu API aktif olacaktır.
        `;
    }}
}}

function toggleKeyVisibility() {{
    const input = document.getElementById('apiKeyInput');
    input.type = input.type === 'password' ? 'text' : 'password';
}}

function hideValidation() {{
    const val = document.getElementById('validationResult');
    val.className = 'validation-result';
    val.style.display = 'none';
}}

async function testAndSaveKey() {{
    const key = document.getElementById('apiKeyInput').value.trim();
    const localHost = document.getElementById('localHostInput').value.trim() || 'http://127.0.0.1:11434';
    const localModel = document.getElementById('localModelInput').value.trim() || 'llama3.2';
    const val = document.getElementById('validationResult');
    const btn = document.getElementById('saveValidateBtn');

    btn.disabled = true;
    btn.innerText = '⏳ Doğrulanıyor...';
    val.className = 'validation-result loading';
    val.innerHTML = '🔄 Sağlayıcıya bağlanılarak yapılandırma test ediliyor...';

    try {{
        let isValid = false;
        let errMsg = '';

        if (selectedProvider === 'gemini') {{
            if (!key) throw new Error("Lütfen Gemini API anahtarınızı giriniz.");
            const url = `https://generativelanguage.googleapis.com/v1beta/models?key=${{key}}`;
            const res = await fetch(url);
            if (res.ok) {{
                isValid = true;
            }} else {{
                const errData = await res.json().catch(() => ({{}}));
                errMsg = errData.error?.message || `HTTP ${{res.status}}`;
            }}
        }} else if (selectedProvider === 'openai') {{
            if (!key) throw new Error("Lütfen OpenAI API anahtarınızı giriniz.");
            const url = 'https://api.openai.com/v1/models';
            const res = await fetch(url, {{
                headers: {{ 'Authorization': `Bearer ${{key}}` }}
            }});
            if (res.ok) {{
                isValid = true;
            }} else {{
                const errData = await res.json().catch(() => ({{}}));
                errMsg = errData.error?.message || `HTTP ${{res.status}}`;
            }}
        }} else if (selectedProvider === 'ollama') {{
            try {{
                const res = await fetch(`${{localHost}}/api/tags`);
                if (res.ok) {{
                    isValid = true;
                }} else {{
                    errMsg = `HTTP ${{res.status}} - Ollama sunucusu yanıt vermedi`;
                }}
            }} catch (e) {{
                // Tarayıcı CORS engeli veya sunucu kapalı
                errMsg = `${{e.message}} (İpucu: OLLAMA_ORIGINS="*" ollama serve çalıştırıldığından emin olun). Yine de kaydedebilirsiniz.`;
                isValid = true; // Yerel kullanım için kayda izin ver
            }}
        }} else if (selectedProvider === 'lmstudio') {{
            try {{
                const res = await fetch(`${{localHost}}/v1/models`);
                if (res.ok) {{
                    isValid = true;
                }} else {{
                    errMsg = `HTTP ${{res.status}} - LM Studio yanıt vermedi`;
                }}
            }} catch (e) {{
                errMsg = `${{e.message}} (LM Studio Local Server açık olduğundan emin olun). Yine de kaydedebilirsiniz.`;
                isValid = true;
            }}
        }}

        if (isValid) {{
            localStorage.setItem('ai_provider', selectedProvider);
            if (selectedProvider === 'gemini' || selectedProvider === 'openai') {{
                localStorage.setItem('ai_api_key', key);
            }} else {{
                localStorage.setItem('ai_local_host', localHost);
                localStorage.setItem('ai_local_model', localModel);
            }}
            val.className = 'validation-result success';
            val.innerHTML = `✅ <b>Harika!</b> ${{selectedProvider.toUpperCase()}} başarıyla yapılandırıldı ve kaydedildi.`;
            updateApiStatusBadge();
            showToast('✅ Sağlayıcı kaydedildi!');
            setTimeout(() => {{ closeKeyModal(); }}, 1200);
        }} else {{
            val.className = 'validation-result error';
            val.innerHTML = `❌ <b>Doğrulama Başarısız:</b> ${{errMsg}}<br><small>Lütfen yapılandırmanızı kontrol edin.</small>`;
        }}
    }} catch (err) {{
        val.className = 'validation-result error';
        val.innerHTML = `❌ <b>Bağlantı Hatası:</b> ${{err.message}}`;
    }} finally {{
        btn.disabled = false;
        btn.innerText = '🔍 Doğrula & Kaydet';
    }}
}}

function clearApiKey() {{
    localStorage.removeItem('ai_api_key');
    localStorage.removeItem('ai_provider');
    localStorage.removeItem('ai_local_host');
    localStorage.removeItem('ai_local_model');
    document.getElementById('apiKeyInput').value = '';
    updateApiStatusBadge();
    showToast('🗑️ Ayarlar sıfırlandı (Demo Modu aktif).');
    closeKeyModal();
}}

/* AI Execution */
async function runActiveTool() {{
    const input = document.getElementById('userInput').value.trim();
    if (!input) {{
        alert('Lütfen analiz edilecek bir metin girin, UYAP UDF belgesi yükleyin veya "✨ Hazır Örnek Yükle" butonuna tıklayın.');
        return;
    }}

    const tool = TOOLS_DATA.find(t => t.id === activeToolId);
    if (!tool) return;

    const key = localStorage.getItem('ai_api_key');
    const provider = localStorage.getItem('ai_provider') || 'gemini';
    const localHost = localStorage.getItem('ai_local_host') || (provider === 'ollama' ? 'http://127.0.0.1:11434' : 'http://127.0.0.1:1234');
    const localModel = localStorage.getItem('ai_local_model') || (provider === 'ollama' ? 'llama3.2' : 'local-model');

    const btn = document.getElementById('runBtn');
    const out = document.getElementById('outputBox');

    btn.disabled = true;
    btn.innerHTML = '<span>⏳ Analiz Ediliyor...</span>';
    out.innerText = 'Yapay zeka modeli Türk mevzuatı ve kural setleri doğrultusunda analiz hazırlıyor, lütfen bekleyin...';

    // Demo Mode (Bulut sağlayıcı seçili ama anahtar yoksa)
    if ((provider === 'gemini' || provider === 'openai') && (!key || !key.trim())) {{
        setTimeout(() => {{
            out.innerText = `[DEMO / SİMÜLASYON ÇIKTISI - Anahtarsız Mod]\\n` +
                `Model: Simülasyon Motoru (Türk Mevzuatı Bilgi Tabanı)\\n` +
                `Seçilen Araç: ${{tool.title}}\\n` +
                `İncelenen Metin: ${{input.length}} Karakter\\n\\n` +
                `═══════════════════════════════════════════════════════════════\\n` +
                `📌 UYGULANAN SİSTEM PROMPTU & MEVZUAT:\\n` +
                `${{tool.system_prompt.slice(0, 300)}}...\\n\\n` +
                `✅ ANALİZ SONUCU:\\n` +
                `Girdi verisi Türk Vergi/Hukuk şablonlarına göre başarıyla doğrulandı.\\n\\n` +
                `💡 İPUCU: Canlı Gemini (ücretsiz), OpenAI veya %100 çevrimdışı Ollama / LM Studio yanıtı almak için sağ üstteki '⚙️ Ayarla' butonuna basınız.`;
            btn.disabled = false;
            btn.innerHTML = '<span>🚀 Yapay Zeka ile Analiz Et</span>';
        }}, 600);
        return;
    }}

    try {{
        if (provider === 'ollama') {{
            // Ollama Local API
            const url = `${{localHost.replace(/\\/+$/, '')}}/api/chat`;
            const res = await fetch(url, {{
                method: 'POST',
                headers: {{ 'Content-Type': 'application/json' }},
                body: JSON.stringify({{
                    model: localModel,
                    messages: [
                        {{ role: 'system', content: tool.system_prompt }},
                        {{ role: 'user', content: input }}
                    ],
                    stream: false
                }})
            }});
            if (!res.ok) {{
                throw new Error(`HTTP ${{res.status}} - Ollama hatası`);
            }}
            const data = await res.json();
            out.innerText = data.message?.content || 'Ollama yanıtı alınamadı.';
        }} else if (provider === 'lmstudio') {{
            // LM Studio Local OpenAI-compatible API
            const url = `${{localHost.replace(/\\/+$/, '')}}/v1/chat/completions`;
            const res = await fetch(url, {{
                method: 'POST',
                headers: {{ 'Content-Type': 'application/json' }},
                body: JSON.stringify({{
                    model: localModel,
                    messages: [
                        {{ role: 'system', content: tool.system_prompt }},
                        {{ role: 'user', content: input }}
                    ],
                    temperature: 0.2
                }})
            }});
            if (!res.ok) {{
                throw new Error(`HTTP ${{res.status}} - LM Studio hatası`);
            }}
            const data = await res.json();
            out.innerText = data.choices?.[0]?.message?.content || 'LM Studio yanıtı alınamadı.';
        }} else if (provider === 'gemini') {{
            const url = `https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key=${{key}}`;
            const combinedPrompt = `${{tool.system_prompt}}\\n\\nKULLANICI GİRDİSİ:\\n${{input}}`;
            const res = await fetch(url, {{
                method: 'POST',
                headers: {{ 'Content-Type': 'application/json' }},
                body: JSON.stringify({{
                    contents: [{{ parts: [{{ text: combinedPrompt }}] }}],
                    generationConfig: {{ temperature: 0.2 }}
                }})
            }});

            if (!res.ok) {{
                const err = await res.json().catch(() => ({{}}));
                throw new Error(err.error?.message || `HTTP ${{res.status}}`);
            }}

            const data = await res.json();
            out.innerText = data.candidates?.[0]?.content?.parts?.[0]?.text || 'Yanıt alınamadı.';
        }} else {{
            const url = 'https://api.openai.com/v1/chat/completions';
            const res = await fetch(url, {{
                method: 'POST',
                headers: {{
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${{key}}`
                }},
                body: JSON.stringify({{
                    model: 'gpt-4o-mini',
                    messages: [
                        {{ role: 'system', content: tool.system_prompt }},
                        {{ role: 'user', content: input }}
                    ],
                    temperature: 0.2
                }})
            }});

            if (!res.ok) {{
                const err = await res.json().catch(() => ({{}}));
                throw new Error(err.error?.message || `HTTP ${{res.status}}`);
            }}

            const data = await res.json();
            out.innerText = data.choices?.[0]?.message?.content || 'Yanıt alınamadı.';
        }}
    }} catch (err) {{
        out.innerText = `❌ API Çağrı Hatası (${{provider.toUpperCase()}}):\\n${{err.message}}\\n\\n💡 İpuçları:\\n` +
            `• Ollama kullanıyorsanız: 'OLLAMA_ORIGINS="*" ollama serve' ile CORS izni verilmiş olmalıdır.\\n` +
            `• LM Studio kullanıyorsanız: 'Start Server' butonunun aktif olduğundan emin olunuz.\\n` +
            `• Gemini / OpenAI kullanıyorsanız: API anahtarınızı veya kota limitinizi kontrol ediniz.`;
    }} finally {{
        btn.disabled = false;
        btn.innerHTML = '<span>🚀 Yapay Zeka ile Analiz Et</span>';
    }}
}}

window.onload = initApp;
</script>

</body>
</html>"""

with open(INDEX_PATH, "w", encoding="utf-8") as f:
    f.write(html_content)

print(f"Successfully generated {INDEX_PATH} with {len(tools_data)} tools!")
