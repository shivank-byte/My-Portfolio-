import streamlit as st

st.set_page_config(
    page_title="ArthaSutra",
    page_icon="◈",
    layout="wide",
    initial_sidebar_state="collapsed",
)

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
    --text-dim:   #8a837a;
    --red:        #dc2626;
    --red-light:  #fef2f2;
    --red-mid:    rgba(220,38,38,0.12);
    --serif:      'Playfair Display', Georgia, serif;
    --sans:       'Inter', system-ui, sans-serif;
    --mono:       'JetBrains Mono', monospace;
}

/* ── Reset ── */
.stApp {
    background: var(--white) !important;
    font-family: var(--sans);
    color: var(--text);
}
#MainMenu, footer, header { visibility: hidden; }
.block-container {
    padding: 0 !important;
    max-width: 100% !important;
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
    font-size: 0.82rem; font-weight: 500;
    color: var(--text-mid); letter-spacing: 0.5px;
}
.nav-links a {
    color: var(--text-mid); text-decoration: none;
    transition: color 0.2s;
}
.nav-links a:hover { color: var(--red); }
.nav-tag {
    font-size: 0.72rem; font-weight: 500;
    color: var(--red); letter-spacing: 1.5px;
    border: 1px solid rgba(220,38,38,0.3);
    padding: 4px 12px; border-radius: 20px;
    background: var(--red-light);
    font-family: var(--mono);
}

