import streamlit as st
import requests
import uuid
import json
import os
import html

st.set_page_config(
    page_title="Multimedia Chatbot",
    page_icon="📖",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600&family=DM+Mono:wght@400;500&display=swap');

:root {
    --bg:       #0c0c0e;
    --surface:  #131316;
    --surface2: #1c1c21;
    --border:   #1e2a3a;
    --accent:   #3b82f6;
    --accent-fg:#ffffff;
    --green:    #4ade80;
    --text:     #ececf1;
    --muted:    #5b8ab0;
    --user-bg:  #0f1c2e;
    --ai-bg:    #0a1220;
}

*, *::before, *::after { box-sizing: border-box; }

html, body, .stApp {
    background: var(--bg) !important;
    color: var(--text) !important;
    font-family: 'DM Sans', sans-serif !important;
}

/* ── Hide Streamlit chrome ── */
#MainMenu, footer, header,
[data-testid="stToolbar"],
[data-testid="stDecoration"],
[data-testid="stStatusWidget"],
.stDeployButton { display: none !important; }

/* ── Hide ALL collapse buttons — sidebar stays open always ── */
[data-testid="collapsedControl"],
[data-testid="stSidebarCollapsedControl"],
[data-testid="stSidebarNavCollapseIcon"],
button[aria-label="open sidebar"],
button[aria-label="close sidebar"],
button[aria-label="Close sidebar"],
button[aria-label="Open sidebar"],
button[kind="header"] {
    display: none !important;
    visibility: hidden !important;
    pointer-events: none !important;
}

/* ── Sidebar locked open ── */
section[data-testid="stSidebar"] {
    background: var(--surface) !important;
    border-right: 1px solid var(--border) !important;
    width: 270px !important;
    min-width: 270px !important;
    max-width: 270px !important;
    transform: translateX(0) !important;
    visibility: visible !important;
    display: flex !important;
    flex-direction: column !important;
    transition: none !important;
}
section[data-testid="stSidebar"] > div:first-child {
    padding: 0 !important;
    width: 270px !important;
    overflow-y: auto !important;
    overflow-x: hidden !important;
    height: 100vh !important;
}

/* ── API key input padding ── */
section[data-testid="stSidebar"] [data-testid="stTextInput"] {
    padding: 0 14px !important;
}
/* New Chat button padding */
section[data-testid="stSidebar"] .new-chat-wrap {
    padding: 0 12px !important;
}

/* ── API key input ── */
.stTextInput input {
    background: var(--surface2) !important;
    border: 1px solid var(--border) !important;
    border-radius: 8px !important;
    color: var(--text) !important;
    font-family: 'DM Mono', monospace !important;
    font-size: 0.75rem !important;
    padding: 8px 10px !important;
}
.stTextInput input:focus {
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 2px rgba(59,130,246,0.15) !important;
    outline: none !important;
}
.stTextInput label {
    color: var(--accent) !important;
    font-size: 0.68rem !important;
    font-weight: 500 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.09em !important;
}

/* ── Sidebar all buttons base ── */
section[data-testid="stSidebar"] .stButton > button {
    background: transparent !important;
    border: none !important;
    color: var(--text) !important;
    text-align: left !important;
    padding: 6px 10px !important;
    border-radius: 6px !important;
    width: 100% !important;
    font-size: 0.8rem !important;
    font-family: 'DM Sans', sans-serif !important;
    transition: color 0.12s, background 0.12s !important;
}
section[data-testid="stSidebar"] .stButton > button:hover {
    background: var(--surface2) !important;
    color: var(--muted) !important;
}

/* ── New chat button ── */
.new-chat-wrap .stButton > button {
    background: var(--accent) !important;
    color: var(--accent-fg) !important;
    border-radius: 9px !important;
    font-weight: 600 !important;
    padding: 9px 16px !important;
    font-size: 0.85rem !important;
}
.new-chat-wrap .stButton > button:hover {
    opacity: 0.88 !important;
    background: var(--accent) !important;
    color: var(--accent-fg) !important;
}

/* ── Section label ── */
.sb-section-label {
    padding: 14px 16px 6px;
    font-size: 0.65rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.12em;
    color: var(--accent);
}

/* ── Chat cards ── */
.chat-card {
    margin: 2px 8px;
    padding: 9px 12px;
    border-radius: 8px;
    border: 1px solid transparent;
    cursor: pointer;
    transition: background 0.15s;
}
.chat-card:hover { background: var(--surface2); }
.chat-card-active {
    background: rgba(59,130,246,0.1) !important;
    border-color: rgba(59,130,246,0.3) !important;
}
.chat-card-title {
    font-size: 0.83rem;
    font-weight: 500;
    color: var(--text);
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    margin-bottom: 3px;
    line-height: 1.3;
}
.chat-card-doc {
    display: inline-flex;
    align-items: center;
    gap: 4px;
    font-size: 0.67rem;
    font-family: 'DM Mono', monospace;
    color: rgba(59,130,246,0.65);
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    max-width: 200px;
}

/* Active chat button */
.chat-click-btn-active .stButton > button {
    background: rgba(59,130,246,0.1) !important;
    border-color: rgba(59,130,246,0.3) !important;
    color: var(--text) !important;
}
.chat-click-btn .stButton > button {
    background: transparent !important;
    border: 1px solid transparent !important;
    border-radius: 8px !important;
    color: var(--text) !important;
    text-align: left !important;
    padding: 5px 10px !important;
    width: 100% !important;
    font-size: 0.83rem !important;
    font-weight: 500 !important;
    font-family: 'DM Sans', sans-serif !important;
    line-height: 1.3 !important;
    transition: background 0.15s !important;
    white-space: nowrap !important;
    overflow: hidden !important;
    text-overflow: ellipsis !important;
}
.chat-click-btn .stButton > button:hover {
    background: var(--surface2) !important;
    color: var(--muted) !important;
}

/* ── Tighten sidebar chat list spacing ── */
section[data-testid="stSidebar"] [data-testid="stVerticalBlock"] {
    gap: 2px !important;
}
section[data-testid="stSidebar"] [data-testid="element-container"] {
    margin: 0 !important;
    padding: 0 !important;
}
section[data-testid="stSidebar"] .stButton {
    margin: 0 !important;
    padding: 0 !important;
}
/* Horizontal block (chat + menu button row) */
section[data-testid="stSidebar"] div[data-testid="stHorizontalBlock"] {
    gap: 2px !important;
    margin: 0 !important;
    padding: 0 !important;
    align-items: center !important;
}

/* Menu ⋮ button */
.menu-btn .stButton > button {
    padding: 4px 6px !important;
    font-size: 1.1rem !important;
    color: var(--muted) !important;
    line-height: 1 !important;
    border-radius: 5px !important;
}

/* ── Main content ── */
.block-container {
    padding: 0 2.5rem 2rem !important;
    max-width: 900px !important;
}

/* ── Top bar ── */
.topbar {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 22px 0 16px;
    border-bottom: 1px solid var(--border);
    margin-bottom: 20px;
}
.topbar-title {
    font-size: 1.1rem;
    font-weight: 600;
    letter-spacing: -0.025em;
    color: var(--text);
}
.topbar-doc {
    display: flex;
    align-items: center;
    gap: 6px;
    padding: 4px 12px;
    background: rgba(74,222,128,0.07);
    border: 1px solid rgba(74,222,128,0.2);
    border-radius: 20px;
    font-size: 0.72rem;
    font-family: 'DM Mono', monospace;
    color: var(--green);
}
.topbar-doc-resumed {
    background: rgba(59,130,246,0.07);
    border-color: rgba(59,130,246,0.25);
    color: rgba(59,130,246,0.9);
}

/* ── File uploader ── */
[data-testid="stFileUploader"] {
    background: var(--surface) !important;
    border: 1.5px dashed var(--border) !important;
    border-radius: 12px !important;
    padding: 10px 16px !important;
    transition: border-color 0.2s !important;
    margin-bottom: 16px !important;
}
[data-testid="stFileUploader"]:hover {
    border-color: var(--accent) !important;
}
[data-testid="stFileUploaderDropzoneInstructions"] div,
[data-testid="stFileUploader"] label {
    color: rgba(91,138,176,0.9) !important;
    font-size: 0.8rem !important;
}

/* ── Messages ── */
.msg { margin-bottom: 16px; animation: msgIn 0.18s ease; }
@keyframes msgIn {
    from { opacity: 0; transform: translateY(5px); }
    to   { opacity: 1; transform: translateY(0); }
}
.msg-user { display: flex; justify-content: flex-end; }
.msg-user .bbl {
    background: var(--user-bg);
    border: 1px solid rgba(59,130,246,0.2);
    border-radius: 16px 16px 3px 16px;
    padding: 11px 15px;
    max-width: 72%;
    font-size: 0.875rem;
    line-height: 1.65;
    color: var(--text);
    word-wrap: break-word;
}
.msg-ai { display: flex; gap: 10px; align-items: flex-start; }
.msg-ai .av {
    width: 26px; height: 26px; flex-shrink: 0;
    background: var(--accent);
    border-radius: 7px;
    display: flex; align-items: center; justify-content: center;
    font-size: 0.6rem; font-weight: 700;
    color: white;
    margin-top: 3px;
    font-family: 'DM Mono', monospace;
}
.msg-ai .bbl {
    background: var(--ai-bg);
    border: 1px solid var(--border);
    border-radius: 3px 16px 16px 16px;
    padding: 11px 15px;
    max-width: 80%;
    font-size: 0.875rem;
    line-height: 1.72;
    color: var(--text);
    white-space: pre-wrap;
    word-wrap: break-word;
}

/* ── Empty state ── */
.empty {
    text-align: center;
    padding: 64px 20px;
    color: var(--muted);
}
.empty-icon { font-size: 2rem; margin-bottom: 12px; }
.empty h3 { font-size: 0.95rem; font-weight: 500; color: var(--text); margin-bottom: 6px; }
.empty p  { font-size: 0.8rem; line-height: 1.65; }

/* ── Chat input ── */
[data-testid="stChatInput"] {
    background: var(--surface) !important;
    border: 1px solid var(--border) !important;
    border-radius: 12px !important;
}
[data-testid="stChatInput"]:focus-within {
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 2px rgba(59,130,246,0.08) !important;
}
[data-testid="stChatInput"] textarea {
    color: var(--text) !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.875rem !important;
    background: transparent !important;
}
[data-testid="stChatInputSubmitButton"] svg {
    color: var(--accent) !important;
}

/* ── Alerts ── */
.stSuccess > div, .stInfo > div,
.stWarning > div, .stError > div {
    border-radius: 8px !important;
    font-size: 0.8rem !important;
    font-family: 'DM Sans', sans-serif !important;
}

/* ── Dev expander ── */
[data-testid="stExpander"] {
    border: none !important;
    border-top: 1px solid var(--border) !important;
    border-radius: 0 !important;
    background: transparent !important;
}
[data-testid="stExpander"] summary {
    color: var(--muted) !important;
    font-size: 0.72rem !important;
}

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 3px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: var(--border); border-radius: 2px; }

