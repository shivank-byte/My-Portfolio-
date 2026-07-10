import streamlit as st
import streamlit.components.v1 as components
import datetime
import re
import plotly.graph_objects as go

def html(body, **kwargs):
    """Render an HTML block safely.

    Streamlit's markdown parser follows CommonMark rules, where 4+ leading
    spaces on a line make it a literal code block. Because our HTML strings
    are written with normal Python indentation, some deeply-nested lines
    (e.g. inside a project card) were being rendered as raw visible text
    instead of HTML. Stripping the leading whitespace on every line before
    handing it to st.markdown fixes that.
    """
    kwargs.setdefault("unsafe_allow_html", True)
    st.markdown(re.sub(r"(?m)^[ \t]+", "", body), **kwargs)

# ── EMBEDDED MEDIA (base64) — must be defined before any data structures use them ──

# ── EMBEDDED VIDEOS (compressed, base64) ────────────────────────────────────


# ── REAL PROJECT SCREENSHOTS (cropped, base64-embedded) ────────────────────────







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
if "selected_project" not in st.session_state:
    st.session_state.selected_project = None
if "show_utility_projects" not in st.session_state:
    st.session_state.show_utility_projects = False
if "video_shown" not in st.session_state:
    st.session_state.video_shown = {}

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
html(f"""
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
padding: 0 clamp(20px, 6vw, 60px);
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
padding: clamp(40px, 8vw, 72px) clamp(20px, 6vw, 60px) 48px;
position: relative; overflow: hidden;
}}
/* Background is scoped to .hero-intro only (name/bio/photo area) — not the
stat row below — per feedback to keep it "above" the 4+ / 21 / 706 numbers. */
.hero-intro {{ position: relative; }}
/* Foreground grid — rendered in the SAME html() call as .hero-outer and
.hero-data-bg (no more st.columns for this section), so the background
is a genuine DOM ancestor and inset:0 sizes against real content. */
.hero-grid {{
position: relative; z-index: 1;
display: grid; grid-template-columns: 1.5fr 1fr; gap: 40px; align-items: center;
padding-bottom: 28px;
}}
@media (max-width: 900px) {{
  .hero-grid {{ grid-template-columns: 1fr; }}
}}

/* FULL-HERO DATA BACKGROUND — several independently-positioned fragments,
   spans .hero-intro (including behind the name and around the photo), sits
   behind all text/photo content. Each fragment carries its own position. */
.hero-data-bg {{
/* This is now rendered INSIDE the same html() call as .hero-outer (real
   DOM nesting, not just visually-nested Python code across separate
   Streamlit blocks), and the hero's foreground is a CSS grid in that same
   call too — so inset:0 correctly fills the real, full-height parent and
   sits behind everything, edge to edge, for the whole intro area. */
position: absolute; inset: 0; z-index: 0; pointer-events: none; overflow: hidden;
}}
.hbg-glow {{
position: absolute; border-radius: 50%; filter: blur(40px);
pointer-events: none;
}}
.hbg-frag {{ position: absolute; display: block; }}
.hbg-symbol {{
position: absolute; font-family: var(--mono); font-weight: 700;
animation: hbg-float 7s ease-in-out infinite;
}}
@keyframes hbg-float {{ 0%,100% {{ transform: translateY(0); opacity: 0.45; }} 50% {{ transform: translateY(-12px); opacity: 0.8; }} }}
.hbg-bar {{ transform-origin: bottom; animation: hbg-grow 3.4s ease-in-out infinite alternate; }}
@keyframes hbg-grow {{ 0% {{ transform: scaleY(0.6); }} 100% {{ transform: scaleY(1); }} }}
.hbg-line {{
stroke-dasharray: 400; stroke-dashoffset: 400;
animation: hbg-draw 5s ease-in-out infinite;
}}
@keyframes hbg-draw {{
0% {{ stroke-dashoffset: 400; opacity: 0.9; }}
60% {{ stroke-dashoffset: 0; opacity: 0.9; }}
100% {{ stroke-dashoffset: 0; opacity: 0.9; }}
}}
.hbg-curve {{ stroke-dasharray: 320; stroke-dashoffset: 320; animation: hbg-draw 6.5s ease-in-out infinite; }}
.hbg-dot {{ animation: hbg-pulse 2.6s ease-in-out infinite; }}
@keyframes hbg-pulse {{ 0%,100% {{ opacity: 0.35; r: 4; }} 50% {{ opacity: 0.75; r: 6; }} }}
.hbg-donut {{
animation: hbg-spin 14s linear infinite;
transform-origin: center;
}}
@keyframes hbg-spin {{ 0% {{ transform: rotate(-90deg); }} 100% {{ transform: rotate(270deg); }} }}
.hbg-scatter {{ animation: hbg-fade 3.6s ease-in-out infinite; }}
@keyframes hbg-fade {{ 0%,100% {{ opacity: 0.35; }} 50% {{ opacity: 0.85; }} }}
.hbg-grid-cell {{ animation: hbg-fade 4.2s ease-in-out infinite; }}
@media (max-width: 640px) {{
  .hbg-frag {{ transform: scale(0.7); }}
  .hbg-symbol {{ font-size: 1.4rem !important; }}
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
.photo-zone {{ position: relative; z-index: 1; width: 100%; max-width: 340px; margin: 0 auto; }}
.photo-zone-large {{ max-width: 430px; }}

.blob-shape {{
width: 100%; aspect-ratio: 1/1.08;
background: linear-gradient(135deg, var(--red) 0%, #b8241c 100%);
border-radius: 42% 58% 65% 35% / 50% 45% 55% 50%;
position: absolute; inset: 0;
transform: scale(1.07) translate(5%, 5%);
opacity: 0.9; filter: blur(0.5px);
box-shadow: 0 25px 60px -15px rgba(224,52,42,0.45);
}}
.blob-photo {{
width: 100%; aspect-ratio: 1/1.08; object-fit: cover;
object-position: center 15%;
border-radius: 42% 58% 65% 35% / 50% 45% 55% 50%;
position: relative; z-index: 1;
border: 3px solid var(--bg);
box-shadow: 0 8px 32px rgba(0,0,0,0.28);
}}

/* LIVE DATA PANEL — replaces the old hidden SVG + video-that-needs-a-tap.
Pure CSS/SVG animation, always playing, no click required. */
.data-panel {{
margin-top: 20px; padding: 22px 22px 16px;
background: var(--bg-card); border: 1.5px solid rgba(224,52,42,0.4);
border-radius: 14px; position: relative; z-index: 1; overflow: hidden;
box-shadow: 0 0 0 1px rgba(224,52,42,0.08), 0 10px 30px rgba(224,52,42,0.12);
}}
.data-panel-label {{
font-family: var(--mono); font-size: 0.74rem; color: var(--red);
letter-spacing: 2.5px; text-align: center; margin-top: 12px; font-weight: 700;
}}
.data-panel svg {{ width: 100%; height: 160px; display: block; }}
.doodle-video {{ width: 100%; max-height: 220px; display: block; border-radius: 10px; object-fit: contain; background: transparent; }}
/* Doodle sits inside the (already dark) contact section, blended straight
into its background with mix-blend-mode instead of a separate boxed frame —
its own dark backdrop disappears into the section, leaving just the drawn
lines visible, sitting elegantly next to the closing line. */
.contact-flex {{
display: flex; align-items: center; justify-content: center; gap: 56px;
text-align: left; max-width: 1100px; margin: 0 auto;
}}
.contact-doodle-wrap {{ flex: 0 0 260px; position: relative; }}
.contact-doodle-video {{
width: 100%; max-height: 260px; display: block;
mix-blend-mode: screen; opacity: 0.92;
}}
.contact-text {{ flex: 1 1 auto; text-align: left; }}
@media (max-width: 780px) {{
  .contact-flex {{ flex-direction: column; text-align: center; gap: 20px; }}
  .contact-doodle-wrap {{ flex-basis: auto; width: 70%; max-width: 260px; }}
  .contact-text {{ text-align: center; }}
  .contact-cta {{ margin-left: auto; margin-right: auto; }}
  .contact-links {{ justify-content: center; }}
}}
.robot-badge {{
position: fixed; bottom: 18px; right: 18px; width: 110px; height: 110px;
z-index: 9999; border-radius: 14px; overflow: hidden;
box-shadow: 0 10px 30px rgba(0,0,0,0.4); border: 1px solid rgba(224,52,42,0.35);
background: #0a0a0c; pointer-events: none;
}}
.robot-badge video {{ width: 100%; height: 100%; object-fit: cover; display: block; }}
@media (max-width: 640px) {{
  .robot-badge {{ width: 78px; height: 78px; bottom: 12px; right: 12px; }}
}}
.dp-bar {{ transform-origin: bottom; animation: dp-grow 2.6s ease-in-out infinite alternate; }}
.dp-bar:nth-child(2) {{ animation-delay: 0s; }}
.dp-bar:nth-child(3) {{ animation-delay: 0.15s; }}
.dp-bar:nth-child(4) {{ animation-delay: 0.3s; }}
.dp-bar:nth-child(5) {{ animation-delay: 0.45s; }}
.dp-bar:nth-child(6) {{ animation-delay: 0.6s; }}
@keyframes dp-grow {{ 0% {{ transform: scaleY(0.5); }} 100% {{ transform: scaleY(1); }} }}
.dp-line {{
stroke-dasharray: 300; stroke-dashoffset: 300;
animation: dp-draw 3.2s ease-in-out infinite;
filter: drop-shadow(0 0 4px rgba(224,52,42,0.6));
}}
@keyframes dp-draw {{
0% {{ stroke-dashoffset: 300; }}
55% {{ stroke-dashoffset: 0; }}
100% {{ stroke-dashoffset: 0; opacity: 0; }}
}}
.dp-dot {{ animation: dp-pulse 1.8s ease-in-out infinite; filter: drop-shadow(0 0 6px rgba(224,52,42,0.9)); }}
@keyframes dp-pulse {{ 0%,100% {{ opacity: 0.5; r: 4; }} 50% {{ opacity: 1; r: 6.5; }} }}

/* STAT ROW */
.stat-row {{
display: flex; border-top: 1px solid var(--rule);
position: relative; z-index: 1;
}}
.stat-block {{
flex: 1; padding: 30px 10px 26px 0; border-right: 1px solid var(--rule);
position: relative;
}}
.stat-block::before {{
content: ''; position: absolute; top: 0; left: 0; width: 28px; height: 3px;
background: var(--red);
}}
.stat-block:last-child {{ border-right: none; }}
.stat-num {{
font-family: var(--serif); font-size: 2.3rem; font-weight: 800;
color: var(--text); margin-bottom: 4px; letter-spacing: -1px;
}}
.stat-num span {{ color: var(--red); }}
.stat-label {{ font-size: 0.76rem; color: var(--text-dim); line-height: 1.4; text-transform: uppercase; letter-spacing: 0.5px; }}

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
.section {{ padding: clamp(40px, 8vw, 72px) clamp(20px, 6vw, 60px); }}
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
.proj-editorial:first-child {{
padding-top: 8px; position: relative;
}}
.proj-editorial:first-child::before {{
content: 'FEATURED'; position: absolute; top: -14px; left: 80px;
font-family: var(--mono); font-size: 0.74rem; letter-spacing: 2.5px;
color: var(--red); background: var(--bg); padding: 0 8px;
}}
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
.proj-editorial:first-child .proj-title-big {{ font-size: 2.1rem; }}
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
.proj-link:hover {{ background: var(--red); color: white; box-shadow: 0 4px 16px rgba(224,52,42,0.35); }}
.proj-img-col {{
position: relative; background: var(--bg-card2); border: 1px solid var(--rule);
border-radius: 14px; padding: 10px; box-shadow: 0 10px 30px rgba(0,0,0,0.25);
}}
.proj-collage {{
display: grid; grid-template-columns: 1fr 1fr; gap: 8px; border-radius: 10px; overflow: hidden;
}}
.proj-collage img {{
width: 100%; aspect-ratio: 4/3; object-fit: cover; border-radius: 6px;
transition: transform 0.3s ease, box-shadow 0.3s ease;
}}
.proj-collage img:hover {{ transform: scale(1.04); box-shadow: 0 6px 20px rgba(0,0,0,0.35); }}
.proj-collage-single img {{
width: 100%; border-radius: 10px; object-fit: cover; display: block;
}}
.proj-collage-3 {{
grid-template-columns: 1.4fr 1fr; grid-template-rows: 1fr 1fr;
}}
.proj-collage-lead {{ grid-row: 1 / 3; aspect-ratio: 3/4 !important; }}
.proj-collage-many {{
grid-template-columns: 1fr 1fr; max-height: 640px; overflow-y: auto; padding-right: 4px;
}}
.proj-collage-many img {{ aspect-ratio: 4/3; }}
.proj-collage-many::-webkit-scrollbar {{ width: 6px; }}
.proj-collage-many::-webkit-scrollbar-thumb {{ background: var(--rule); border-radius: 3px; }}

/* MINI STAT STRIP — fills the dead space under project visuals */
.proj-mini-stats {{
    display: flex; gap: 10px; flex-wrap: wrap; margin-top: 14px;
}}
.proj-mini-stat {{
    flex: 1; min-width: 110px; text-align: center;
    background: var(--bg-card2); border: 1px solid var(--rule);
    border-radius: 10px; padding: 12px 8px;
}}
.proj-mini-stat-num {{
    font-family: var(--serif); font-weight: 800; font-size: 1.15rem; color: var(--red);
}}
.proj-mini-stat-label {{
    font-size: 0.78rem; color: var(--text-dim); margin-top: 2px; line-height: 1.35;
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

/* MINOR PROJECTS — horizontal, click-to-reveal cards */
.minor-scroll {{
    display: flex; gap: 16px; overflow-x: auto; padding: 6px 2px 18px;
    scroll-snap-type: x proximity;
}}
.minor-scroll::-webkit-scrollbar {{ height: 6px; }}
.minor-scroll::-webkit-scrollbar-thumb {{ background: var(--red); border-radius: 3px; }}
.minor-card {{
    flex: 0 0 240px; scroll-snap-align: start;
    background: var(--bg-card2); border: 1px dashed var(--rule);
    border-radius: 12px; padding: 18px 18px; transition: all 0.2s;
}}
.minor-card[open] {{ flex-basis: 300px; border-style: solid; background: var(--bg-card); box-shadow: 0 10px 30px rgba(0,0,0,0.25); }}
.minor-card:hover {{ border-color: rgba(224,52,42,0.3); box-shadow: 0 8px 24px var(--red-glow); transform: translateY(-2px); }}
.minor-card summary {{ cursor: pointer; list-style: none; }}
.minor-card summary::-webkit-details-marker {{ display: none; }}
.minor-summary-row {{ display: flex; align-items: center; justify-content: space-between; gap: 8px; }}
.minor-chevron {{ font-family: var(--mono); font-size: 0.7rem; color: var(--red); transition: transform 0.2s; }}
.minor-card[open] .minor-chevron {{ transform: rotate(90deg); }}
.minor-eyebrow {{ font-family: var(--mono); font-size: 0.78rem; color: var(--text-dim); letter-spacing: 1.3px; margin-bottom: 10px; }}
.minor-title {{ font-family: var(--serif); font-size: 1.02rem; font-weight: 700; color: var(--text-mid); margin-bottom: 4px; line-height: 1.3; }}
.minor-body {{ margin-top: 12px; }}
.minor-desc {{ font-size: 0.82rem; color: var(--text-dim); line-height: 1.65; margin-bottom: 14px; }}
.minor-stack {{ display: flex; flex-wrap: wrap; gap: 6px; margin-bottom: 14px; }}
.minor-tag {{ font-family: var(--mono); font-size: 0.76rem; color: var(--text-dim); background: var(--bg-card); border: 1px solid var(--rule); padding: 3px 9px; border-radius: 4px; }}
.minor-footer {{ display: flex; align-items: center; justify-content: space-between; padding-top: 12px; border-top: 1px solid var(--rule); }}
.minor-cat {{ font-size: 0.7rem; color: var(--text-dim); font-family: var(--mono); }}
.minor-hint {{ font-family: var(--mono); font-size: 0.76rem; color: var(--text-dim); letter-spacing: 1px; text-align: center; margin: -8px 0 14px; }}
.minor-imgs {{ display: flex; gap: 6px; margin-bottom: 12px; }}
.minor-imgs img {{ width: 100%; aspect-ratio: 4/3; object-fit: cover; border-radius: 6px; border: 1px solid var(--rule); }}

/* SKILLS — compact */
.skills-grid {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 12px; }}
.skill-block {{
background: var(--bg-card); border: 1px solid var(--rule); border-radius: 10px;
padding: 14px 16px; transition: all 0.2s;
}}
.skill-block:hover {{ border-color: rgba(224,52,42,0.3); }}
.skill-block-title {{
font-family: var(--mono); font-size: 0.76rem; color: var(--red);
letter-spacing: 1.2px; text-transform: uppercase; margin-bottom: 9px;
}}
.skill-tile-row {{ display: flex; flex-wrap: wrap; gap: 8px; }}
.skill-tile {{
display: flex; flex-direction: column; align-items: center; justify-content: center;
gap: 7px; width: 74px; padding: 12px 6px 10px;
background: var(--bg-card2); border: 1px solid var(--rule); border-radius: 10px;
transition: all 0.2s;
}}
.skill-tile:hover {{ border-color: var(--red); background: rgba(224,52,42,0.06); transform: translateY(-2px); }}
.skill-tile-icon {{ width: 26px; height: 26px; object-fit: contain; }}
.skill-tile-monogram {{
width: 30px; height: 20px; padding: 0 3px; border-radius: 6px; background: rgba(224,52,42,0.12);
color: var(--red); font-family: var(--mono); font-weight: 700; font-size: 0.62rem; letter-spacing: 0.2px;
align-items: center; justify-content: center; display: flex;
}}
.skill-tile-label {{
font-size: 0.74rem; color: var(--text-mid); text-align: center; line-height: 1.3;
font-weight: 500;
}}

#skills.section {{ padding-bottom: 28px; }}
#skills .section-sub {{ margin-bottom: 22px; }}

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
.proj-gallery {{ display: grid; grid-template-columns: repeat(2, 1fr); gap: 10px; margin-top: 14px; }}

/* COMPACT PROJECT CARDS — photo + intro only; full detail lives behind
"View full case study" (click-through), so the grid stays a fast, visual
overview instead of a wall of text. */
.proj-card-compact {{
border: 1px solid var(--rule); border-radius: 16px; overflow: hidden;
margin-bottom: 22px; background: var(--bg-card);
transition: box-shadow 0.2s, transform 0.2s;
}}
.proj-card-compact:hover {{ box-shadow: 0 12px 30px rgba(0,0,0,0.12); transform: translateY(-2px); }}
.proj-card-compact-img {{ width: 100%; aspect-ratio: 16/8.2; overflow: hidden; background: var(--bg-card2); }}
.proj-card-compact-img img {{ width: 100%; height: 100%; object-fit: cover; display: block; }}
.proj-card-compact-body {{ padding: 20px 24px 6px; }}
.proj-card-compact-eyebrow {{
font-family: var(--mono); font-size: 0.72rem; color: var(--text-dim);
letter-spacing: 1.5px; text-transform: uppercase; margin-bottom: 8px;
display: flex; align-items: center; gap: 10px; flex-wrap: wrap;
}}
.proj-card-compact-title {{
font-family: var(--serif); font-size: 1.4rem; font-weight: 700;
color: var(--text); margin-bottom: 8px; line-height: 1.25;
}}
.proj-card-compact-intro {{
font-size: 0.94rem; color: var(--text-mid); line-height: 1.6; margin-bottom: 4px;
}}
.proj-tier-heading {{
font-family: var(--mono); font-size: 0.8rem; color: var(--red);
letter-spacing: 2px; text-transform: uppercase; margin: 44px 0 18px;
padding-bottom: 8px; border-bottom: 1px solid var(--rule);
}}
.proj-tier-heading:first-of-type {{ margin-top: 0; }}
.proj-detail-header {{
display: flex; align-items: center; gap: 10px; margin-bottom: 24px;
font-family: var(--mono); font-size: 0.82rem; color: var(--text-dim);
}}

/* NETFLIX-STYLE PROJECT ROWS — poster art on top, title/category always
visible below (NOT hover-gated: hover doesn't exist on touchscreens, so
anything hidden-until-hover is permanently invisible on mobile). Hovering
on desktop still pops the card slightly and reveals a short intro line as
a bonus, but the title itself is always on screen for everyone. */
.netflix-row {{
display: flex; gap: 18px; overflow-x: auto; padding: 24px 4px 40px;
scroll-snap-type: x proximity; -webkit-overflow-scrolling: touch;
}}
.netflix-row::-webkit-scrollbar {{ height: 6px; }}
.netflix-row::-webkit-scrollbar-thumb {{ background: var(--rule); border-radius: 3px; }}
.netflix-card {{
flex: 0 0 220px; scroll-snap-align: start; text-decoration: none; color: inherit;
display: block; border-radius: 8px; overflow: hidden; background: var(--bg-card);
border: 1px solid var(--rule); transition: transform 0.2s ease, box-shadow 0.2s ease, border-radius 0.2s ease;
position: relative; transform-origin: center top; cursor: pointer;
}}
.netflix-card:hover {{
transform: scale(1.06);
box-shadow: 0 24px 48px -6px rgba(0,0,0,0.6);
border-radius: 6px 6px 8px 8px;
transition: transform 0.25s ease 150ms, box-shadow 0.25s ease 150ms;
z-index: 5;
}}
.netflix-card-img {{ width: 100%; aspect-ratio: 2/3; overflow: hidden; background: var(--bg-card2); }}
.netflix-card-img img {{ width: 100%; height: 100%; object-fit: cover; display: block; }}
/* Always visible: eyebrow + title + a one-line intro. This is the core fix —
previously this whole block was max-height:0/opacity:0 until :hover. */
.netflix-card-body {{
padding: 12px 14px 16px;
}}
.netflix-card-eyebrow {{
font-family: var(--mono); font-size: 0.72rem; color: var(--text-dim);
letter-spacing: 1px; text-transform: uppercase; margin-bottom: 6px;
display: flex; align-items: center; gap: 6px; flex-wrap: wrap;
}}
.netflix-card-title {{ font-family: var(--serif); font-weight: 700; font-size: 1.05rem; color: var(--text); line-height: 1.28; margin-bottom: 6px; }}
.netflix-card-intro {{ font-size: 0.85rem; color: var(--text-mid); line-height: 1.5; }}
.netflix-card-cta {{
font-family: var(--mono); font-size: 0.74rem; color: var(--red);
letter-spacing: 1px; margin-top: 10px;
}}
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
padding: clamp(40px, 8vw, 80px) clamp(20px, 6vw, 60px); text-align: center;
background: #0a0a0c; position: relative; overflow: hidden;
}}
.contact-wrap::before {{
content: ''; position: absolute; inset: 0;
background-image: repeating-linear-gradient(135deg, rgba(224,52,42,0.07) 0px, rgba(224,52,42,0.07) 2px, transparent 2px, transparent 30px);
}}
.contact-inner {{ position: relative; z-index: 1; }}
.contact-heading {{ font-family: var(--serif); font-size: 2.8rem; font-weight: 900; color: #f5f4f2; margin-bottom: 14px; }}
.contact-heading em {{ color: var(--red); font-style: italic; }}
.contact-sub {{ font-size: 1rem; color: rgba(245,244,242,0.5); margin-bottom: 8px; font-style: italic; font-family: var(--serif); }}
.contact-cta {{ font-size: 0.84rem; color: rgba(245,244,242,0.35); margin-bottom: 36px; font-family: var(--mono); line-height: 1.6; max-width: 480px; }}
.contact-links {{ display: flex; gap: 12px; justify-content: flex-start; flex-wrap: wrap; }}
.contact-link {{
display: inline-block; font-family: var(--mono); font-size: 0.84rem;
color: var(--red); background: rgba(224,52,42,0.08);
border: 1px solid rgba(224,52,42,0.3); padding: 11px 24px;
border-radius: 8px; text-decoration: none; transition: all 0.2s;
}}
.contact-link:hover {{ background: var(--red); color: white; }}

/* FOOTER */
.footer {{
padding: 20px clamp(20px, 6vw, 60px); border-top: 1px solid rgba(255,255,255,0.06);
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
.skills-grid {{ grid-template-columns: 1fr; }}
.minor-card {{ flex-basis: 210px; }}
.illus-grid {{ grid-template-columns: repeat(2,1fr); }}
.consult-card {{ grid-template-columns: 1fr; }}
.consult-img {{ min-height: 140px; }}
.mosaic-grid {{ grid-template-columns: repeat(2,1fr); }}
}}
</style>
""")

