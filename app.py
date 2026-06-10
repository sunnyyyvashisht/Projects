import streamlit as st
from pathlib import Path
import os
import time

# ─── Page Config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="FileForge",
    page_icon="🗂️",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ─── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=Syne:wght@400;600;700;800&display=swap');

/* ── Root & Background ── */
:root {
    --bg:        #0d0d0d;
    --surface:   #141414;
    --border:    #2a2a2a;
    --accent:    #c8f060;
    --accent2:   #60c8f0;
    --danger:    #f06060;
    --text:      #e8e8e8;
    --muted:     #666;
    --radius:    12px;
}

html, body, [data-testid="stAppViewContainer"] {
    background-color: var(--bg) !important;
    color: var(--text) !important;
    font-family: 'Syne', sans-serif;
}

[data-testid="stAppViewContainer"] {
    background:
        radial-gradient(ellipse 60% 40% at 80% 10%, rgba(200,240,96,.08) 0%, transparent 70%),
        radial-gradient(ellipse 50% 35% at 10% 90%, rgba(96,200,240,.06) 0%, transparent 70%),
        var(--bg);
}

/* hide default Streamlit chrome */
#MainMenu, footer, header { visibility: hidden; }
[data-testid="stDecoration"] { display: none; }

/* ── Hero Banner ── */
.hero {
    text-align: center;
    padding: 3rem 1rem 2rem;
    position: relative;
}
.hero-tag {
    display: inline-block;
    font-family: 'Space Mono', monospace;
    font-size: .72rem;
    letter-spacing: .18em;
    text-transform: uppercase;
    color: var(--accent);
    border: 1px solid rgba(200,240,96,.35);
    border-radius: 99px;
    padding: .3rem 1rem;
    margin-bottom: 1.4rem;
}
.hero-title {
    font-size: clamp(2.6rem, 7vw, 4.5rem);
    font-weight: 800;
    line-height: 1.05;
    letter-spacing: -.02em;
    margin: 0 0 .8rem;
    background: linear-gradient(135deg, var(--text) 30%, var(--accent) 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}
.hero-sub {
    font-size: 1rem;
    color: var(--muted);
    font-family: 'Space Mono', monospace;
    margin: 0;
}

/* ── Operation Cards ── */
.op-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: .75rem;
    margin: 2rem 0 2.5rem;
}
.op-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 1.1rem .8rem;
    text-align: center;
    cursor: pointer;
    transition: border-color .2s, transform .15s;
    text-decoration: none;
}
.op-card:hover { border-color: var(--accent); transform: translateY(-2px); }
.op-card.active { border-color: var(--accent); background: rgba(200,240,96,.07); }
.op-icon { font-size: 1.6rem; margin-bottom: .5rem; }
.op-label {
    font-size: .75rem;
    font-weight: 700;
    letter-spacing: .08em;
    text-transform: uppercase;
    color: var(--muted);
}
.op-card.active .op-label { color: var(--accent); }

/* ── Panel Card ── */
.panel {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 2rem 2rem 2.5rem;
    margin-bottom: 2rem;
}
.panel-title {
    font-size: 1.25rem;
    font-weight: 700;
    margin-bottom: 1.5rem;
    display: flex;
    align-items: center;
    gap: .6rem;
    color: var(--text);
}
.panel-title span { font-size: 1.4rem; }

/* ── Streamlit widget overrides ── */
[data-testid="stTextInput"] > div > div > input,
[data-testid="stTextArea"] textarea {
    background: #1a1a1a !important;
    border: 1px solid var(--border) !important;
    border-radius: 8px !important;
    color: var(--text) !important;
    font-family: 'Space Mono', monospace !important;
    font-size: .9rem !important;
    padding: .7rem 1rem !important;
    transition: border-color .2s !important;
}
[data-testid="stTextInput"] > div > div > input:focus,
[data-testid="stTextArea"] textarea:focus {
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 3px rgba(200,240,96,.12) !important;
}

label[data-testid="stWidgetLabel"] p {
    font-family: 'Space Mono', monospace !important;
    font-size: .78rem !important;
    letter-spacing: .06em !important;
    text-transform: uppercase !important;
    color: var(--muted) !important;
    margin-bottom: .4rem !important;
}