hr { border-color: var(--border) !important; }
</style>
""", unsafe_allow_html=True)

# ── Storage ───────────────────────────────────────────────────────────
CHAT_FOLDER = "chats"
os.makedirs(CHAT_FOLDER, exist_ok=True)


def load_chat(chat_id):
    path = os.path.join(CHAT_FOLDER, f"{chat_id}.json")
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
            if isinstance(data, list):
                return {"title": chat_id[:8], "messages": data, "doc_id": None}
            return data
    return {"title": "New Chat", "messages": [], "doc_id": None}


def save_chat(chat_id, title, messages, doc_id, injection_time=None):
    path = os.path.join(CHAT_FOLDER, f"{chat_id}.json")
    existing = {}
    if os.path.exists(path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                existing = json.load(f)
                if isinstance(existing, list):
                    existing = {}
        except Exception:
            existing = {}
    payload = {"title": title, "messages": messages, "doc_id": doc_id}
    if injection_time is not None:
        payload["injection_time"] = injection_time
    elif "injection_time" in existing:
        payload["injection_time"] = existing["injection_time"]
    with open(path, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)


def delete_chat(chat_id):
    path = os.path.join(CHAT_FOLDER, f"{chat_id}.json")
    if os.path.exists(path):
        os.remove(path)


def list_chats():
    chats = []
    if not os.path.exists(CHAT_FOLDER):
        return chats
    for file in sorted(os.listdir(CHAT_FOLDER), reverse=True):
        if file.endswith(".json"):
            cid = file.replace(".json", "")
            data = load_chat(cid)
            chats.append({
                "id": cid,
                "title": data.get("title", cid[:8]),
                "doc_id": data.get("doc_id")
            })
    return chats


def render_message(role, content):
    safe = html.escape(str(content))
    if role == "user":
        st.markdown(
            f'<div class="msg msg-user"><div class="bbl">{safe}</div></div>',
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            f'<div class="msg msg-ai"><div class="av">AI</div><div class="bbl">{safe}</div></div>',
            unsafe_allow_html=True
        )


# ── Session state ─────────────────────────────────────────────────────
defaults = {
    "page": "chat",
    "messages": [],
    "chat_id": str(uuid.uuid4()),
    "chat_title": "New Chat",
    "current_doc_id": None,
    "uploaded_file_name": None,
    "menu_open_id": None,
    "renaming_id": None,
    "upload_triggered": False,
    "chat_resumed": False,
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v


def go(page):
    st.session_state.page = page
    st.rerun()

# ── Sidebar ───────────────────────────────────────────────────────────
with st.sidebar:
    # Logo
    st.markdown("""
        <div style="padding:16px 16px 14px; border-bottom:1px solid var(--border); margin-bottom:16px;">
            <div style="display:flex; align-items:center; gap:10px;">
                <div style="width:30px;height:30px;background:var(--accent);border-radius:8px;
                            display:flex;align-items:center;justify-content:center;font-size:0.85rem;">
                    📖
                </div>
                <span style="font-size:1rem;font-weight:600;color:var(--text);letter-spacing:-0.02em;">
                    Multimedia Chatbot
                </span>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # API Key
    api_key = st.text_input(
        "Enter Gemini API Key", type="password",
        key="gemini_api_key_input", placeholder="AIza…"
    )
    st.markdown('<div style="height:12px;"></div>', unsafe_allow_html=True)

    # New Chat
    st.markdown('<div class="new-chat-wrap">', unsafe_allow_html=True)
    if st.button("＋  New Chat", use_container_width=True, key="new_chat_btn"):
        st.session_state.update({
            "messages": [],
            "chat_id": str(uuid.uuid4()),
            "chat_title": "New Chat",
            "current_doc_id": None,
            "uploaded_file_name": None,
            "menu_open_id": None,
            "renaming_id": None,
            "upload_triggered": False,
            "chat_resumed": False,
        })
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('<div style="height:14px;"></div>', unsafe_allow_html=True)

    # ── Navigation buttons ──
    st.markdown('<div class="sb-section-label">Tools</div>', unsafe_allow_html=True)
    st.markdown('<div style="padding:0 8px;">', unsafe_allow_html=True)
    if st.button("📊  Performance Metrics", use_container_width=True, key="nav_metrics"):
        go("metrics")
    if st.button("🔑  What is an API Key?", use_container_width=True, key="nav_api_guide"):
        go("api_guide")
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('<div style="height:10px;"></div>', unsafe_allow_html=True)

    # Chat list
    st.markdown('<div class="sb-section-label">All Chats</div>', unsafe_allow_html=True)
    st.markdown('<div style="height:10px;"></div>', unsafe_allow_html=True)

    all_chats = list_chats()
    if not all_chats:
        st.markdown(
            '<p style="padding:8px 16px;font-size:0.76rem;color:var(--accent);">No chats yet</p>',
            unsafe_allow_html=True
        )

    for chat in all_chats:
        cid = chat["id"]
        ctitle = chat["title"]
        cdoc = chat["doc_id"]
        is_active = cid == st.session_state.chat_id

        # ── Rename mode ──
        if st.session_state.renaming_id == cid:
            new_name = st.text_input(
                "", value=ctitle, key=f"rename_input_{cid}",
                label_visibility="collapsed"
            )
            c1, c2 = st.columns(2)
            with c1:
                if st.button("✓ Save", key=f"save_{cid}", use_container_width=True):
                    d = load_chat(cid)
                    save_chat(cid, new_name, d["messages"], d.get("doc_id"))
                    if st.session_state.chat_id == cid:
                        st.session_state.chat_title = new_name
                    st.session_state.renaming_id = None
                    st.rerun()
            with c2:
                if st.button("✕", key=f"cancel_{cid}", use_container_width=True):
                    st.session_state.renaming_id = None
                    st.rerun()
            continue

        # ── Chat card ──
        active_class = "chat-card-active" if is_active else ""
        title_display = ctitle if len(ctitle) <= 28 else ctitle[:25] + "…"
        doc_html = ""
        if cdoc:
            doc_name = os.path.basename(cdoc)
            doc_short = doc_name if len(doc_name) <= 24 else doc_name[:21] + "…"
            doc_html = f'<div class="chat-card-doc">📄 {html.escape(doc_short)}</div>'

        col_click, col_menu = st.columns([5, 1])
        with col_click:
            active_wrap_class = "chat-click-btn-active" if is_active else ""
            st.markdown(f'<div class="chat-click-btn {active_wrap_class}">', unsafe_allow_html=True)
            if st.button(title_display, key=f"chat_{cid}", use_container_width=True):
                if cid != st.session_state.chat_id:
                    d = load_chat(cid)
                    st.session_state.update({
                        "messages": d["messages"],
                        "chat_id": cid,
                        "chat_title": ctitle,
                        "current_doc_id": d.get("doc_id"),
                        "uploaded_file_name": d.get("doc_id"),
                        "menu_open_id": None,
                        "upload_triggered": False,
                        "chat_resumed": bool(d.get("doc_id")),
                    })
                    st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

        with col_menu:
            st.markdown('<div class="menu-btn">', unsafe_allow_html=True)
            if st.button("⋮", key=f"menu_{cid}"):
                st.session_state.menu_open_id = (
                    cid if st.session_state.menu_open_id != cid else None
                )
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

        if st.session_state.menu_open_id == cid:
            cr, cd = st.columns(2)
            with cr:
                if st.button("✏️ Rename", key=f"rename_{cid}", use_container_width=True):
                    st.session_state.renaming_id = cid
                    st.session_state.menu_open_id = None
                    st.rerun()
            with cd:
                if st.button("🗑️ Delete", key=f"delete_{cid}", use_container_width=True):
                    delete_chat(cid)
                    if st.session_state.chat_id == cid:
                        st.session_state.update({
                            "messages": [],
                            "chat_id": str(uuid.uuid4()),
                            "chat_title": "New Chat",
                            "current_doc_id": None,
                            "uploaded_file_name": None,
                            "upload_triggered": False,
                            "chat_resumed": False,
                        })
                    st.session_state.menu_open_id = None
                    st.rerun()

    # Dev tools
    st.markdown("<br>", unsafe_allow_html=True)
    with st.expander("⚙️ Dev Tools"):
        if st.button("🔄 Reset Milvus Collection", use_container_width=True):
            try:
                r = requests.post("http://127.0.0.1:8000/reset-collection", timeout=30)
                st.success(r.json().get("message", "Reset done."))
                st.session_state.update({
                    "messages": [],
                    "chat_id": str(uuid.uuid4()),
                    "chat_title": "New Chat",
                    "current_doc_id": None,
                    "uploaded_file_name": None,
                    "upload_triggered": False,
                    "chat_resumed": False,
                })
                st.rerun()
            except Exception as e:
                st.error(f"❌ {e}")

