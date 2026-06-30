import streamlit as st
import datetime

st.set_page_config(
    page_title="ArthaSutra",
    page_icon="◈",
    layout="wide",
    initial_sidebar_state="collapsed",
)

CURRENT_YEAR = datetime.datetime.now().year

# ── CSS ──────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,700;0,900;1,400&family=Inter:wght@300;400;500;600&family=JetBrains+Mono:wght@400;500&display=swap');

:root {
    --white:      #ffffff;
    --off-white:  #f9f8f6;
    --paper:      #f3f1ee;
    --rule:       #e8e4df;
    --text:       #1a1814;
    --text-mid:   #4a453e;
    --text-dim:   #756e64;
    --red:        #dc2626;
    --red-deep:   #991b1b;
    --red-light:  #fef2f2;
    --red-mid:    rgba(220,38,38,0.12);
    --serif:      'Playfair Display', Georgia, serif;
    --sans:       'Inter', system-ui, sans-serif;
    --mono:       'JetBrains Mono', monospace;
}

/* ── Reset ── */
html, body, .stApp {
    background: var(--off-white) !important;
    font-family: var(--sans);
    color: var(--text);
    font-size: 16px;
}
#MainMenu, footer, header { visibility: hidden; }
.block-container {
    padding: 0 !important;
    max-width: 100% !important;
}

/* ── Striped background texture (subtle, crimson + white) ── */
.stApp {
    background-image:
        repeating-linear-gradient(
            135deg,
            rgba(220,38,38,0.035) 0px,
            rgba(220,38,38,0.035) 2px,
            transparent 2px,
            transparent 26px
        );
    background-attachment: fixed;
}

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 4px; }
::-webkit-scrollbar-track { background: var(--paper); }
::-webkit-scrollbar-thumb { background: var(--red); border-radius: 2px; }

/* ── Sidebar hidden ── */
[data-testid="stSidebar"] { display: none; }
[data-testid="collapsedControl"] { display: none; }

/* ── Nav bar ── */
.nav-bar {
    position: sticky; top: 0; z-index: 999;
    background: rgba(255,255,255,0.96);
    backdrop-filter: blur(8px);
    border-bottom: 1px solid var(--rule);
    padding: 0 60px;
    display: flex; align-items: center; justify-content: space-between;
    height: 58px;
}
.nav-logo {
    font-family: var(--serif);
    font-size: 1.25rem; font-weight: 900;
    color: var(--text); letter-spacing: 0.5px;
}
.nav-logo span { color: var(--red); }
.nav-links {
    display: flex; gap: 36px;
    font-size: 0.85rem; font-weight: 500;
    color: var(--text-mid); letter-spacing: 0.5px;
}
.nav-links a {
    color: var(--text-mid); text-decoration: none;
    transition: color 0.2s;
}
.nav-links a:hover { color: var(--red); }
.nav-tag {
    font-size: 0.75rem; font-weight: 500;
    color: var(--red); letter-spacing: 1.5px;
    border: 1px solid rgba(220,38,38,0.3);
    padding: 4px 12px; border-radius: 20px;
    background: var(--red-light);
    font-family: var(--mono);
}

/* ── Hero ── */
.hero {
    padding: 70px 60px 56px;
    border-bottom: 1px solid var(--rule);
    background: var(--white);
    position: relative; overflow: hidden;
}
.hero::after {
    content: '◈';
    position: absolute; right: 60px; top: 50%;
    transform: translateY(-50%);
    font-size: 14rem; color: rgba(220,38,38,0.04);
    font-family: var(--serif); pointer-events: none;
    line-height: 1;
}
.hero-eyebrow {
    font-family: var(--mono);
    font-size: 0.78rem; color: var(--red);
    letter-spacing: 3px; text-transform: uppercase;
    margin-bottom: 18px;
}
.hero-name {
    font-family: var(--serif);
    font-size: 4rem; font-weight: 900;
    color: var(--text); line-height: 1.1;
    margin-bottom: 6px;
}
.hero-name span { color: var(--red); }
.hero-title {
    font-family: var(--serif);
    font-size: 1.5rem; font-weight: 400; font-style: italic;
    color: var(--text-mid); margin-bottom: 20px;
}
.hero-bio {
    font-size: 1.05rem; color: var(--text-mid);
    line-height: 1.75; max-width: 560px;
    font-weight: 400;
}
.hero-rule {
    width: 48px; height: 3px;
    background: var(--red); margin: 22px 0;
    border-radius: 2px;
}
.hero-meta {
    display: flex; gap: 28px; margin-top: 24px;
    flex-wrap: wrap;
}
.hero-meta-item {
    font-size: 0.85rem; color: var(--text-dim);
    font-family: var(--mono);
}
.hero-meta-item b { color: var(--text-mid); font-weight: 500; }