/* Primary button */
.stButton > button {
    background: var(--accent) !important;
    color: #0d0d0d !important;
    border: none !important;
    border-radius: 8px !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important;
    font-size: .9rem !important;
    letter-spacing: .04em !important;
    padding: .6rem 1.8rem !important;
    transition: opacity .2s, transform .15s !important;
    width: 100%;
}
.stButton > button:hover {
    opacity: .88 !important;
    transform: translateY(-1px) !important;
}

/* Radio buttons */
[data-testid="stRadio"] > div {
    flex-direction: row !important;
    gap: .8rem !important;
    flex-wrap: wrap !important;
}
[data-testid="stRadio"] > div > label {
    background: #1a1a1a;
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: .5rem 1.1rem;
    cursor: pointer;
    font-family: 'Space Mono', monospace;
    font-size: .8rem;
    transition: border-color .2s;
}
[data-testid="stRadio"] > div > label:hover { border-color: var(--accent); }

/* ── Alerts / Feedback ── */
.msg-success, .msg-error, .msg-info {
    border-radius: 10px;
    padding: .9rem 1.2rem;
    font-family: 'Space Mono', monospace;
    font-size: .85rem;
    margin-top: 1rem;
    display: flex;
    align-items: center;
    gap: .7rem;
}
.msg-success { background: rgba(200,240,96,.1);  border: 1px solid rgba(200,240,96,.3); color: var(--accent); }
.msg-error   { background: rgba(240,96,96,.1);   border: 1px solid rgba(240,96,96,.3);  color: var(--danger); }
.msg-info    { background: rgba(96,200,240,.1);  border: 1px solid rgba(96,200,240,.3); color: var(--accent2); }

/* ── File content box ── */
.file-content {
    background: #111;
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 1.2rem 1.4rem;
    font-family: 'Space Mono', monospace;
    font-size: .85rem;
    color: var(--accent2);
    white-space: pre-wrap;
    word-break: break-word;
    line-height: 1.7;
    margin-top: 1rem;
    max-height: 300px;
    overflow-y: auto;
}

/* ── Divider ── */
.divider {
    border: none;
    border-top: 1px solid var(--border);
    margin: 1.4rem 0;
}

/* ── Footer ── */
.footer {
    text-align: center;
    color: var(--muted);
    font-family: 'Space Mono', monospace;
    font-size: .72rem;
    padding: 2rem 0 3rem;
    letter-spacing: .05em;
}
.footer a { color: var(--accent); text-decoration: none; }
</style>
""", unsafe_allow_html=True)


# ─── Helpers ──────────────────────────────────────────────────────────────────
def success(msg): st.markdown(f'<div class="msg-success">✅ {msg}</div>', unsafe_allow_html=True)
def error(msg):   st.markdown(f'<div class="msg-error">✗ {msg}</div>',   unsafe_allow_html=True)
def info(msg):    st.markdown(f'<div class="msg-info">ℹ {msg}</div>',    unsafe_allow_html=True)

BASE_DIR = Path("fileforge_files")
BASE_DIR.mkdir(exist_ok=True)

def safe_path(name: str) -> Path:
    return BASE_DIR / name.strip()

def list_files():
    return [f.name for f in sorted(BASE_DIR.iterdir()) if f.is_file()]


# ─── Hero ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <div class="hero-tag">🗂 File Management System</div>
    <h1 class="hero-title">FileForge</h1>
    <p class="hero-sub">create · read · update · delete — elegantly</p>
</div>
""", unsafe_allow_html=True)


# ─── Operation Selector ────────────────────────────────────────────────────────
if "op" not in st.session_state:
    st.session_state.op = "Create"

ops = [("✦ Create", "Create"), ("◎ Read", "Read"), ("⟳ Update", "Update"), ("✕ Delete", "Delete")]

cols = st.columns(4)
for col, (label, key) in zip(cols, ops):
    with col:
        active = "active" if st.session_state.op == key else ""
        st.markdown(f"""
        <div class="op-card {active}" id="op-{key}">
            <div class="op-label">{label}</div>
        </div>""", unsafe_allow_html=True)
        if st.button(key, key=f"btn_{key}", use_container_width=True):
            st.session_state.op = key
            st.rerun()

op = st.session_state.op