# ══════════════════════════════════════════════════════════════════════
# PAGE: CHAT
# ══════════════════════════════════════════════════════════════════════
if st.session_state.page == "chat":

    doc_name = os.path.basename(st.session_state.current_doc_id) if st.session_state.current_doc_id else None

    if doc_name:
        resumed  = st.session_state.chat_resumed
        pill_cls = "topbar-doc-resumed" if resumed else "topbar-doc"
        icon     = "↩" if resumed else "●"
        doc_html = f'<div class="{pill_cls}">{icon} {html.escape(doc_name)}</div>'
    else:
        doc_html = ""

    st.markdown(f"""
        <div class="topbar">
            <div class="topbar-title">Chat with your Document</div>
            {doc_html}
        </div>
    """, unsafe_allow_html=True)

    # ── File uploader ──────────────────────────────────────────────────
    if not st.session_state.current_doc_id:
        uploaded_file = st.file_uploader(
            "Upload a document — PDF, DOCX, TXT, PPTX",
            type=["pdf", "docx", "txt", "pptx"],
            key="file_uploader",
        )
        if uploaded_file and not st.session_state.upload_triggered:
            if not api_key:
                st.warning("⚠️ Enter your Gemini API key in the sidebar first.")
            else:
                st.session_state.upload_triggered = True
                ph = st.empty()
                ph.info(f"⏳ Indexing **{uploaded_file.name}**…")
                import time as _time
                _inj_t0 = _time.time()
                try:
                    resp = requests.post(
                        "http://127.0.0.1:8000/upload",
                        files={"file": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)},
                        data={"api_key": api_key},
                        timeout=600,
                    )
                    resp.raise_for_status()
                    result = resp.json()
                    _injection_time = round(_time.time() - _inj_t0, 2)
                    ph.empty()
                    if result.get("status") in ("success", "already_exists"):
                        st.session_state.uploaded_file_name = uploaded_file.name
                        st.session_state.current_doc_id     = uploaded_file.name
                        st.session_state.chat_resumed       = False
                        save_chat(
                            st.session_state.chat_id,
                            st.session_state.chat_title,
                            st.session_state.messages,
                            uploaded_file.name,
                            injection_time=_injection_time,
                        )
                        st.rerun()
                    else:
                        st.error(f"❌ {result.get('message', 'Upload failed')}")
                        st.session_state.upload_triggered = False
                except requests.exceptions.ConnectionError:
                    ph.empty()
                    st.error("❌ Cannot connect to backend. Is FastAPI running on port 8000?")
                    st.session_state.upload_triggered = False
                except requests.exceptions.Timeout:
                    ph.empty()
                    st.error("❌ Timed out. Try a smaller file.")
                    st.session_state.upload_triggered = False
                except Exception as e:
                    ph.empty()
                    st.error(f"❌ {e}")
                    st.session_state.upload_triggered = False
    else:
        _, col_change = st.columns([8, 1])
        with col_change:
            if st.button("Change", key="change_doc"):
                st.session_state.update({
                    "messages": [], "chat_id": str(uuid.uuid4()),
                    "chat_title": "New Chat", "current_doc_id": None,
                    "uploaded_file_name": None, "upload_triggered": False,
                    "chat_resumed": False,
                })
                st.rerun()

    # ── Chat messages ──────────────────────────────────────────────────
    if not st.session_state.messages:
        if not st.session_state.current_doc_id:
            st.markdown("""
                <div class="empty">
                    <div class="empty-icon">📄</div>
                    <h3>No document loaded</h3>
                    <p>Upload a PDF, DOCX, TXT or PPTX above<br>to start chatting.</p>
                </div>
            """, unsafe_allow_html=True)
        else:
            fname = html.escape(os.path.basename(st.session_state.current_doc_id))
            st.markdown(f"""
                <div class="empty">
                    <div class="empty-icon">💬</div>
                    <h3>Ready to chat</h3>
                    <p><b>{fname}</b> is indexed.<br>Ask anything below.</p>
                </div>
            """, unsafe_allow_html=True)
    else:
        for msg in st.session_state.messages:
            render_message(msg["role"], msg["content"])

    # ── Chat input ─────────────────────────────────────────────────────
    query = st.chat_input("Ask anything about the document…")

    if query:
        if not api_key:
            st.warning("⚠️ Enter your Gemini API key in the sidebar.")
        elif not st.session_state.current_doc_id:
            st.warning("⚠️ Upload a document first.")
        else:
            st.session_state.messages.append({"role": "user", "content": query})
            if len(st.session_state.messages) == 1:
                st.session_state.chat_title = query[:42] + ("…" if len(query) > 42 else "")

            ph = st.empty()
            ph.info("⏳ Thinking…")
            import time as _time
            _t0 = _time.time()
            try:
                resp = requests.post(
                    "http://127.0.0.1:8000/chat",
                    data={
                        "query":   query,
                        "api_key": api_key,
                        "doc_id":  st.session_state.current_doc_id,
                    },
                    timeout=120,
                )
                resp.raise_for_status()
                answer = resp.json().get("answer") or "No answer returned."
            except requests.exceptions.ConnectionError:
                answer = "❌ Cannot connect to backend. Is FastAPI running on port 8000?"
            except requests.exceptions.Timeout:
                answer = "❌ Request timed out. Please try again."
            except Exception as e:
                answer = f"❌ {e}"
            _response_time = round(_time.time() - _t0, 2)

            ph.empty()
            st.session_state.messages.append({
                "role": "assistant",
                "content": answer,
                "response_time": _response_time,
            })
            save_chat(
                st.session_state.chat_id,
                st.session_state.chat_title,
                st.session_state.messages,
                st.session_state.current_doc_id,
            )
            st.rerun()


