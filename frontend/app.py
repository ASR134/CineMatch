import streamlit as st
import requests

API_URL = "https://movie-recommender-pn4m.onrender.com"

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="CineMatch",
    page_icon="🎬",
    layout="wide",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;900&family=DM+Sans:wght@300;400;500&display=swap');

  /* ── Reset & base ── */
    html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    }

    .stApp {
    background: #0a0a0f;
    color: #f0ede8;
    }

  /* ── Hide Streamlit chrome ── */
    #MainMenu, footer, header { visibility: hidden; }
    .block-container { padding: 2rem 3rem 4rem; max-width: 1300px; }

  /* ── Hero header ── */
    .hero {
    text-align: center;
    padding: 3.5rem 0 2rem;
    position: relative;
    }
    .hero::before {
    content: '';
    position: absolute;
    top: 0; left: 50%; transform: translateX(-50%);
    width: 600px; height: 300px;
    background: radial-gradient(ellipse at center, rgba(229,160,50,0.18) 0%, transparent 70%);
    pointer-events: none;
    }
    .hero-eyebrow {
    font-family: 'DM Sans', sans-serif;
    font-size: 0.75rem;
    font-weight: 500;
    letter-spacing: 0.3em;
    text-transform: uppercase;
    color: #e5a032;
    margin-bottom: 0.75rem;
    }
    .hero-title {
    font-family: 'Playfair Display', serif;
    font-size: clamp(3rem, 6vw, 5rem);
    font-weight: 900;
    line-height: 1.05;
    color: #f0ede8;
    margin: 0;
    letter-spacing: -0.02em;
    }
    .hero-title span { color: #e5a032; }
    .hero-sub {
    margin-top: 1rem;
    font-size: 1rem;
    color: #7a7875;
    font-weight: 300;ui
    }

  /* ── Divider ── */
    .gold-line {
    width: 60px; height: 2px;
    background: #e5a032;
    margin: 2rem auto;
    border-radius: 2px;
    }

  /* ── Select box label override ── */
    label[data-testid="stWidgetLabel"] p {
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.72rem !important;
    font-weight: 500 !important;
    letter-spacing: 0.2em !important;
    text-transform: uppercase !important;
    color: #7a7875 !important;
    }

  /* ── Selectbox ── */
    .stSelectbox > div > div {
    background: #141418 !important;
    border: 1px solid #2a2a32 !important;
    border-radius: 8px !important;
    color: #f0ede8 !important;
    font-size: 1rem !important;
    transition: border-color 0.2s;
    }
    .stSelectbox > div > div:hover,
    .stSelectbox > div > div:focus-within {
    border-color: #e5a032 !important;
    box-shadow: 0 0 0 3px rgba(229,160,50,0.12) !important;
    }

  /* ── Button ── */
    .stButton > button {
    background: #e5a032 !important;
    color: #0a0a0f !important;
    border: none !important;
    border-radius: 8px !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.85rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.12em !important;
    text-transform: uppercase !important;
    padding: 0.65rem 2.4rem !important;
    width: 100% !important;
    cursor: pointer !important;
    transition: background 0.2s, transform 0.1s, box-shadow 0.2s !important;
    box-shadow: 0 4px 20px rgba(229,160,50,0.25) !important;
    }
    .stButton > button:hover {
    background: #f0b84a !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 8px 28px rgba(229,160,50,0.4) !important;
    }
    .stButton > button:active {
    transform: translateY(0) !important;
    }

  /* ── Selected badge ── */
    .selected-badge {
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    background: rgba(229,160,50,0.1);
    border: 1px solid rgba(229,160,50,0.3);
    border-radius: 40px;
    padding: 0.35rem 1rem;
    font-size: 0.85rem;
    color: #e5a032;
    margin: 0.75rem 0 1.5rem;
    }
    .selected-badge .dot {
    width: 6px; height: 6px;
    border-radius: 50%;
    background: #e5a032;
    animation: pulse 1.6s ease-in-out infinite;
    }
    @keyframes pulse {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.3; }
    }

  /* ── Section heading ── */
    .rec-heading {
    font-family: 'Playfair Display', serif;
    font-size: 1.6rem;
    font-weight: 700;
    color: #f0ede8;
    margin: 2.5rem 0 1.5rem;
    letter-spacing: -0.01em;
    }
    .rec-heading span { color: #e5a032; }

  /* ── Movie card ── */
    .movie-card {
    background: #141418;
    border: 1px solid #1e1e26;
    border-radius: 12px;
    overflow: hidden;
    transition: transform 0.25s ease, box-shadow 0.25s ease, border-color 0.25s;
    cursor: pointer;
    position: relative;
    }
    .movie-card:hover {
    transform: translateY(-6px) scale(1.02);
    box-shadow: 0 20px 50px rgba(0,0,0,0.6), 0 0 0 1px rgba(229,160,50,0.25);
    border-color: rgba(229,160,50,0.4);
    }
        .movie-card img {
    width: 100%;
    display: block;
    aspect-ratio: 2/3;
    object-fit: cover;
    }
    .card-overlay {
    position: absolute;
    bottom: 0; left: 0; right: 0;
    background: linear-gradient(to top, rgba(10,10,15,0.98) 0%, rgba(10,10,15,0.6) 60%, transparent 100%);
    padding: 1.5rem 0.9rem 0.9rem;
    }
    .card-index {
    font-size: 0.65rem;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: #e5a032;
    font-weight: 600;
    margin-bottom: 0.2rem;
    }
    .card-title {
    font-family: 'DM Sans', sans-serif;
    font-size: 0.88rem;
    font-weight: 500;
    color: #f0ede8;
    line-height: 1.35;
    margin: 0;
    }

  /* ── Spinner override ── */
    .stSpinner > div { border-top-color: #e5a032 !important; }

  /* ── Error ── */
    .stAlert { border-radius: 8px !important; }

  /* ── Columns gap ── */
    [data-testid="column"] { padding: 0 0.4rem !important; }
</style>
""", unsafe_allow_html=True)


# ── Hero ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <div class="hero-eyebrow">✦ AI-Powered Discovery</div>
    <h1 class="hero-title">Cine<span>Match</span></h1>
    <p class="hero-sub">Tell us one film you love. We'll find five more you'll adore.</p>
</div>
<div class="gold-line"></div>
""", unsafe_allow_html=True)


# ── Data fetching ─────────────────────────────────────────────────────────────
@st.cache_data(show_spinner=False)
def fetch_movies():
    try:
        res = requests.get(f"{API_URL}/movies", timeout=10)
        return res.json()["movies"]
    except Exception:
        return []

def fetch_recommended_movies(movie):
    try:
        res = requests.post(f"{API_URL}/recommend", json={"movie": movie}, timeout=15)
        if res.status_code == 200:
            return res.json()["recommended_movies"]
    except Exception as e:
        st.error(f"Could not fetch recommendations: {e}")
    return []


# ── Controls ──────────────────────────────────────────────────────────────────
movie_list = fetch_movies()

if not movie_list:
    st.warning("⚠️ Unable to load movie list. Please check the API connection.")
    st.stop()

col_sel, col_btn = st.columns([4, 1], gap="medium")

with col_sel:
    option = st.selectbox(
        "Choose your starting film",
        movie_list,
        label_visibility="visible",
    )

with col_btn:
    st.markdown("<div style='padding-top:1.75rem'></div>", unsafe_allow_html=True)
    recommend_clicked = st.button("✦ Discover", type="primary")

# Selected badge
st.markdown(f"""
<div class="selected-badge">
    <span class="dot"></span>
    {option}
</div>
""", unsafe_allow_html=True)


# ── Recommendations ───────────────────────────────────────────────────────────
if recommend_clicked:
    with st.spinner("Curating your picks…"):
        recs = fetch_recommended_movies(option)

    if recs:
        st.markdown(f"""
        <div class="rec-heading">
            Because you chose <span>"{option}"</span>
        </div>
        """, unsafe_allow_html=True)

        cols = st.columns(5, gap="small")
        labels = ["01", "02", "03", "04", "05"]

        for i, col in enumerate(cols):
            if i < len(recs):
                rec = recs[i]
                with col:
                    poster = rec.get("poster_url", "")
                    title  = rec.get("title", "Unknown")

                    # Build card HTML
                    st.markdown(f"""
                    <div class="movie-card">
                        <img src="{poster}" alt="{title}" 
                            onerror="this.src='https://via.placeholder.com/300x450/141418/333?text=No+Poster'"/>
                        <div class="card-overlay">
                        <div class="card-index">{labels[i]}</div>
                        <p class="card-title">{title}</p>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
    else:
        st.error("No recommendations returned. Try a different film.")