# ── DATA ──────────────────────────────────────────────────────────────────────

# ── Tier 1: FLAGSHIP — economics/finance-relevant, the projects that lead ──────
FLAGSHIP_PROJECTS = [
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
        "link": "https://artha-a-i.streamlit.app/",
        "images": [
            "app/static/artha_lead.png",
            "app/static/artha_live1_b64.jpg",
            "app/static/artha_live2_b64.jpg",
        ],
        "video": "app/static/artha_demo_video_b64.mp4",
        "mini_stats": [("4", "Models compared"), ("147", "Months of CPI data"), ("2", "Bugs caught pre-deploy")],
        "methodology": "The forecasting core uses month-over-month % change in CPI — not the raw index — because the raw series is non-stationary (trending upward), violating the core assumption behind ARIMA. Differencing to % change brings it statistically closer to stationary, verified by the same logic an Augmented Dickey-Fuller test would formalize. Four models are compared rather than choosing one upfront because each has a distinct known blind spot: linear AR (only linear relationships), ARIMA (no nonlinear interactions), Prophet (weak on sharp shocks), XGBoost (no built-in trend/seasonality). Complexity has to earn its keep against a simple baseline — not be assumed superior.",
        "globe": False,
    },
    {
        "num": "03",
        "title": "Loan Default Risk Predictor",
        "category": "Machine Learning · Credit Risk",
        "status": "live",
        "status_label": "Live",
        "desc": "A binary classifier predicting loan default probability from 255,347 real Kaggle loan records, built around the hard part most intro projects skip: default is rare (11.6% of records), so raw accuracy is actively misleading — a model that always predicts 'no default' scores ~88% while catching zero real defaulters. The deployed model deliberately trades accuracy for recall, because a missed defaulter costs a lender far more than a false alarm.",
        "features": "Logistic Regression (ROC-AUC 0.753) vs. Random Forest (ROC-AUC 0.754) — near-identical, so the lighter 1KB model ships instead of the 28MB one · class_weight='balanced' instead of discarding 196k majority-class rows · Stratified train/test split preserving the true default rate · Live coefficient-based explanation of each individual prediction",
        "pitch": "Age emerged as the single strongest predictor of default — ahead of interest rate, income, and credit score, which isn't the textbook expectation. It's reported as a data pattern the model found, not a validated causal claim. A planned feature — auto-calculating Debt-to-Income from income and loan terms — was dropped after directly testing the assumption: DTI showed essentially zero correlation (|r| < 0.003) with every other numeric field, meaning it was generated independently in this dataset rather than computed realistically. Surfacing that limitation directly in the app beat silently feeding the model a fabricated value.",
        "stack": ["Python", "Scikit-learn", "Logistic Regression", "Random Forest", "Streamlit", "Pandas"],
        "link": "https://loandefaultriskpredictor.streamlit.app/",
        "images": [
            "app/static/loan_lead.jpg",
            "app/static/loan_app_title_b64.jpg",
            "app/static/loan_result_b64.jpg",
            "app/static/loan_feature_b64.jpg",
            "app/static/loan_eval_b64.jpg",
            "app/static/loan_form_b64.jpg",
            "app/static/loan_result2_b64.jpg",
            "app/static/loan_shap_b64.jpg",
        ],
        "videos": [
            "app/static/loan_demo_video_b64.mp4",
            "app/static/loan_demo_video2_b64.mp4",
        ],
        "mini_stats": [("70%", "Recall on defaulters"), ("11.6%", "True default rate"), ("0.754", "Best ROC-AUC")],
        "methodology": "The cost of a missed defaulter (full unpaid principal) is far higher than a false alarm (an extra manual review), so a model tuned for pure accuracy is economically the wrong target — it would happily under-flag the rare, expensive class to look good on paper. The deployed model catches ~70% of actual defaulters, deliberately trading off precision (~22%) to do it. That trade-off is a design decision justified by asymmetric costs, not a limitation to apologize for.",
        "globe": False,
    },
    {
        "num": "10",
        "title": "PolicySim — Generative Agent-Based Economic Simulation",
        "category": "AI + Economics · Agent-Based Modeling",
        "status": "wip",
        "status_label": "Live Preview · Research Ongoing",
        "desc": "A miniature economy of households, firms, and a government that reasons each round and reacts to live-triggered policy shocks — fuel subsidy cuts, minimum wage hikes, luxury taxes, cash transfers — via a color card or QR code held up to a webcam. Backed by a zero-dependency heuristic reasoning engine (with optional live LLM reasoning via Ollama/Groq), so the demo never breaks on stage. A full statistical evaluation (40 runs × 20 rounds per condition, Welch's t-test, Cohen's d) tested whether a cash transfer actually moves the simulated economy — it does, and in a counter-intuitive direction.",
        "features": "Household/firm/government agents with persistent memory · Round-based simulation loop tracking price level, spending, wealth Gini, income Gini, and unemployment · OpenCV color-card and QR-code policy triggers · 40-run × 20-round statistical evaluation with Welch's t-test and Cohen's d · Robustness-checked at 2x population size · 38-test regression suite · Live Streamlit dashboard with real-time charts and a transparent agent-reasoning feed",
        "pitch": "The headline finding is counter-intuitive: a flat cash transfer to low/mid-income households makes income inequality better (Gini 0.325→0.317, p<0.0001) but makes wealth inequality worse (Gini 0.495→0.531, p<0.0001, Cohen's d=4.13). The mechanism is real economics, not a bug — the transfer is a fixed amount, small relative to high earners' income, so high-tier households keep compounding savings at their usual pace while low/mid households spend a larger share of their now-slightly-bigger income rather than saving it. That's the same gradient in marginal propensity to consume documented in PSID data (~0.15 for the lowest wealth quintile vs. ~0.06 for the highest) and the Penn Wharton Budget Model — reproduced here in miniature, not asserted by hand. The effect held under a 2x population robustness check (d=3.74 vs. d=4.13) and unemployment's flat 0% in the default setup was diagnosed as a labor-supply ceiling, then confirmed by re-running with genuine labor-market slack (unemployment 11.25%→0.00%, p<0.0001).",
        "stack": ["Python", "Ollama · Llama 3.1 8B", "Groq (optional)", "OpenCV", "Streamlit", "Pandas", "NumPy", "Three.js"],
        "link": "https://github.com/shivank-byte/Policy_Sims",
        "images": [
            "app/static/policysim_chart1_b64.jpg",
            "app/static/policysim_chart2_b64.jpg",
        ],
        "mini_stats": [("4.13", "Cohen's d, wealth Gini effect"), ("40×20", "Runs × rounds per condition"), ("38", "Passing regression tests")],
        "methodology": "Deliberately built with a zero-dependency heuristic backend as the default (LLM reasoning via Ollama/Groq is optional, layered on top) — a live demo can't depend on internet access or API uptime, and a research result that costs money per run isn't reproducible by anyone else. Every headline number here comes from actually running the simulation engine end-to-end 40 times per condition, not a mock table — and the most surprising result (wealth Gini rising) was stress-tested twice: once by checking it wasn't a magnitude artifact (it isn't — it's a threshold effect with a mild ceiling, not a dial), and once by doubling the population to rule out a small-sample fluke (the effect held, d=3.74).",
        "globe": False,
    },
    {
        "num": "11",
        "title": "GrainFlow — Optimizing India's Grain Storage & Distribution",
        "category": "Operations Research · Optimization",
        "status": "wip",
        "status_label": "In Progress · Model Built, Deploying Soon",
        "desc": "CAG audits and RTI replies have repeatedly documented Indian food-grain spoiling in open storage — concentrated in surplus states like Punjab and Haryana — while other regions still depend on central-pool shipments running into thousands of crores in avoidable freight and storage losses. GrainFlow is a multi-period transportation-and-inventory linear program across a 10-state network (5 surplus, 5 deficit) that decides how much grain to hold, in which storage type, and when to ship it — then compares that optimized policy against a rule-based 'business as usual' simulation built from documented FCI behavior patterns.",
        "features": "Multi-period LP solved with scipy.optimize.linprog (HiGHS) · decision variables for shipments, covered-vs-CAP storage levels, and an OMSS/ethanol/export release valve · every parameter cited to a public source (PIB procurement bulletins, CAG audit findings, FCI buffer-norm data) or explicitly flagged as a calibrated estimate · interactive Streamlit dashboard with live sliders for spoilage rate, grain value, and freight-cost assumptions · cost-breakdown and storage-trajectory comparison charts · a Plotly shipment-flow map across the network",
        "pitch": "The first cut of the 'business as usual' baseline produced an implausible result — a 94 lakh-tonne annual distress-dump figure, far outside the real cited damage rates. Catching that and recalibrating (more realistic storage capacity, a believable naive decision policy) was the actual engineering work here, not the LP itself, which solved cleanly on the first correct formulation. The recalibrated comparison lands on a defensible ~63% cost reduction and ~21% less spoilage under the optimized policy — a credible efficiency gap, not an inflated one.",
        "stack": ["Python", "SciPy (linprog/HiGHS)", "Streamlit", "Plotly", "Pandas", "NumPy"],
        "link": "https://github.com/shivank-byte/GrainFlow-FCI-Optimizer",
        "images": [
            "app/static/grainflow_lead.png",
        ],
        "mini_stats": [("~63%", "Modeled cost reduction vs. baseline"), ("10", "State network (5 surplus, 5 deficit)"), ("~21%", "Modeled spoilage reduction")],
        "methodology": "Every parameter in the model is either cited directly to a public source (PIB wheat/rice procurement bulletins, CAG audit reports, FCI buffer-norm and actual-stock data) or explicitly labeled as a calibrated estimate where no exact public figure exists — for example, deficit-state demand is derived from NFSA population coverage, not an official allocation table, and per-storage-type spoilage rates are back-calculated to match a cited CAG damage figure for Punjab rather than sourced as an official per-type rate. The baseline is a transparent rule-based simulation of documented FCI behavior patterns (e.g. drawing down covered storage before CAP storage, since it's operationally more convenient — which is exactly where CAG's damage findings concentrate), not a real historical shipment record, since no such granular dataset is public. Full methodology, every citation, and all stated simplifications are in the project's README and blueprint PDF.",
        "globe": False,
    },
]

