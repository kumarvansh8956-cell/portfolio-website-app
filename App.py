
import base64
from pathlib import Path

import streamlit as st

st.set_page_config(
    page_title="Vansh Kumar | Portfolio",
    page_icon="🤖",
    layout="wide",
)

BASE_DIR = Path(__file__).resolve().parent
background_path = BASE_DIR / "assets" / "background.png"

if background_path.exists():
    bg = base64.b64encode(background_path.read_bytes()).decode("utf-8")
    background_style = f"""
        linear-gradient(90deg, rgba(2, 6, 23, 0.78), rgba(15, 23, 42, 0.42)),
        url("data:image/png;base64,{bg}")
    """
else:
    background_style = """
        linear-gradient(90deg, rgba(2, 6, 23, 0.85), rgba(15, 23, 42, 0.60))
    """

st.markdown(
    f"""
    <style>
        :root {{
            --bg: rgba(2, 6, 23, 0.88);
            --panel: rgba(15, 23, 42, 0.76);
            --panel-soft: rgba(15, 23, 42, 0.50);
            --text: #e2e8f0;
            --muted: #cbd5e1;
            --accent: #7dd3fc;
            --accent-2: #c084fc;
        }}

        .stApp {{
            background: {background_style};
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
            background-repeat: no-repeat;
            color: var(--text);
        }}

        [data-testid="stMain"],
        [data-testid="stMainBlockContainer"] {{
            background: transparent;
        }}

        [data-testid="stHeader"] {{
            background: rgba(15, 23, 42, 0.28);
            backdrop-filter: blur(8px);
        }}

        .block-container {{
            padding-top: 2rem;
            padding-bottom: 3rem;
        }}

        div[data-testid="stVerticalBlock"] > div:has(> .stAlert) {{
            border-radius: 12px;
        }}

        .stButton > button,
        .stDownloadButton > button,
        .stLinkButton > button {{
            border-radius: 12px;
            border: 1px solid rgba(125, 211, 252, 0.4);
            background: linear-gradient(135deg, rgba(125, 211, 252, 0.18), rgba(192, 132, 252, 0.18));
            color: white;
            transition: 0.2s ease;
        }}

        .stButton > button:hover,
        .stDownloadButton > button:hover,
        .stLinkButton > button:hover {{
            transform: translateY(-1px);
            box-shadow: 0 8px 18px rgba(125, 211, 252, 0.12);
        }}
    </style>
    """,
    unsafe_allow_html=True,
)

home = st.Page(
    BASE_DIR / "Pages" / "Home.py",
    title="Home",
    icon="🏠",
    default=True,
)

projects = st.Page(
    BASE_DIR / "Pages" / "projects.py",
    title="Projects",
    icon="🚀",
)

about = st.Page(
    BASE_DIR / "Pages" / "about.py",
    title="About",
    icon="👨‍💻",
)

assistant = st.Page(
    BASE_DIR / "Chatbot" / "chatbot.py",
    title="Assistant",
    icon="🤖",
)

navigation = st.navigation([home, projects, about, assistant], position="top")
navigation.run()