# ─── Panel ────────────────────────────────────────────────────────────────────
icons = {"Create": "✦", "Read": "◎", "Update": "⟳", "Delete": "✕"}

st.markdown(f"""
<div class="panel">
    <div class="panel-title"><span>{icons[op]}</span> {op} File</div>
""", unsafe_allow_html=True)

# ── CREATE ────────────────────────────────────────────────────────────────────
if op == "Create":
    filename = st.text_input("File name", placeholder="e.g.  notes.txt")
    content  = st.text_area("File content", placeholder="Start writing…", height=160)

    if st.button("Create File"):
        if not filename:
            error("Please enter a file name.")
        else:
            path = safe_path(filename)
            if path.exists():
                error(f"'{filename}' already exists. Choose a different name.")
            else:
                path.write_text(content)
                success(f"'{filename}' created successfully!")

# ── READ ──────────────────────────────────────────────────────────────────────
elif op == "Read":
    files = list_files()
    if not files:
        info("No files yet. Create one first!")
    else:
        filename = st.selectbox("Select a file to read", files)
        if st.button("Read File"):
            path = safe_path(filename)
            content = path.read_text()
            if content.strip():
                st.markdown(f'<div class="file-content">{content}</div>', unsafe_allow_html=True)
            else:
                info("This file is empty.")

# ── UPDATE ────────────────────────────────────────────────────────────────────
elif op == "Update":
    files = list_files()
    if not files:
        info("No files yet. Create one first!")
    else:
        filename = st.selectbox("Select a file to update", files)
        st.markdown("<hr class='divider'>", unsafe_allow_html=True)

        action = st.radio("Operation", ["Rename", "Append content", "Overwrite content"], horizontal=True)

        if action == "Rename":
            new_name = st.text_input("New file name", placeholder="e.g.  renamed.txt")
            if st.button("Rename File"):
                if not new_name:
                    error("Please enter a new name.")
                elif safe_path(new_name).exists():
                    error(f"'{new_name}' already exists.")
                else:
                    safe_path(filename).rename(safe_path(new_name))
                    success(f"Renamed to '{new_name}' successfully!")
                    st.rerun()

        elif action == "Append content":
            data = st.text_area("Content to append", height=130)
            if st.button("Append"):
                if not data:
                    error("Nothing to append.")
                else:
                    with open(safe_path(filename), "a") as f:
                        f.write("\n" + data)
                    success("Content appended successfully!")

        else:  # Overwrite
            current = safe_path(filename).read_text()
            data = st.text_area("New content (replaces everything)", value=current, height=160)
            if st.button("Overwrite File"):
                safe_path(filename).write_text(data)
                success("File overwritten successfully!")

# ── DELETE ────────────────────────────────────────────────────────────────────
elif op == "Delete":
    files = list_files()
    if not files:
        info("No files to delete.")
    else:
        filename = st.selectbox("Select a file to delete", files)
        st.markdown(
            f'<div class="msg-error" style="margin-top:.6rem">⚠ This will permanently delete <b>{filename}</b>. This cannot be undone.</div>',
            unsafe_allow_html=True,
        )
        confirm = st.checkbox(f'I understand — delete "{filename}"')
        if st.button("Delete File"):
            if not confirm:
                error("Please check the confirmation box first.")
            else:
                safe_path(filename).unlink()
                success(f"'{filename}' deleted successfully!")
                st.rerun()

st.markdown("</div>", unsafe_allow_html=True)  # close .panel

# ─── File List Sidebar ─────────────────────────────────────────────────────────
files = list_files()
if files:
    with st.expander(f"📁  {len(files)} file{'s' if len(files)!=1 else ''} in workspace", expanded=False):
        for f in files:
            size = (BASE_DIR / f).stat().st_size
            st.markdown(
                f'<span style="font-family:Space Mono,monospace;font-size:.82rem;color:#888">📄 {f}'
                f'<span style="float:right;color:#555">{size} B</span></span><br>',
                unsafe_allow_html=True,
            )

# ─── Footer ───────────────────────────────────────────────────────────────────
st.markdown("""
<div class="footer">
    Built with ♥ using Python & Streamlit &nbsp;·&nbsp; FileForge
</div>
""", unsafe_allow_html=True)