# Real, embedded live version of the heuristic engine renders on this
# project's detail page — see render_policysim_widget() below. Full 3D
# village view and live LLM reasoning exist in the project's codebase.
# built out. Code (agents, simulation engine, trigger system, stats layer,
# test suite) already exists; this entry will get real images and a link
# once the dashboard is demo-ready.

# ── Tier 2: STRONG TECHNICAL WORK — heavier engineering, less econ-adjacent ────
STRONG_TECH_PROJECTS = [
    {
        "num": "02",
        "title": "Indian Banking Credit Dashboard",
        "category": "Business Analytics · Tableau",
        "status": "live",
        "status_label": "Complete",
        "desc": "A Tableau dashboard unifying 18 inconsistent RBI publications (FY1996–97 to FY2025–26) into one analysis-ready model spanning credit deployment, priority sector lending, CASA, NPAs, digital payments (UPI/IMPS/NEFT), and state-wise credit-deposit ratios. Answers the cross-cutting questions single RBI tables can't: does credit growth track GDP? Do high-CD-ratio states also carry worse NPAs? Has digital payments actually changed deposit behavior?",
        "features": "18 RBI datasets cleaned into one FY-standardized model · Merged-header resolution via openpyxl · Wide-to-long reshaping for state/bank-group data · Floor-adjusted NPA & CASA forecasts · Explicit correlation-vs-causation caveat on the UPI–NPA relationship · 5 dashboard pages, 20 verified charts",
        "pitch": "GNPA peaked at 11.2% after the 2015–2018 Asset Quality Review and fell to 2.75% by FY2023-24 — the sharpest balance-sheet healing event in Indian banking in two decades. UPI volume grew ~10,000x since FY17. The r = -0.94 correlation between UPI growth and NPA decline is striking, but the dashboard explicitly flags it as coincident, not causal — both trends share the same post-2018 policy environment, and claiming otherwise would be methodologically unsound. A less obvious finding: six states (Andhra Pradesh 155%, Tamil Nadu 120%, Telangana 112%, Maharashtra 100%, Rajasthan 93.5%, Delhi 88.6%) run credit-deposit ratios so high they're structurally funding local lending through inter-bank borrowing, while 12 states sit below 50% CD — meaning over half their deposits get intermediated out to fund credit elsewhere. That geographic dimension is invisible in any national aggregate.",
        "stack": ["Python", "Pandas", "openpyxl", "Tableau", "RBI DBIE"],
        "link": "https://github.com/shivank-byte/Indian_banking_dashboard",
        "images": [
            "app/static/banking_lead.webp",
            "app/static/bank_page1_b64.jpg",
            "app/static/bank_page2_b64.jpg",
            "app/static/bank_page3_b64.jpg",
            "app/static/bank_page4_b64.jpg",
            "app/static/bank_page5_b64.jpg",
        ],
        "mini_stats": [("18", "RBI datasets unified"), ("2.75%", "GNPA FY24, from 11.2%"), ("~10,000x", "UPI growth since FY17")],
        "methodology": "Fiscal year labels alone had four inconsistent formats across sources ('2023-24', '2023-2024', 2024, 'Mar-2024') — joining on a naive key would silently mismatch data. A normalizer function maps every source to a common 'YYYY-YY' key before any merge. State-wise data filtering also broke early: an assumption that all-uppercase state names were subtotal rows was wrong (RBI's real state names ARE all-uppercase) and silently dropped every valid row — caught only by printing raw values before filtering.",
        "globe": False,
    },
    {
        "num": "04",
        "title": "Women Literacy Prediction",
        "category": "Machine Learning · Public Policy",
        "status": "live",
        "status_label": "Live",
        "desc": "A district-level classifier predicting women's literacy across 706 Indian districts using NFHS-5 survey data and 12 socio-economic indicators. A tuned Random Forest reaches 83.8% accuracy (R²=0.77 on the regression variant, ±4.6pt mean error) — up from a 50.3% baseline. The more useful result is which indicator matters most: low BMI among women (a malnutrition proxy), not income or school infrastructure, emerges as the top predictor.",
        "features": "706 districts · 36 states/UTs · 12 socio-economic indicators (NFHS-5) · Tuned Random Forest (GridSearchCV) · SHAP TreeExplainer for global + per-district explainability · Auto-generated plain-English district intelligence reports driven entirely by SHAP values (no hardcoded narrative rules) · District-vs-district head-to-head comparison (bar/radar/gap charts) · Interactive choropleth map · Light/dark theme re-skins both UI and Plotly charts",
        "pitch": "Low BMI among women outranking direct education-access indicators as the top predictor reframes the policy question: it suggests literacy gaps in the worst-off districts may be as much a health and nutrition problem as a schools problem — a finding that changes where a rupee of policy spend should go, not just how many schools get built. Kerala and Lakshadweep lead the state rankings; Bihar sits lowest at 57.6% average.",
        "stack": ["Python", "Scikit-learn", "Pandas", "Streamlit", "Matplotlib", "Seaborn", "SHAP", "Plotly"],
        "link": "https://tjqe.streamlit.app",
        "images": [
            "app/static/literacy_lead.jpg",
            "app/static/lit_overview2_b64.jpg",
            "app/static/lit_map2_b64.jpg",
            "app/static/lit_compare2_b64.jpg",
            "app/static/lit_hero_b64.jpg",
            "app/static/lit_compare_b64.jpg",
            "app/static/lit_model_b64.jpg",
        ],
        "videos": ["app/static/lit_demo1_b64.mp4", "app/static/lit_demo2_b64.mp4"],
        "mini_stats": [("706", "Districts analyzed"), ("83.8%", "Tuned Random Forest accuracy"), ("0.77", "Regression R²")],
        "methodology": None,
        "globe": False,
    },
    {
        "num": "05",
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
            "app/static/geosphere_lead.jpg",
        ],
        "gallery": [
            ("app/static/geo_pumice_b64.jpg", "Rock ID card"),
            ("app/static/geo_river_b64.jpg", "Indian rivers module"),
            ("app/static/geo_volcano_b64.jpg", "Active volcano tracker"),
            ("app/static/geo_charts_b64.jpg", "Mineral reserves & seismic zones"),
            ("app/static/geo_obsidian_b64.jpg", "Obsidian mineral ID card"),
            ("app/static/geo_halite_b64.jpg", "Halite mineral ID card"),
            ("app/static/geo_dashboard_b64.jpg", "Mission Control dashboard"),
            ("app/static/geo_quiz_b64.jpg", "Geo Quiz mode"),
            ("app/static/geo_missionctrl_b64.jpg", "Mission Control — Earth at a Glance"),
            ("app/static/geo_diary_b64.jpg", "Field diary — BHU semester log"),
        ],
        "mini_stats": [("21", "Modules built"), ("3800", "Lines, single file"), ("M4.5+", "Live USGS feed")],
        "methodology": None,
        "globe": True,
    },
    {
        "num": "06",
        "title": "Online vs. Offline Learning",
        "category": "Research & Statistics · BHU Thesis",
        "status": "live",
        "status_label": "Published",
        "desc": "B.Sc. (Hons.) Statistics undergraduate thesis at Banaras Hindu University, supervised by Dr. Abhay Kumar Tiwari, Dept. of Statistics. Primary survey of 110 students examining how learning mode affects GPA, stress, sleep, and screen time. Uses correlation analysis, Chi-Square testing, and multiple linear regression. Offline learners show highest GPA (8.36) and lowest stress (9.3/20).",
        "features": "110-respondent primary survey · Chi-Square + regression + correlation · Self-selection bias explicitly acknowledged · Educational analytics",
        "pitch": "High-stress students sleep 1.25 hours less per night than low-stress peers, and 73.6% of respondents report moderate stress overall — the sleep–stress–performance chain shows up consistently across every cross-tab in the study, not just the headline offline-vs-online comparison.",
        "stack": ["Excel", "Pivot Tables", "Chi-Square Test", "Multiple Regression", "Google Forms"],
        "link": "https://github.com/shivank-byte/BHU_Files",
        "images": [
            "app/static/online_offline_lead.jpg",
            "app/static/bhu_fig_34_b64.jpg",
            "app/static/bhu_fig_35_b64.jpg",
            "app/static/bhu_fig_37_b64.jpg",
            "app/static/bhu_fig_38_b64.jpg",
            "app/static/bhu_fig_41_b64.jpg",
            "app/static/bhu_fig_42_b64.jpg",
            "app/static/bhu_fig_43_b64.jpg",
        ],
        "mini_stats": [("110", "Students surveyed"), ("8.36", "Offline learners' avg GPA"), ("9.3/20", "Offline learners' avg stress")],
        "methodology": "The data shows offline learners have the highest GPA and lowest stress — but this correlation has a hidden problem: students don't randomly choose their learning mode. Disciplined, motivated students may self-select offline, and those same traits also produce better grades. A true causal test would require randomly assigned groups — nearly impossible in education research. That limitation is worth naming explicitly.",
        "globe": False,
    },
]