# ══════════════════════════════════════════════════════════════════════
# PAGE: PERFORMANCE METRICS
# ══════════════════════════════════════════════════════════════════════
elif st.session_state.page == "metrics":
    import re
    import pandas as pd

    if st.button("← Back to Chat", key="back_metrics_top"):
        go("chat")

    st.markdown("""
        <div class="topbar">
            <div class="topbar-title">📊 Performance Metrics</div>
        </div>
    """, unsafe_allow_html=True)
    st.caption("Computed from your stored chat history and uploaded documents.")

    UPLOAD_FOLDER = "uploads"

    def classify(answer):
        if not answer or not answer.strip(): return "empty"
        a = answer.lower()
        if any(s in a for s in ["rate limit","quota","resource_exhausted","please wait"]):
            return "rate_limit"
        if any(s in a for s in ["error:","traceback","exception","invalid_argument",
                                  "api key not valid","unexpected keyword","unauthenticated",
                                  "not found for api"]):
            return "error"
        if any(s in a for s in ["not related to","not covered","no related content",
                                  "could not find","topic isn't covered"]):
            return "no_answer"
        if len(answer.strip()) < 20: return "empty"
        return "answered"

    def word_overlap(q, a):
        stop = {'the','a','an','is','are','was','what','how','why','can','u','i',
                'me','my','please','explain','tell','about','more','this','it','in','of','to'}
        qw = set(re.sub(r'[^\w\s]','',q.lower()).split()) - stop
        aw = set(re.sub(r'[^\w\s]','',a.lower()).split()) - stop
        return round(len(qw & aw) / len(qw), 2) if qw else 0.0

    def length_score(a):
        w = len(a.split())
        if w < 10: return 0.0
        if w < 30: return 0.5
        if w < 300: return 1.0
        return 0.9

    def faithfulness_score(answer):
        """
        Heuristic faithfulness: penalise hallucination signals.
        Returns 0.0-1.0. High = answer seems grounded in retrieved context.
        """
        a = answer.lower()
        # Strong hallucination signals → low faithfulness
        hallucination_phrases = [
            "i think", "i believe", "in my opinion", "probably", "i'm not sure",
            "i don't know", "as far as i know", "i assume", "generally speaking",
            "it is widely known", "most people", "everyone knows",
        ]
        penalty = sum(1 for p in hallucination_phrases if p in a)
        # Grounding signals → boost faithfulness
        grounding_phrases = [
            "according to the document", "the document states", "based on the provided",
            "as mentioned in", "the text says", "per the document", "the passage",
            "in the document", "from the document", "the document mentions",
        ]
        boost = sum(1 for p in grounding_phrases if p in a)
        score = max(0.0, min(1.0, 0.75 + boost * 0.08 - penalty * 0.12))
        return round(score, 2)



    all_chats_data = list_chats()

    # Build doc → injection_time lookup from chat files
    doc_injection_times = {}
    for ch in all_chats_data:
        d = load_chat(ch["id"])
        doc = d.get("doc_id")
        it  = d.get("injection_time")
        if doc and it is not None:
            doc_injection_times[os.path.basename(doc)] = it

    docs_list = []
    if os.path.exists(UPLOAD_FOLDER):
        for f in os.listdir(UPLOAD_FOLDER):
            sz = os.path.getsize(os.path.join(UPLOAD_FOLDER, f))
            inj = doc_injection_times.get(f)
            docs_list.append({
                "Document":         f,
                "Size (KB)":        round(sz/1024, 1),
                "Injection Time (s)": inj if inj is not None else "—",
            })

    qa_pairs = []
    for ch in all_chats_data:
        d = load_chat(ch["id"])
        msgs = d.get("messages", [])
        for i, msg in enumerate(msgs):
            if msg["role"] != "user": continue
            for j in range(i+1, len(msgs)):
                if msgs[j]["role"] == "assistant":
                    ans = msgs[j]["content"]
                    qa_pairs.append({
                        "chat_title":        ch["title"],
                        "doc_id":            ch.get("doc_id") or "—",
                        "question":          msg["content"],
                        "answer":            ans,
                        "status":            classify(ans),
                        "relevance":         word_overlap(msg["content"], ans),
                        "quality":           length_score(ans),
                        "faithfulness":      faithfulness_score(ans),
                        "response_time":     msgs[j].get("response_time", None),
                        "hit":                msgs[j].get("hit", None),
                    })
                    break

    seen, unique = set(), []
    for q in qa_pairs:
        k = (q["question"], q["answer"][:50])
        if k not in seen:
            seen.add(k)
            unique.append(q)

    total    = len(unique)
    answered = [q for q in unique if q["status"] == "answered"]
    errors   = [q for q in unique if q["status"] == "error"]
    no_ans   = [q for q in unique if q["status"] == "no_answer"]
    rate_lim = [q for q in unique if q["status"] == "rate_limit"]

    succ  = round(len(answered)/total*100, 1) if total else 0
    a_rel = round(sum(q["relevance"] for q in answered)/len(answered), 2) if answered else 0
    a_qua = round(sum(q["quality"]   for q in answered)/len(answered), 2) if answered else 0
    a_wrd = round(sum(len(q["answer"].split()) for q in answered)/len(answered)) if answered else 0
    a_faith = round(sum(q["faithfulness"] for q in answered)/len(answered), 2) if answered else 0
    timed   = [q for q in answered if q["response_time"] is not None]
    a_time  = round(sum(q["response_time"] for q in timed)/len(timed), 2) if timed else None
    inj_vals = [v for v in doc_injection_times.values() if v is not None]
    a_inj    = round(sum(inj_vals)/len(inj_vals), 2) if inj_vals else None

    # R@K / Hit Rate: fraction of answered Qs where backend signalled a hit (or heuristic: answer has > 40 words = retrieved context used)
    hit_qs   = [q for q in answered if q.get("hit") is not None]
    if hit_qs:
        hit_rate = round(sum(1 for q in hit_qs if q["hit"])/len(hit_qs), 2)
    else:
        # Heuristic fallback: long answers likely used retrieved chunks
        hit_rate = round(sum(1 for q in answered if len(q["answer"].split()) > 40)/len(answered), 2) if answered else 0.0

    # Answer Completeness Rate: % of answers with >= 50 words (thorough, not one-liners)
    completeness_rate = round(sum(1 for q in answered if len(q["answer"].split()) >= 50) / len(answered), 2) if answered else 0.0

    def mcard(col, val, label, good=None):
        color = ""
        if good is not None:
            color = "color:#4ade80" if good else "color:#f87171"
        col.markdown(
            f'<div style="background:#131316;border:1px solid #1e2a3a;border-radius:12px;'
            f'padding:18px;text-align:center;margin-bottom:8px;">'
            f'<div style="font-size:2rem;font-weight:700;{color}">{val}</div>'
            f'<div style="font-size:0.75rem;color:#5b8ab0;margin-top:4px;">{label}</div></div>',
            unsafe_allow_html=True
        )

    # ── Row 1: Info (no colour) ──────────────────────────────────────
    i1,i2,i3,i4,i5 = st.columns(5)
    mcard(i1, total,                "Total Questions",  None)
    mcard(i2, len(answered),        "Answered",         None)
    mcard(i3, len(errors),          "API Errors",       None)
    mcard(i4, len(docs_list),       "Docs Uploaded",    None)
    mcard(i5, len(all_chats_data),  "Chat Sessions",    None)

    st.markdown("<br>", unsafe_allow_html=True)
    # ── Row 2: Core performance ───────────────────────────────────────
    p1,p2,p3,p4 = st.columns(4)
    mcard(p1, f"{succ}%", "Success Rate",           succ >= 60)
    mcard(p2, a_rel,       "Keyword Relevance (0–1)", a_rel >= 0.3)
    mcard(p3, a_qua,       "Answer Quality (0–1)",    a_qua >= 0.7)
    mcard(p4, a_wrd,       "Avg Answer Words",        a_wrd >= 50)

    st.markdown("<br>", unsafe_allow_html=True)
    # ── Row 3: Quality & timing ───────────────────────────────────────
    t1,t2,t3 = st.columns(3)
    mcard(t1, a_faith, "Faithfulness (0–1)", a_faith >= 0.7)
    time_display = f"{a_time}s" if a_time is not None else "N/A"
    time_good    = (a_time < 25) if a_time is not None else None
    mcard(t2, time_display, "Avg Response Time", time_good)
    inj_display  = f"{a_inj}s" if a_inj is not None else "N/A"
    inj_good     = (a_inj < 60) if a_inj is not None else None
    mcard(t3, inj_display, "Avg Injection Time", inj_good)

    st.markdown("<br>", unsafe_allow_html=True)
    # ── Row 4: Retrieval ──────────────────────────────────────────────
    s1, s2 = st.columns(2)
    hit_pct = f"{round(hit_rate*100,1)}%"
    mcard(s1, hit_pct, "R@K Hit Rate", hit_rate >= 0.7)
    comp_pct = f"{round(completeness_rate*100,1)}%"
    mcard(s2, comp_pct, "Answer Completeness Rate", completeness_rate >= 0.7)

    st.markdown("---")
    col_bar, col_tbl = st.columns(2)
    breakdown = {
        "✅ Answered":     len(answered),
        "❌ API Error":    len(errors),
        "🔶 No Answer":    len(no_ans),
        "⏳ Rate Limited": len(rate_lim),
    }
    with col_bar:
        st.markdown("**Response Breakdown**")
        df_b = pd.DataFrame({"Count": breakdown}).rename_axis("Category")
        st.bar_chart(df_b, color="#3b82f6")
    with col_tbl:
        st.markdown("**By category**")
        for lbl, cnt in breakdown.items():
            pct = round(cnt/total*100,1) if total else 0
            st.markdown(f"- {lbl}: **{cnt}** ({pct}%)")

    st.markdown("---")
    st.markdown("**Uploaded Documents**")
    if docs_list:
        st.dataframe(pd.DataFrame(docs_list), use_container_width=True, hide_index=True)
    else:
        st.info("No documents in uploads folder.")

    st.markdown("---")
    st.markdown("**Q&A Detail**")
    filt = st.selectbox("Filter:", ["All","✅ Answered","❌ API Error","🔶 No Answer","⏳ Rate Limited"])
    fmap = {"All":None,"✅ Answered":"answered","❌ API Error":"error",
            "🔶 No Answer":"no_answer","⏳ Rate Limited":"rate_limit"}
    rows = [q for q in unique if fmap[filt] is None or q["status"]==fmap[filt]]
    if rows:
        st.dataframe(pd.DataFrame([{
            "Chat":              r["chat_title"][:20],
            "Document":          r["doc_id"],
            "Question":          r["question"][:60],
            "Answer":            r["answer"][:80]+("…" if len(r["answer"])>80 else ""),
            "Status":            r["status"],
            "Relevance":         r["relevance"],
            "Quality":           r["quality"],
            "Faithfulness":      r["faithfulness"],
            "Response Time (s)":      r["response_time"] if r["response_time"] is not None else "—",
            "Hit":                    ("✅" if r.get("hit") else ("✅" if len(r["answer"].split()) > 40 else "❌")),
        } for r in rows]), use_container_width=True, hide_index=True)
    else:
        st.info("No records match this filter.")

    st.markdown("---")
    if st.button("← Back to Chat", key="back_metrics_bottom"):
        go("chat")