/* ── Hero ── */
.hero {
    padding: 90px 60px 70px;
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
    font-size: 0.72rem; color: var(--red);
    letter-spacing: 3px; text-transform: uppercase;
    margin-bottom: 20px;
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
    color: var(--text-mid); margin-bottom: 22px;
}
.hero-bio {
    font-size: 1rem; color: var(--text-mid);
    line-height: 1.75; max-width: 560px;
    font-weight: 400;
}
.hero-rule {
    width: 48px; height: 3px;
    background: var(--red); margin: 24px 0;
    border-radius: 2px;
}
.hero-meta {
    display: flex; gap: 28px; margin-top: 28px;
    flex-wrap: wrap;
}
.hero-meta-item {
    font-size: 0.8rem; color: var(--text-dim);
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
    padding: 64px 60px;
    border-bottom: 1px solid var(--rule);
}
.section-alt { background: var(--off-white); }
.section-label {
    font-family: var(--mono);
    font-size: 0.7rem; color: var(--red);
    letter-spacing: 3px; text-transform: uppercase;
    margin-bottom: 10px;
}
.section-heading {
    font-family: var(--serif);
    font-size: 2rem; font-weight: 700;
    color: var(--text); margin-bottom: 8px;
}
.section-sub {
    font-size: 0.92rem; color: var(--text-dim);
    margin-bottom: 40px; line-height: 1.6;
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
.proj-card-alt { background: var(--white); }
.proj-number {
    font-family: var(--mono);
    font-size: 0.68rem; color: var(--red);
    letter-spacing: 2px; margin-bottom: 14px;
    opacity: 0.7;
}
.proj-title {
    font-family: var(--serif);
    font-size: 1.2rem; font-weight: 700;
    color: var(--text); margin-bottom: 8px;
    line-height: 1.3;
}
.proj-desc {
    font-size: 0.86rem; color: var(--text-mid);
    line-height: 1.7; margin-bottom: 18px;
}
.proj-stack {
    display: flex; flex-wrap: wrap; gap: 6px;
    margin-bottom: 18px;
}
.stack-tag {
    font-family: var(--mono);
    font-size: 0.68rem; font-weight: 500;
    color: var(--text-mid);
    background: var(--paper);
    border: 1px solid var(--rule);
    padding: 3px 9px; border-radius: 4px;
    letter-spacing: 0.3px;
}
.proj-footer {
    display: flex; align-items: center;
    justify-content: space-between;
    margin-top: auto;
    padding-top: 14px;
    border-top: 1px solid var(--rule);
}
.status-badge {
    font-family: var(--mono);
    font-size: 0.65rem; font-weight: 500;
    padding: 3px 10px; border-radius: 20px;
    letter-spacing: 1px;
}
.status-live    { background:#f0fdf4; color:#16a34a; border:1px solid #bbf7d0; }
.status-wip     { background:#fefce8; color:#ca8a04; border:1px solid #fef08a; }
.status-planned { background:var(--red-light); color:var(--red); border:1px solid rgba(220,38,38,0.25); }
.proj-category {
    font-size: 0.7rem; color: var(--text-dim);
    font-family: var(--mono); letter-spacing: 1px;
}

/* ── Flagship card ── */
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
.flagship-card::after {
    content: '★ FLAGSHIP';
    position: absolute; top: 20px; right: 20px;
    font-family: var(--mono);
    font-size: 0.62rem; color: var(--red);
    letter-spacing: 2px; opacity: 0.8;
}
.flagship-title {
    font-family: var(--serif);
    font-size: 1.6rem; font-weight: 900;
    color: var(--white); margin-bottom: 10px;
    line-height: 1.25;
}
.flagship-desc {
    font-size: 0.9rem; color: rgba(255,255,255,0.6);
    line-height: 1.75; margin-bottom: 22px;
    max-width: 520px;
}
.flagship-stack { display: flex; flex-wrap: wrap; gap: 7px; margin-bottom: 22px; }
.flagship-tag {
    font-family: var(--mono);
    font-size: 0.68rem;
    color: rgba(255,255,255,0.5);
    border: 1px solid rgba(255,255,255,0.12);
    padding: 3px 10px; border-radius: 4px;
    background: rgba(255,255,255,0.05);
}
.flagship-tag-red {
    color: var(--red); border-color: rgba(220,38,38,0.4);
    background: rgba(220,38,38,0.08);
}
.flagship-meta {
    font-family: var(--mono); font-size: 0.72rem;
    color: rgba(255,255,255,0.3); letter-spacing: 1px;
}

/* ── Skills ── */
.skill-group-title {
    font-family: var(--mono); font-size: 0.7rem;
    color: var(--red); letter-spacing: 2px;
    text-transform: uppercase; margin-bottom: 12px;
}
.skill-pill {
    display: inline-block;
    font-size: 0.8rem; color: var(--text-mid);
    background: var(--white); border: 1px solid var(--rule);
    border-radius: 6px; padding: 5px 12px;
    margin: 4px; font-family: var(--sans);
    font-weight: 400;
    transition: all 0.2s;
}
.skill-pill:hover {
    border-color: rgba(220,38,38,0.35);
    color: var(--red); background: var(--red-light);
}

/* ── Consulting card ── */
.consult-card {
    border: 1px solid var(--rule);
    border-radius: 10px;
    padding: 26px 24px;
    background: var(--white);
    transition: all 0.22s;
}
.consult-card:hover {
    border-color: rgba(220,38,38,0.3);
    box-shadow: 0 6px 24px rgba(220,38,38,0.07);
}
.consult-tag {
    font-family: var(--mono); font-size: 0.65rem;
    color: var(--red); letter-spacing: 2px;
    margin-bottom: 10px;
}
.consult-title {
    font-family: var(--serif);
    font-size: 1.05rem; font-weight: 700;
    color: var(--text); margin-bottom: 8px;
    line-height: 1.35;
}
.consult-deliverable {
    font-size: 0.78rem; color: var(--text-dim);
    padding: 3px 0; border-bottom: 1px solid var(--rule);
    margin-bottom: 4px;
}
.consult-deliverable:last-child { border-bottom: none; }

/* ── Contact ── */
.contact-section {
    padding: 72px 60px;
    background: var(--text);
    text-align: center;
}
.contact-heading {
    font-family: var(--serif);
    font-size: 2.4rem; font-weight: 900;
    color: var(--white); margin-bottom: 12px;
}
.contact-sub {
    font-size: 0.92rem; color: rgba(255,255,255,0.45);
    margin-bottom: 36px; font-style: italic;
    font-family: var(--serif);
}
.contact-link {
    display: inline-block;
    font-family: var(--mono); font-size: 0.82rem;
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
    padding: 20px 60px;
    background: var(--text);
    border-top: 1px solid rgba(255,255,255,0.06);
    display: flex; justify-content: space-between; align-items: center;
}
.footer-left {
    font-family: var(--mono); font-size: 0.68rem;
    color: rgba(255,255,255,0.2); letter-spacing: 1px;
}
.footer-right {
    font-family: var(--serif); font-size: 0.78rem;
    color: rgba(255,255,255,0.15); font-style: italic;
}

/* ── Streamlit widget overrides ── */
.stButton > button {
    background: var(--red) !important;
    color: white !important;
    border: none !important;
    border-radius: 6px !important;
    font-family: var(--mono) !important;
    font-size: 0.78rem !important;
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
</style>
""", unsafe_allow_html=True)

# ── DATA ─────────────────────────────────────────────────────────────────────

PROJECTS = [
    {
        "id": "02",
        "title": "GeoSphere India",
        "category": "Software Engineering",
        "desc": "An interactive Earth Science learning platform — geological maps, tectonic simulators, mineral explorer, earthquake live data, structural tools, and a 20-section curriculum for BHU's 4-year UG programme.",
        "stack": ["Python", "Streamlit", "Plotly", "USGS API", "Pandas"],
        "status": "live",
        "status_label": "Live",
        "highlight": "20 interactive modules · Live earthquake data · Hidden Easter eggs",
    },
    {
        "id": "03",
        "title": "Women Literacy Prediction",
        "category": "Machine Learning",
        "desc": "ML pipeline predicting female literacy rates across Indian districts using socioeconomic indicators. Includes feature engineering, model comparison, and an interactive Streamlit dashboard.",
        "stack": ["Python", "Scikit-learn", "Pandas", "Streamlit", "Matplotlib"],
        "status": "wip",
        "status_label": "Upgrading",
        "highlight": "Feature importance · Model comparison · District-level analysis",
    },
    {
        "id": "04",
        "title": "Indian Banking Credit Dashboard",
        "category": "Business Analytics",
        "desc": "Comprehensive analytics dashboard covering credit growth, NPA trends, priority sector lending, CASA ratios, and digital banking adoption across Indian public and private sector banks.",
        "stack": ["Python", "SQL", "Power BI", "Pandas", "Plotly"],
        "status": "planned",
        "status_label": "Coming Soon",
        "highlight": "RBI data · State-wise credit · NPA heatmaps",
    },
    {
        "id": "06",
        "title": "B.Sc Research Thesis",
        "category": "Research & Statistics",
        "desc": "Undergraduate research thesis combining survey design, regression analysis, and statistical inference. Documents methodology, findings, and policy implications with academic rigour.",
        "stack": ["R / Python", "Regression", "Survey Design", "Statistics"],
        "status": "live",
        "status_label": "Published",
        "highlight": "Survey design · Regression · Policy implications",
    },
]

CONSULTING_CASES = [
    {
        "tag": "CASE 01 · EDUCATION POLICY",
        "title": "Why Do Government Schools Underperform in India?",
        "deliverables": [
            "Problem statement & scoping",
            "Root cause analysis (5-Why framework)",
            "State-level benchmarking",
            "Cost-benefit analysis of interventions",
            "100-day implementation roadmap",
        ],
        "status": "planned",
    },
    {
        "tag": "CASE 02 · LABOUR ECONOMICS",
        "title": "Why is Female Labour Force Participation Low in India?",
        "deliverables": [
            "Executive summary & market context",
            "FLFP trend analysis (1990–2024)",
            "State-wise comparison & clustering",
            "Structural vs cultural drivers",
            "Policy recommendations & impact assessment",
        ],
        "status": "planned",
    },
]

SKILLS = {
    "Languages": ["Python", "SQL", "R"],
    "ML & AI": ["Scikit-learn", "XGBoost", "ARIMA", "Prophet", "LangChain", "RAG", "LLMs"],
    "Data & BI": ["Pandas", "NumPy", "Power BI", "Plotly", "Matplotlib", "Seaborn"],
    "Engineering": ["Streamlit", "Git", "GitHub", "APIs", "Agentic AI"],
    "Domain": ["Economics", "Earth Science", "Geology", "Banking Analytics", "Policy Research"],
}

# ── NAV ──────────────────────────────────────────────────────────────────────
st.markdown("""
<div class='nav-bar'>
    <div class='nav-logo'>Artha<span>Sutra</span></div>
    <div class='nav-links'>
        <a href='#projects'>Projects</a>
        <a href='#consulting'>Consulting</a>
        <a href='#skills'>Skills</a>
        <a href='#contact'>Contact</a>
    </div>
    <div class='nav-tag'>OPEN TO WORK</div>
</div>
""", unsafe_allow_html=True)

# ── HERO ─────────────────────────────────────────────────────────────────────
col_hero, col_photo = st.columns([3, 1])
with col_hero:
    st.markdown("""
    <div class='hero'>
        <div class='hero-eyebrow'>◈ Economics · Analytics · AI</div>
        <div class='hero-name'>Your<span>Name</span></div>
        <div class='hero-title'>Economics & Earth Science, BHU · IIT Kanpur Intern</div>
        <div class='hero-rule'></div>
        <div class='hero-bio'>
            Building at the intersection of economics, machine learning, and earth science.
            I turn complex datasets into decisions — from inflation forecasting with LLMs
            to geological intelligence platforms.
        </div>
        <div class='hero-meta'>
            <div class='hero-meta-item'><b>Institution</b> · Banaras Hindu University</div>
            <div class='hero-meta-item'><b>Intern</b> · IIT Kanpur</div>
            <div class='hero-meta-item'><b>Programme</b> · B.Sc (Hons.) Earth Science</div>
            <div class='hero-meta-item'><b>Minor</b> · Geography</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

with col_photo:
    st.markdown("""
    <div style='padding:90px 40px 0 0;display:flex;flex-direction:column;align-items:center;'>
        <div class='photo-wrap'>📷</div>
        <div style='font-size:0.72rem;color:#8a837a;font-family:JetBrains Mono,monospace;
            letter-spacing:1px;text-align:center;'>
            PHOTO<br>PLACEHOLDER
        </div>
    </div>
    """, unsafe_allow_html=True)

# ── FLAGSHIP ─────────────────────────────────────────────────────────────────
st.markdown("""
<div class='section'>
    <div class='section-label'>★ Flagship Project</div>
    <div class='flagship-card'>
        <div style='display:grid;grid-template-columns:1fr 1fr;gap:40px;'>
            <div>
                <div class='flagship-title'>AI Inflation Advisor</div>
                <div class='flagship-desc'>
                    An agentic AI system that forecasts Indian inflation using ARIMA, Prophet,
                    and XGBoost — then explains its predictions through a RAG-powered LLM interface.
                    Compares model performance, surfaces drivers, and answers policy questions
                    in natural language. Built during IIT Kanpur internship.
                </div>
                <div class='flagship-stack'>
                    <span class='flagship-tag flagship-tag-red'>LangChain</span>
                    <span class='flagship-tag flagship-tag-red'>RAG</span>
                    <span class='flagship-tag flagship-tag-red'>LLM</span>
                    <span class='flagship-tag'>ARIMA</span>
                    <span class='flagship-tag'>Prophet</span>
                    <span class='flagship-tag'>XGBoost</span>
                    <span class='flagship-tag'>Scikit-learn</span>
                    <span class='flagship-tag'>Pandas</span>
                    <span class='flagship-tag'>Streamlit</span>
                </div>
                <div class='flagship-meta'>IIT KANPUR INTERNSHIP · AI + ECONOMICS · 2025</div>
            </div>
            <div style='display:flex;flex-direction:column;justify-content:center;gap:16px;'>
                <div style='border:1px solid rgba(255,255,255,0.08);border-radius:8px;padding:18px 20px;'>
                    <div style='font-family:JetBrains Mono,monospace;font-size:0.65rem;
                        color:rgba(255,255,255,0.3);letter-spacing:2px;margin-bottom:8px;'>WHAT IT DOES</div>
                    <div style='font-size:0.85rem;color:rgba(255,255,255,0.6);line-height:1.7;'>
                    Fetches live CPI data → runs 3 forecasting models → compares accuracy →
                    RAG pipeline retrieves RBI policy context → LLM explains the forecast
                    in plain language.
                    </div>
                </div>
                <div style='border:1px solid rgba(255,255,255,0.08);border-radius:8px;padding:18px 20px;'>
                    <div style='font-family:JetBrains Mono,monospace;font-size:0.65rem;
                        color:rgba(255,255,255,0.3);letter-spacing:2px;margin-bottom:8px;'>WHY IT MATTERS</div>
                    <div style='font-size:0.85rem;color:rgba(255,255,255,0.6);line-height:1.7;'>
                    Demonstrates AI + Economics + Software Engineering in one project.
                    Recruiters at analytics and policy firms rarely see this combination at undergrad level.
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ── PROJECTS GRID ─────────────────────────────────────────────────────────────
st.markdown("""
<div class='section section-alt' id='projects'>
    <div class='section-label'>Portfolio</div>
    <div class='section-heading'>Projects</div>
    <div class='section-sub'>Each project demonstrates a distinct capability — no overlap by design.</div>
</div>
""", unsafe_allow_html=True)

with st.container():
    st.markdown("<div style='padding:0 60px 60px;background:#f9f8f6;'>", unsafe_allow_html=True)
    cols = st.columns(2)
    for i, proj in enumerate(PROJECTS):
        status_class = f"status-{proj['status']}"
        with cols[i % 2]:
            st.markdown(f"""
            <div class='proj-card'>
                <div class='proj-number'>PROJECT {proj['id']}</div>
                <div style='font-size:0.7rem;color:#8a837a;font-family:JetBrains Mono,monospace;
                    letter-spacing:1.5px;margin-bottom:10px;'>{proj['category'].upper()}</div>
                <div class='proj-title'>{proj['title']}</div>
                <div class='proj-desc'>{proj['desc']}</div>
                <div class='proj-stack'>
                    {''.join([f"<span class='stack-tag'>{t}</span>" for t in proj['stack']])}
                </div>
                <div style='font-size:0.78rem;color:#dc2626;font-style:italic;margin-bottom:14px;'>
                    ◈ {proj['highlight']}
                </div>
                <div class='proj-footer'>
                    <span class='{status_class} status-badge'>{proj['status_label'].upper()}</span>
                    <span class='proj-category'>{proj['category'].upper()}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# ── CONSULTING ───────────────────────────────────────────────────────────────
st.markdown("""
<div class='section' id='consulting'>
    <div class='section-label'>Consulting Portfolio</div>
    <div class='section-heading'>Case Studies</div>
    <div class='section-sub'>
        Structured like real consulting engagements — problem scoping, data analysis,
        root causes, and actionable recommendations.
    </div>
</div>
""", unsafe_allow_html=True)

with st.container():
    st.markdown("<div style='padding:0 60px 60px;'>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    for i, case in enumerate(CONSULTING_CASES):
        with [c1, c2][i]:
            delivs = "".join([
                f"<div class='consult-deliverable'>→ {d}</div>"
                for d in case["deliverables"]
            ])
            st.markdown(f"""
            <div class='consult-card'>
                <div class='consult-tag'>{case['tag']}</div>
                <div class='consult-title'>{case['title']}</div>
                <div style='margin-top:16px;'>
                    <div style='font-family:JetBrains Mono,monospace;font-size:0.65rem;
                        color:#8a837a;letter-spacing:2px;margin-bottom:10px;'>DELIVERABLES</div>
                    {delivs}
                </div>
                <div style='margin-top:16px;'>
                    <span class='status-planned status-badge'>COMING SOON</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# ── SKILLS ───────────────────────────────────────────────────────────────────
st.markdown("""
<div class='section section-alt' id='skills'>
    <div class='section-label'>Capabilities</div>
    <div class='section-heading'>Skills</div>
    <div class='section-sub'>Tools and frameworks across the full analytics stack.</div>
</div>
""", unsafe_allow_html=True)

with st.container():
    st.markdown("<div style='padding:0 60px 60px;background:#f9f8f6;'>", unsafe_allow_html=True)
    sk_cols = st.columns(5)
    for i, (group, skills) in enumerate(SKILLS.items()):
        with sk_cols[i]:
            pills = "".join([f"<span class='skill-pill'>{s}</span>" for s in skills])
            st.markdown(f"""
            <div>
                <div class='skill-group-title'>{group.upper()}</div>
                <div>{pills}</div>
            </div>
            """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# ── CONTACT ──────────────────────────────────────────────────────────────────
st.markdown("""
<div class='contact-section' id='contact'>
    <div class='contact-heading'>Let's Talk</div>
    <div class='contact-sub'>Open to analytics, research, and consulting internships.</div>
    <div>
        <a class='contact-link' href='mailto:your@email.com'>✉ Email</a>
        <a class='contact-link' href='https://linkedin.com/in/yourprofile'>in LinkedIn</a>
        <a class='contact-link' href='https://github.com/yourgithub'>⌥ GitHub</a>
    </div>
</div>
<div class='footer'>
    <div class='footer-left'>ARTHASUTRA · BHU · 2025</div>
    <div class='footer-right'>Economics · Analytics · AI</div>
</div>
""", unsafe_allow_html=True)
