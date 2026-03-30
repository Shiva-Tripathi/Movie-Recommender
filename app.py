import requests
import streamlit as st
from typing import Optional


# =============================
# CONFIG
# =============================
API_BASE = "https://movie-recommender-vrr6.onrender.com" or "http://127.0.0.1:8000"
TMDB_IMG = "https://image.tmdb.org/t/p/w500"

st.set_page_config(page_title="CineMatch", page_icon="🎬", layout="wide")

# =============================
# STYLES
# =============================
st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Outfit:wght@200;300;400;500;600&display=swap');

/* ═══════════════════════════════════════
   KILL THE STREAMLIT CHROME
   (toolbar with "Deploy", top header,
    footer, main menu hamburger)
═══════════════════════════════════════ */
#MainMenu,
header[data-testid="stHeader"],
footer,
[data-testid="stToolbar"],
[data-testid="stDecoration"],
[data-testid="stStatusWidget"],
.stDeployButton,
button[kind="header"] { display: none !important; visibility: hidden !important; }

/* ═══════════════════════════════════════
   DESIGN TOKENS
═══════════════════════════════════════ */
:root {
  --bg:         #0b0b0f;
  --bg2:        #111116;
  --bg3:        #18181f;
  --bg4:        #1f1f28;
  --gold:       #f0b429;
  --gold-soft:  #d99a1a;
  --gold-glow:  rgba(240,180,41,0.18);
  --silver:     #8888a0;
  --text:       #e6e6f0;
  --text-dim:   #9898b0;
  --border:     rgba(240,180,41,0.14);
  --border-w:   rgba(255,255,255,0.055);
  --r:          12px;
  --r-sm:       7px;
  --transition: 0.22s cubic-bezier(.4,0,.2,1);
}

/* ═══════════════════════════════════════
   GLOBAL BASE
═══════════════════════════════════════ */
html, body { background: var(--bg) !important; }

*, *::before, *::after {
  font-family: 'Outfit', sans-serif;
  box-sizing: border-box;
}

.stApp {
  background: var(--bg);
  /* Layered: noise-like dot grid + radial gold bloom */
  background-image:
    radial-gradient(ellipse 110% 55% at 50% -5%,
      rgba(240,180,41,0.07) 0%,
      transparent 65%),
    radial-gradient(circle 1px at 1px 1px,
      rgba(255,255,255,0.06) 1px, transparent 0);
  background-size: 100% 100%, 28px 28px;
  min-height: 100vh;
  color: var(--text);
}

/* ═══════════════════════════════════════
   LAYOUT — give room since header is gone
═══════════════════════════════════════ */
.block-container {
  padding-top: 2.5rem !important;
  padding-bottom: 4rem;
  max-width: 1520px;
}

/* ═══════════════════════════════════════
   SIDEBAR
═══════════════════════════════════════ */
[data-testid="stSidebar"] {
  background: var(--bg2) !important;
  border-right: 1px solid var(--border-w) !important;
  padding-top: 1.6rem;
}
[data-testid="stSidebar"] > div { padding: 1rem 1.2rem; }

/* sidebar brand */
[data-testid="stSidebar"] .stMarkdown h2 {
  font-family: 'Bebas Neue', sans-serif;
  font-size: 2rem;
  letter-spacing: 0.14em;
  color: var(--gold);
  margin: 0 0 4px;
  line-height: 1;
}

/* sidebar labels */
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] .stMarkdown p,
[data-testid="stSidebar"] .stMarkdown h3 {
  color: var(--silver) !important;
  font-size: 0.72rem !important;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  font-weight: 500 !important;
}

[data-testid="stSidebar"] hr {
  border: none;
  border-top: 1px solid var(--border-w) !important;
  margin: 1rem 0 !important;
}

