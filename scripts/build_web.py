# -*- coding: utf-8 -*-
"""
build_web.py
------------
web/index.html dosyasını en güncel 20 araç, zenginleştirilmiş BYOK API anahtarı
çubuğu, canlı API anahtarı test/doğrulama özelliği ve modern arayüz ile üretir.
"""

import json
import os

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

        .btn-group {{ display: flex; gap: 10px; align-items: center; }}
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
            background: white; width: 540px; max-width: 90vw; border-radius: 14px;
            box-shadow: 0 20px 25px -5px rgba(0,0,0,0.25); overflow: hidden;
            display: flex; flex-direction: column;
        }}
        .modal-header {{
            padding: 20px 24px; border-bottom: 1px solid var(--border);
            display: flex; justify-content: space-between; align-items: center;
        }}
        .modal-header h3 {{ font-size: 1.15rem; color: #0f172a; font-weight: 700; display: flex; align-items: center; gap: 8px; }}
        .modal-close-btn {{ background: none; border: none; font-size: 1.25rem; color: #94a3b8; cursor: pointer; }}
        .modal-close-btn:hover {{ color: #0f172a; }}

        .modal-body {{ padding: 24px; display: flex; flex-direction: column; gap: 18px; }}

        /* Provider Tabs */
        .provider-cards {{ display: grid; grid-template-columns: 1fr 1fr; gap: 12px; }}
        .provider-card {{
            border: 2px solid var(--border); border-radius: 10px; padding: 14px; cursor: pointer;
            transition: all 0.2s; text-align: left; background: #f8fafc;
        }}
        .provider-card:hover {{ border-color: #cbd5e1; }}
        .provider-card.active {{ border-color: var(--primary); background: var(--primary-light); }}
        .provider-card-title {{ font-weight: 700; font-size: 0.92rem; color: #1e293b; margin-bottom: 4px; display: flex; align-items: center; gap: 6px; }}
        .provider-card-desc {{ font-size: 0.74rem; color: var(--text-muted); line-height: 1.35; }}
        .free-badge {{ background: #dcfce7; color: #15803d; font-size: 0.65rem; font-weight: 700; padding: 2px 6px; border-radius: 4px; margin-left: 4px; }}

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
            display: flex; justify-content: space-between; align-items: center;
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
        <span id="noticeBannerText">💡 <b>Demo / Simülasyon Modu:</b> Canlı yapay zeka analizleri için ücretsiz bir Google Gemini veya OpenAI API anahtarı ekleyebilirsiniz.</span>
        <div>
            <button class="notice-banner-btn" onclick="openKeyModal()">🔑 Anahtar Ekle</button>
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
                    <button class="btn btn-outline btn-sm" onclick="loadSampleData()">✨ Hazır Örnek Yükle</button>
                </div>
            </div>
            <div class="card-body">
                <textarea id="userInput" placeholder="İncelenecek metni, faturayı, sözleşme maddesini veya mizan verisini buraya yapıştırın..."></textarea>
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
            <h3>🔑 API Anahtarı ve Model Ayarları</h3>
            <button class="modal-close-btn" onclick="closeKeyModal()">&times;</button>
        </div>
        <div class="modal-body">
            <p style="font-size: 0.85rem; color: #475569; line-height: 1.45;">
                API anahtarınız <b>yalnızca tarayıcınızın yerel hafızasında (localStorage)</b> saklanır. Hiçbir sunucuya kaydedilmez veya üçüncü şahıslarla paylaşılmaz (%100 BYOK Gizliliği).
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
            </div>

            <div>
                <label style="display:block; font-size: 0.8rem; font-weight: 700; margin-bottom: 6px; color: #334155;">API Anahtarınız</label>
                <div class="input-with-actions">
                    <input type="password" id="apiKeyInput" placeholder="AIzaSy... veya sk-...">
                    <button class="btn btn-outline" onclick="toggleKeyVisibility()" title="Göster / Gizle">👁️</button>
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
    document.getElementById('outputBox').innerText = 'Analiz için metin giriniz veya "✨ Hazır Örnek Yükle" butonuna tıklayınız...';
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
    setTimeout(() => {{ t.style.display = 'none'; }}, 2800);
}}

/* API Key & Mode Management */
function updateApiStatusBadge() {{
    const key = localStorage.getItem('ai_api_key');
    const prov = localStorage.getItem('ai_provider') || 'gemini';
    const dot = document.getElementById('keyStatusDot');
    const text = document.getElementById('keyStatusText');
    const banner = document.getElementById('noticeBanner');
    const bannerText = document.getElementById('noticeBannerText');

    if (key && key.trim()) {{
        dot.className = 'status-dot active';
        text.innerText = `🟢 Canlı AI (${{prov === 'gemini' ? 'Google Gemini' : 'OpenAI'}})`;
        banner.style.display = 'none';
    }} else {{
        dot.className = 'status-dot';
        text.innerText = '🧪 Demo / Test Modu (Anahtarsız)';
        banner.style.display = 'flex';
        banner.className = 'notice-banner demo-mode';
        bannerText.innerHTML = '💡 <b>Demo / Simülasyon Modu:</b> Canlı yapay zeka analizleri için <b>30 saniyede ücretsiz bir Gemini API anahtarı</b> ekleyebilirsiniz.';
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
    hideValidation();
}}

function closeKeyModal() {{
    document.getElementById('keyModal').style.display = 'none';
}}

function selectProvider(prov) {{
    selectedProvider = prov;
    document.getElementById('cardGemini').classList.toggle('active', prov === 'gemini');
    document.getElementById('cardOpenai').classList.toggle('active', prov === 'openai');
    
    const guideBox = document.getElementById('keyGuideBox');
    const input = document.getElementById('apiKeyInput');

    if (prov === 'gemini') {{
        input.placeholder = 'AIzaSy... ile başlayan anahtar';
        guideBox.innerHTML = `
            <b>Google Gemini API Anahtarı (Önerilen):</b><br>
            1. <a href="https://aistudio.google.com/app/apikey" target="_blank">Google AI Studio</a> sayfasını açın.<br>
            2. Google hesabınızla oturum açın (Kredi kartı gerekmez).<br>
            3. "Create API Key" butonuna tıklayın ve üretilen anahtarı buraya yapıştırın.
        `;
    }} else {{
        input.placeholder = 'sk-... ile başlayan anahtar';
        guideBox.innerHTML = `
            <b>OpenAI API Anahtarı:</b><br>
            1. <a href="https://platform.openai.com/api-keys" target="_blank">OpenAI Platform API Keys</a> sayfasını açın.<br>
            2. "Create new secret key" butonuna tıklayıp anahtarınızı buraya yapıştırın.
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
    const val = document.getElementById('validationResult');
    const btn = document.getElementById('saveValidateBtn');

    if (!key) {{
        val.className = 'validation-result error';
        val.innerHTML = '❌ Lütfen bir API anahtarı giriniz veya Demo Modunu seçiniz.';
        return;
    }}

    btn.disabled = true;
    btn.innerText = '⏳ Doğrulanıyor...';
    val.className = 'validation-result loading';
    val.innerHTML = '🔄 API sağlayıcısına bağlanılarak anahtar test ediliyor...';

    try {{
        let isValid = false;
        let errMsg = '';

        if (selectedProvider === 'gemini') {{
            const url = `https://generativelanguage.googleapis.com/v1beta/models?key=${{key}}`;
            const res = await fetch(url);
            if (res.ok) {{
                isValid = true;
            }} else {{
                const errData = await res.json().catch(() => ({{}}));
                errMsg = errData.error?.message || `HTTP ${{res.status}}`;
            }}
        }} else {{
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
        }}

        if (isValid) {{
            localStorage.setItem('ai_api_key', key);
            localStorage.setItem('ai_provider', selectedProvider);
            val.className = 'validation-result success';
            val.innerHTML = '✅ <b>Harika!</b> API anahtarınız başarıyla doğrulandı ve kaydedildi.';
            updateApiStatusBadge();
            showToast('✅ API anahtarı kaydedildi!');
            setTimeout(() => {{ closeKeyModal(); }}, 1200);
        }} else {{
            val.className = 'validation-result error';
            val.innerHTML = `❌ <b>Doğrulama Başarısız:</b> ${{errMsg}}<br><small>Lütfen anahtarın tam kopyalandığından emin olun.</small>`;
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
    document.getElementById('apiKeyInput').value = '';
    updateApiStatusBadge();
    showToast('🗑️ API anahtarı temizlendi (Demo Modu aktif).');
    closeKeyModal();
}}

/* AI Execution */
async function runActiveTool() {{
    const input = document.getElementById('userInput').value.trim();
    if (!input) {{
        alert('Lütfen analiz edilecek bir metin girin veya "✨ Hazır Örnek Yükle" butonuna tıklayın.');
        return;
    }}

    const tool = TOOLS_DATA.find(t => t.id === activeToolId);
    if (!tool) return;

    const key = localStorage.getItem('ai_api_key');
    const provider = localStorage.getItem('ai_provider') || 'gemini';
    const btn = document.getElementById('runBtn');
    const out = document.getElementById('outputBox');

    btn.disabled = true;
    btn.innerHTML = '<span>⏳ Analiz Ediliyor...</span>';
    out.innerText = 'Yapay zeka modeli Türk mevzuatı ve kural setleri doğrultusunda analiz hazırlıyor, lütfen bekleyin...';

    if (!key) {{
        // Deterministic Simulation
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
                `💡 NOT: Canlı OpenAI (GPT-4o-mini) veya Google Gemini yanıtı almak için sağ üstteki '⚙️ Ayarla' butonuna basıp 30 saniyede ücretsiz bir API anahtarı tanımlayabilirsiniz.`;
            btn.disabled = false;
            btn.innerHTML = '<span>🚀 Yapay Zeka ile Analiz Et</span>';
        }}, 700);
        return;
    }}

    try {{
        if (provider === 'gemini') {{
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
        out.innerText = `❌ API Çağrı Hatası (${{provider.toUpperCase()}}):\\n${{err.message}}\\n\\n💡 Lütfen API anahtarınızı, internet bağlantınızı veya kota durumunuzu kontrol ediniz.`;
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
