import streamlit as st
import datetime
import plotly.graph_objects as go

st.set_page_config(
    page_title="ArthaSutra · Shivank Thakur",
    page_icon="◈",
    layout="wide",
    initial_sidebar_state="collapsed",
)

CURRENT_YEAR = datetime.datetime.now().year

# ── SESSION STATE ─────────────────────────────────────────────────────────────
if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = True
if "show_all_projects" not in st.session_state:
    st.session_state.show_all_projects = False

DM = st.session_state.dark_mode

# ── THEME VARIABLES ───────────────────────────────────────────────────────────
if DM:
    BG          = "#0a0a0c"
    BG_CARD     = "#131316"
    BG_CARD2    = "#1a1a1f"
    TEXT        = "#f5f4f2"
    TEXT_MID    = "rgba(245,244,242,0.62)"
    TEXT_DIM    = "rgba(245,244,242,0.38)"
    RULE        = "rgba(255,255,255,0.08)"
    NAV_BG      = "rgba(10,10,12,0.88)"
    STRIPE      = "rgba(224,52,42,0.03)"
    BADGE_BG    = "rgba(224,52,42,0.1)"
else:
    BG          = "#f8f7f4"
    BG_CARD     = "#ffffff"
    BG_CARD2    = "#f0eeea"
    TEXT        = "#1a1814"
    TEXT_MID    = "rgba(26,24,20,0.65)"
    TEXT_DIM    = "rgba(26,24,20,0.42)"
    RULE        = "rgba(0,0,0,0.1)"
    NAV_BG      = "rgba(248,247,244,0.92)"
    STRIPE      = "rgba(224,52,42,0.025)"
    BADGE_BG    = "rgba(224,52,42,0.08)"

RED       = "#e0342a"
RED_DEEP  = "#a8241c"
RED_GLOW  = "rgba(224,52,42,0.18)"
GOLD      = "#c9a86a"

# ── CSS ───────────────────────────────────────────────────────────────────────
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,300;0,9..144,500;0,9..144,700;0,9..144,900;1,9..144,400;1,9..144,600&family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500;600&display=swap');

:root {{
    --bg:       {BG};
    --bg-card:  {BG_CARD};
    --bg-card2: {BG_CARD2};
    --text:     {TEXT};
    --text-mid: {TEXT_MID};
    --text-dim: {TEXT_DIM};
    --rule:     {RULE};
    --red:      {RED};
    --red-deep: {RED_DEEP};
    --red-glow: {RED_GLOW};
    --gold:     {GOLD};
    --serif:    'Fraunces', Georgia, serif;
    --sans:     'Inter', system-ui, sans-serif;
    --mono:     'JetBrains Mono', monospace;
}}

html, body, .stApp {{
    background: var(--bg) !important;
    font-family: var(--sans);
    color: var(--text);
    font-size: 16px;
    transition: background 0.35s ease, color 0.35s ease;
}}
#MainMenu, footer, header {{ visibility: hidden; }}
.block-container {{ padding: 0 !important; max-width: 100% !important; }}
[data-testid="stSidebar"] {{ display: none; }}
[data-testid="collapsedControl"] {{ display: none; }}

.stApp {{
    background-image: repeating-linear-gradient(
        135deg,
        {STRIPE} 0px, {STRIPE} 2px,
        transparent 2px, transparent 32px
    );
    background-attachment: fixed;
}}

::-webkit-scrollbar {{ width: 4px; }}
::-webkit-scrollbar-track {{ background: var(--bg); }}
::-webkit-scrollbar-thumb {{ background: var(--red); border-radius: 2px; }}

/* NAV */
.nav-bar {{
    position: sticky; top: 0; z-index: 999;
    background: {NAV_BG};
    backdrop-filter: blur(14px);
    border-bottom: 1px solid var(--rule);
    padding: 0 60px;
    display: flex; align-items: center; justify-content: space-between;
    height: 66px;
}}
.nav-logo {{
    font-family: var(--serif);
    font-size: 1.3rem; font-weight: 700; font-style: italic;
    color: var(--text); letter-spacing: 0.3px;
}}
.nav-logo span {{ color: var(--red); font-style: normal; font-weight: 900; }}
.nav-links {{ display: flex; gap: 6px; font-size: 0.83rem; font-weight: 500; }}
.nav-links a {{
    color: var(--text-dim); text-decoration: none;
    transition: all 0.2s; padding: 7px 14px; border-radius: 20px;
}}
.nav-links a:hover {{ color: var(--text); background: var(--rule); }}
.nav-cta {{
    font-size: 0.8rem; font-weight: 600; color: var(--bg);
    border: none; padding: 10px 22px; border-radius: 24px;
    background: var(--text); font-family: var(--sans);
    text-decoration: none; transition: all 0.2s; cursor: pointer;
    display: inline-block;
}}
.nav-cta:hover {{ background: var(--red); color: white; }}

/* HERO */
.hero-outer {{
    padding: 72px 60px 0;
    position: relative; overflow: hidden;
}}
.hero-eyebrow {{
    font-family: var(--mono); font-size: 0.78rem; color: var(--red);
    letter-spacing: 3px; text-transform: uppercase; margin-bottom: 20px;
    position: relative; z-index: 1;
}}
.hero-hello {{
    font-family: var(--serif); font-size: 1.3rem; font-weight: 400;
    color: var(--text-mid); margin-bottom: 6px; position: relative; z-index: 1;
}}
.hero-name {{
    font-family: var(--serif); font-size: 4rem; font-weight: 900;
    color: var(--text); line-height: 1.08; margin-bottom: 6px;
    position: relative; z-index: 1; letter-spacing: -1px;
}}
.hero-name em {{ color: var(--red); font-style: italic; font-weight: 500; }}
.hero-role {{
    font-family: var(--serif); font-size: 1.4rem; font-weight: 300;
    font-style: italic; color: var(--text-dim);
    margin-bottom: 24px; position: relative; z-index: 1;
}}
.hero-bio {{
    font-size: 1.02rem; color: var(--text-mid); line-height: 1.8;
    max-width: 460px; margin-bottom: 30px; position: relative; z-index: 1;
}}
.hero-pitch {{
    font-size: 0.88rem; color: var(--text-dim); line-height: 1.7;
    max-width: 460px; margin-bottom: 32px; position: relative; z-index: 1;
    border-left: 2px solid var(--red); padding-left: 14px;
    font-style: italic;
}}
.hero-btns {{ display: flex; gap: 12px; margin-bottom: 52px; position: relative; z-index: 1; flex-wrap: wrap; }}
.btn-primary {{
    display: inline-block; font-family: var(--sans); font-weight: 600;
    font-size: 0.9rem; color: #fff; background: var(--red);
    padding: 13px 28px; border-radius: 28px; text-decoration: none; transition: all 0.2s;
}}
.btn-primary:hover {{ background: var(--red-deep); transform: translateY(-2px); box-shadow: 0 8px 24px var(--red-glow); }}
.btn-secondary {{
    display: inline-block; font-family: var(--sans); font-weight: 500;
    font-size: 0.9rem; color: var(--text); background: transparent;
    padding: 13px 28px; border-radius: 28px; text-decoration: none;
    border: 1px solid var(--rule); transition: all 0.2s;
}}
.btn-secondary:hover {{ border-color: var(--red); color: var(--red); }}

