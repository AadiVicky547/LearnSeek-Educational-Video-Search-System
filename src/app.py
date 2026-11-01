"""Streamlit entry point for the LearnSeek educational video search UI."""

from html import escape

import streamlit as st

if __package__ in {None, ""}:
    # Streamlit executes this file as a script and places src/ on sys.path.
    from presentation import build_theme_stylesheet, relevance_label, short_description
    from youtube_service import YouTubeSearchError, search_youtube_videos
else:
    # Python tests and callers can also import the app as src.app.
    from .presentation import build_theme_stylesheet, relevance_label, short_description
    from .youtube_service import YouTubeSearchError, search_youtube_videos


st.set_page_config(
    page_title="LearnSeek — Educational Video Search",
    page_icon="▶",
    layout="wide",
    initial_sidebar_state="collapsed",
)

try:
    dark_theme = st.context.theme.type == "dark"
except (AttributeError, RuntimeError):
    dark_theme = False

BASE_STYLES = """
    :root { color-scheme: light; }
    .stApp, [data-testid="stAppViewContainer"] {
        background: #f7f9fc;
        color: #172b4d;
        font-family: Inter, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
    }
    [data-testid="stHeader"] { display: none !important; }
    [data-testid="stToolbar"] { display: none !important; }
    .block-container { max-width: 1120px; padding: 0 2rem 3rem; }
    [data-testid="stMarkdownContainer"], [data-testid="stMarkdownContainer"] p,
    [data-testid="stMarkdownContainer"] li, label, [data-testid="stCaptionContainer"] {
        color: #526176 !important;
    }
    h1, h2, h3, h4 { color: #15243b !important; letter-spacing: -0.035em; }

    .st-key-learnseek-header {
        padding: 0.7rem 0; margin-bottom: 1.2rem;
    }
    .brand-lockup { display: flex; align-items: center; justify-content: center; }
    .st-key-learnseek-header [data-testid="stMarkdownContainer"] a.brand-name,
    .st-key-learnseek-header [data-testid="stMarkdownContainer"] a.brand-name:visited {
        color: #ffffff !important; -webkit-text-fill-color: #ffffff !important;
        opacity: 1 !important; filter: none !important;
        font-size: clamp(1.65rem, 3vw, 2rem); font-weight: 780;
        letter-spacing: -0.05em; line-height: 1.15; text-decoration: none;
    }

    .hero { max-width: 770px; margin: 0 auto 1.25rem; text-align: center; }
    .hero-eyebrow { color: #315fbd; font-size: 0.73rem; font-weight: 700; letter-spacing: 0.13em; text-transform: uppercase; margin-bottom: 0.55rem; }
    .hero-title { color: #15243b; font-size: clamp(2rem, 4vw, 3rem); font-weight: 740; letter-spacing: -0.06em; line-height: 1.08; margin: 0 0 0.7rem; }
    .hero-copy { color: #65748a; font-size: 0.98rem; line-height: 1.6; margin: 0 auto; max-width: 640px; }

    [data-testid="stForm"] {
        max-width: 830px; margin: 0 auto; padding: 0.5rem;
        background: #fff; border: 1px solid #dce4ef; border-radius: 15px;
        box-shadow: 0 8px 25px rgba(25, 48, 84, 0.07);
    }
    [data-testid="stTextInput"] input {
        min-height: 2.9rem; color: #172b4d !important; background: #fff !important;
        border: 1px solid transparent !important; box-shadow: none !important; font-size: 0.98rem;
    }
    [data-testid="stTextInput"] input::placeholder { color: #8794a7 !important; opacity: 1; }
    button[kind="primary"] {
        min-height: 2.9rem; color: #fff !important; background: #315fbd !important;
        border: 1px solid #315fbd !important; border-radius: 10px !important; font-weight: 650 !important;
    }
    button[kind="primary"]:hover { background: #244fa7 !important; border-color: #244fa7 !important; }
    button[kind="primary"] p { color: #fff !important; }
    div[data-testid="stButton"] button {
        min-height: 2rem; padding: 0.2rem 0.65rem; color: #53647d !important;
        background: #fff !important; border: 1px solid #e0e7f0 !important;
        border-radius: 999px !important; font-size: 0.76rem !important;
    }
    div[data-testid="stButton"] button:hover { color: #244fa7 !important; border-color: #aebfe0 !important; }
    .try-label { color: #8794a7; font-size: 0.76rem; text-align: center; margin: 0.55rem 0 0.15rem; }

    .section-rule { height: 1px; background: #e6ebf2; margin: 2.3rem 0 1.5rem; }
    .results-title { color: #15243b; font-size: 1.28rem; font-weight: 690; letter-spacing: -0.035em; margin: 0; }
    .results-subtitle { color: #8290a3; font-size: 0.82rem; margin-top: 0.25rem; }
    [data-testid="stVerticalBlockBorderWrapper"] {
        background: #fff; border-color: #e1e8f1 !important; border-radius: 14px;
        box-shadow: 0 2px 8px rgba(25, 48, 84, 0.035);
    }
    [data-testid="stLinkButton"] a {
        color: #244f9a !important; background: #eaf1ff !important;
        border: 1px solid #c9d6e9 !important; border-radius: 9px !important;
        font-weight: 650 !important;
    }
    [data-testid="stLinkButton"] a:hover { color: #fff !important; background: #315fbd !important; border-color: #315fbd !important; }
    .empty-state { max-width: 700px; margin: 0 auto; padding: 1.5rem; text-align: center; background: #fff; border: 1px solid #e4eaf2; border-radius: 15px; }
    .empty-title { color: #273a55; font-size: 0.98rem; font-weight: 650; margin: 0 0 0.3rem; }
    .empty-copy { color: #7a889c; font-size: 0.85rem; line-height: 1.55; margin: 0; }
    .about-footer { border-top: 1px solid #e6ebf2; margin-top: 2.75rem; padding: 1rem 0 0; color: #8a96a8; font-size: 0.76rem; text-align: center; }
    @media (max-width: 760px) {
        .block-container { padding: 0.1rem 1rem 2rem; }
        .st-key-learnseek-header { margin-bottom: 0.9rem; }
        .brand-lockup { justify-content: center; }
        .hero-title { font-size: clamp(1.85rem, 8vw, 2.45rem); }
        [data-testid="stForm"] { padding: 0.35rem; }
        [data-testid="stVerticalBlockBorderWrapper"] { padding: 0.7rem !important; }
    }
    @media (prefers-reduced-motion: reduce) { *, *::before, *::after { transition-duration: 0.01ms !important; scroll-behavior: auto !important; } }
"""