/* ── Photo placeholder ── */
.photo-wrap {
    width: 180px; height: 180px;
    border-radius: 50%;
    border: 3px solid var(--rule);
    background: var(--paper);
    display: flex; align-items: center; justify-content: center;
    font-size: 4rem; color: var(--rule);
    margin-bottom: 20px;
    position: relative; overflow: hidden;
}
.photo-wrap::after {
    content: '';
    position: absolute; inset: 0;
    border-radius: 50%;
    border: 3px solid var(--red);
    opacity: 0.2;
}

/* ── Section ── */
.section {
    padding: 48px 60px;
}
.section-alt {
    background: rgba(220,38,38,0.025);
}
.section-divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, var(--rule) 15%, var(--rule) 85%, transparent);
}
.section-label {
    font-family: var(--mono);
    font-size: 0.75rem; color: var(--red);
    letter-spacing: 3px; text-transform: uppercase;
    margin-bottom: 10px;
}
.section-heading {
    font-family: var(--serif);
    font-size: 2rem; font-weight: 700;
    color: var(--text); margin-bottom: 8px;
}
.section-sub {
    font-size: 0.98rem; color: var(--text-dim);
    margin-bottom: 32px; line-height: 1.6;
    max-width: 640px;
}

/* ── Project card ── */
.proj-card {
    background: var(--white);
    border: 1px solid var(--rule);
    border-radius: 10px;
    padding: 28px 26px;
    transition: all 0.22s ease;
    height: 100%;
    position: relative;
}
.proj-card:hover {
    border-color: rgba(220,38,38,0.35);
    box-shadow: 0 8px 32px rgba(220,38,38,0.08);
    transform: translateY(-2px);
}
.proj-number {
    font-family: var(--mono);
    font-size: 0.72rem; color: var(--red);
    letter-spacing: 2px; margin-bottom: 14px;
    opacity: 0.75;
}
.proj-title {
    font-family: var(--serif);
    font-size: 1.25rem; font-weight: 700;
    color: var(--text); margin-bottom: 8px;
    line-height: 1.3;
}
.proj-desc {
    font-size: 0.92rem; color: var(--text-mid);
    line-height: 1.7; margin-bottom: 18px;
}
.proj-stack {
    display: flex; flex-wrap: wrap; gap: 6px;
    margin-bottom: 18px;
}
.stack-tag {
    font-family: var(--mono);
    font-size: 0.72rem; font-weight: 500;
    color: var(--text-mid);
    background: var(--paper);
    border: 1px solid var(--rule);
    padding: 3px 9px; border-radius: 4px;
    letter-spacing: 0.3px;
}
.proj-link {
    display: inline-block;
    font-family: var(--mono);
    font-size: 0.78rem; font-weight: 500;
    color: var(--red);
    text-decoration: none;
    margin-bottom: 16px;
    border-bottom: 1px solid rgba(220,38,38,0.3);
    padding-bottom: 1px;
    transition: border-color 0.2s, opacity 0.2s;
}
.proj-link:hover {
    border-color: var(--red);
    opacity: 0.8;
}
.proj-footer {
    display: flex; align-items: center;
    justify-content: space-between;
    margin-top: auto;
    padding-top: 14px;
    border-top: 1px solid var(--rule);
}