/* sidebar home button */
[data-testid="stSidebar"] .stButton > button {
  background: transparent;
  border: 1px solid var(--border);
  color: var(--gold);
  font-size: 0.8rem;
  font-weight: 500;
  letter-spacing: 0.08em;
  border-radius: var(--r-sm);
  padding: 0.5rem 0.8rem;
  width: 100%;
  transition: all var(--transition);
}
[data-testid="stSidebar"] .stButton > button:hover {
  background: var(--gold-glow);
  border-color: var(--gold);
  color: #fff;
  box-shadow: 0 0 18px var(--gold-glow);
}

/* sidebar selectbox */
[data-testid="stSidebar"] .stSelectbox [data-baseweb="select"] > div {
  background: var(--bg3) !important;
  border-color: var(--border-w) !important;
  border-radius: var(--r-sm) !important;
}

/* ═══════════════════════════════════════
   HERO HEADER STRIP
═══════════════════════════════════════ */
.hero-wrap {
  position: relative;
  padding: 2.4rem 0 2rem;
  margin-bottom: 0.4rem;
  overflow: hidden;
}
/* filmstrip perforations top */
.hero-wrap::before {
  content: '';
  position: absolute;
  top: 0; left: 0; right: 0;
  height: 10px;
  background: repeating-linear-gradient(
    90deg,
    transparent 0px, transparent 18px,
    var(--border) 18px, var(--border) 30px
  );
  opacity: 0.6;
}
/* filmstrip perforations bottom */
.hero-wrap::after {
  content: '';
  position: absolute;
  bottom: 0; left: 0; right: 0;
  height: 10px;
  background: repeating-linear-gradient(
    90deg,
    transparent 0px, transparent 18px,
    var(--border) 18px, var(--border) 30px
  );
  opacity: 0.6;
}