/* BLOB PHOTO + DATA ART */
.photo-zone {{ position: relative; width: 100%; max-width: 360px; margin: 0 auto; }}

/* Data art SVG decorations around the blob */
.data-art {{
    position: absolute; inset: -40px; pointer-events: none; z-index: 0;
    opacity: {'0.55' if DM else '0.35'};
}}

.blob-shape {{
    width: 100%; aspect-ratio: 1/1.08;
    background: var(--red);
    border-radius: 42% 58% 65% 35% / 50% 45% 55% 50%;
    position: absolute; inset: 0;
    transform: scale(1.07) translate(5%, 5%);
    opacity: 0.88; filter: blur(0.5px);
}}
.blob-photo {{
    width: 100%; aspect-ratio: 1/1.08; object-fit: cover;
    border-radius: 42% 58% 65% 35% / 50% 45% 55% 50%;
    position: relative; z-index: 1;
    border: 2px solid var(--rule);
}}

/* STAT ROW */
.stat-row {{
    display: flex; border-top: 1px solid var(--rule);
    position: relative; z-index: 1;
}}
.stat-block {{ flex: 1; padding: 26px 8px 26px 0; border-right: 1px solid var(--rule); }}
.stat-block:last-child {{ border-right: none; }}
.stat-num {{
    font-family: var(--serif); font-size: 1.9rem; font-weight: 800;
    color: var(--text); margin-bottom: 4px;
}}
.stat-num span {{ color: var(--red); }}
.stat-label {{ font-size: 0.76rem; color: var(--text-dim); line-height: 1.4; }}

/* MARQUEE TICKER */
.ticker-wrap {{
    overflow: hidden; border-top: 1px solid var(--rule);
    border-bottom: 1px solid var(--rule);
    background: var(--bg-card); padding: 14px 0;
}}
.ticker-track {{
    display: flex; gap: 0; white-space: nowrap;
    animation: ticker 28s linear infinite;
}}
.ticker-item {{
    font-family: var(--mono); font-size: 0.78rem; color: var(--text-dim);
    letter-spacing: 2px; padding: 0 36px;
}}
.ticker-item span {{ color: var(--red); margin-right: 12px; }}
@keyframes ticker {{ 0% {{ transform: translateX(0); }} 100% {{ transform: translateX(-50%); }} }}

/* SECTION BASE */
.section {{ padding: 60px 60px; }}
.section-alt {{ background: var(--bg-card); }}
.section-divider {{
    height: 1px;
    background: linear-gradient(90deg, transparent, var(--rule) 15%, var(--rule) 85%, transparent);
}}
.section-label {{
    font-family: var(--mono); font-size: 0.76rem; color: var(--red);
    letter-spacing: 3px; text-transform: uppercase; margin-bottom: 10px;
}}
.section-heading {{
    font-family: var(--serif); font-size: 2.6rem; font-weight: 800;
    color: var(--text); margin-bottom: 10px; letter-spacing: -0.5px;
}}
.section-sub {{ font-size: 1rem; color: var(--text-dim); margin-bottom: 44px; line-height: 1.6; max-width: 640px; }}

/* 01/02/03 EDITORIAL PROJECT LAYOUT */
.proj-editorial {{
    display: grid; grid-template-columns: 80px 1fr 1fr;
    gap: 0 48px; padding: 52px 0;
    border-bottom: 1px solid var(--rule);
    align-items: start;
}}
.proj-editorial:first-child {{ padding-top: 0; }}
.proj-editorial:last-child {{ border-bottom: none; }}
.proj-num {{
    font-family: var(--serif); font-size: 3.5rem; font-weight: 900;
    color: var(--rule); line-height: 1; padding-top: 4px;
    transition: color 0.2s;
}}
.proj-editorial:hover .proj-num {{ color: var(--red); }}
.proj-meta {{ position: relative; }}
.proj-eyebrow {{
    font-family: var(--mono); font-size: 0.72rem; color: var(--red);
    letter-spacing: 2px; margin-bottom: 14px;
}}
.proj-title-big {{
    font-family: var(--serif); font-size: 1.8rem; font-weight: 800;
    color: var(--text); line-height: 1.2; margin-bottom: 14px;
}}
.proj-desc-big {{
    font-size: 0.96rem; color: var(--text-mid); line-height: 1.8;
    margin-bottom: 20px;
}}
.proj-features {{
    font-size: 0.84rem; color: var(--text-dim); line-height: 1.7;
    margin-bottom: 22px; font-style: italic;
    border-left: 2px solid var(--rule); padding-left: 12px;
}}
.proj-stack {{ display: flex; flex-wrap: wrap; gap: 7px; margin-bottom: 22px; }}
.proj-tag {{
    font-family: var(--mono); font-size: 0.7rem; color: var(--text-mid);
    background: var(--bg-card2); border: 1px solid var(--rule);
    padding: 4px 11px; border-radius: 5px;
}}
.proj-actions {{ display: flex; gap: 12px; align-items: center; flex-wrap: wrap; margin-bottom: 16px; }}
.proj-link {{
    display: inline-block; font-family: var(--mono); font-size: 0.78rem;
    color: var(--red); text-decoration: none;
    border: 1px solid rgba(224,52,42,0.35); padding: 8px 18px; border-radius: 6px;
    transition: all 0.2s;
}}
.proj-link:hover {{ background: var(--red); color: white; }}
.proj-img-col {{ position: relative; }}
.proj-collage {{
    display: grid; grid-template-columns: 1fr 1fr; gap: 8px; border-radius: 12px; overflow: hidden;
}}
.proj-collage img {{
    width: 100%; aspect-ratio: 4/3; object-fit: cover; border-radius: 6px;
    transition: transform 0.3s ease;
}}
.proj-collage img:hover {{ transform: scale(1.04); }}
.proj-collage-single img {{
    width: 100%; border-radius: 12px; object-fit: cover;
}}