/* ── Uniform status badge system ── */
.status-badge {
    font-family: var(--mono);
    font-size: 0.7rem; font-weight: 500;
    padding: 3px 10px; border-radius: 20px;
    letter-spacing: 1px;
    display: inline-flex; align-items: center; gap: 5px;
}
.status-badge::before {
    content: ''; width: 6px; height: 6px; border-radius: 50%;
    display: inline-block;
}
.status-live    { background:#f0fdf4; color:#16a34a; border:1px solid #bbf7d0; }
.status-live::before    { background:#16a34a; }
.status-wip     { background:#fefce8; color:#ca8a04; border:1px solid #fef08a; }
.status-wip::before     { background:#ca8a04; }
.status-planned { background:var(--red-light); color:var(--red); border:1px solid rgba(220,38,38,0.25); }
.status-planned::before { background:var(--red); }
.proj-category {
    font-size: 0.75rem; color: var(--text-dim);
    font-family: var(--mono); letter-spacing: 1px;
}

/* ── Flagship card (interactive) ── */
.flagship-card {
    background: var(--text);
    border-radius: 12px;
    padding: 36px 32px;
    position: relative; overflow: hidden;
}
.flagship-card::before {
    content: '';
    position: absolute; top: 0; left: 0;
    width: 4px; height: 100%;
    background: var(--red);
}
.flagship-title {
    font-family: var(--serif);
    font-size: 1.7rem; font-weight: 900;
    color: var(--white); margin-bottom: 10px;
    line-height: 1.25;
}
.flagship-desc {
    font-size: 0.96rem; color: rgba(255,255,255,0.65);
    line-height: 1.75; margin-bottom: 22px;
    max-width: 520px;
}
.flagship-stack { display: flex; flex-wrap: wrap; gap: 7px; margin-bottom: 22px; }
.flagship-tag {
    font-family: var(--mono);
    font-size: 0.72rem;
    color: rgba(255,255,255,0.55);
    border: 1px solid rgba(255,255,255,0.12);
    padding: 3px 10px; border-radius: 4px;
    background: rgba(255,255,255,0.05);
}
.flagship-tag-red {
    color: var(--red); border-color: rgba(220,38,38,0.4);
    background: rgba(220,38,38,0.08);
}
.flagship-meta {
    font-family: var(--mono); font-size: 0.75rem;
    color: rgba(255,255,255,0.35); letter-spacing: 1px;
}
.flagship-info-box {
    border: 1px solid rgba(255,255,255,0.1);
    border-radius: 8px;
    padding: 18px 20px;
    transition: border-color 0.2s, background 0.2s;
}
.flagship-info-box:hover {
    border-color: rgba(220,38,38,0.4);
    background: rgba(220,38,38,0.06);
}
.flagship-info-label {
    font-family: var(--mono); font-size: 0.7rem;
    color: rgba(255,255,255,0.35); letter-spacing: 2px;
    margin-bottom: 8px;
}
.flagship-info-text {
    font-size: 0.9rem; color: rgba(255,255,255,0.65); line-height: 1.7;
}

/* ── Skills (redesigned: single flowing panel, not isolated columns) ── */
.skills-panel {
    background: var(--white);
    border: 1px solid var(--rule);
    border-radius: 12px;
    padding: 36px 38px;
}
.skill-row {
    display: flex; align-items: baseline; gap: 22px;
    padding: 16px 0;
    border-bottom: 1px solid var(--rule);
    flex-wrap: wrap;
}
.skill-row:last-child { border-bottom: none; padding-bottom: 0; }
.skill-row:first-child { padding-top: 0; }
.skill-group-title {
    font-family: var(--mono); font-size: 0.75rem;
    color: var(--red); letter-spacing: 2px;
    text-transform: uppercase;
    flex: 0 0 180px;
    padding-top: 4px;
}
.skill-pills {
    display: flex; flex-wrap: wrap; gap: 8px;
    flex: 1; min-width: 240px;
}
.skill-pill {
    display: inline-block;
    font-size: 0.85rem; color: var(--text-mid);
    background: var(--paper); border: 1px solid var(--rule);
    border-radius: 6px; padding: 6px 14px;
    font-family: var(--sans);
    font-weight: 500;
    transition: all 0.2s;
}
.skill-pill:hover {
    border-color: var(--red);
    color: var(--red); background: var(--red-light);
    transform: translateY(-1px);
}

/* ── Consulting card with side image ── */
.consult-card {
    border: 1px solid var(--rule);
    border-radius: 10px;
    overflow: hidden;
    background: var(--white);
    transition: all 0.22s;
    display: grid;
    grid-template-columns: 140px 1fr;
}
.consult-card:hover {
    border-color: rgba(220,38,38,0.3);
    box-shadow: 0 6px 24px rgba(220,38,38,0.07);
}
.consult-card.consult-placeholder {
    border-style: dashed;
    background: var(--off-white);
}
.consult-image {
    background-size: cover;
    background-position: center;
    min-height: 100%;
    position: relative;
}
.consult-image::after {
    content: '';
    position: absolute; inset: 0;
    background: linear-gradient(180deg, rgba(220,38,38,0.08), rgba(26,24,20,0.35));
}
.consult-body {
    padding: 24px 26px;
}
.consult-tag {
    font-family: var(--mono); font-size: 0.7rem;
    color: var(--red); letter-spacing: 2px;
    margin-bottom: 10px;
}
.consult-title {
    font-family: var(--serif);
    font-size: 1.1rem; font-weight: 700;
    color: var(--text); margin-bottom: 8px;
    line-height: 1.35;
}
.consult-deliverable {
    font-size: 0.84rem; color: var(--text-dim);
    padding: 4px 0; border-bottom: 1px solid var(--rule);
    margin-bottom: 4px;
}
.consult-deliverable:last-child { border-bottom: none; }
.consult-placeholder-text {
    font-size: 0.88rem; color: var(--text-dim);
    font-style: italic; line-height: 1.6;
}

/* ── Contact ── */
.contact-section {
    padding: 64px 60px;
    background: var(--text);
    text-align: center;
    position: relative;
    overflow: hidden;
}
.contact-section::before {
    content: '';
    position: absolute; inset: 0;
    background-image: repeating-linear-gradient(
        135deg,
        rgba(220,38,38,0.08) 0px, rgba(220,38,38,0.08) 2px,
        transparent 2px, transparent 30px
    );
}
.contact-inner { position: relative; z-index: 1; }
.contact-heading {
    font-family: var(--serif);
    font-size: 2.4rem; font-weight: 900;
    color: var(--white); margin-bottom: 12px;
}
.contact-sub {
    font-size: 0.98rem; color: rgba(255,255,255,0.5);
    margin-bottom: 8px; font-style: italic;
    font-family: var(--serif);
}
.contact-sub-line {
    font-size: 0.85rem; color: rgba(255,255,255,0.35);
    margin-bottom: 32px; font-family: var(--mono);
    letter-spacing: 0.5px;
}
.contact-link {
    display: inline-block;
    font-family: var(--mono); font-size: 0.85rem;
    color: var(--red);
    background: rgba(220,38,38,0.1);
    border: 1px solid rgba(220,38,38,0.3);
    padding: 10px 22px; border-radius: 6px;
    margin: 6px; letter-spacing: 1px;
    text-decoration: none;
    transition: all 0.2s;
}
.contact-link:hover {
    background: var(--red); color: white;
}

/* ── Footer ── */
.footer {
    padding: 18px 60px;
    background: var(--text);
    border-top: 1px solid rgba(255,255,255,0.06);
    display: flex; justify-content: space-between; align-items: center;
}
.footer-left {
    font-family: var(--mono); font-size: 0.72rem;
    color: rgba(255,255,255,0.25); letter-spacing: 1px;
}
.footer-right {
    font-family: var(--serif); font-size: 0.82rem;
    color: rgba(255,255,255,0.18); font-style: italic;
}

/* ── Streamlit widget overrides ── */
.stButton > button {
    background: var(--red) !important;
    color: white !important;
    border: none !important;
    border-radius: 6px !important;
    font-family: var(--mono) !important;
    font-size: 0.8rem !important;
    font-weight: 500 !important;
    letter-spacing: 1px !important;
    padding: 0.55rem 1.4rem !important;
    transition: all 0.2s !important;
}
.stButton > button:hover {
    background: #b91c1c !important;
    box-shadow: 0 4px 16px rgba(220,38,38,0.35) !important;
    transform: translateY(-1px) !important;
}
.stSelectbox label, .stRadio label { font-family: var(--mono) !important; }

/* ── Interactive forecast widget ── */
.demo-shell {
    background: var(--white);
    border: 1px solid var(--rule);
    border-radius: 10px;
    padding: 22px 24px;
    margin-top: 18px;
}
.demo-output {
    font-family: var(--mono);
    font-size: 0.95rem;
    color: var(--red-deep);
    background: var(--red-light);
    border: 1px solid rgba(220,38,38,0.2);
    border-radius: 6px;
    padding: 14px 16px;
    margin-top: 12px;
}

@media (max-width: 900px) {
    .nav-bar, .hero, .section, .contact-section, .footer { padding-left: 24px !important; padding-right: 24px !important; }
    .hero-name { font-size: 2.6rem; }
    .consult-card { grid-template-columns: 1fr; }
    .consult-image { min-height: 140px; }
    .skill-group-title { flex-basis: 100%; }
}
</style>
""", unsafe_allow_html=True)

# ── DATA ─────────────────────────────────────────────────────────────────────

# Ordered so "live" projects lead, then "wip", then "planned" — numbering reflects
# display order, not a fixed historical sequence.
PROJECTS = [
    {
        "id": "01",
        "title": "GeoSphere India",
        "category": "Software Engineering",
        "desc": "An interactive geospatial analytics platform — geological maps, tectonic simulators, a mineral explorer, live earthquake data feeds, and structural analysis tools, packaged as a 20-module interactive application.",
        "stack": ["Python", "Streamlit", "Plotly", "USGS API", "Pandas"],
        "status": "live",
        "status_label": "Live",
        "highlight": "20 interactive modules · Live earthquake data · Hidden Easter eggs",
        "link": "https://geosphere-india.streamlit.app/",
    },
    {
        "id": "02",
        "title": "Resume Optimizer AI",
        "category": "Prompt Engineering",
        "desc": "A structured-output prompt engineering project: one LLM system prompt acts as an ATS scorer, recruiter critic, and resume rewriter in a single call. Combines dual-persona role prompting, few-shot calibration against a concrete bad/good bullet pair, conditional schema logic, and an anti-fabrication guardrail that inserts a bracketed placeholder instead of inventing metrics.",
        "stack": ["Python", "Gemini 2.5 Flash", "Streamlit", "pdfplumber", "python-docx"],
        "status": "live",
        "status_label": "Live",
        "highlight": "Single-call structured output · Anti-hallucination guardrails · Web + CLI front ends",
        "link": "https://shivank-resume-optimiser.streamlit.app/",
        "methodology": "This project isn't about data analysis — it's about precision under constraints. Getting a language model to reliably return structured, valid JSON every single time (not just \"usually\") requires the same discipline an economist needs when designing a survey instrument: anticipate every edge case before it happens. The anti-fabrication rule — forcing the model to write `[X%]` instead of inventing a fake number — mirrors a core research ethic: never let a model (or a person) silently fill gaps with fabricated data. That's a transferable instinct, whether you're building an AI tool or running a regression.",
    },
    {
        "id": "03",
        "title": "SmartCalc Pro",
        "category": "Desktop Application",
        "desc": "A desktop calculator built with Python and Tkinter covering basic math, scientific functions, statistics, finance/economics (EMI, CAGR, compound interest, inflation adjustment), and everyday conversions — with calculation history, input validation, and a dark/light theme toggle. Calculation logic is fully separated from the GUI layer, so every function is independently testable.",
        "stack": ["Python", "Tkinter", "Standard Library"],
        "status": "live",
        "status_label": "Live",
        "highlight": "25+ functions · Zero external dependencies · GUI-independent logic layer",
        "methodology": "This is a fundamentals project, not a research one — and that's intentional. It shows the foundation everything else is built on: clean code structure, separating logic from interface, and handling errors instead of letting them crash the app. Recruiters don't just want to see complex econometric thinking; they want proof you can write maintainable, well-organized code under the hood. This project is that proof.",
    },
    {
        "id": "04",
        "title": "AI Inflation Advisor",
        "category": "AI + Economics",
        "desc": "An AI-powered economic forecasting platform combining statistical forecasting, machine learning, and generative AI to explain inflation trends and support economic decision-making. Fetches live CPI data, runs three forecasting models, compares accuracy, then a RAG pipeline retrieves RBI policy context so an LLM can explain the forecast in plain language.",
        "stack": ["LangChain", "RAG", "LLM", "ARIMA", "Prophet", "XGBoost", "Scikit-learn", "Pandas", "Streamlit"],
        "status": "wip",
        "status_label": "Working On",
        "highlight": "3 forecasting models · RAG-grounded LLM explanations · Live CPI data",
    },
    {
        "id": "05",
        "title": "Online vs. Offline Learning: A Statistical Analysis",
        "category