# ── Tier 3: UTILITY / SIDE PROJECTS — fine to include, shouldn't compete for
# top billing. Shown collapsed behind "See all" per the tiering recommendation. ─
UTILITY_PROJECTS = [
    {
        "num": "07", "title": "SmartCalc Pro",
        "category": "Desktop Application",
        "status": "live", "status_label": "Live",
        "desc": "A fully-featured calculator with 5 tabs — Basic, Scientific, Statistics, Finance/Economics (EMI, CAGR, compound interest, inflation adjustment), and Utility. Now ships as both a Tkinter desktop app and an installable PWA (HTML/CSS/JS, no Python required, works offline via service worker). 40+ functions, calculation logic fully separated from GUI — every function independently unit-testable — plus a full calculation history log.",
        "stack": ["Python", "Tkinter", "HTML/CSS/JS", "PWA", "Standard Library"],
        "link": "https://github.com/shivank-byte/SmartCalcPro",
        "images": [
            "app/static/calc_lead.jpg",
            "app/static/smartcalc_live1_b64.jpg",
            "app/static/smartcalc_live2_b64.jpg",
        ],
        "videos": [
            "app/static/smartcalc_demo1_b64.mp4",
            "app/static/smartcalc_demo2_b64.mp4",
        ],
    },
    {
        "num": "08", "title": "Guesstimate Coach",
        "category": "AI Coaching · Fermi Estimation",
        "status": "live", "status_label": "Live",
        "desc": "An AI coach for Fermi/guesstimate problems — the estimation drill used in consulting and product interviews. Walks a learner through 5 coached steps (Clarify, Structure, Estimate, Calculate, Sanity-Check) without ever doing the reasoning for them, then a 6th Verify stage grounds the final guess against a live web-search reference figure instead of a static answer key, graded on Fermi-appropriate order-of-magnitude tolerance (within 2–3x counts as sound).",
        "features": "5-step coaching framework sourced directly from Guesstimation, Guesstimation 2.0, and Hacking the Case Interview · Coaching system prompt explicitly forbidden from issuing numeric estimates or full answers · Live Google Custom Search snippets synthesized into a reference figure via structured JSON, not a static answer key · Fermi tolerance grading (~2–3x counts as sound) instead of meaningless exact-match scoring · Original hand-drawn SVG watermark and custom ruler-tick progress tracker, not templated Streamlit widgets · Zero backend — runs on the user's own Anthropic + Google API keys, held only in session memory",
        "pitch": "The hard part wasn't the estimation logic — it was stopping an open-ended AI assistant from just answering the question. Left unconstrained, a coaching assistant tends to solve the problem for the learner instead of coaching them through it, which defeats the entire point. That's tackled by scoping the system prompt to short, step-bound nudges that react only to the learner's own draft. The other real design problem: there's no API that returns 'the correct answer' to an open-ended estimation question, so the app pulls live search snippets and has the model synthesize a reference figure from unstructured text — which keeps the feedback current (populations and market sizes drift; a static textbook answer key silently goes stale, a live one doesn't) at the cost of being bounded by search-result quality on obscure questions.",
        "stack": ["Python", "Streamlit", "Anthropic API", "Google Custom Search", "Custom SVG UI"],
        "link": "https://guesstimatecoach.streamlit.app/",
        "images": [
            "app/static/guess_lead.jpg",
            "app/static/guess_step_b64.jpg",
            "app/static/guess_panel_b64.jpg",
        ],
        "mini_stats": [("6", "Coached stages"), ("2–3x", "Fermi tolerance for a 'sound' guess"), ("3", "Source frameworks synthesized")],
        "methodology": "Guesstimates are judged on order of magnitude, not precision, so exact-match grading would be meaningless — the grading prompt encodes an explicit Fermi tolerance rule instead (roughly within 2–3x of the inferred reference counts as sound). That grading only checks the final numeric guess, not the validity of the reasoning path, so two very different reasoning approaches can both land a GOOD verdict — a real limitation, not a hidden one. The tool is also deliberately zero-infrastructure: no backend, no stored user data, no session persistence across runs, which means no history or long-term progress tracking either — a privacy/simplicity trade-off made explicitly, not by default.",
    },
    {
        "num": "09", "title": "Resume Optimizer AI",
        "category": "Prompt Engineering · LLM Systems",
        "status": "live", "status_label": "Live",
        "desc": "A single structured prompt acting simultaneously as an ATS compatibility scorer, senior FAANG recruiter critic, and resume rewriter, powered by Gemini 2.5 Flash. Takes a resume (PDF/DOCX/text) plus an optional job description and returns an ATS score, job-match score, missing keywords, and rewritten bullet points using a fixed XYZ accomplishment formula. An anti-fabrication guardrail forces the model to output [X%] placeholders instead of inventing metrics it can't verify.",
        "features": "Dual-persona role prompting (ATS parser + 15-year FAANG recruiter in one call) · Few-shot bad/good bullet calibration anchored to the XYZ formula · Forced structured JSON output with fence-stripping and defensive parsing · Conditional schema logic — job_match_score stays null with no JD, preventing hallucinated comparisons · Two interchangeable front ends (Streamlit web app + Rich-based CLI) sharing one prompt",
        "pitch": "The interesting part isn't the file parsing or the UI — both are intentionally thin. It's that one non-conversational API call reliably does five separate jobs at once: role-setting, few-shot calibration, conditional logic, anti-hallucination guardrails, and strict structured output. The anti-fabrication constraint is the detail worth noticing — if the original resume has no metric, the model is instructed to insert a bracketed placeholder like [X%] rather than invent a specific, false number. That's the difference between a tool that helps someone write a stronger bullet and a tool that quietly puts fabricated statistics on someone's resume.",
        "stack": ["Python", "Gemini 2.5 Flash", "Streamlit", "pdfplumber", "python-docx", "Rich (CLI)"],
        "link": "https://github.com/shivank-byte/Resume_Optimiser",
        "images": [
            "app/static/resume_lead.jpg",
            "app/static/resume_app_title_b64.jpg",
            "app/static/resume_ats_bar_b64.jpg",
            "app/static/resume_score_b64.jpg",
        ],
        "videos": ["app/static/resume_demo_video_b64.mp4"],
        "mini_stats": [("95/100", "Sample ATS score"), ("5", "Prompt engineering techniques"), ("1,500/day", "Free-tier Gemini requests")],
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

# Best-effort simple-icons CDN slug per skill. Not every skill has a real
# brand logo (ARIMA, Regression, Chi-Square, etc. are concepts/techniques,
# not products, and a handful of tools genuinely have no logo in the
# simple-icons library) — those map to None and fall back to a monogram
# tile using MONOGRAM_OVERRIDES below instead of a bare single initial.
# Even a wrong/missing slug degrades gracefully via onerror.
SKILL_ICON_SLUGS = {
    "Python": "python", "SQL": "postgresql",
    "Advanced Excel": "microsoftexcel", "Pandas": "pandas", "NumPy": "numpy",
    "Regression": None, "Scikit-learn": "scikitlearn", "LangChain": "langchain",
    "ARIMA": None, "XGBoost": None,
    "Streamlit": "streamlit", "Plotly": "plotly", "Matplotlib": None, "Seaborn": None,
    "Git": "git", "GitHub": "github", "Flet": None, "Tkinter": None,
    "Survey Design": None, "Chi-Square": None, "Statistical Inference": None,
}

# Plain first-letter monograms collide (SQL and Seaborn both reduce to "S")
# and lose all meaning for single-word skills (ARIMA -> "A"). These give
# every no-logo skill a short, legible, non-colliding fallback label instead.
MONOGRAM_OVERRIDES = {
    "Regression": "R²", "ARIMA": "ARI", "XGBoost": "XGB",
    "Matplotlib": "MPL", "Seaborn": "SNS", "Flet": "FLT", "Tkinter": "TK",
    "Survey Design": "SVY", "Chi-Square": "χ²", "Statistical Inference": "SI",
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
        "status": "live", "status_label": "Complete",
        "image": "app/static/edu_case_classroom.jpg",
        "link": "https://github.com/shivank-byte/Indian-education-policy-case",
        "placeholder": False,
    },
    {
        "tag": "CASE 02 · CORPORATE STRATEGY",
        "title": "Tesla's India Strategy: Why 383 Units, Not 30,000",
        "thesis": "Tesla's import-only, single-SKU, ₹60L+ strategy sold 383 units in a market that grew 84% — the fix is reposition first, localize second, a path modeled to grow volume ~23x by FY29.",
        "deliverables": [
            "4Ps + Porter's Five Forces diagnostic vs. BYD's 47–48 dealership network",
            "Duty-structure cost model: ~₹31.5L per-unit gap from skipping localization",
            "Four strategic paths weighed (Exit / Hold / Reposition / Localize) — scored on investment, timing, and risk",
            "Breakeven model: ₹4,150 Cr investment recovered by FY29 on duty savings alone",
            "Bear/Base/Bull scenario stress test — recommendation holds in all three",
            "Objection-and-rebuttal section addressing Tesla's 2025 global delivery slowdown",
        ],
        "status": "live", "status_label": "Complete",
        "image": "app/static/tesla_car_b64.jpg",
        "link": "https://github.com/shivank-byte/Tesla_India_CaseStudy",
        "placeholder": False,
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

# ── NAV ───────────────────────────────────────────────────────────────────────
mode_icon = "☀️" if DM else "🌙"
col_nav1, col_nav2 = st.columns([10, 1])
with col_nav1:
    html(f"""
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
""")
with col_nav2:
    if st.button(mode_icon, key="theme_toggle"):
        st.session_state.dark_mode = not st.session_state.dark_mode
        st.rerun()

# ── HERO ──────────────────────────────────────────────────────────────────────
# Everything below — background, text, photo, stat row — is now ONE html() call.
# That's the actual fix for "animation disappears / hides behind the photo":
# previously the background lived in its own Streamlit block, a sibling of
# .hero-outer rather than a real child, so it had no real parent height to
# fill and no reliable stacking relationship with the photo. Rendered together
# like this, `position:absolute; inset:0` on the background genuinely fills
# the hero and sits behind the real, once-nested foreground.
_bg_color = "#ff4438" if DM else "#e0342a"
_bg_dim = "rgba(224,52,42,0.20)" if DM else "rgba(224,52,42,0.15)"
_bg_dim2 = "rgba(224,52,42,0.13)" if DM else "rgba(224,52,42,0.10)"

# ── HERO ──────────────────────────────────────────────────────────────────────
# Everything below — background, text, photo, stat row — is now ONE html() call.
# That's the actual fix for "animation disappears / hides behind the photo":
# previously the background lived in its own Streamlit block, a sibling of
# .hero-outer rather than a real child, so it had no real parent height to
# fill and no reliable stacking relationship with the photo. Rendered together
# like this, `position:absolute; inset:0` on the background genuinely fills
# .hero-intro and sits behind the real, once-nested foreground — and stops
# above the stat row, which sits outside .hero-intro entirely.
_bg_color = "#ff4438" if DM else "#e0342a"
_bg_dim = "rgba(224,52,42,0.30)" if DM else "rgba(224,52,42,0.22)"
_bg_dim2 = "rgba(224,52,42,0.20)" if DM else "rgba(224,52,42,0.15)"
_bg_glow = "#ff4438" if DM else "#e0342a"

html(f"""
<div class='hero-outer'>

<div class='hero-intro'>

<div class='hero-data-bg'>

<div class='hbg-glow' style='top:-70px; right:-40px; width:320px; height:320px; background: radial-gradient(circle, {_bg_glow}2e, transparent 70%);'></div>
<div class='hbg-glow' style='bottom:-60px; left:8%; width:260px; height:260px; background: radial-gradient(circle, {_bg_glow}22, transparent 70%);'></div>
<div class='hbg-glow' style='top:30%; left:48%; width:200px; height:200px; background: radial-gradient(circle, {_bg_glow}1c, transparent 70%);'></div>

<svg class='hbg-frag' style='top:3%; left:1%; width:150px; height:100px;' viewBox='0 0 150 100' xmlns='http://www.w3.org/2000/svg'>
<rect class='hbg-bar' x='10' y='40' width='18' height='55' rx='3' fill='{_bg_dim}'/>
<rect class='hbg-bar' x='36' y='20' width='18' height='75' rx='3' fill='{_bg_dim}'/>
<rect class='hbg-bar' x='62' y='50' width='18' height='45' rx='3' fill='{_bg_dim}'/>
<rect class='hbg-bar' x='88' y='10' width='18' height='85' rx='3' fill='{_bg_dim}'/>
</svg>

<svg class='hbg-frag' style='top:2%; right:2%; width:130px; height:130px;' viewBox='0 0 130 130' xmlns='http://www.w3.org/2000/svg'>
<circle cx='65' cy='65' r='48' fill='none' stroke='{_bg_dim}' stroke-width='16'/>
<circle class='hbg-donut' cx='65' cy='65' r='48' fill='none' stroke='{_bg_color}' stroke-width='16'
    stroke-dasharray='300' stroke-dashoffset='80' opacity='0.55' transform='rotate(-90 65 65)'/>
</svg>

<svg class='hbg-frag' style='top:16%; left:32%; width:200px; height:90px;' viewBox='0 0 200 90' xmlns='http://www.w3.org/2000/svg'>
<polyline class='hbg-line' points='10,70 50,45 90,60 130,25 170,40'
    fill='none' stroke='{_bg_dim}' stroke-width='3' stroke-linecap='round' stroke-linejoin='round'/>
<circle class='hbg-dot' cx='130' cy='25' r='5' fill='{_bg_color}' opacity='0.55'/>
<circle class='hbg-dot' cx='170' cy='40' r='5' fill='{_bg_color}' opacity='0.55' style='animation-delay:0.7s'/>
</svg>

<svg class='hbg-frag' style='top:6%; left:60%; width:110px; height:70px;' viewBox='0 0 110 70' xmlns='http://www.w3.org/2000/svg'>
<rect class='hbg-bar' x='6' y='30' width='14' height='34' rx='2' fill='{_bg_dim}' style='animation-delay:0.2s'/>
<rect class='hbg-bar' x='26' y='14' width='14' height='50' rx='2' fill='{_bg_dim}' style='animation-delay:0.5s'/>
<rect class='hbg-bar' x='46' y='24' width='14' height='40' rx='2' fill='{_bg_dim}' style='animation-delay:0.8s'/>
<rect class='hbg-bar' x='66' y='6' width='14' height='58' rx='2' fill='{_bg_dim}' style='animation-delay:1.1s'/>
</svg>

<svg class='hbg-frag' style='top:38%; right:6%; width:150px; height:90px;' viewBox='0 0 150 90' xmlns='http://www.w3.org/2000/svg'>
<circle class='hbg-scatter' cx='15' cy='55' r='5' fill='{_bg_dim}'/>
<circle class='hbg-scatter' cx='45' cy='30' r='4' fill='{_bg_dim}' style='animation-delay:0.4s'/>
<circle class='hbg-scatter' cx='75' cy='65' r='6' fill='{_bg_dim}' style='animation-delay:0.8s'/>
<circle class='hbg-scatter' cx='105' cy='20' r='4' fill='{_bg_dim}' style='animation-delay:1.2s'/>
<circle class='hbg-scatter' cx='135' cy='50' r='5' fill='{_bg_dim}' style='animation-delay:0.6s'/>
</svg>

<svg class='hbg-frag' style='bottom:20%; left:58%; width:90px; height:90px;' viewBox='0 0 90 90' xmlns='http://www.w3.org/2000/svg'>
<circle cx='45' cy='45' r='34' fill='none' stroke='{_bg_dim2}' stroke-width='12'/>
<circle class='hbg-donut' cx='45' cy='45' r='34' fill='none' stroke='{_bg_color}' stroke-width='12'
    stroke-dasharray='214' stroke-dashoffset='140' opacity='0.5' transform='rotate(-90 45 45)' style='animation-delay:0.5s'/>
</svg>

<svg class='hbg-frag' style='bottom:22%; left:4%; width:120px; height:70px;' viewBox='0 0 120 70' xmlns='http://www.w3.org/2000/svg'>
<rect class='hbg-bar' x='8'  y='25' width='16' height='40' rx='2' fill='{_bg_dim}' style='animation-delay:0.3s'/>
<rect class='hbg-bar' x='32' y='10' width='16' height='55' rx='2' fill='{_bg_dim}' style='animation-delay:0.6s'/>
<rect class='hbg-bar' x='56' y='32' width='16' height='33' rx='2' fill='{_bg_dim}' style='animation-delay:0.9s'/>
<rect class='hbg-bar' x='80' y='18' width='16' height='47' rx='2' fill='{_bg_dim}' style='animation-delay:1.1s'/>
</svg>

<svg class='hbg-frag' style='bottom:4%; right:20%; width:170px; height:80px;' viewBox='0 0 170 80' xmlns='http://www.w3.org/2000/svg'>
<path class='hbg-curve' d='M5,70 C40,70 45,10 85,10 C125,10 130,70 165,70' fill='none' stroke='{_bg_dim}' stroke-width='2.5'/>
</svg>

<svg class='hbg-frag' style='top:52%; left:20%; width:100px; height:100px;' viewBox='0 0 100 100' xmlns='http://www.w3.org/2000/svg'>
<g class='hbg-grid-cell'>
<rect x='0' y='0' width='28' height='28' fill='{_bg_dim2}'/><rect x='36' y='0' width='28' height='28' fill='{_bg_dim}'/>
<rect x='72' y='0' width='28' height='28' fill='{_bg_dim2}'/><rect x='0' y='36' width='28' height='28' fill='{_bg_dim}'/>
<rect x='36' y='36' width='28' height='28' fill='{_bg_dim2}'/><rect x='72' y='36' width='28' height='28' fill='{_bg_dim}'/>
</g>
</svg>

<svg class='hbg-frag' style='top:76%; right:4%; width:110px; height:60px;' viewBox='0 0 110 60' xmlns='http://www.w3.org/2000/svg'>
<polyline class='hbg-line' points='6,50 30,20 54,38 78,10 102,26'
    fill='none' stroke='{_bg_dim2}' stroke-width='2.5' stroke-linecap='round' stroke-linejoin='round' style='animation-delay:0.4s'/>
</svg>

<div class='hbg-symbol' style='top:10%; left:46%; font-size:2.4rem; color:{_bg_color}; opacity:0.55;'>Σ</div>
<div class='hbg-symbol' style='top:62%; left:6%; font-size:2rem; color:{_bg_dim}; animation-delay:1s;'>β</div>
<div class='hbg-symbol' style='top:6%; left:78%; font-size:1.8rem; color:{_bg_dim}; animation-delay:2s;'>μ</div>
<div class='hbg-symbol' style='bottom:34%; left:74%; font-size:1.6rem; color:{_bg_dim}; animation-delay:0.6s;'>σ</div>
<div class='hbg-symbol' style='top:66%; right:6%; font-size:1.5rem; color:{_bg_dim}; animation-delay:1.6s;'>√x</div>
<div class='hbg-symbol' style='bottom:8%; left:40%; font-size:1.5rem; color:{_bg_dim}; animation-delay:2.4s;'>π</div>
<div class='hbg-symbol' style='top:24%; right:16%; font-size:1.5rem; color:{_bg_dim}; animation-delay:1.1s;'>∞</div>
<div class='hbg-symbol' style='bottom:14%; right:32%; font-size:1.4rem; color:{_bg_dim2}; animation-delay:1.8s;'>ρ</div>
<div class='hbg-symbol' style='top:30%; left:2%; font-family:var(--mono); font-size:0.85rem; color:{_bg_dim}; animation-delay:0.9s;'>R² = 0.83</div>
<div class='hbg-symbol' style='bottom:42%; right:1%; font-family:var(--mono); font-size:0.85rem; color:{_bg_dim}; animation-delay:1.3s;'>ŷ = β₀+β₁x</div>
<div class='hbg-symbol' style='top:44%; left:44%; font-family:var(--mono); font-size:0.85rem; color:{_bg_dim2}; animation-delay:1.9s;'>p &lt; 0.05</div>
<div class='hbg-symbol' style='top:2%; left:20%; font-family:var(--mono); font-size:0.8rem; color:{_bg_dim2}; animation-delay:2.1s;'>χ² test</div>
<div class='hbg-symbol' style='bottom:2%; left:66%; font-family:var(--mono); font-size:0.8rem; color:{_bg_dim2}; animation-delay:0.3s;'>n = 706</div>

</div>

<div class='hero-grid'>
<div>
<div class='hero-eyebrow'>◈ Portfolio · Operations Research &amp; Applied ML</div>
<div class='hero-hello'>Hello, I'm</div>
<div class='hero-name'>Shivank <em>Thakur</em></div>
<div class='hero-role'>Optimization, statistics, and decisions</div>
<div class='hero-bio'>
I'm an M.Sc. Operations Research student at IIT Bombay with a statistics
foundation from BHU. I build tools that turn messy real-world problems —
resource allocation, forecasting, risk, policy design — into models you can
actually optimize, not just describe: <strong>linear programming, simulation,
and applied ML</strong>, grounded in real data instead of toy datasets.
GeoSphere and a couple of others reflect broader technical curiosity beyond
that core.
</div>
<div class='hero-pitch'>
M.Sc. Operations Research · IIT Bombay<br/>
B.Sc. (Hons.) Statistics · Banaras Hindu University
</div>
<div class='hero-btns'>
<a class='btn-primary' href='#contact'>Let's Talk →</a>
<a class='btn-secondary' href='#projects'>View Work ↓</a>
</div>
</div>
<div>
<div class='photo-zone photo-zone-large'>
<div class='blob-shape'></div>
<img class='blob-photo' src='app/static/photo_b64.jpg' alt='Shivank Thakur'/>
</div>
</div>
</div>

</div>

<div class='stat-row'>
<div class='stat-block'><div class='stat-num'><span>4</span>+</div><div class='stat-label'>Completed &amp; deployed projects</div></div>
<div class='stat-block'><div class='stat-num'><span>21</span></div><div class='stat-label'>GeoSphere modules built</div></div>
<div class='stat-block'><div class='stat-num'><span>706</span></div><div class='stat-label'>Districts analyzed, literacy model</div></div>
<div class='stat-block'><div class='stat-num'><span>82.4<span style="font-size:1.2rem">%</span></span></div><div class='stat-label'>Random Forest accuracy, NFHS-5</div></div>
</div>

</div>
""")



# ── ROBOTIC HAND — persistent floating badge, bottom-right corner ─────────────
# The earlier version used an iframe + JS trick to reach outside Streamlit's
# component sandbox and react to link clicks. That's blocked by browser/Streamlit
# security policies, which is why it rendered nowhere. This version is plain
# HTML5 video + CSS position:fixed, rendered directly by Streamlit (no iframe,
# no cross-frame JS) — it always plays on loop, so it's guaranteed to show up.
html(f"""
<div class='robot-badge'>
<video autoplay muted loop playsinline>
<source src='app/static/robot_2_b64.mp4' type='video/mp4'>
</video>
</div>
""")

# ── TICKER ───────────────────────────────────────────────────────────────────
items = ["Python", "Statistics", "Machine Learning", "Economics", "Streamlit", "LangChain", "ARIMA", "Plotly", "Data Science", "IIT Bombay", "Operations Research", "Linear Programming", "Optimization", "SciPy", "Simulation", "Decision Science"]
ticker_html = "".join(f"<span class='ticker-item'><span>◈</span>{i}</span>" for i in items * 3)
st.markdown(f"<div class='ticker-wrap'><div class='ticker-track'>{ticker_html}</div></div>", unsafe_allow_html=True)

st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)

# ── POLICYSIM — EMBEDDED LIVE ENGINE ───────────────────────────────────────────
# This is a direct, faithful port of the real PolicySim engine's zero-dependency
# "heuristic" backend (agents.py / brain.py / simulation.py / policies.py /
# stats_engine.py from the actual repo) — not a mocked-up stand-in. The full
# project additionally supports live LLM reasoning (Ollama/Groq) and a 3D
# village view; those live in the linked GitHub repo. What runs here is the
# same round-based economy, the same policy math, the same Gini calculation.
import random as _ps_random

_PS_POLICY_LIBRARY = {
    "subsidy_cut": {"label": "Fuel/Input Subsidy Cut", "description": "Cuts the subsidy that lowers firms' input costs.", "default_magnitude": 0.20},
    "minimum_wage_increase": {"label": "Minimum Wage Increase", "description": "Raises the legal wage floor firms must pay.", "default_magnitude": 0.15},
    "luxury_tax": {"label": "Luxury Tax Introduced", "description": "Adds a surcharge on high-income households' tax rate.", "default_magnitude": 0.10},
    "cash_transfer": {"label": "Cash Transfer to Low-Income Households", "description": "Direct payment boosting low/mid income each round.", "default_magnitude": 1000.0},
}


class _PSHousehold:
    def __init__(self, tier, base_income, consumption_propensity, savings):
        self.tier = tier
        self.base_income = base_income
        self.consumption_propensity = consumption_propensity
        self.savings = savings
        self.employed = True
        self.last_spend = 0.0
        self.last_income = 0.0
        self.last_reasoning = ""

    def disposable_income(self, gov):
        income = self.base_income if self.employed else self.base_income * 0.25
        tax_rate = gov["tax_rate"] + (gov["luxury_tax_surcharge"] if self.tier == "high" else 0.0)
        income *= (1 - tax_rate)
        if self.tier == "low":
            income += gov["cash_transfer_low"]
        elif self.tier == "mid":
            income += gov["cash_transfer_mid"]
        return max(income, 0.0)

    def state(self, gov, price_level):
        return dict(role="household", tier=self.tier, disposable_income=self.disposable_income(gov),
                    savings=self.savings, employed=self.employed, price_level=price_level,
                    consumption_propensity=self.consumption_propensity, active_policies=list(gov["active_policies"]))

    def apply_decision(self, decision, gov):
        income = self.disposable_income(gov)
        spend_fraction = min(max(decision["spend_fraction"], 0.0), 1.0)
        spend = income * spend_fraction
        self.savings += (income - spend)
        self.last_spend, self.last_income, self.last_reasoning = spend, income, decision["reasoning"]


class _PSFirm:
    def __init__(self, name, kind, price, wage, unit_cost, employees, max_employees, capacity_per_employee):
        self.name, self.kind = name, kind
        self.price, self.wage, self.unit_cost = price, wage, unit_cost
        self.employees, self.max_employees = employees, max_employees
        self.capacity_per_employee = capacity_per_employee
        self.last_revenue = 0.0
        self.last_demand = 0.0
        self.last_reasoning = ""
        self.last_effective_cost = None

    def state(self, gov):
        return dict(role="firm", name=self.name, kind=self.kind, price=self.price, wage=self.wage,
                    min_wage=gov["minimum_wage"], unit_cost=self.unit_cost, employees=self.employees,
                    max_employees=self.max_employees, last_demand=self.last_demand,
                    capacity_per_employee=self.capacity_per_employee, subsidy_rate=gov["firm_subsidy_rate"],
                    last_effective_cost=self.last_effective_cost, active_policies=list(gov["active_policies"]))

    def apply_decision(self, decision, gov):
        new_wage = max(decision["wage"], gov["minimum_wage"])
        self.price = max(decision["price"], self.unit_cost * 0.5)
        self.wage = new_wage
        self.employees = min(max(self.employees + decision["employees_delta"], 0), self.max_employees)
        self.last_reasoning = decision["reasoning"]
        self.last_effective_cost = self.unit_cost * (1 - gov["firm_subsidy_rate"])


def _ps_gini(values):
    arr = sorted(v for v in values if v is not None)
    n = len(arr)
    if n == 0:
        return 0.0
    mn = min(arr)
    if mn < 0:
        arr = [v - mn for v in arr]
    cum = 0.0
    cum_list = []
    for v in arr:
        cum += v
        cum_list.append(cum)
    total = cum_list[-1]
    if total == 0:
        return 0.0
    weighted = sum((i + 1) * v for i, v in enumerate(arr))
    return (2 * weighted - (n + 1) * total) / (n * total)


def _ps_heuristic_household(state):
    base = state["consumption_propensity"]
    price_level, income, tier, policies = state["price_level"], state["disposable_income"], state["tier"], state["active_policies"]
    adj, reasons = 0.0, []
    if price_level > 1.05:
        adj -= 0.08 * min((price_level - 1.0) * 4, 1.0)
        reasons.append(f"prices up {((price_level-1)*100):.0f}%, cutting back")
    elif price_level < 0.95:
        adj += 0.05
        reasons.append("prices dropped, spending a bit more")
    if not state["employed"]:
        adj -= 0.25
        reasons.append("lost job, spending on essentials only")
    if "cash_transfer" in policies:
        adj += 0.06 if tier in ("low", "mid") else 0.0
        reasons.append("cash transfer gives more room to spend")
    if "luxury_tax" in policies and tier == "high":
        adj -= 0.07
        reasons.append("luxury tax → holding back on discretionary buys")
    if "minimum_wage_increase" in policies and tier == "low":
        adj += 0.04
        reasons.append("higher minimum wage → more take-home pay")
    if "subsidy_cut" in policies:
        adj -= 0.03
        reasons.append("subsidy cut → everyday costs feel tighter")
    if tier == "low":
        adj += 0.02
    elif tier == "high":
        adj -= 0.02
    noise = _ps_random.uniform(-0.02, 0.02)
    spend_fraction = min(max(base + adj + noise, 0.15), 0.98)
    return {"spend_fraction": round(spend_fraction, 3), "reasoning": "; ".join(reasons) if reasons else f"steady income of {income:.0f}, spending as usual"}


def _ps_heuristic_firm(state):
    price, wage, min_wage, unit_cost = state["price"], state["wage"], state["min_wage"], state["unit_cost"]
    demand, employees, max_employees = state["last_demand"], state["employees"], state["max_employees"]
    subsidy_rate, policies = state["subsidy_rate"], state["active_policies"]
    reasons = []
    effective_cost = unit_cost * (1 - subsidy_rate)
    cap_per_emp = state.get("capacity_per_employee", 20.0)
    capacity = max(employees, 1) * cap_per_emp
    utilization = demand / capacity if capacity else 1.0
    price_delta = 0.0
    if utilization > 1.1:
        price_delta = 0.06
        reasons.append("demand outstripping supply → raising prices")
    elif utilization < 0.7:
        price_delta = -0.04
        reasons.append("soft demand → trimming prices")
    new_wage = max(wage, min_wage)
    if min_wage > wage:
        reasons.append(f"minimum wage rose to {min_wage:.2f} → raising pay")
    if new_wage > wage:
        price_delta += (new_wage - wage) / max(unit_cost, 1) * 0.3
    last_effective_cost = state.get("last_effective_cost")
    if last_effective_cost and last_effective_cost > 0:
        cost_change_pct = (effective_cost - last_effective_cost) / last_effective_cost
        if abs(cost_change_pct) > 1e-6:
            price_delta += cost_change_pct * 0.6
            reasons.append(f"input costs {'rose' if cost_change_pct>0 else 'fell'} {abs(cost_change_pct)*100:.1f}% → passing some through to price")
    price_delta = min(max(price_delta, -0.10), 0.10)
    new_price = max(price * (1 + price_delta), effective_cost * 1.05)
    employees_delta = 0
    margin = (new_price - effective_cost) / max(new_price, 0.01)
    if utilization > 1.15 and employees < max_employees:
        employees_delta = 1
        reasons.append("hiring to keep up with demand")
    elif (utilization < 0.6 or margin < 0.05) and employees > 0:
        employees_delta = -1
        reasons.append("weak demand/margins → cutting staff")
    noise = _ps_random.uniform(-0.01, 0.01)
    new_price = round(max(new_price * (1 + noise), 0.5), 2)
    return {"price": new_price, "wage": round(new_wage, 2), "employees_delta": employees_delta,
            "reasoning": "; ".join(reasons) if reasons else "holding price and staffing steady"}


class _PSSimulation:
    def __init__(self):
        self.government = dict(tax_rate=0.15, luxury_tax_surcharge=0.0, minimum_wage=12.0,
                                cash_transfer_low=0.0, cash_transfer_mid=0.0, firm_subsidy_rate=0.10,
                                active_policies={})
        hh_spec = [("low", 24000, 0.85, 4), ("mid", 50000, 0.65, 4), ("high", 120000, 0.45, 2)]
        self.households = []
        for tier, income, prop, n in hh_spec:
            for _ in range(n):
                self.households.append(_PSHousehold(tier, income, prop, savings=income * _ps_random.uniform(0.5, 2.0)))
        self.firms = [
            _PSFirm("Corner Shop", "small_shop", 200.0, 220.0, 120.0, 3, 6, 300.0),
            _PSFirm("Metro Industries", "large_firm", 500.0, 280.0, 300.0, 8, 15, 20.0),
        ]
        self.round_num = 0
        self.history = []
        self.thought_feed = []
        self._base_price = None

    def apply_policy_event(self, policy_id):
        spec = _PS_POLICY_LIBRARY[policy_id]
        mag = spec["default_magnitude"]
        gov = self.government
        if policy_id in gov["active_policies"]:
            m = gov["active_policies"][policy_id]
            if policy_id == "subsidy_cut":
                gov["firm_subsidy_rate"] = min(1.0, gov["firm_subsidy_rate"] / max(1e-6, 1 - m))
            elif policy_id == "minimum_wage_increase":
                gov["minimum_wage"] /= (1 + m)
            elif policy_id == "luxury_tax":
                gov["luxury_tax_surcharge"] = max(0.0, gov["luxury_tax_surcharge"] - m)
            elif policy_id == "cash_transfer":
                gov["cash_transfer_low"] = max(0.0, gov["cash_transfer_low"] - m)
                gov["cash_transfer_mid"] = max(0.0, gov["cash_transfer_mid"] - m * 0.4)
            del gov["active_policies"][policy_id]
        else:
            if policy_id == "subsidy_cut":
                gov["firm_subsidy_rate"] = max(0.0, gov["firm_subsidy_rate"] * (1 - mag))
            elif policy_id == "minimum_wage_increase":
                gov["minimum_wage"] *= (1 + mag)
            elif policy_id == "luxury_tax":
                gov["luxury_tax_surcharge"] += mag
            elif policy_id == "cash_transfer":
                gov["cash_transfer_low"] += mag
                gov["cash_transfer_mid"] += mag * 0.4
            gov["active_policies"][policy_id] = mag

    def _price_level(self):
        avg = sum(f.price for f in self.firms) / len(self.firms)
        if self._base_price is None:
            self._base_price = avg
        return avg / self._base_price if self._base_price else 1.0

    def run_round(self):
        self.round_num += 1
        for firm in self.firms:
            decision = _ps_heuristic_firm(firm.state(self.government))
            firm.apply_decision(decision, self.government)
            self.thought_feed.append({"round": self.round_num, "agent": f"Firm:{firm.name}", "thought": firm.last_reasoning})

        price_level = self._price_level()
        total_spending = 0.0
        for hh in self.households:
            decision = _ps_heuristic_household(hh.state(self.government, price_level))
            hh.apply_decision(decision, self.government)
            total_spending += hh.last_spend
            self.thought_feed.append({"round": self.round_num, "agent": f"Household:{hh.tier}", "thought": hh.last_reasoning})
        self.thought_feed = self.thought_feed[-30:]

        weights = [1 / max(f.price, 0.01) for f in self.firms]
        wsum = sum(weights) or 1
        for firm, w in zip(self.firms, weights):
            demand_share = total_spending * (w / wsum)
            firm.last_demand = demand_share / max(firm.price, 0.01)
            firm.last_revenue = demand_share

        total_jobs = sum(f.employees for f in self.firms)
        employed_households = min(len(self.households), total_jobs)
        for i, hh in enumerate(self.households):
            hh.employed = i < employed_households
        unemployment_rate = 1 - (employed_households / len(self.households)) if self.households else 0.0

        incomes = [hh.disposable_income(self.government) for hh in self.households]
        wealth = [hh.savings for hh in self.households]
        stats = dict(round=self.round_num, price_level=price_level, total_spending=total_spending,
                     gini=_ps_gini(wealth), gini_income=_ps_gini(incomes), unemployment_rate=unemployment_rate)
        self.history.append(stats)
        return stats


def render_policysim_widget():
    if "ps_sim" not in st.session_state:
        st.session_state.ps_sim = _PSSimulation()
    sim = st.session_state.ps_sim

    html("""
<div style='margin-top:8px;padding:20px 22px;border:1px solid var(--rule);border-radius:16px;background:var(--bg-card);'>
<div class='proj-eyebrow' style='margin-bottom:6px;'>◈ LIVE, RUNNING IN-BROWSER</div>
<div style='font-family:var(--serif);font-weight:700;font-size:1.15rem;margin-bottom:6px;'>Try the real engine</div>
<div style='font-size:0.86rem;color:var(--text-mid);line-height:1.55;'>
This is the actual zero-dependency heuristic backend from the PolicySim repo — 10 households across 3 income
tiers, 2 firms, 1 government — not a mockup. Trigger a policy, step the economy forward, and watch price level,
inequality, and unemployment respond. (The full project also supports live LLM reasoning and a 3D village view.)
</div>
</div>
""")

    ctrl_cols = st.columns([1, 1, 2])
    if ctrl_cols[0].button("Step round →", key="ps_step", use_container_width=True):
        sim.run_round()
    if ctrl_cols[1].button("↺ Restart", key="ps_restart", use_container_width=True):
        st.session_state.ps_sim = _PSSimulation()
        sim = st.session_state.ps_sim
    ctrl_cols[2].markdown(f"<div style='padding-top:8px;font-family:var(--mono);font-size:0.82rem;color:var(--text-dim);'>Round {sim.round_num}</div>", unsafe_allow_html=True)

    pol_cols = st.columns(4)
    for i, (policy_id, spec) in enumerate(_PS_POLICY_LIBRARY.items()):
        active = policy_id in sim.government["active_policies"]
        label = f"{'🟢' if active else '⚪'} {spec['label']}"
        if pol_cols[i].button(label, key=f"ps_policy_{policy_id}", use_container_width=True, help=spec["description"]):
            sim.apply_policy_event(policy_id)

    if sim.history:
        latest = sim.history[-1]
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Price index", f"{latest['price_level']:.2f}")
        m2.metric("Unemployment", f"{latest['unemployment_rate']*100:.0f}%")
        m3.metric("Wealth Gini", f"{latest['gini']:.3f}")
        m4.metric("Income Gini", f"{latest['gini_income']:.3f}")

        rounds = [h["round"] for h in sim.history]
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=rounds, y=[h["price_level"] for h in sim.history], name="Price index", line=dict(color="#e0342a")))
        fig.add_trace(go.Scatter(x=rounds, y=[h["gini"] for h in sim.history], name="Wealth Gini", line=dict(color="#4c72a8")))
        fig.add_trace(go.Scatter(x=rounds, y=[h["gini_income"] for h in sim.history], name="Income Gini", line=dict(color="#6fae7a")))
        fig.add_trace(go.Scatter(x=rounds, y=[h["unemployment_rate"] for h in sim.history], name="Unemployment", line=dict(color="#c9a227")))
        bg_color = "#0a0a0c" if DM else "#f8f7f4"
        fig.update_layout(height=280, margin=dict(l=0, r=0, t=10, b=0), paper_bgcolor=bg_color, plot_bgcolor=bg_color,
                           font=dict(color="#f5f4f2" if DM else "#0a0a0c", size=11),
                           legend=dict(orientation="h", yanchor="bottom", y=1.02))
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

        with st.expander("💬 Agent reasoning feed (heuristic, plain-language)"):
            for t in reversed(sim.thought_feed[-12:]):
                st.markdown(f"<div style='font-family:var(--mono);font-size:0.78rem;color:var(--text-mid);margin-bottom:6px;'><b>R{t['round']} · {t['agent']}</b> — {t['thought']}</div>", unsafe_allow_html=True)
    else:
        st.caption("Press **Step round →** to run the first round, or trigger a policy first to see its effect from round 1.")