DARK_STYLES = """
        :root { color-scheme: dark; }
        .stApp, [data-testid="stAppViewContainer"] { background: #111927 !important; color: #e4ebf5 !important; }
        [data-testid="stHeader"] { background: rgba(17, 25, 39, 0.97) !important; }
        [data-testid="stMarkdownContainer"], [data-testid="stMarkdownContainer"] p,
        [data-testid="stMarkdownContainer"] li, label, [data-testid="stCaptionContainer"] { color: #aebbd0 !important; }
        h1, h2, h3, h4 { color: #f1f5fb !important; }
        .hero-title, .results-title { color: #f1f5fb !important; }
        .hero-copy, .results-subtitle, .sort-label { color: #aebbd0 !important; }
        .section-rule { background: #28364a !important; }
        [data-testid="stForm"], [data-testid="stVerticalBlockBorderWrapper"], .empty-state { background: #192437 !important; border-color: #2c3a50 !important; }
        [data-testid="stTextInput"] input { color: #eff4fb !important; background: #111927 !important; }
        [data-testid="stTextInput"] input::placeholder { color: #8d9bb0 !important; }
        div[data-testid="stButton"] button { color: #d0daea !important; background: #192437 !important; border-color: #34445d !important; }
        div[data-testid="stButton"] button:hover { color: #fff !important; border-color: #6687c7 !important; }
        [data-testid="stLinkButton"] a { color: #dce8ff !important; background: #263a5d !important; border-color: #405a83 !important; }
        [data-testid="stLinkButton"] a:hover { color: #fff !important; background: #315fbd !important; border-color: #4779d0 !important; }
        .empty-title { color: #e6edf7 !important; }
        .empty-copy, .about-footer { color: #9eacc1 !important; }
        [data-testid="stAlert"] { background: #202d42 !important; color: #e4ebf5 !important; }
"""

st.markdown(
    build_theme_stylesheet(BASE_STYLES, DARK_STYLES, dark_theme),
    unsafe_allow_html=True,
)


def _set_query(example: str) -> None:
    """Put an example topic in the search field without submitting it."""
    st.session_state.search_query = example


with st.container(key="learnseek-header"):
    st.markdown(
        '<div class="brand-lockup"><a class="brand-name" href="#search" '
        'style="color:#ffffff!important;-webkit-text-fill-color:#ffffff!important;opacity:1!important">'
        'LearnSeek</a></div>',
        unsafe_allow_html=True,
    )