# ══════════════════════════════════════════════════════════════════════
# PAGE: API KEY GUIDE
# ══════════════════════════════════════════════════════════════════════
elif st.session_state.page == "api_guide":

    if st.button("← Back to Chat", key="back_guide_top"):
        go("chat")

    st.markdown("""
        <div class="topbar">
            <div class="topbar-title">🔑 What is a Gemini API Key?</div>
        </div>
    """, unsafe_allow_html=True)

    def info_card(title, body):
        st.markdown(f"""
        <div style="background:#131316;border:1px solid #1e2a3a;border-radius:12px;
                    padding:20px 24px;margin-bottom:14px;">
            <div style="color:#3b82f6;font-weight:600;font-size:1rem;margin-bottom:8px;">{title}</div>
            <div style="color:#cbd5e1;font-size:0.875rem;line-height:1.75;">{body}</div>
        </div>""", unsafe_allow_html=True)

    info_card("🤔 What is an API Key?",
        "An <b>API key</b> is a unique code that identifies you when your app communicates with "
        "Google's Gemini AI. Think of it as a <b>password + username combined</b> that proves "
        "you have permission to use their AI service.")

    info_card("❓ Why Does This App Need It?",
        "This RAG chatbot uses two Gemini services:<br>"
        "• <b>Gemini Embedding Model</b> — converts your document into searchable vectors.<br>"
        "• <b>Gemini Flash Model</b> — reads the document chunks and generates your answer.<br><br>"
        "The key is entered by <i>you</i> and is never stored by this app.")

    st.markdown(
        '<div style="color:#3b82f6;font-size:0.7rem;font-weight:700;text-transform:uppercase;'
        'letter-spacing:0.1em;padding:18px 0 10px;">📋 How to Create Your Key — Step by Step</div>',
        unsafe_allow_html=True
    )

    steps = [
        ("Open Google AI Studio",
         'Go to <a href="https://aistudio.google.com" target="_blank" style="color:#3b82f6;">https://aistudio.google.com</a> in your browser.'),
        ("Sign In with Google",
         'Click <b>Sign In</b> and log in with your personal Gmail account.<br>'
         '⚠️ College/institution emails may be blocked — use a personal Gmail.'),
        ("Go to API Keys",
         'Click <b>"Get API Key"</b> on the left sidebar, or go to '
         '<a href="https://aistudio.google.com/apikey" target="_blank" style="color:#3b82f6;">https://aistudio.google.com/apikey</a>.'),
        ("Create a New Key",
         'Click <b>"Create API key"</b> → select <b>"Create API key in new project"</b>.<br>'
         'Using a <i>new project</i> gives you fresh free-tier quota.'),
        ("Copy the Key",
         'Your key will look like: <code style="background:#0c0c0e;padding:2px 7px;border-radius:4px;'
         'font-family:DM Mono,monospace;font-size:0.8rem;">AIzaSyXXXXXXXXXXXXXXXXXX</code><br>'
         'Click the <b>copy icon</b> next to it. <b>Save it somewhere safe.</b>'),
        ("Paste it in This App",
         'Come back here and paste your key into the <b>"Enter Gemini API Key"</b> field in the left sidebar.'),
    ]

    for i, (title, body) in enumerate(steps, 1):
        st.markdown(f"""
        <div style="background:#131316;border:1px solid #1e2a3a;border-radius:12px;
                    padding:16px 20px;margin-bottom:10px;display:flex;gap:14px;align-items:flex-start;">
            <div style="background:#3b82f6;color:white;border-radius:50%;width:28px;height:28px;
                        display:flex;align-items:center;justify-content:center;font-weight:700;
                        font-size:0.85rem;flex-shrink:0;margin-top:2px;">{i}</div>
            <div>
                <div style="color:#ececf1;font-weight:600;font-size:0.9rem;margin-bottom:5px;">{title}</div>
                <div style="color:#cbd5e1;font-size:0.825rem;line-height:1.7;">{body}</div>
            </div>
        </div>""", unsafe_allow_html=True)

    info_card("💸 Is It Free?",
        "Yes — Google offers a <b>free tier</b>:<br>"
        "• ✅ 15 requests/minute for Gemini Flash (answer generation)<br>"
        "• ✅ 100 requests/minute for embedding models<br>"
        "• ✅ No credit card required for the free tier<br>"
        "• ⚠️ If you hit the limit, wait 1 minute and try again.")

    info_card("🔧 Common Problems",
        '• <b>"API key not valid"</b> — Copied incorrectly. Go back to AI Studio and copy again.<br>'
        '• <b>"Quota exceeded / limit: 0"</b> — Create the key in a <i>brand new project</i>.<br>'
        '• <b>College email not working</b> — Your institution may have blocked Gemini API. Use personal Gmail.<br>'
        '• <b>Key not working after a while</b> — Make sure you copy the full key with no spaces.')

    st.markdown("---")
    if st.button("← Back to Chat", key="back_guide_bottom"):
        go("chat")