/* STATUS BADGES */
.status-badge {{
    font-family: var(--mono); font-size: 0.7rem; font-weight: 500;
    padding: 4px 12px; border-radius: 20px; letter-spacing: 1px;
    display: inline-flex; align-items: center; gap: 5px;
}}
.status-badge::before {{ content: ''; width: 6px; height: 6px; border-radius: 50%; display: inline-block; }}
.status-live    {{ background: rgba(34,197,94,0.12); color: #4ade80; border: 1px solid rgba(74,222,128,0.3); }}
.status-live::before    {{ background: #4ade80; }}
.status-wip     {{ background: rgba(234,179,8,0.12); color: #facc15; border: 1px solid rgba(250,204,21,0.3); }}
.status-wip::before     {{ background: #facc15; }}
.status-planned {{ background: rgba(224,52,42,0.1); color: var(--red); border: 1px solid rgba(224,52,42,0.3); }}
.status-planned::before {{ background: var(--red); }}

/* MINOR PROJECTS GRID */
.minor-grid {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; }}
.minor-card {{
    background: var(--bg-card2); border: 1px dashed var(--rule);
    border-radius: 12px; padding: 24px 22px; transition: all 0.2s;
}}
.minor-card:hover {{ border-color: rgba(224,52,42,0.3); background: var(--bg-card); }}
.minor-eyebrow {{ font-family: var(--mono); font-size: 0.68rem; color: var(--text-dim); letter-spacing: 1.5px; margin-bottom: 10px; }}
.minor-title {{ font-family: var(--serif); font-size: 1.05rem; font-weight: 700; color: var(--text-mid); margin-bottom: 8px; line-height: 1.3; }}
.minor-desc {{ font-size: 0.82rem; color: var(--text-dim); line-height: 1.65; margin-bottom: 14px; }}
.minor-stack {{ display: flex; flex-wrap: wrap; gap: 6px; margin-bottom: 14px; }}
.minor-tag {{ font-family: var(--mono); font-size: 0.66rem; color: var(--text-dim); background: var(--bg-card); border: 1px solid var(--rule); padding: 3px 9px; border-radius: 4px; }}
.minor-footer {{ display: flex; align-items: center; justify-content: space-between; padding-top: 12px; border-top: 1px solid var(--rule); }}
.minor-cat {{ font-size: 0.7rem; color: var(--text-dim); font-family: var(--mono); }}

/* SKILLS */
.skills-grid {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 18px; }}
.skill-block {{
    background: var(--bg-card); border: 1px solid var(--rule); border-radius: 14px;
    padding: 28px 24px; transition: all 0.2s;
}}
.skill-block:hover {{ border-color: rgba(224,52,42,0.3); }}
.skill-block-title {{
    font-family: var(--mono); font-size: 0.74rem; color: var(--red);
    letter-spacing: 2px; text-transform: uppercase; margin-bottom: 16px;
}}
.skill-pills {{ display: flex; flex-wrap: wrap; gap: 8px; }}
.skill-pill {{
    font-size: 0.85rem; color: var(--text-mid);
    background: var(--bg-card2); border: 1px solid var(--rule);
    border-radius: 7px; padding: 7px 14px; font-weight: 500; transition: all 0.2s;
}}
.skill-pill:hover {{ border-color: var(--red); color: var(--red); background: rgba(224,52,42,0.06); }}

/* CASE STUDIES */
.consult-card {{
    display: grid; grid-template-columns: 160px 1fr;
    border: 1px solid var(--rule); border-radius: 14px;
    overflow: hidden; background: var(--bg-card); transition: all 0.22s;
    margin-bottom: 20px;
}}
.consult-card:hover {{ border-color: rgba(224,52,42,0.3); box-shadow: 0 8px 32px var(--red-glow); }}
.consult-card.placeholder {{ border-style: dashed; background: var(--bg-card2); }}
.consult-img {{ background-size: cover; background-position: center; min-height: 100%; position: relative; }}
.consult-img::after {{ content: ''; position: absolute; inset: 0; background: linear-gradient(180deg, rgba(224,52,42,0.08), rgba(10,10,12,0.45)); }}
.consult-body {{ padding: 26px 28px; }}
.consult-tag {{ font-family: var(--mono); font-size: 0.7rem; color: var(--red); letter-spacing: 2px; margin-bottom: 10px; }}
.consult-title {{ font-family: var(--serif); font-size: 1.15rem; font-weight: 800; color: var(--text); margin-bottom: 12px; line-height: 1.35; }}
.consult-del {{ font-size: 0.84rem; color: var(--text-dim); padding: 5px 0; border-bottom: 1px solid var(--rule); }}
.consult-del:last-of-type {{ border-bottom: none; }}

/* ILLUSTRATION SECTION */
.illus-grid {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 20px; }}
.illus-card {{
    background: var(--bg-card); border: 1px solid var(--rule); border-radius: 12px;
    overflow: hidden; transition: all 0.2s;
}}
.illus-card:hover {{ transform: translateY(-4px); box-shadow: 0 12px 36px var(--red-glow); border-color: rgba(224,52,42,0.3); }}
.illus-card img {{ width: 100%; aspect-ratio: 1/1; object-fit: cover; }}
.illus-cap {{ padding: 12px 14px; font-size: 0.78rem; color: var(--text-dim); font-family: var(--mono); }}

/* MOSAIC CLOSING GRID */
.mosaic-grid {{
    display: grid; grid-template-columns: repeat(4, 1fr); gap: 0;
    height: 280px;
}}
.mosaic-cell {{ overflow: hidden; }}
.mosaic-cell img {{ width: 100%; height: 100%; object-fit: cover; filter: brightness(0.75) saturate(0.8); transition: all 0.3s; }}
.mosaic-cell:hover img {{ filter: brightness(1) saturate(1); transform: scale(1.05); }}

/* CONTACT */
.contact-wrap {{
    padding: 80px 60px; text-align: center;
    background: #0a0a0c; position: relative; overflow: hidden;
}}
.contact-wrap::before {{
    content: ''; position: absolute; inset: 0;
    background-image: repeating-linear-gradient(135deg, rgba(224,52,42,0.07) 0px, rgba(224,52,42,0.07) 2px, transparent 2px, transparent 30px);
}}
.contact-inner {{ position: relative; z-index: 1; }}
.contact-heading {{ font-family: var(--serif); font-size: 2.8rem; font-weight: 900; color: #f5f4f2; margin-bottom: 14px; }}
.contact-sub {{ font-size: 1rem; color: rgba(245,244,242,0.5); margin-bottom: 8px; font-style: italic; font-family: var(--serif); }}
.contact-cta {{ font-size: 0.84rem; color: rgba(245,244,242,0.35); margin-bottom: 36px; font-family: var(--mono); line-height: 1.6; max-width: 520px; margin-left: auto; margin-right: auto; }}
.contact-links {{ display: flex; gap: 12px; justify-content: center; flex-wrap: wrap; }}
.contact-link {{
    display: inline-block; font-family: var(--mono); font-size: 0.84rem;
    color: var(--red); background: rgba(224,52,42,0.08);
    border: 1px solid rgba(224,52,42,0.3); padding: 11px 24px;
    border-radius: 8px; text-decoration: none; transition: all 0.2s;
}}
.contact-link:hover {{ background: var(--red); color: white; }}

/* FOOTER */
.footer {{
    padding: 20px 60px; border-top: 1px solid rgba(255,255,255,0.06);
    display: flex; justify-content: space-between; align-items: center;
    background: #0a0a0c;
}}
.footer-left {{ font-family: var(--mono); font-size: 0.72rem; color: rgba(255,255,255,0.25); letter-spacing: 1px; }}
.footer-right {{ font-family: var(--serif); font-size: 0.82rem; color: rgba(255,255,255,0.2); font-style: italic; }}

/* STREAMLIT WIDGET OVERRIDES */
.stButton > button {{
    background: var(--red) !important; color: white !important; border: none !important;
    border-radius: 8px !important; font-family: var(--mono) !important;
    font-size: 0.8rem !important; font-weight: 500 !important;
    letter-spacing: 1px !important; padding: 0.6rem 1.4rem !important;
    transition: all 0.2s !important;
}}
.stButton > button:hover {{ background: var(--red-deep) !important; }}
.stSelectbox label {{ font-family: var(--mono) !important; color: var(--text-mid) !important; font-size: 0.8rem !important; }}

/* METHODOLOGY EXPANDER */
.streamlit-expanderHeader {{
    font-family: var(--mono) !important; font-size: 0.78rem !important;
    color: var(--red) !important; letter-spacing: 1.5px !important;
}}

@media (max-width: 960px) {{
    .nav-bar, .hero-outer, .section, .contact-wrap, .footer {{ padding-left: 24px !important; padding-right: 24px !important; }}
    .hero-name {{ font-size: 2.6rem; }}
    .proj-editorial {{ grid-template-columns: 60px 1fr; }}
    .proj-img-col {{ display: none; }}
    .minor-grid, .skills-grid {{ grid-template-columns: 1fr; }}
    .illus-grid {{ grid-template-columns: repeat(2,1fr); }}
    .consult-card {{ grid-template-columns: 1fr; }}
    .consult-img {{ min-height: 140px; }}
    .mosaic-grid {{ grid-template-columns: repeat(2,1fr); }}
}}
</style>
""", unsafe_allow_html=True)

# ── DATA ──────────────────────────────────────────────────────────────────────

MAJOR_PROJECTS = [
    {
        "num": "01",
        "title": "Artha_AI — Intelligent Macroeconomic Forecasting & RAG Agent",
        "category": "AI + Economics · LLM Systems",
        "status": "live",
        "status_label": "Live · Phase 2+3",
        "desc": "An AI-powered economic forecasting engine combining deep statistical time-series models with a Retrieval-Augmented Generation pipeline. Trains on 147 months of real MoSPI CPI data (Jan 2013–Mar 2025), compares four forecasting approaches (Linear AR, ARIMA, Prophet, XGBoost) with honest accuracy metrics, then retrieves actual RBI policy statement text via semantic search to generate verifiably grounded inflation explanations — with an automated groundedness checker that verifies every number in the answer against source material.",
        "features": "4-model forecast comparison (Linear AR · ARIMA · Prophet · XGBoost) · ChromaDB semantic search over real RBI policy statements · Automated groundedness verification · Stationary % change series (non-stationary index avoided) · Chronological train/test split — zero data leakage · 80MB sentence-transformer for free-tier hosting · TF-IDF fallback when embeddings unavailable",
        "pitch": "The core insight: asking an LLM to explain inflation from general knowledge risks confident, invented claims in a domain where that is genuinely harmful. Instead, the system retrieves actual RBI policy text first, constrains the explanation to that text plus computed forecast numbers, then verifies its own output — catching two real numeric-tolerance bugs in testing before deployment. That combination — useful and verifiably honest — is the more important engineering lesson beyond any individual model's accuracy.",
        "stack": ["Python", "Streamlit", "Pandas", "statsmodels", "Prophet", "XGBoost", "ChromaDB", "sentence-transformers", "Google Gemini API", "Plotly", "scikit-learn"],
        "link": None,
        "images": [
            "https://images.unsplash.com/photo-1611974789855-9c2a0a7236a3?w=400&q=80",
            "https://images.unsplash.com/photo-1518186285589-2f7649de83e0?w=400&q=80",
            "https://images.unsplash.com/photo-1551288049-bebda4e38f71?w=400&q=80",
            "https://images.unsplash.com/photo-1460925895917-afdab827c52f?w=400&q=80",
        ],
        "methodology": "The forecasting core uses month-over-month % change in CPI — not the raw index — because the raw series is non-stationary (trending upward), violating the core assumption behind ARIMA. Differencing to % change brings it statistically closer to stationary, verified by the same logic an Augmented Dickey-Fuller test would formalize. Four models are compared rather than choosing one upfront because each has a distinct known blind spot: linear AR (only linear relationships), ARIMA (no nonlinear interactions), Prophet (weak on sharp shocks), XGBoost (no built-in trend/seasonality). Complexity has to earn its keep against a simple baseline — not be assumed superior.",
        "globe": False,
    },
    {
        "num": "02",
        "title": "GeoSphere India",
        "category": "Software Engineering · Earth Science",
        "status": "live",
        "status_label": "Live",
        "desc": "A 21-module interactive Earth Science intelligence platform built on the BHU NEP 4-year syllabus — the most complete single-file project here (~3,800 lines). Covers the complete undergraduate curriculum: mineralogy, petrology, structural geology, stratigraphy, geomorphology, Indian rivers, oceanography, earthquake monitoring, economic geology, and more. Live USGS earthquake data, Wikipedia photo API, Gemini AI integration with 60+ topic fallback, and a field diary capturing the lived experience of geology at BHU.",
        "features": "Interactive 3D Tectonic Globe · 20 fully functional modules with live data · Multi-Module Earth Science Intelligence Engine · Flawless Mobile-Optimized Dashboard Design · Live USGS M4.5+ earthquake feed · Wikipedia REST API photos · Gemini AI geology Q&A · BHU NEP syllabus alignment across all 8 semesters",
        "pitch": "I handled the system architecture, data modeling, UX design, and module integration across 21 independent sections — leveraging AI to accelerate generation and debugging of modular components while owning the full technical direction. Built by one student, using only free tools, in parallel with a full academic semester.",
        "stack": ["Python", "Streamlit", "Plotly", "USGS API", "Wikipedia REST API", "Google Gemini API", "Pandas", "Requests"],
        "link": "https://geosphere-india.streamlit.app/",
        "images": [
            "https://images.unsplash.com/photo-1614728263952-84ea256f9679?w=400&q=80",
            "https://images.unsplash.com/photo-1451187580459-43490279c0fa?w=400&q=80",
            "https://images.unsplash.com/photo-1579621970563-ebec7560ff3e?w=400&q=80",
            "https://images.unsplash.com/photo-1547722070-7e80e0509ee6?w=400&q=80",
        ],
        "methodology": None,
        "globe": True,
    },
    {
        "num": "03",
        "title": "Resume Optimizer AI",
        "category": "Prompt Engineering · LLM Systems",
        "status": "live",
        "status_label": "Live",
        "desc": "A single structured prompt that acts simultaneously as an ATS compatibility scorer, senior FAANG recruiter critic, and resume rewriter — powered by Gemini 2.5 Flash. The anti-fabrication guardrail forces the model to write [X%] instead of inventing metrics, mirroring the same epistemic discipline required in statistical research.",
        "features": "Single-call structured JSON output · Anti-hallucination bracket guardrail · PDF/DOCX/TXT parsing · ATS score + job-match score + bullet rewrites in one pass",
        "pitch": None,
        "stack": ["Python", "Gemini 2.5 Flash", "Streamlit", "pdfplumber", "python-docx", "Google GenAI SDK"],
        "link": "https://shivank-resume-optimiser.streamlit.app/",
        "images": [
            "https://images.unsplash.com/photo-1586281380349-632531db7ed4?w=400&q=80",
            "https://images.unsplash.com/photo-1467232004584-a241de8bcf5d?w=400&q=80",
        ],
        "methodology": "This project isn't about data analysis — it's about precision under constraints. Getting a language model to reliably return structured, valid JSON every single time requires the same discipline an economist needs when designing a survey instrument: anticipate every edge case before it happens. The anti-fabrication rule mirrors a core research ethic: never let a model silently fill gaps with invented data.",
        "globe": False,
    },
    {
        "num": "04",
        "title": "Online vs. Offline Learning",
        "category": "Research & Statistics · BHU Thesis",
        "status": "live",
        "status_label": "Published",
        "desc": "B.Sc. (Hons.) Statistics undergraduate thesis at Banaras Hindu University. Primary survey of 110 students examining how learning mode affects GPA, stress, sleep, and screen time. Uses correlation analysis, Chi-Square testing, and multiple linear regression. Offline learners show highest GPA (8.36) and lowest stress (9.3/20).",
        "features": "110-respondent primary survey · Chi-Square + regression + correlation · Self-selection bias explicitly acknowledged · Educational analytics",
        "pitch": None,
        "stack": ["Excel", "Pivot Tables", "Chi-Square Test", "Multiple Regression", "Google Forms"],
        "link": None,
        "images": [
            "https://images.unsplash.com/photo-1456513080510-7bf3a84b82f8?w=400&q=80",
            "https://images.unsplash.com/photo-1434030216411-0b793f4b4173?w=400&q=80",
        ],
        "methodology": "The data shows offline learners have the highest GPA and lowest stress — but this correlation has a hidden problem: students don't randomly choose their learning mode. Disciplined, motivated students may self-select offline, and those same traits also produce better grades. A true causal test would require randomly assigned groups — nearly impossible in education research. That limitation is worth naming explicitly.",
        "globe": False,
    },
]

MINOR_PROJECTS = [
    {
        "num": "05", "title": "SmartCalc Pro",
        "category": "Desktop Application",
        "status": "live", "status_label": "Live",
        "desc": "A fully-featured desktop calculator with 5 tabs — Basic, Scientific, Statistics, Finance/Economics (EMI, CAGR, compound interest, inflation adjustment), and Utility. Calculation logic fully separated from GUI — every function independently testable.",
        "stack": ["Python", "Tkinter", "Standard Library"],
    },
    {
        "num": "06", "title": "Women Literacy Prediction",
        "category": "Machine Learning",
        "status": "wip", "status_label": "Upgrading",
        "desc": "ML dashboard classifying 706 Indian districts by women's literacy using NFHS-5 data and 109 socio-economic indicators. Random Forest achieves 82.4% accuracy; malnutrition emerges as the top predictor.",
        "stack": ["Python", "Scikit-learn", "Pandas", "Streamlit", "Matplotlib", "Seaborn"],
    },
    {
        "num": "07", "title": "Indian Banking Credit Dashboard",
        "category": "Business Analytics",
        "status": "wip", "status_label": "Working On",
        "desc": "Analytics dashboard covering credit growth, NPA trends, priority sector lending, CASA ratios, and digital banking adoption across Indian public and private sector banks using RBI data.",
        "stack": ["Python", "SQL", "Power BI", "Pandas", "Plotly"],
    },
    {
        "num": "08", "title": "Varanasi House Price Intelligence",
        "category": "ML + Web App",
        "status": "live", "status_label": "Live",
        "desc": "Flet web app that loads a CSV, filters for Varanasi, trains a Linear Regression model, and lets you predict property prices with a full form UI. Shows actual vs. predicted scatter and feature coefficient charts.",
        "stack": ["Python", "Flet", "Scikit-learn", "Matplotlib", "Pandas"],
    },
]

SKILLS = {
    "Programming": ["Python", "SQL"],
    "Data Analysis": ["Advanced Excel", "Pandas", "NumPy"],
    "ML & AI": ["Regression", "Scikit-learn", "LangChain", "ARIMA", "XGBoost"],
    "Visualization": ["Streamlit", "Plotly", "Matplotlib", "Seaborn"],
    "Development": ["Git", "GitHub", "Flet", "Tkinter"],
    "Research": ["Survey Design", "Chi-Square", "Statistical Inference"],
}

CONSULTING_CASES = [
    {
        "tag": "CASE 01 · EDUCATION POLICY",
        "title": "Why Do Government Schools Underperform in India?",
        "deliverables": [
            "MECE Issue Tree decomposing demand, supply, and governance branches",
            "5-Why drill-down identifying RTE 2009 as structural root cause",
            "Mincer equation model: USD 1.3T economic cost of learning poverty",
            "Punjab–UP paradox benchmarking: pedagogy > infrastructure compliance",
            "Cost-benefit analysis: FLN reform delivers 469x ROI vs ~1x for infra spend",
            "100-day district pilot roadmap with Go/No-Go decision gate",
        ],
        "status": "wip", "status_label": "Working On",
        "image": "https://images.unsplash.com/photo-1497633762265-9d179a990aa6?w=400&q=80",
        "placeholder": False,
    },
    {
        "tag": "CASE 02 · RESERVED",
        "title": "Coming Soon",
        "deliverables": [],
        "status": "planned", "status_label": "Coming Soon",
        "image": None, "placeholder": True,
        "note": "Currently scoping the problem. Details to follow.",
    },
    {
        "tag": "CASE 03 · RESERVED",
        "title": "Coming Soon",
        "deliverables": [],
        "status": "planned", "status_label": "Coming Soon",
        "image": None, "placeholder": True,
        "note": "Currently scoping the problem. Details to follow.",
    },
]

ILLUSTRATIONS = [
    ("https://images.unsplash.com/photo-1551288049-bebda4e38f71?w=400&q=80", "Data Analysis"),
    ("https://images.unsplash.com/photo-1460925895917-afdab827c52f?w=400&q=80", "Economics"),
    ("https://images.unsplash.com/photo-1504868584819-f8e8b4b6d7e3?w=400&q=80", "ML Models"),
    ("https://images.unsplash.com/photo-1543286386-2e659306cd6c?w=400&q=80", "Statistics"),
]

status_class = {"live": "status-live", "wip": "status-wip", "planned": "status-planned"}

ECONOMIC_TITLES = {"Online vs. Offline Learning", "Women Literacy Prediction"}

PHOTO_B64 = "iVBORw0KGgoAAAANSUhEUgAAAQAAAAENCAIAAABvjizvAAAACXBIWXMAAA7EAAAOxAGVKw4bAAAFUGlUWHRYTUw6Y29tLmFkb2JlLnhtcAAAAAAAPD94cGFja2V0IGJlZ2luPSfvu78nIGlkPSdXNU0wTXBDZWhpSHpyZVN6TlRjemtjOWQnPz4KPHg6eG1wbWV0YSB4bWxuczp4PSdhZG9iZTpuczptZXRhLyc+CjxyZGY6UkRGIHhtbG5zOnJkZj0naHR0cDovL3d3dy53My5vcmcvMTk5OS8wMi8yMi1yZGYtc3ludGF4LW5zIyc+CgogPHJkZjpEZXNjcmlwdGlvbiByZGY6YWJvdXQ9JycKICB4bWxuczpBdHRyaWI9J2h0dHA6Ly9ucy5hdHRyaWJ1dGlvbi5jb20vYWRzLzEuMC8nPgogIDxBdHRyaWI6QWRzPgogICA8cmRmOlNlcT4KICAgIDxyZGY6bGkgcmRmOnBhcnNlVHlwZT0nUmVzb3VyY2UnPgogICAgIDxBdHRyaWI6Q3JlYXRlZD4yMDI2LTA2LTI5PC9BdHRyaWI6Q3JlYXRlZD4KICAgICA8QXR0cmliOkRhdGE+eyZxdW90O2RvYyZxdW90OzomcXVvdDtEQUhOOFNPZjhSOCZxdW90OywmcXVvdDt1c2VyJnF1b3Q7OiZxdW90O1VBRkxuSVFhNVo0JnF1b3Q7LCZxdW90O2JyYW5kJnF1b3Q7OiZxdW90O0JBRkxuSGxZc0F3JnF1b3Q7fTwvQXR0cmliOkRhdGE+CiAgICAgPEF0dHJpYjpFeHRJZD44Y2Q3MDY1Zi04YzlhLTQyNDAtYjk5NC03MTA2ZDZhYTI2MmY8L0F0dHJpYjpFeHRJZD4KICAgICA8QXR0cmliOkZiSWQ+NTI1MjY1OTE0MTc5NTgwPC9BdHRyaWI6RmJJZD4KICAgICA8QXR0cmliOlRvdWNoVHlwZT4yPC9BdHRyaWI6VG91Y2hUeXBlPgogICAgPC9yZGY6bGk+CiAgIDwvcmRmOlNlcT4KICA8L0F0dHJpYjpBZHM+CiA8L3JkZjpEZXNjcmlwdGlvbj4KCiA8cmRmOkRlc2NyaXB0aW9uIHJkZjphYm91dD0nJwogIHhtbG5zOmRjPSdodHRwOi8vcHVybC5vcmcvZGMvZWxlbWVudHMvMS4x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"

# ── NAV ───────────────────────────────────────────────────────────────────────
mode_icon = "☀️" if DM else "🌙"
col_nav1, col_nav2 = st.columns([10, 1])
with col_nav1:
    st.markdown(f"""
    <div class='nav-bar'>
        <div class='nav-logo'>Artha<span>Sutra</span></div>
        <div class='nav-links'>
            <a href='#projects'>Flagship Projects</a>
            <a href='#lab'>Experiments</a>
            <a href='#skills'>Skills</a>
            <a href='#deep-dives'>Deep Dives</a>
            <a href='#contact'>Contact</a>
        </div>
        <a class='nav-cta' href='#contact'>Get in touch</a>
    </div>
    """, unsafe_allow_html=True)
with col_nav2:
    if st.button(mode_icon, key="theme_toggle"):
        st.session_state.dark_mode = not st.session_state.dark_mode
        st.rerun()

# ── HERO ──────────────────────────────────────────────────────────────────────
st.markdown("<div class='hero-outer'>", unsafe_allow_html=True)

h_col1, h_col2 = st.columns([1.5, 1])

with h_col1:
    st.markdown(f"""
    <div class='hero-eyebrow'>◈ Portfolio · Data &amp; Statistics</div>
    <div class='hero-hello'>Hello, I'm</div>
    <div class='hero-name'>Shivank <em>Thakur</em></div>
    <div class='hero-role'>Statistics, data, and decisions</div>
    <div class='hero-bio'>
        I build tools that turn raw data into decisions — geospatial dashboards, 
        statistical research, and machine learning models grounded in real-world 
        Indian datasets. The <strong>ultimate trifecta: rigorous statistical theory, 
        high-level economic frameworking, and modern data-engineering skills.</strong>
    </div>
    <div class='hero-pitch'>
        B.Sc. (Hons.) Statistics · Banaras Hindu University<br/>
        Incoming M.Sc. Economics · IIT Kanpur
    </div>
    <div class='hero-btns'>
        <a class='btn-primary' href='#contact'>Let's Talk →</a>
        <a class='btn-secondary' href='#projects'>View Work ↓</a>
    </div>
    """, unsafe_allow_html=True)

with h_col2:
    # SVG data art around the blob
    svg_color = "rgba(224,52,42,0.6)" if DM else "rgba(224,52,42,0.4)"
    st.markdown(f"""
    <div class='photo-zone'>
        <svg class='data-art' viewBox='0 0 440 440' fill='none' xmlns='http://www.w3.org/2000/svg'>
            <!-- Scatter dots -->
            <circle cx='40' cy='80' r='3' fill='{svg_color}'/>
            <circle cx='60' cy='120' r='2' fill='{svg_color}'/>
            <circle cx='30' cy='160' r='4' fill='{svg_color}'/>
            <circle cx='55' cy='200' r='2' fill='{svg_color}'/>
            <circle cx='35' cy='240' r='3' fill='{svg_color}'/>
            <circle cx='400' cy='90' r='2' fill='{svg_color}'/>
            <circle cx='410' cy='130' r='3' fill='{svg_color}'/>
            <circle cx='395' cy='170' r='2' fill='{svg_color}'/>
            <circle cx='415' cy='210' r='4' fill='{svg_color}'/>
            <circle cx='60' cy='350' r='3' fill='{svg_color}'/>
            <circle cx='80' cy='390' r='2' fill='{svg_color}'/>
            <circle cx='380' cy='340' r='3' fill='{svg_color}'/>
            <circle cx='360' cy='380' r='2' fill='{svg_color}'/>
            <!-- Trend line top-left -->
            <polyline points='20,320 40,290 60,300 80,270 100,280 120,250' stroke='{svg_color}' stroke-width='1.5' fill='none' opacity='0.7'/>
            <!-- Bar chart bottom-right -->
            <rect x='330' y='360' width='12' height='40' fill='{svg_color}' opacity='0.5'/>
            <rect x='348' y='350' width='12' height='50' fill='{svg_color}' opacity='0.5'/>
            <rect x='366' y='340' width='12' height='60' fill='{svg_color}' opacity='0.5'/>
            <rect x='384' y='345' width='12' height='55' fill='{svg_color}' opacity='0.5'/>
            <!-- Axis lines -->
            <line x1='20' y1='400' x2='120' y2='400' stroke='{svg_color}' stroke-width='1' opacity='0.4'/>
            <line x1='20' y1='400' x2='20' y2='310' stroke='{svg_color}' stroke-width='1' opacity='0.4'/>
            <!-- Normal curve -->
            <path d='M 330,50 Q 350,20 370,50 Q 390,80 410,50' stroke='{svg_color}' stroke-width='1.5' fill='none' opacity='0.6'/>
            <!-- Small text labels -->
            <text x='22' y='78' fill='{svg_color}' font-size='8' opacity='0.5' font-family='monospace'>r=0.67</text>
            <text x='390' y='78' fill='{svg_color}' font-size='8' opacity='0.5' font-family='monospace'>82.4%</text>
            <text x='335' y='335' fill='{svg_color}' font-size='8' opacity='0.5' font-family='monospace'>MAPE</text>
            <text x='22' y='268' fill='{svg_color}' font-size='8' opacity='0.5' font-family='monospace'>CPI%</text>
        </svg>
        <div class='blob-shape'></div>
        <img class='blob-photo' src='data:image/png;base64,{PHOTO_B64}'/>
    </div>
    """, unsafe_allow_html=True)

    # Animated character video
    import os
    video_path = "hero_video.mp4"
    if os.path.exists(video_path):
        st.markdown("<div style='margin-top:20px;border-radius:14px;overflow:hidden;border:1px solid var(--rule);'>", unsafe_allow_html=True)
        st.video(video_path, autoplay=True, loop=True, muted=True)
        st.markdown("<div style='font-family:monospace;font-size:0.68rem;color:var(--text-dim);letter-spacing:2px;text-align:center;padding:6px 0;'>◈ DATA · STATISTICS · ML</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
st.markdown("""
<div class='stat-row'>
    <div class='stat-block'><div class='stat-num'><span>4</span>+</div><div class='stat-label'>Completed &amp; deployed projects</div></div>
    <div class='stat-block'><div class='stat-num'><span>21</span></div><div class='stat-label'>GeoSphere modules built</div></div>
    <div class='stat-block'><div class='stat-num'><span>706</span></div><div class='stat-label'>Districts analyzed, literacy model</div></div>
    <div class='stat-block'><div class='stat-num'><span>82.4<span style="font-size:1.2rem">%</span></span></div><div class='stat-label'>Random Forest accuracy, NFHS-5</div></div>
</div>
""", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)  # close hero-outer

# ── TICKER ───────────────────────────────────────────────────────────────────
items = ["Python", "Statistics", "Machine Learning", "Economics", "Streamlit", "LangChain", "ARIMA", "Plotly", "Data Science", "IIT Kanpur"]
ticker_html = "".join(f"<span class='ticker-item'><span>◈</span>{i}</span>" for i in items * 3)
st.markdown(f"<div class='ticker-wrap'><div class='ticker-track'>{ticker_html}</div></div>", unsafe_allow_html=True)

st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)

# ── FLAGSHIP PROJECTS ─────────────────────────────────────────────────────────
st.markdown("""
<div class='section' id='projects'>
    <div class='section-label'>◈ Flagship Projects</div>
    <div class='section-heading'>Completed Work</div>
    <div class='section-sub'>Four finished, deployed pieces of work — shown in editorial format with real descriptions drawn from the actual code.</div>
</div>
""", unsafe_allow_html=True)

st.markdown("<div style='padding: 0 60px;'>", unsafe_allow_html=True)

show_all = st.session_state.show_all_projects
projects_to_show = MAJOR_PROJECTS if show_all else MAJOR_PROJECTS[:3]

ECONOMIC_LOGIC_TITLES = {"Online vs. Offline Learning", "Women Literacy Prediction"}

for p in projects_to_show:
    imgs_html = ""
    if len(p["images"]) >= 4:
        imgs_html = f"""
        <div class='proj-collage'>
            <img src='{p["images"][0]}' alt='{p["title"]}'/>
            <img src='{p["images"][1]}' alt='{p["title"]}'/>
            <img src='{p["images"][2]}' alt='{p["title"]}'/>
            <img src='{p["images"][3]}' alt='{p["title"]}'/>
        </div>"""
    elif len(p["images"]) >= 2:
        imgs_html = f"""
        <div class='proj-collage'>
            <img src='{p["images"][0]}' alt='{p["title"]}'/>
            <img src='{p["images"][1]}' alt='{p["title"]}'/>
        </div>"""
    elif p["images"]:
        img0 = p["images"][0]
        ptitle = p["title"]
        imgs_html = f"<div class='proj-collage-single'><img src='{img0}' alt='{ptitle}'/></div>"

    stack_html = "".join(f"<span class='proj-tag'>{s}</span>" for s in p["stack"])
    link_html = f"<a class='proj-link' href='{p['link']}' target='_blank'>Visit project ↗</a>" if p.get("link") else ""
    pitch_html = f"<div class='proj-features'>{p['pitch']}</div>" if p.get("pitch") else ""

    if p.get("globe"):
        # GeoSphere: use 2-column layout with real Plotly globe
        col_meta, col_globe = st.columns([1, 1])
        with col_meta:
            st.markdown(f"""
            <div style='padding: 52px 0 52px;'>
                <div class='proj-eyebrow'>{p["num"]} &nbsp;·&nbsp; {p["category"]} &nbsp;·&nbsp; <span class='status-badge {status_class[p["status"]]}'>{p["status_label"]}</span></div>
                <div class='proj-title-big'>{p["title"]}</div>
                <div class='proj-desc-big'>{p["desc"]}</div>
                <div class='proj-features'>{p["features"]}</div>
                {pitch_html}
                <div class='proj-stack'>{stack_html}</div>
                <div class='proj-actions'>{link_html}</div>
            </div>
            """, unsafe_allow_html=True)
        with col_globe:
            bg_color = "#0a0a0c" if DM else "#f8f7f4"
            line_color = "rgba(224,52,42,0.6)"
            ocean_color = "#0d1b2a" if DM else "#cce4f5"
            land_color = "#1a2d1a" if DM else "#c8e6c9"
            fig_globe = go.Figure(go.Scattergeo(
                lon=[72.8, 77.2, 80.9, 88.3, 78.5, 76.9, 72.5, 68.0, 74.8, 85.3, 91.7, 93.9],
                lat=[18.9, 28.6, 13.1, 22.6, 17.4, 30.7, 23.0, 23.0, 32.7, 20.3, 26.2, 24.8],
                mode="markers",
                marker=dict(size=6, color=line_color, opacity=0.85, symbol="circle"),
                name="Seismic zones",
                hovertemplate="India seismic zone<extra></extra>",
            ))
            # India tectonic boundary line
            fig_globe.add_trace(go.Scattergeo(
                lon=[68, 77, 88, 97, 92, 80, 77, 72, 68],
                lat=[23, 35, 35, 28, 8, 8, 8, 20, 23],
                mode="lines",
                line=dict(width=1.5, color=line_color),
                name="India outline",
                hoverinfo="skip",
            ))
            fig_globe.update_layout(
                geo=dict(
                    projection_type="orthographic",
                    projection_rotation=dict(lon=80, lat=20, roll=0),
                    showland=True, landcolor=land_color,
                    showocean=True, oceancolor=ocean_color,
                    showlakes=False,
                    showcountries=True, countrycolor="rgba(255,255,255,0.1)",
                    showcoastlines=True, coastlinecolor="rgba(255,255,255,0.15)",
                    bgcolor=bg_color,
                ),
                paper_bgcolor=bg_color,
                plot_bgcolor=bg_color,
                margin=dict(l=0, r=0, t=0, b=0),
                height=360,
                showlegend=False,
            )
            st.plotly_chart(fig_globe, use_container_width=True, config={"scrollZoom": True, "displayModeBar": False})
        st.markdown("<div style='border-bottom:1px solid var(--rule);margin: 0 0 0 0;'></div>", unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class='proj-editorial'>
            <div class='proj-num'>{p["num"]}</div>
            <div class='proj-meta'>
                <div class='proj-eyebrow'>{p["category"]} &nbsp;·&nbsp; <span class='status-badge {status_class[p["status"]]}'>{p["status_label"]}</span></div>
                <div class='proj-title-big'>{p["title"]}</div>
                <div class='proj-desc-big'>{p["desc"]}</div>
                <div class='proj-features'>{p["features"]}</div>
                {pitch_html}
                <div class='proj-stack'>{stack_html}</div>
                <div class='proj-actions'>{link_html}</div>
            </div>
            <div class='proj-img-col'>{imgs_html}</div>
        </div>
        """, unsafe_allow_html=True)

    if p.get("methodology"):
        label = "🔬 Economic Thinking" if any(t in p["title"] for t in ECONOMIC_LOGIC_TITLES) else "💡 Why This Project Matters"
        with st.expander(label):
            st.markdown(p["methodology"])

if not show_all:
    st.markdown("<div style='margin-top:32px;'></div>", unsafe_allow_html=True)
    if st.button("See All Projects →", key="show_all_btn"):
        st.session_state.show_all_projects = True
        st.rerun()

st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)

# ── EXPERIMENTS & R&D ─────────────────────────────────────────────────────────
st.markdown("""
<div class='section section-alt' id='lab'>
    <div class='section-label'>◈ Experiments &amp; R&D</div>
    <div class='section-heading'>In the Lab</div>
    <div class='section-sub'>Earlier-stage work — shown for transparency, not polish. Always building.</div>
</div>
""", unsafe_allow_html=True)

st.markdown("<div style='padding: 0 60px 60px;background:var(--bg-card);'>", unsafe_allow_html=True)
st.markdown("<div class='minor-grid'>", unsafe_allow_html=True)
for p in MINOR_PROJECTS:
    stack_html = "".join(f"<span class='minor-tag'>{s}</span>" for s in p["stack"])
    st.markdown(f"""
    <div class='minor-card'>
        <div class='minor-eyebrow'>{p["num"]} · {p["category"]}</div>
        <div class='minor-title'>{p["title"]}</div>
        <div class='minor-desc'>{p["desc"]}</div>
        <div class='minor-stack'>{stack_html}</div>
        <div class='minor-footer'>
            <div class='minor-cat'>{p["category"]}</div>
            <div class='status-badge {status_class[p["status"]]}'>{p["status_label"]}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
st.markdown("</div></div>", unsafe_allow_html=True)

st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)

# ── ILLUSTRATIONS ─────────────────────────────────────────────────────────────
st.markdown("<div class='section'>", unsafe_allow_html=True)
st.markdown("<div class='illus-grid'>", unsafe_allow_html=True)
for img_url, cap in ILLUSTRATIONS:
    st.markdown(f"""
    <div class='illus-card'>
        <img src='{img_url}' alt='{cap}'/>
        <div class='illus-cap'>{cap}</div>
    </div>
    """, unsafe_allow_html=True)
st.markdown("</div></div>", unsafe_allow_html=True)

st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)

# ── SKILLS ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class='section' id='skills'>
    <div class='section-label'>◈ Toolkit</div>
    <div class='section-heading'>Skills</div>
    <div class='section-sub'>Grouped by what they're for — not where they'd sit on a resume.</div>
</div>
""", unsafe_allow_html=True)

st.markdown("<div style='padding: 0 60px 60px;'>", unsafe_allow_html=True)
skill_blocks = ""
for group, items in SKILLS.items():
    pills = "".join(f"<span class='skill-pill'>{s}</span>" for s in items)
    skill_blocks += f"<div class='skill-block'><div class='skill-block-title'>{group}</div><div class='skill-pills'>{pills}</div></div>"
st.markdown(f"<div class='skills-grid'>{skill_blocks}</div>", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)

# ── DEEP DIVES (CASE STUDIES) ─────────────────────────────────────────────────
st.markdown("""
<div class='section section-alt' id='deep-dives'>
    <div class='section-label'>◈ Deep Dives</div>
    <div class='section-heading'>Case Studies</div>
    <div class='section-sub'>Consulting-style research with structured frameworks, quantitative models, and implementation roadmaps.</div>
</div>
""", unsafe_allow_html=True)

st.markdown("<div style='padding: 0 60px 60px; background: var(--bg-card);'>", unsafe_allow_html=True)
for c in CONSULTING_CASES:
    if c["placeholder"]:
        st.markdown(f"""
        <div class='consult-card placeholder'>
            <div class='consult-img' style='background:var(--bg-card2);display:flex;align-items:center;justify-content:center;'>
                <span style='font-size:2rem;color:var(--rule);'>◈</span>
            </div>
            <div class='consult-body'>
                <div class='consult-tag'>{c["tag"]}</div>
                <div class='consult-title'>{c["title"]}</div>
                <div style='font-size:0.86rem;color:var(--text-dim);font-style:italic;'>{c["note"]}</div>
                <div style='margin-top:14px;'><span class='status-badge {status_class[c["status"]]}'>{c["status_label"]}</span></div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        dels = "".join(f"<div class='consult-del'>{d}</div>" for d in c["deliverables"])
        st.markdown(f"""
        <div class='consult-card'>
            <div class='consult-img' style='background-image:url("{c["image"]}");'></div>
            <div class='consult-body'>
                <div class='consult-tag'>{c["tag"]}</div>
                <div class='consult-title'>{c["title"]}</div>
                {dels}
                <div style='margin-top:14px;'><span class='status-badge {status_class[c["status"]]}'>{c["status_label"]}</span></div>
            </div>
        </div>
        """, unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)

# ── MOSAIC CLOSING GRID ───────────────────────────────────────────────────────
mosaic_imgs = [
    "https://images.unsplash.com/photo-1551288049-bebda4e38f71?w=600&q=80",
    "https://images.unsplash.com/photo-1614728263952-84ea256f9679?w=600&q=80",
    "https://images.unsplash.com/photo-1460925895917-afdab827c52f?w=600&q=80",
    "https://images.unsplash.com/photo-1504868584819-f8e8b4b6d7e3?w=600&q=80",
]
cells = "".join(f"<div class='mosaic-cell'><img src='{u}' alt='portfolio'/></div>" for u in mosaic_imgs)
st.markdown(f"<div class='mosaic-grid'>{cells}</div>", unsafe_allow_html=True)

# ── CONTACT ───────────────────────────────────────────────────────────────────
st.markdown("""
<div class='contact-wrap' id='contact'>
    <div class='contact-inner'>
        <div class='contact-heading'>Thanks for visiting.</div>
        <div class='contact-sub'>Open to Data Science, Economics, and Consulting opportunities.</div>
        <div class='contact-cta'>
            Looking for full-time roles and freelance consulting work in data science and applied economics.<br/>
            Available for coffee chats, project collaboration, or campus recruiting at IIT Kanpur.
        </div>
        <div class='contact-links'>
            <a class='contact-link' href='mailto:thakuryshivank143@gmail.com'>✉ Email</a>
            <a class='contact-link' href='https://github.com/shivank-byte/' target='_blank'>GitHub ↗</a>
            <a class='contact-link' href='https://www.linkedin.com/in/shivank-byte/' target='_blank'>LinkedIn ↗</a>
            <a class='contact-link' href='https://geosphere-india.streamlit.app/' target='_blank'>GeoSphere ↗</a>
            <a class='contact-link' href='https://shivank-resume-optimiser.streamlit.app/' target='_blank'>Resume AI ↗</a>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ── FOOTER ────────────────────────────────────────────────────────────────────
st.markdown(f"""
<div class='footer'>
    <div class='footer-left'>ARTHASUTRA · {CURRENT_YEAR}</div>
    <div class='footer-right'>Designed &amp; built by Shivank Thakur</div>
</div>
""", unsafe_allow_html=True)