st.markdown(
    """
    <section class="hero" id="search">
      <div class="hero-eyebrow">Learn something new</div>
      <h1 class="hero-title">Find the video that makes it click.</h1>
      <p class="hero-copy">Explore real educational videos across subjects, then choose the explanation that works for you.</p>
    </section>
    """,
    unsafe_allow_html=True,
)

with st.form("video_search", clear_on_submit=False):
    search_col, button_col = st.columns([5, 1.25], vertical_alignment="center")
    with search_col:
        query = st.text_input(
            "Search educational videos",
            placeholder="What would you like to understand today?",
            label_visibility="collapsed",
            key="search_query",
        )
    with button_col:
        submitted = st.form_submit_button(
            "Search videos", type="primary", use_container_width=True
        )

st.markdown('<div class="try-label">Try a topic</div>', unsafe_allow_html=True)
example_queries = (
    "Computer networks",
    "Learn Python basics",
    "Why do seasons change?",
    "Introduction to genetics",
)
example_columns = st.columns(len(example_queries))
for column, example in zip(example_columns, example_queries):
    with column:
        st.button(
            example,
            key=f"example_{example}",
            on_click=_set_query,
            args=(example,),
            use_container_width=True,
        )

st.session_state.setdefault("learnseek_results", None)
st.session_state.setdefault("learnseek_query", "")
st.session_state.setdefault("learnseek_error", "")
st.session_state.setdefault("learnseek_has_searched", False)

if submitted:
    st.session_state.learnseek_has_searched = True
    st.session_state.learnseek_query = query.strip()
    st.session_state.learnseek_results = None
    st.session_state.learnseek_error = ""

    if not query.strip():
        st.session_state.learnseek_error = "Enter a subject or question to search."
    else:
        try:
            with st.spinner("Finding educational videos…"):
                st.session_state.learnseek_results = search_youtube_videos(query)
        except YouTubeSearchError as error:
            st.session_state.learnseek_error = str(error)

st.markdown('<div class="section-rule"></div>', unsafe_allow_html=True)

if st.session_state.learnseek_error:
    st.error(st.session_state.learnseek_error)
elif not st.session_state.learnseek_has_searched:
    st.markdown(
        """
        <div class="empty-state">
          <p class="empty-title">Your next great explanation is out there.</p>
          <p class="empty-copy">Search a subject or question to discover real videos from educators and learning channels.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
elif not st.session_state.learnseek_results:
    st.markdown(
        f"""
        <div class="empty-state">
          <p class="empty-title">No videos found for “{escape(st.session_state.learnseek_query)}”.</p>
          <p class="empty-copy">Try a broader subject or use different words.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
else:
    videos = st.session_state.learnseek_results
    safe_query = escape(st.session_state.learnseek_query)
    st.markdown(
        f'<h2 class="results-title">Videos for “{safe_query}”</h2>'
        f'<div class="results-subtitle">{len(videos)} results from YouTube · ordered by YouTube relevance</div>',
        unsafe_allow_html=True,
    )

    # Render each result with Streamlit's native components. This avoids
    # Markdown reinterpreting later HTML cards as literal source text.
    for video in videos:
        with st.container(border=True):
            thumbnail_col, details_col = st.columns(
                [1.05, 2.4], gap="large", vertical_alignment="center"
            )
            with thumbnail_col:
                thumbnail_url = video.get("thumbnail_url")
                if thumbnail_url:
                    st.image(thumbnail_url, use_container_width=True)
                else:
                    st.caption("Thumbnail unavailable")
            with details_col:
                st.subheader(video.get("title") or "Untitled video")
                metadata_parts = [
                    str(value)
                    for value in (video.get("channel_name"), video.get("published_at"))
                    if value
                ]
                if metadata_parts:
                    st.caption(" · ".join(metadata_parts))

                category = video.get("category") or video.get("subject")
                if category:
                    st.caption(f"Topic: {category}")

                description = short_description(video)
                if description:
                    st.write(description)

                score = relevance_label(video)
                if score:
                    st.markdown(f"**{score}**")

                video_url = video.get("video_url")
                if video_url:
                    st.link_button("Watch on YouTube ↗", video_url)

    if not any(relevance_label(video) for video in videos):
        st.caption(
            "Relevance percentages will appear when LearnSeek’s ranking is connected."
        )

st.markdown(
    '<footer class="about-footer" id="about">LearnSeek · Discover. Learn. Understand.</footer>',
    unsafe_allow_html=True,
)