# ── PROJECTS (tiered: Flagship → Strong Technical → Utility) ──────────────────
ECONOMIC_LOGIC_TITLES = {"Online vs. Offline Learning", "Women Literacy Prediction"}
ALL_TIERED_PROJECTS = {p["num"]: p for p in FLAGSHIP_PROJECTS + STRONG_TECH_PROJECTS + UTILITY_PROJECTS}


def _first_sentence(text, max_len=150):
    """Short intro line for a compact card — first sentence of desc, hard-capped."""
    if not text:
        return ""
    cut = text.split(". ")[0].strip()
    if not cut.endswith("."):
        cut += "."
    if len(cut) > max_len:
        cut = cut[:max_len].rsplit(" ", 1)[0] + "…"
    return cut


def render_netflix_row(projects):
    """Horizontally-scrollable vertical poster cards — Netflix style. Each
    whole card is a plain <a href='?project=NUM'> link: hovering glows it,
    clicking sets the ?project= query param, which we read below to swap
    into the full detail view. No custom JS/components needed."""
    cards = ""
    for p in projects:
        lead_img = (p.get("images") or [None])[0]
        img_html = f"<img loading='lazy' src='{lead_img}' alt='{p['title']}'/>" if lead_img else ""
        cards += f"""
<a class='netflix-card' href='?project={p["num"]}#projects'>
<div class='netflix-card-img'>{img_html}</div>
<div class='netflix-card-body'>
<div class='netflix-card-eyebrow'>{p["num"]} · {p["category"]} <span class='status-badge {status_class[p["status"]]}'>{p["status_label"]}</span></div>
<div class='netflix-card-title'>{p["title"]}</div>
<div class='netflix-card-intro'>{_first_sentence(p.get("desc"), 95)}</div>
<div class='netflix-card-cta'>VIEW FULL CASE STUDY ↗</div>
</div>
</a>
"""
    html(f"<div class='netflix-row'>{cards}</div>")