.hero-title {
  font-family: 'Bebas Neue', sans-serif;
  font-size: clamp(3.2rem, 7vw, 6.2rem);
  letter-spacing: 0.18em;
  line-height: 0.95;
  color: #fff;
  margin: 0;
  /* subtle text shadow depth */
  text-shadow: 0 2px 30px rgba(0,0,0,0.6);
}
.hero-title .accent {
  color: var(--gold);
  /* animated shimmer */
  background: linear-gradient(110deg, #f0b429 25%, #ffe08a 50%, #f0b429 75%);
  background-size: 200% auto;
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  animation: shimmer 3.5s linear infinite;
}
@keyframes shimmer {
  to { background-position: 200% center; }
}

.hero-sub {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-top: 10px;
}
.hero-sub .tag {
  font-size: 0.68rem;
  font-weight: 500;
  letter-spacing: 0.18em;
  text-transform: uppercase;
  color: var(--silver);
  padding: 3px 10px;
  border: 1px solid var(--border-w);
  border-radius: 100px;
  background: var(--bg3);
}
.hero-sub .sep { color: var(--border); font-size: 0.8rem; }

/* ═══════════════════════════════════════
   DIVIDERS
═══════════════════════════════════════ */
hr {
  border: none !important;
  height: 1px !important;
  background: linear-gradient(
    90deg, transparent, var(--border), transparent
  ) !important;
  margin: 1.6rem 0 !important;
}

/* ═══════════════════════════════════════
   SEARCH INPUT  — oversized, cinematic
═══════════════════════════════════════ */
.stTextInput > label {
  font-size: 0.68rem !important;
  font-weight: 600 !important;
  letter-spacing: 0.18em !important;
  text-transform: uppercase !important;
  color: var(--silver) !important;
  margin-bottom: 6px !important;
}
.stTextInput > div > div {
  background: var(--bg2) !important;
  border: 1px solid rgba(240,180,41,0.22) !important;
  border-radius: var(--r) !important;
  transition: border-color var(--transition), box-shadow var(--transition) !important;
}
.stTextInput > div > div:focus-within {
  border-color: var(--gold) !important;
  box-shadow: 0 0 0 4px rgba(240,180,41,0.1),
              0 8px 32px rgba(0,0,0,0.4) !important;
}
.stTextInput input {
  color: var(--text) !important;
  font-size: 1.05rem !important;
  font-weight: 300 !important;
  letter-spacing: 0.03em !important;
  padding: 0.75rem 1rem !important;
  background: transparent !important;
}
.stTextInput input::placeholder { color: #55556a !important; }

/* ═══════════════════════════════════════
   SELECTBOX
═══════════════════════════════════════ */
.stSelectbox > label {
  font-size: 0.68rem !important;
  font-weight: 600 !important;
  letter-spacing: 0.16em !important;
  text-transform: uppercase !important;
  color: var(--silver) !important;
}
.stSelectbox [data-baseweb="select"] > div {
  background: var(--bg2) !important;
  border-color: var(--border) !important;
  border-radius: var(--r-sm) !important;
  color: var(--text) !important;
  transition: border-color var(--transition) !important;
}
.stSelectbox [data-baseweb="select"] > div:hover {
  border-color: var(--gold) !important;
}

/* ═══════════════════════════════════════
   BUTTONS
═══════════════════════════════════════ */
.stButton > button {
  background: var(--bg3) !important;
  border: 1px solid var(--border) !important;
  color: var(--gold) !important;
  font-size: 0.65rem !important;
  font-weight: 600 !important;
  letter-spacing: 0.14em !important;
  text-transform: uppercase !important;
  border-radius: var(--r-sm) !important;
  padding: 0.38rem 0 !important;
  width: 100% !important;
  transition: all var(--transition) !important;
  position: relative;
  overflow: hidden;
}
/* shimmer sweep on hover */
.stButton > button::after {
  content: '';
  position: absolute;
  inset: 0;
  background: linear-gradient(
    110deg,
    transparent 30%,
    rgba(240,180,41,0.12) 50%,
    transparent 70%
  );
  transform: translateX(-100%);
  transition: transform 0.5s ease;
}
.stButton > button:hover::after { transform: translateX(100%); }
.stButton > button:hover {
  background: rgba(240,180,41,0.1) !important;
  border-color: var(--gold) !important;
  color: #fff !important;
  transform: translateY(-2px) !important;
  box-shadow: 0 6px 24px rgba(240,180,41,0.2) !important;
}
.stButton > button:active {
  transform: translateY(0) !important;
  box-shadow: none !important;
}

/* ═══════════════════════════════════════
   POSTER IMAGES — film-frame hover
═══════════════════════════════════════ */
[data-testid="stImage"] img {
  border-radius: var(--r-sm) !important;
  border: 1px solid var(--border-w) !important;
  transition:
    transform 0.3s cubic-bezier(.34,1.56,.64,1),
    box-shadow 0.3s ease,
    border-color 0.3s ease !important;
  display: block;
}
[data-testid="stImage"]:hover img {
  transform: scale(1.045) translateY(-4px) !important;
  box-shadow:
    0 16px 48px rgba(0,0,0,0.7),
    0 0 0 1px rgba(240,180,41,0.45) !important;
  border-color: rgba(240,180,41,0.45) !important;
}

/* ═══════════════════════════════════════
   MOVIE TITLE UNDER POSTER
═══════════════════════════════════════ */
.movie-title {
  font-size: 0.72rem;
  font-weight: 400;
  line-height: 1.3;
  height: 2.4rem;
  overflow: hidden;
  color: #8888a8;
  letter-spacing: 0.01em;
  margin-top: 4px;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
}

/* ═══════════════════════════════════════
   DETAIL CARD
═══════════════════════════════════════ */
.card {
  background: linear-gradient(145deg, var(--bg3), var(--bg2));
  border: 1px solid var(--border);
  border-radius: var(--r);
  padding: 28px 32px;
  box-shadow:
    0 4px 24px rgba(0,0,0,0.4),
    inset 0 1px 0 rgba(255,255,255,0.04);
  height: 100%;
}

/* ═══════════════════════════════════════
   META CHIPS
═══════════════════════════════════════ */
.small-muted {
  color: var(--silver);
  font-size: 0.78rem;
  letter-spacing: 0.06em;
  text-transform: uppercase;
}
.meta-chip {
  display: inline-block;
  background: rgba(240,180,41,0.08);
  border: 1px solid rgba(240,180,41,0.22);
  color: var(--gold);
  font-size: 0.65rem;
  font-weight: 600;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  border-radius: 100px;
  padding: 3px 11px;
  margin: 0 5px 5px 0;
  transition: background var(--transition);
}
.meta-chip:hover {
  background: rgba(240,180,41,0.16);
}

/* ═══════════════════════════════════════
   SECTION HEADINGS
═══════════════════════════════════════ */
.section-heading {
  display: flex;
  align-items: center;
  gap: 12px;
  margin: 2.2rem 0 1.2rem;
}
.section-heading .line {
  flex: 1;
  height: 1px;
  background: linear-gradient(to right, rgba(240,180,41,0.2), transparent);
}
.section-heading .label {
  font-size: 0.65rem;
  font-weight: 700;
  letter-spacing: 0.22em;
  text-transform: uppercase;
  color: var(--gold);
  white-space: nowrap;
  padding: 4px 12px;
  border: 1px solid var(--border);
  border-radius: 100px;
  background: rgba(240,180,41,0.06);
}

/* ═══════════════════════════════════════
   ALERTS
═══════════════════════════════════════ */
.stAlert {
  background: var(--bg3) !important;
  border: 1px solid var(--border-w) !important;
  border-radius: var(--r-sm) !important;
  color: var(--text-dim) !important;
}

/* ═══════════════════════════════════════
   SLIDER (grid columns)
═══════════════════════════════════════ */
[data-testid="stSidebar"] [data-testid="stSlider"] {
  padding: 0.2rem 0;
}

/* ═══════════════════════════════════════
   SCROLLBAR
═══════════════════════════════════════ */
::-webkit-scrollbar { width: 5px; height: 5px; }
::-webkit-scrollbar-track { background: var(--bg); }
::-webkit-scrollbar-thumb {
  background: var(--bg4);
  border-radius: 4px;
}
::-webkit-scrollbar-thumb:hover { background: var(--gold-soft); }

/* ═══════════════════════════════════════
   MISC STREAMLIT OVERRIDES
═══════════════════════════════════════ */
.stCaption, caption {
  color: var(--silver) !important;
  font-size: 0.72rem !important;
}
/* Remove default st.title top padding now that header is gone */
.stApp h1 {
  font-family: 'Bebas Neue', sans-serif;
  letter-spacing: 0.14em;
  color: var(--text);
}
</style>
""",
    unsafe_allow_html=True,
)

# =============================
# STATE + ROUTING (single-file pages)
# =============================
if "view" not in st.session_state:
    st.session_state.view = "home"  # home | details
if "selected_tmdb_id" not in st.session_state:
    st.session_state.selected_tmdb_id = None

qp_view = st.query_params.get("view")
qp_id = st.query_params.get("id")
if qp_view in ("home", "details"):
    st.session_state.view = qp_view
if qp_id:
    try:
        st.session_state.selected_tmdb_id = int(qp_id)
        st.session_state.view = "details"
    except:
        pass


def goto_home():
    st.session_state.view = "home"
    st.query_params["view"] = "home"
    if "id" in st.query_params:
        del st.query_params["id"]
    st.rerun()


def goto_details(tmdb_id: int):
    st.session_state.view = "details"
    st.session_state.selected_tmdb_id = int(tmdb_id)
    st.query_params["view"] = "details"
    st.query_params["id"] = str(int(tmdb_id))
    st.rerun()


# =============================
# API HELPERS
# =============================
@st.cache_data(ttl=30)  # short cache for autocomplete
def api_get_json(path: str, params: Optional[dict] = None):
    try:
        r = requests.get(f"{API_BASE}{path}", params=params, timeout=25)
        if r.status_code >= 400:
            return None, f"HTTP {r.status_code}: {r.text[:300]}"
        return r.json(), None
    except Exception as e:
        return None, f"Request failed: {e}"


def poster_grid(cards, cols=6, key_prefix="grid"):
    if not cards:
        st.info("No movies to show.")
        return

    rows = (len(cards) + cols - 1) // cols
    idx = 0
    for r in range(rows):
        colset = st.columns(cols)
        for c in range(cols):
            if idx >= len(cards):
                break
            m = cards[idx]
            idx += 1

            tmdb_id = m.get("tmdb_id")
            title = m.get("title", "Untitled")
            poster = m.get("poster_url")

            with colset[c]:
                if poster:
                    st.image(poster, use_column_width=True)
                else:
                    st.write("🖼️ No poster")

                if st.button("Open", key=f"{key_prefix}_{r}_{c}_{idx}_{tmdb_id}"):
                    if tmdb_id:
                        goto_details(tmdb_id)

                st.markdown(
                    f"<div class='movie-title'>{title}</div>", unsafe_allow_html=True
                )


def to_cards_from_tfidf_items(tfidf_items):
    cards = []
    for x in tfidf_items or []:
        tmdb = x.get("tmdb") or {}
        if tmdb.get("tmdb_id"):
            cards.append(
                {
                    "tmdb_id": tmdb["tmdb_id"],
                    "title": tmdb.get("title") or x.get("title") or "Untitled",
                    "poster_url": tmdb.get("poster_url"),
                }
            )
    return cards


# =============================
# IMPORTANT: Robust TMDB search parsing
# Supports BOTH API shapes:
# 1) raw TMDB: {"results":[{id,title,poster_path,...}]}
# 2) list cards: [{tmdb_id,title,poster_url,...}]
# =============================
def parse_tmdb_search_to_cards(data, keyword: str, limit: int = 24):
    """
    Returns:
      suggestions: list[(label, tmdb_id)]
      cards: list[{tmdb_id,title,poster_url}]
    """
    keyword_l = keyword.strip().lower()

    # A) If API returns dict with 'results'
    if isinstance(data, dict) and "results" in data:
        raw = data.get("results") or []
        raw_items = []
        for m in raw:
            title = (m.get("title") or "").strip()
            tmdb_id = m.get("id")
            poster_path = m.get("poster_path")
            if not title or not tmdb_id:
                continue
            raw_items.append(
                {
                    "tmdb_id": int(tmdb_id),
                    "title": title,
                    "poster_url": f"{TMDB_IMG}{poster_path}" if poster_path else None,
                    "release_date": m.get("release_date", ""),
                }
            )

    # B) If API returns already as list
    elif isinstance(data, list):
        raw_items = []
        for m in data:
            tmdb_id = m.get("tmdb_id") or m.get("id")
            title = (m.get("title") or "").strip()
            poster_url = m.get("poster_url")
            if not title or not tmdb_id:
                continue
            raw_items.append(
                {
                    "tmdb_id": int(tmdb_id),
                    "title": title,
                    "poster_url": poster_url,
                    "release_date": m.get("release_date", ""),
                }
            )
    else:
        return [], []

    # Word-match filtering (contains)
    matched = [x for x in raw_items if keyword_l in x["title"].lower()]

    # If nothing matched, fallback to raw list (so never blank)
    final_list = matched if matched else raw_items

    # Suggestions = top 10 labels
    suggestions = []
    for x in final_list[:10]:
        year = (x.get("release_date") or "")[:4]
        label = f"{x['title']} ({year})" if year else x["title"]
        suggestions.append((label, x["tmdb_id"]))

    # Cards = top N
    cards = [
        {"tmdb_id": x["tmdb_id"], "title": x["title"], "poster_url": x["poster_url"]}
        for x in final_list[:limit]
    ]
    return suggestions, cards


# =============================
# SIDEBAR
# =============================
with st.sidebar:
    st.markdown("## 🎬 CineMatch")
    if st.button("🏠 Home"):
        goto_home()

    st.markdown("---")
    st.markdown("### Home Feed")
    home_category = st.selectbox(
        "Category",
        ["trending", "popular", "top_rated", "now_playing", "upcoming"],
        index=0,
    )
    grid_cols = st.slider("Grid columns", 4, 8, 6)

# =============================
# HEADER
# =============================
st.markdown(
    """
    <div class="hero-wrap">
      <div class="hero-title">CINE<span class="accent">MATCH</span></div>
      <div class="hero-sub">
        <span class="tag">Discover</span>
        <span class="sep">&middot;</span>
        <span class="tag">Explore</span>
        <span class="sep">&middot;</span>
        <span class="tag">Recommend</span>
      </div>
    </div>
    """,
    unsafe_allow_html=True,
)
st.divider()

# ==========================================================
# VIEW: HOME
# ==========================================================
if st.session_state.view == "home":
    typed = st.text_input(
        "Search by movie title", placeholder="avenger, batman, love..."
    )

    st.divider()

    # SEARCH MODE
    if typed.strip():
        if len(typed.strip()) < 2:
            st.caption("Type at least 2 characters for suggestions.")
        else:
            data, err = api_get_json("/tmdb/search", params={"query": typed.strip()})

            if err or data is None:
                st.error(f"Search failed: {err}")
            else:
                suggestions, cards = parse_tmdb_search_to_cards(
                    data, typed.strip(), limit=24
                )

                if suggestions:
                    labels = ["-- Select a movie --"] + [s[0] for s in suggestions]
                    selected = st.selectbox("Suggestions", labels, index=0)

                    if selected != "-- Select a movie --":
                        label_to_id = {s[0]: s[1] for s in suggestions}
                        goto_details(label_to_id[selected])
                else:
                    st.info("No suggestions found. Try another keyword.")

                st.markdown(
                    "<div class='section-heading'>"
                    "<div class='line'></div>"
                    "<div class='label'>Search Results</div>"
                    "<div class='line'></div>"
                    "</div>",
                    unsafe_allow_html=True,
                )
                poster_grid(cards, cols=grid_cols, key_prefix="search_results")

        st.stop()

    # HOME FEED MODE
    st.markdown(
        f"<div class='section-heading'>"
        f"<div class='line'></div>"
        f"<div class='label'>{home_category.replace('_', ' ').title()}</div>"
        f"<div class='line'></div>"
        f"</div>",
        unsafe_allow_html=True,
    )

    home_cards, err = api_get_json(
        "/home", params={"category": home_category, "limit": 24}
    )
    if err or not home_cards:
        st.error(f"Home feed failed: {err or 'Unknown error'}")
        st.stop()

    poster_grid(home_cards, cols=grid_cols, key_prefix="home_feed")

# ==========================================================
# VIEW: DETAILS
# ==========================================================
elif st.session_state.view == "details":
    tmdb_id = st.session_state.selected_tmdb_id
    if not tmdb_id:
        st.warning("No movie selected.")
        if st.button("← Back to Home"):
            goto_home()
        st.stop()

    # Top bar
    a, b = st.columns([3, 1])
    with a:
        st.markdown(
            "<div class='section-heading' style='margin-top:0;'>"
            "<div class='label'>Movie Details</div>"
            "<div class='line'></div>"
            "</div>",
            unsafe_allow_html=True,
        )
    with b:
        if st.button("← Back to Home"):
            goto_home()

    # Details
    data, err = api_get_json(f"/movie/id/{tmdb_id}")
    if err or not data:
        st.error(f"Could not load details: {err or 'Unknown error'}")
        st.stop()

    # Layout: Poster LEFT, Details RIGHT
    left, right = st.columns([1, 2.4], gap="large")

    with left:
        st.markdown("<div class='card' style='padding:12px;'>", unsafe_allow_html=True)
        if data.get("poster_url"):
            st.image(data["poster_url"], use_column_width=True)
        else:
            st.write("🖼️ No poster")
        st.markdown("</div>", unsafe_allow_html=True)

    with right:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        title_text = data.get("title", "")
        st.markdown(
            f"<div style='font-family:\"Bebas Neue\",sans-serif; font-size:2.6rem; "
            f"letter-spacing:0.1em; color:#fff; line-height:1.1; margin-bottom:10px;'>"
            f"{title_text}</div>",
            unsafe_allow_html=True,
        )

        release = data.get("release_date") or "-"
        genres = data.get("genres", [])

        st.markdown(
            f"<div class='small-muted' style='margin-bottom:8px;'>📅 {release}</div>",
            unsafe_allow_html=True,
        )

        genre_chips = "".join(
            [f"<span class='meta-chip'>{g['name']}</span>" for g in genres]
        ) or "<span class='small-muted'>No genres</span>"
        st.markdown(
            f"<div style='margin-bottom:14px;'>{genre_chips}</div>",
            unsafe_allow_html=True,
        )

        st.markdown(
            "<div style='height:1px; background:rgba(232,176,75,0.15); margin:12px 0 16px;'></div>",
            unsafe_allow_html=True,
        )

        st.markdown(
            "<div style='font-size:0.72rem; font-weight:500; letter-spacing:0.18em; "
            "text-transform:uppercase; color:#e8b04b; margin-bottom:8px;'>Overview</div>",
            unsafe_allow_html=True,
        )
        overview_text = data.get("overview") or "No overview available."
        st.markdown(
            f"<p style='color:#b8b8cc; font-size:0.95rem; line-height:1.78; font-weight:300;'>"
            f"{overview_text}</p>",
            unsafe_allow_html=True,
        )
        st.markdown("</div>", unsafe_allow_html=True)

    if data.get("backdrop_url"):
        st.markdown(
            "<div class='section-heading'>"
            "<div class='line'></div>"
            "<div class='label'>Backdrop</div>"
            "<div class='line'></div>"
            "</div>",
            unsafe_allow_html=True,
        )
        st.image(data["backdrop_url"], use_column_width=True)

    st.divider()

    # Recommendations
    title = (data.get("title") or "").strip()
    if title:
        bundle, err2 = api_get_json(
            "/movie/search",
            params={"query": title, "tfidf_top_n": 12, "genre_limit": 12},
        )

        if not err2 and bundle:
            st.markdown(
                "<div class='section-heading'>"
                "<div class='line'></div>"
                "<div class='label'>🔎 Similar Movies — TF-IDF</div>"
                "<div class='line'></div>"
                "</div>",
                unsafe_allow_html=True,
            )
            poster_grid(
                to_cards_from_tfidf_items(bundle.get("tfidf_recommendations")),
                cols=grid_cols,
                key_prefix="details_tfidf",
            )

            st.markdown(
                "<div class='section-heading'>"
                "<div class='line'></div>"
                "<div class='label'>🎭 More Like This — Genre</div>"
                "<div class='line'></div>"
                "</div>",
                unsafe_allow_html=True,
            )
            poster_grid(
                bundle.get("genre_recommendations", []),
                cols=grid_cols,
                key_prefix="details_genre",
            )
        else:
            st.info("Showing Genre recommendations (fallback).")
            genre_only, err3 = api_get_json(
                "/recommend/genre", params={"tmdb_id": tmdb_id, "limit": 18}
            )
            if not err3 and genre_only:
                poster_grid(
                    genre_only, cols=grid_cols, key_prefix="details_genre_fallback"
                )
            else:
                st.warning("No recommendations available right now.")
    else:
        st.warning("No title available to compute recommendations.")