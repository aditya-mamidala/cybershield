import re
import math
import streamlit as st
from urllib.parse import urlparse

st.set_page_config(
    page_title="CyberShield — URL Intelligence",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Space+Grotesk:wght@500;600;700&display=swap');

:root {
  --bg:#05070c; --panel:rgba(15,20,31,.72); --border:rgba(148,163,184,.16);
  --muted:#8c98aa; --text:#f5f7fb; --accent:#6ee7ff; --accent2:#8b7cff;
}
.stApp {
  background:
    radial-gradient(circle at 15% 10%, rgba(110,231,255,.10), transparent 30%),
    radial-gradient(circle at 85% 18%, rgba(139,124,255,.10), transparent 28%),
    radial-gradient(circle at 50% 100%, rgba(0,214,170,.06), transparent 30%),
    var(--bg);
  color:var(--text); font-family:'Inter',sans-serif;
}
.block-container {max-width:1180px; padding:30px 28px 60px;}
#MainMenu, footer, header {visibility:hidden;}

.brand {
  display:flex; align-items:center; justify-content:space-between; margin-bottom:42px;
}
.brand-left {display:flex;align-items:center;gap:12px;}
.logo {
 width:42px;height:42px;border-radius:13px;display:grid;place-items:center;
 background:linear-gradient(135deg,#6ee7ff,#8b7cff);
 color:#061019;font-size:21px;box-shadow:0 0 30px rgba(110,231,255,.22);
}
.brand-name {font-family:'Space Grotesk';font-weight:700;font-size:19px;letter-spacing:-.5px;}
.brand-name span {color:#6ee7ff;}
.status {
 border:1px solid rgba(110,231,255,.20); background:rgba(110,231,255,.06);
 padding:7px 12px;border-radius:999px;color:#a8efff;font-size:12px;font-weight:600;
}

.hero {text-align:center;padding:15px 0 34px;}
.eyebrow {color:#6ee7ff;text-transform:uppercase;letter-spacing:2.8px;font-size:11px;font-weight:700;}
.hero h1 {
 font-family:'Space Grotesk';font-size:clamp(40px,6vw,70px);line-height:1.0;
 letter-spacing:-3px;margin:14px 0 14px;
 background:linear-gradient(90deg,#fff,#aeb9ca 45%,#6ee7ff);
 -webkit-background-clip:text;-webkit-text-fill-color:transparent;
}
.hero p {max-width:650px;margin:auto;color:#929db0;font-size:15px;line-height:1.7;}

.search-card {
 margin:8px auto 30px; max-width:940px; padding:8px;
 border:1px solid var(--border); border-radius:20px;
 background:rgba(15,20,31,.82); box-shadow:0 20px 80px rgba(0,0,0,.34);
}
div[data-testid="stTextInput"] input {
 background:rgba(4,7,13,.85)!important;border:1px solid rgba(148,163,184,.14)!important;
 color:white!important;border-radius:13px!important;padding:18px!important;font-size:15px!important;
}
div[data-testid="stButton"] button {
 border:0!important;border-radius:13px!important;padding:13px 22px!important;
 background:linear-gradient(135deg,#6ee7ff,#8b7cff)!important;color:#061019!important;
 font-weight:800!important;box-shadow:0 10px 35px rgba(110,231,255,.15)!important;
 transition:.2s ease!important;
}
div[data-testid="stButton"] button:hover {transform:translateY(-1px);filter:brightness(1.08);}

.section-title {font-family:'Space Grotesk';font-size:18px;font-weight:700;margin:25px 0 14px;}
.metric-grid {display:grid;grid-template-columns:repeat(3,1fr);gap:14px;margin-bottom:20px;}
.metric {
 padding:20px;border:1px solid var(--border);border-radius:17px;background:var(--panel);
 backdrop-filter:blur(18px);
}
.metric .label {color:#7f8b9e;font-size:11px;text-transform:uppercase;letter-spacing:1.4px;}
.metric .value {font-family:'Space Grotesk';font-size:24px;font-weight:700;margin-top:8px;}
.metric .sub {color:#7f8b9e;font-size:12px;margin-top:5px;}

.result {
 padding:26px;border:1px solid var(--border);border-radius:22px;
 background:linear-gradient(145deg,rgba(15,20,31,.92),rgba(8,12,20,.75));
 box-shadow:0 20px 80px rgba(0,0,0,.25);
}
.riskrow {display:flex;justify-content:space-between;align-items:center;gap:20px;}
.badge {padding:8px 12px;border-radius:999px;font-size:12px;font-weight:800;letter-spacing:.8px;}
.high {background:rgba(255,75,100,.10);color:#ff8090;border:1px solid rgba(255,75,100,.2);}
.medium {background:rgba(255,193,74,.10);color:#ffd27a;border:1px solid rgba(255,193,74,.2);}
.low {background:rgba(55,225,165,.10);color:#76f0be;border:1px solid rgba(55,225,165,.2);}
.score {font-family:'Space Grotesk';font-size:48px;font-weight:700;line-height:1;}
.score small {font-family:Inter;font-size:13px;color:#7f8b9e;font-weight:500;}
.bar {height:7px;background:#1a2230;border-radius:99px;overflow:hidden;margin-top:18px;}
.fill {height:100%;border-radius:99px;background:linear-gradient(90deg,#6ee7ff,#8b7cff);}

.reason {
 padding:13px 15px;border:1px solid rgba(148,163,184,.10);border-radius:12px;
 background:rgba(255,255,255,.025);margin:8px 0;color:#bac3d0;font-size:13px;
}
.footer {text-align:center;color:#596577;font-size:11px;margin-top:55px;letter-spacing:.4px;}

@media(max-width:700px){
 .metric-grid{grid-template-columns:1fr;}
 .hero h1{letter-spacing:-2px;}
 .riskrow{align-items:flex-start;flex-direction:column;}
}
</style>
""", unsafe_allow_html=True)

SUSPICIOUS_WORDS = [
    "login","verify","verification","secure","account","update","password",
    "wallet","bank","bonus","free","gift","claim","signin","confirm","urgent",
    "payment","billing","recover","suspend"
]
SHORTENERS = {"bit.ly","tinyurl.com","t.co","goo.gl","is.gd","cutt.ly","shorturl.at"}

def analyze_url(raw):
    value = raw.strip()
    if not value:
        return None, "Please enter a URL."
    candidate = value if re.match(r"^https?://", value, re.I) else "http://" + value
    parsed = urlparse(candidate)
    host = (parsed.hostname or "").lower()
    if not host:
        return None, "The URL could not be parsed."

    score = 0
    reasons = []

    if parsed.scheme != "https":
        score += 15; reasons.append("The connection does not use HTTPS.")
    if "@" in parsed.netloc:
        score += 25; reasons.append("The URL contains '@', which can obscure the real destination.")
    if len(value) > 100:
        score += 15; reasons.append("The URL is unusually long.")
    if len(value) > 180:
        score += 10; reasons.append("The URL is extremely long.")
    if host.startswith("xn--") or ".xn--" in host:
        score += 20; reasons.append("The domain contains punycode/internationalized characters.")
    if re.search(r"^\d{1,3}(?:\.\d{1,3}){3}$", host):
        score += 20; reasons.append("The destination is an IP address rather than a normal domain.")
    if host.count(".") >= 4:
        score += 10; reasons.append("The domain contains many subdomain levels.")
    if host in SHORTENERS:
        score += 20; reasons.append("This is a URL shortener, hiding the final destination.")
    found = [w for w in SUSPICIOUS_WORDS if w in value.lower()]
    if found:
        score += min(30, len(found)*5)
        reasons.append("Suspicious keywords detected: " + ", ".join(found[:7]) + ".")
    if host.count("-") >= 3:
        score += 10; reasons.append("The domain contains several hyphens.")

    score = min(score,100)
    if score >= 60: level, cls = "HIGH RISK","high"
    elif score >= 30: level, cls = "MEDIUM RISK","medium"
    else: level, cls = "LOW RISK","low"
    if not reasons:
        reasons.append("No obvious phishing indicators were found by the current heuristic checks.")
    return {"domain":host,"score":score,"level":level,"cls":cls,"reasons":reasons}, None

st.markdown("""
<div class="brand">
  <div class="brand-left"><div class="logo">◈</div><div class="brand-name">CYBER<span>SHIELD</span></div></div>
  <div class="status">● SYSTEM ONLINE</div>
</div>
<div class="hero">
  <div class="eyebrow">URL THREAT INTELLIGENCE</div>
  <h1>Think before you click.</h1>
  <p>Analyze suspicious links for common phishing indicators with an explainable security risk assessment.</p>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="search-card">', unsafe_allow_html=True)
url = st.text_input("URL", placeholder="Paste a suspicious URL here  •  example.com/login", label_visibility="collapsed")
st.markdown('</div>', unsafe_allow_html=True)

_, btn, _ = st.columns([1,2,1])
with btn:
    analyze = st.button("◈  ANALYZE THREAT", use_container_width=True)

if analyze:
    result, error = analyze_url(url)
    if error:
        st.error(error)
    else:
        st.markdown('<div class="section-title">Threat assessment</div>', unsafe_allow_html=True)
        st.markdown(f"""
        <div class="result">
          <div class="riskrow">
            <div>
              <div class="badge {result['cls']}">{result['level']}</div>
              <div style="margin-top:14px;color:#7f8b9e;font-size:12px;">ANALYZED DESTINATION</div>
              <div style="font-family:Space Grotesk;font-size:19px;font-weight:600;margin-top:4px;word-break:break-all;">{result['domain']}</div>
            </div>
            <div class="score">{result['score']}<small>/100<br>risk score</small></div>
          </div>
          <div class="bar"><div class="fill" style="width:{result['score']}%"></div></div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown('<div class="metric-grid">', unsafe_allow_html=True)
        st.markdown(f'<div class="metric"><div class="label">Protocol</div><div class="value">{"HTTPS" if url.lower().startswith("https://") else "HTTP"}</div><div class="sub">Connection protocol</div></div>', unsafe_allow_html=True)
        st.markdown(f'<div class="metric"><div class="label">Indicators</div><div class="value">{len(result["reasons"])}</div><div class="sub">Signals detected</div></div>', unsafe_allow_html=True)
        st.markdown(f'<div class="metric"><div class="label">Engine</div><div class="value">HEURISTIC</div><div class="sub">Explainable analysis</div></div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="section-title">Security signals</div>', unsafe_allow_html=True)
        for reason in result["reasons"]:
            st.markdown(f'<div class="reason">◌ &nbsp; {reason}</div>', unsafe_allow_html=True)

        st.info("CyberShield is an educational heuristic analyzer. A LOW RISK result does not guarantee safety. Do not enter passwords, OTPs, or financial information unless you independently trust the destination.")

st.markdown("""
<div class="footer">
CYBERSHIELD  /  URL INTELLIGENCE ENGINE  •  EDUCATIONAL SECURITY PROJECT<br>
Built with Python + Streamlit
</div>
""", unsafe_allow_html=True)