def render_project_detail(p):
    """Full editorial write-up — desc, features, pitch, stack, image collage,
    mini-stats, methodology. Reached by clicking through from a compact card."""
    imgs_html = ""
    imgs = p.get("images", [])
    if len(imgs) > 4:
        tiles = "".join(f"<img loading='lazy' src='{src}' alt='{p['title']}'/>" for src in imgs)
        imgs_html = f"<div class='proj-collage proj-collage-many'>{tiles}</div>"
    elif len(imgs) == 4:
        imgs_html = f"""<div class='proj-collage'>
            <img loading='lazy' src='{imgs[0]}' alt='{p["title"]}'/><img loading='lazy' src='{imgs[1]}' alt='{p["title"]}'/>
            <img loading='lazy' src='{imgs[2]}' alt='{p["title"]}'/><img loading='lazy' src='{imgs[3]}' alt='{p["title"]}'/></div>"""
    elif len(imgs) == 3:
        imgs_html = f"""<div class='proj-collage proj-collage-3'>
            <img loading='lazy' class='proj-collage-lead' src='{imgs[0]}' alt='{p["title"]}'/>
            <img loading='lazy' src='{imgs[1]}' alt='{p["title"]}'/><img loading='lazy' src='{imgs[2]}' alt='{p["title"]}'/></div>"""
    elif len(imgs) >= 2:
        imgs_html = f"""<div class='proj-collage'><img loading='lazy' src='{imgs[0]}' alt='{p["title"]}'/><img loading='lazy' src='{imgs[1]}' alt='{p["title"]}'/></div>"""
    elif imgs:
        imgs_html = f"<div class='proj-collage-single'><img loading='lazy' src='{imgs[0]}' alt='{p['title']}'/></div>"

    stack_html = "".join(f"<span class='proj-tag'>{s}</span>" for s in p.get("stack", []))
    link_html = f"<a class='proj-link' href='{p['link']}' target='_blank'>Visit project ↗</a>" if p.get("link") else ""
    pitch_html = f"<div class='proj-features'>{p['pitch']}</div>" if p.get("pitch") else ""
    mini_stats_html = ""
    if p.get("mini_stats"):
        mini_stats_html = "<div class='proj-mini-stats'>" + "".join(
            f"<div class='proj-mini-stat'><div class='proj-mini-stat-num'>{n}</div><div class='proj-mini-stat-label'>{lbl}</div></div>"
            for n, lbl in p["mini_stats"]
        ) + "</div>"

    if p.get("globe"):
        col_meta, col_globe = st.columns([1, 1])
        with col_meta:
            html(f"""
<div style='padding: 12px 0 24px;'>
<div class='proj-eyebrow'>{p["num"]} &nbsp;·&nbsp; {p["category"]} &nbsp;·&nbsp; <span class='status-badge {status_class[p["status"]]}'>{p["status_label"]}</span></div>
<div class='proj-title-big'>{p["title"]}</div>
<div class='proj-desc-big'>{p["desc"]}</div>
<div class='proj-features'>{p.get("features","")}</div>
{pitch_html}
<div class='proj-stack'>{stack_html}</div>
<div class='proj-actions'>{link_html}</div>
</div>
""")
        with col_globe:
            html("<div class='proj-img-col'>")
            bg_color = "#0a0a0c" if DM else "#f8f7f4"
            line_color = "rgba(224,52,42,0.6)"
            ocean_color = "#0d1b2a" if DM else "#cce4f5"
            land_color = "#1a2d1a" if DM else "#c8e6c9"
            fig_globe = go.Figure(go.Scattergeo(
                lon=[72.8, 77.2, 80.9, 88.3, 78.5, 76.9, 72.5, 68.0, 74.8, 85.3, 91.7, 93.9],
                lat=[18.9, 28.6, 13.1, 22.6, 17.4, 30.7, 23.0, 23.0, 32.7, 20.3, 26.2, 24.8],
                mode="markers", marker=dict(size=6, color=line_color, opacity=0.85, symbol="circle"),
                name="Seismic zones", hovertemplate="India seismic zone<extra></extra>",
            ))
            fig_globe.add_trace(go.Scattergeo(
                lon=[68, 77, 88, 97, 92, 80, 77, 72, 68], lat=[23, 35, 35, 28, 8, 8, 8, 20, 23],
                mode="lines", line=dict(width=1.5, color=line_color), name="India outline", hoverinfo="skip",
            ))
            fig_globe.update_layout(
                geo=dict(
                    projection_type="orthographic", projection_rotation=dict(lon=80, lat=20, roll=0),
                    showland=True, landcolor=land_color, showocean=True, oceancolor=ocean_color,
                    showlakes=False, showcountries=True, countrycolor="rgba(255,255,255,0.1)",
                    showcoastlines=True, coastlinecolor="rgba(255,255,255,0.15)", bgcolor=bg_color,
                ),
                paper_bgcolor=bg_color, plot_bgcolor=bg_color, margin=dict(l=0, r=0, t=0, b=0),
                height=360, showlegend=False,
            )
            st.plotly_chart(fig_globe, use_container_width=True, config={"scrollZoom": True, "displayModeBar": False})
            if p.get("mini_stats"):
                html(mini_stats_html)
            if p.get("gallery"):
                gallery_html = "".join(
                    f"<div class='illus-card'><img loading='lazy' src='{src}' alt='{cap}'/><div class='illus-cap'>{cap}</div></div>"
                    for src, cap in p["gallery"]
                )
                html(f"<div class='proj-gallery'>{gallery_html}</div>")
            html("</div>")
    else:
        html(f"""
<div class='proj-editorial'>
<div class='proj-num'>{p["num"]}</div>
<div class='proj-meta'>
<div class='proj-eyebrow'>{p["category"]} &nbsp;·&nbsp; <span class='status-badge {status_class[p["status"]]}'>{p["status_label"]}</span></div>
<div class='proj-title-big'>{p["title"]}</div>
<div class='proj-desc-big'>{p["desc"]}</div>
<div class='proj-features'>{p.get("features","")}</div>
{pitch_html}
<div class='proj-stack'>{stack_html}</div>
<div class='proj-actions'>{link_html}</div>
</div>
<div class='proj-img-col'>{imgs_html}{mini_stats_html}</div>
</div>
""")

    if p.get("methodology"):
        label = "🔬 Economic Thinking" if any(t in p["title"] for t in ECONOMIC_LOGIC_TITLES) else "💡 Why This Project Matters"
        with st.expander(label, expanded=True):
            st.markdown(p["methodology"])

    videos = p.get("videos") or ([p["video"]] if p.get("video") else [])
    if videos:
        # Lazy-loaded: each video's base64 payload is only sent to the browser
        # once the person actually asks for it, so it doesn't add load weight
        # to everyone just viewing the detail page.
        shown = st.session_state.video_shown.get(p["num"], set())
        cols = st.columns(len(videos)) if len(videos) > 1 else None
        for i, vsrc in enumerate(videos):
            label = "▶  Watch demo video" if len(videos) == 1 else f"▶  Watch demo {i+1}"
            container = cols[i] if cols is not None else None
            target = container if container is not None else st
            if i not in shown:
                if target.button(label, key=f"playvid_{p['num']}_{i}"):
                    shown = set(shown) | {i}
                    st.session_state.video_shown[p["num"]] = shown
                    st.rerun()
            else:
                video_html = f"""
<div style='margin-top:12px; border-radius:14px; overflow:hidden; border:1px solid var(--rule);'>
<video controls autoplay muted playsinline style='width:100%; display:block;'>
<source src='{vsrc}' type='video/mp4'>
</video>
</div>
"""
                if container is not None:
                    with container:
                        html(video_html)
                else:
                    html(video_html)

    if p["num"] == "10":
        render_policysim_widget()


# Read ?project=NUM from the URL (set by clicking a Netflix card's <a> link).
# This is what actually drives "click a card → opens full detail" — a plain
# anchor tag, no custom JS component, no cross-frame tricks.
_qp_project = st.query_params.get("project")
if _qp_project:
    st.session_state.selected_project = _qp_project

if st.session_state.selected_project and st.session_state.selected_project in ALL_TIERED_PROJECTS:
    # ── PROJECT DETAIL "PAGE" — replaces the grid entirely until Back is pressed ──
    sel = ALL_TIERED_PROJECTS[st.session_state.selected_project]
    html("<div class='section' id='projects'></div>")
    st.markdown("<div style='padding: 0 clamp(20px, 6vw, 60px);'>", unsafe_allow_html=True)
    if st.button("← Back to all projects", key="back_to_projects"):
        st.session_state.selected_project = None
        if "project" in st.query_params:
            del st.query_params["project"]
        st.rerun()
    render_project_detail(sel)
    st.markdown("</div>", unsafe_allow_html=True)
else:
    # ── TIER 1: FLAGSHIP ──
    html("""
<div class='section' id='projects'>
<div class='section-label'>◈ Flagship Projects</div>
<div class='section-heading'>Completed Work</div>
<div class='section-sub'>Applied ML, optimization, and policy work — scroll, hover, click a card for the full write-up.</div>
</div>
""")
    st.markdown("<div style='padding: 0 clamp(20px, 6vw, 60px);'>", unsafe_allow_html=True)
    render_netflix_row(FLAGSHIP_PROJECTS)
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)

    # ── TIER 2: STRONG TECHNICAL WORK ──
    html("""
<div class='section section-alt'>
<div class='section-label'>◈ Strong Technical Work</div>
<div class='section-heading'>Deeper Engineering</div>
<div class='section-sub'>Heavier builds, further from the core focus — still worth a close look.</div>
</div>
""")
    st.markdown("<div style='padding: 0 clamp(20px, 6vw, 60px) 60px;background:var(--bg-card);'>", unsafe_allow_html=True)
    render_netflix_row(STRONG_TECH_PROJECTS)
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)

    # ── TIER 3: UTILITY / SIDE PROJECTS — collapsed behind "See all" ──
    html("""
<div class='section' id='lab'>
<div class='section-label'>◈ Utility &amp; Side Projects</div>
<div class='section-heading'>Also Built</div>
<div class='section-sub'>Fine to include, don't need top billing. Tap to reveal.</div>
</div>
""")
    st.markdown("<div style='padding: 0 clamp(20px, 6vw, 60px) 60px;'>", unsafe_allow_html=True)
    if not st.session_state.show_utility_projects:
        if st.button(f"See all {len(UTILITY_PROJECTS)} utility projects →", key="show_utility_btn"):
            st.session_state.show_utility_projects = True
            st.rerun()
    else:
        render_netflix_row(UTILITY_PROJECTS)
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)

# ── SKILLS ────────────────────────────────────────────────────────────────────
html("""
<div class='section' id='skills'>
<div class='section-label'>◈ Toolkit</div>
<div class='section-heading'>Skills</div>
<div class='section-sub'>Grouped by what they're for — not where they'd sit on a resume.</div>
</div>
""")

st.markdown("<div style='padding: 0 clamp(20px, 6vw, 60px) 32px;'>", unsafe_allow_html=True)
skill_blocks = ""
for group, items in SKILLS.items():
    tiles = ""
    for s in items:
        slug = SKILL_ICON_SLUGS.get(s)
        initials = MONOGRAM_OVERRIDES.get(s) or "".join(w[0] for w in s.replace("-", " ").split()[:2]).upper()
        if slug:
            icon_html = f"""<img loading='lazy' src='https://cdn.simpleicons.org/{slug}' alt='{s}' class='skill-tile-icon'
                onerror="this.style.display='none'; this.nextElementSibling.style.display='flex';"/>
                <div class='skill-tile-monogram' style='display:none;'>{initials}</div>"""
        else:
            icon_html = f"<div class='skill-tile-monogram'>{initials}</div>"
        tiles += f"<div class='skill-tile'>{icon_html}<div class='skill-tile-label'>{s}</div></div>"
    skill_blocks += f"<div class='skill-block'><div class='skill-block-title'>{group}</div><div class='skill-tile-row'>{tiles}</div></div>"
st.markdown(f"<div class='skills-grid'>{skill_blocks}</div>", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)

# ── DEEP DIVES (CASE STUDIES) ─────────────────────────────────────────────────
html("""
<div class='section section-alt' id='deep-dives'>
<div class='section-label'>◈ Deep Dives</div>
<div class='section-heading'>Case Studies</div>
<div class='section-sub'>Consulting-style research with structured frameworks, quantitative models, and implementation roadmaps.</div>
</div>
""")

st.markdown("<div style='padding: 0 clamp(20px, 6vw, 60px) 60px; background: var(--bg-card);'>", unsafe_allow_html=True)
for c in CONSULTING_CASES:
    if c["placeholder"]:
        html(f"""
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
""")
    else:
        dels = "".join(f"<div class='consult-del'>{d}</div>" for d in c["deliverables"])
        link_html = f"<a class='proj-link' href='{c['link']}' target='_blank' style='margin-top:14px;display:inline-block;'>View full report ↗</a>" if c.get("link") else ""
        html(f"""
<div class='consult-card'>
<div class='consult-img' style='background-image:url("{c["image"]}");'></div>
<div class='consult-body'>
<div class='consult-tag'>{c["tag"]}</div>
<div class='consult-title'>{c["title"]}</div>
{dels}
<div style='margin-top:14px;'><span class='status-badge {status_class[c["status"]]}'>{c["status_label"]}</span></div>
{link_html}
</div>
</div>
""")
st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)

# ── MOSAIC CLOSING GRID ───────────────────────────────────────────────────────
mosaic_imgs = [
    "https://images.unsplash.com/photo-1551288049-bebda4e38f71?w=600&q=80",
    "https://images.unsplash.com/photo-1614728263952-84ea256f9679?w=600&q=80",
    "https://images.unsplash.com/photo-1460925895917-afdab827c52f?w=600&q=80",
    "https://images.unsplash.com/photo-1504868584819-f8e8b4b6d7e3?w=600&q=80",
]
cells = "".join(f"<div class='mosaic-cell'><img loading='lazy' src='{u}' alt='portfolio'/></div>" for u in mosaic_imgs)
st.markdown(f"<div class='mosaic-grid'>{cells}</div>", unsafe_allow_html=True)

# ── CONTACT — doodle blended into the section, adjacent to one merged closing line ──
html(f"""
<div class='contact-wrap' id='contact'>
<div class='contact-inner'>
<div class='contact-flex'>
<div class='contact-doodle-wrap'>
<video autoplay muted loop playsinline class='contact-doodle-video'>
<source src='app/static/hero_doodle_b64.mp4' type='video/mp4'>
</video>
</div>
<div class='contact-text'>
<div class='contact-heading'>Thanks for stopping by — let's build something <em>that matters.</em></div>
<div class='contact-sub'>M.Sc. Operations Research · IIT Bombay · 2026-28</div>
<div class='contact-cta'>
I'm looking for opportunities at the intersection of operations research, applied ML, and real-world impact — analytics, optimization, or research roles where rigorous thinking and engineering skill both count.<br/>
Open to coffee chats, project collaboration, or campus recruiting at IIT Bombay.
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
</div>
</div>
""")

# ── FOOTER ────────────────────────────────────────────────────────────────────
html(f"""
<div class='footer'>
<div class='footer-left'>ARTHASUTRA · {CURRENT_YEAR}</div>
<div class='footer-right'>Designed &amp; built by Shivank Thakur</div>
</div>
""")
