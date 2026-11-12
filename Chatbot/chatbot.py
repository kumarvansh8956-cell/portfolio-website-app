import base64
import io
import os
import tempfile
from pathlib import Path

import streamlit as st
from gtts import gTTS

try:
    import google.generativeai as genai
except Exception:  # pragma: no cover
    genai = None

try:
    import speech_recognition as sr
except Exception:  # pragma: no cover
    sr = None

PORTFOLIO = {
    "name": "Vansh Kumar",
    "role": "Aspiring AI Engineer | Python Developer",
    "bio": (
        "I’m a Computer Science Engineering student focused on Artificial Intelligence and "
        "Machine Learning. I enjoy building practical Python projects, experimenting with "
        "AI systems, and turning ideas into working real-world tools."
    ),
    "skills": [
        "Python",
        "Machine Learning",
        "Artificial Intelligence",
        "Streamlit",
        "OpenCV",
        "Pandas",
        "NumPy",
        "Data Analysis",
        "Automation",
        "AI Agents",
    ],
    "location": "India",
    "focus": "AI engineering, automation, and practical software projects",
}

PROJECTS = [
    {
        "name": "Personal AI Assistant",
        "category": "AI & Machine Learning",
        "description": "A local-first voice assistant using speech recognition and speech generation.",
        "tech": "Python, Whisper, Piper",
    },
    {
        "name": "EDA Projects",
        "category": "Data Analysis",
        "description": "Exploratory data analysis on multiple real-world datasets.",
        "tech": "Python, Pandas, NumPy, Matplotlib, seaborn",
    },
    {
        "name": "Streamlit Portfolio",
        "category": "Web Applications",
        "description": "A multipage developer portfolio with custom backgrounds and AI integration plans.",
        "tech": "Python, Streamlit",
    },
    {
        "name": "Face Detection System",
        "category": "Python Development",
        "description": "Real-time face, eye and smile detection using a webcam.",
        "tech": "Python, OpenCV, Haar Cascade",
    },
]

DOMAIN_KEYWORDS = {
    "ai": ["ai", "machine learning", "ml", "assistant", "whisper", "piper", "agent"],
    "data": ["data", "eda", "analytics", "pandas", "numpy", "seaborn", "analysis"],
    "web": ["web", "streamlit", "website", "portfolio", "app"],
    "python": ["python", "development", "automation", "coding"],
    "vision": ["vision", "opencv", "face", "camera", "image", "detection"],
}


def normalize_domain(query: str) -> str:
    lowered = query.lower().strip()
    for domain, keywords in DOMAIN_KEYWORDS.items():
        if any(keyword in lowered for keyword in keywords):
            return domain
    return ""


def fetch_projects_by_domain(query: str):
    domain = normalize_domain(query)
    if not domain:
        return PROJECTS

    matched = []
    for project in PROJECTS:
        searchable = " ".join(
            [
                project["name"],
                project["category"],
                project["description"],
                project["tech"],
            ]
        ).lower()
        if any(keyword in searchable for keyword in DOMAIN_KEYWORDS.get(domain, [domain])):
            matched.append(project)
    return matched if matched else PROJECTS


def format_projects(projects):
    if not projects:
        return "I couldn’t find any matching projects for that domain."

    lines = ["Here are the relevant projects:"]
    for project in projects:
        lines.append(f"- {project['name']} ({project['category']})")
        lines.append(f"  {project['description']}")
        lines.append(f"  Tech: {project['tech']}")
    return "\n".join(lines)


def get_api_key():
    try:
        return st.secrets["GEMINI_API_KEY"]
    except Exception:
        return os.getenv("GEMINI_API_KEY")


def build_portfolio_context():
    project_info = "\n".join(
        [
            f"- {project['name']} | Category: {project['category']} | Tech: {project['tech']} | Description: {project['description']}"
            for project in PROJECTS
        ]
    )
    return f"""
    Portfolio for Vansh Kumar
    Name: {PORTFOLIO['name']}
    Role: {PORTFOLIO['role']}
    Bio: {PORTFOLIO['bio']}
    Skills: {', '.join(PORTFOLIO['skills'])}
    Focus: {PORTFOLIO['focus']}
    Location: {PORTFOLIO['location']}

    Projects:
    {project_info}
    """.strip()


def build_memory_context(memory):
    if not memory:
        return "No previous chat memory."
    recent = memory[-6:]
    lines = []
    for item in recent:
        lines.append(f"{item['role'].title()}: {item['content']}")
    return "\n".join(lines)


def call_gemini(prompt: str):
    api_key = get_api_key()
    if not api_key or genai is None:
        return None

    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception:
        return None


def get_answer(query: str, memory=None) -> str:
    q = (query or "").strip()
    memory = memory or []

    if not q:
        return "Ask me about my portfolio, projects, or skills."

    prompt = f"""
    You are a helpful AI assistant for Vansh Kumar's portfolio website.
    Use the following portfolio context as your source of truth:

    {build_portfolio_context()}

    Conversation memory:
    {build_memory_context(memory)}

    User question: {q}

    Rules:
    - Answer naturally and politely.
    - Keep replies brief but helpful.
    - If the user asks for projects, list the relevant ones by domain or category.
    - If the question is about skills, answer based on the explicit portfolio data.
    - Do not invent projects or facts not present in the portfolio context.
    """

    gemini_reply = call_gemini(prompt)
    if gemini_reply:
        return gemini_reply

    q_lower = q.lower()

    if any(word in q_lower for word in ["hello", "hi", "hey", "good morning", "good evening", "hey there"]):
        return f"Hi! I’m {PORTFOLIO['name']}'s AI assistant. I can help with portfolio questions, general chat, and project discovery."

    if any(word in q_lower for word in ["how are you", "how are you doing"]):
        return "I’m doing well — ready to help you explore the portfolio, answer questions, and find domain-specific projects."

    if any(word in q_lower for word in ["who are you", "who is vansh", "about you", "tell me about you", "about me"]):
        return PORTFOLIO["bio"]

    if any(word in q_lower for word in ["skills", "tech stack", "technology", "tools", "expertise", "what do you know"]):
        return "My main skills include: " + ", ".join(PORTFOLIO["skills"]) + "."

    if any(word in q_lower for word in ["show projects", "projects", "fetch projects", "find projects", "list projects"]):
        return format_projects(PROJECTS)

    if any(word in q_lower for word in ["ai", "machine learning", "ml", "assistant", "voice"]):
        return format_projects(fetch_projects_by_domain("ai"))

    if any(word in q_lower for word in ["data analysis", "eda", "analytics", "pandas", "numpy"]):
        return format_projects(fetch_projects_by_domain("data"))

    if any(word in q_lower for word in ["web", "website", "streamlit", "portfolio", "app"]):
        return format_projects(fetch_projects_by_domain("web"))

    if any(word in q_lower for word in ["python", "automation", "development", "coding"]):
        return format_projects(fetch_projects_by_domain("python"))

    if any(word in q_lower for word in ["vision", "opencv", "face detection", "computer vision", "camera"]):
        return format_projects(fetch_projects_by_domain("vision"))

    if any(word in q_lower for word in ["what can you do", "help", "how can you help", "what are you capable of"]):
        return (
            "I can answer portfolio questions, explain key skills, and help you discover projects "
            "by domain like AI, web, data analysis, Python, and computer vision."
        )

    return (
        "I can help with portfolio questions, project discovery, and general conversation. "
        "Try asking things like ‘show AI projects,’ ‘tell me about Vansh,’ or ‘what tech stack do you use?’"
    )


def transcribe_audio(audio_data: bytes):
    if sr is None:
        return None

    try:
        tf = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
        tf.write(audio_data)
        tf.close()
        recognizer = sr.Recognizer()
        with sr.AudioFile(tf.name) as source:
            audio = recognizer.record(source)
        text = recognizer.recognize_google(audio)
        os.unlink(tf.name)
        return text
    except Exception:
        return None


def speak_text(text: str):
    if not text:
        return None

    try:
        audio = gTTS(text=text, lang="en")
        buffer = io.BytesIO()
        audio.write_to_fp(buffer)
        return buffer.getvalue()
    except Exception:
        return None


BASE_DIR = Path(__file__).resolve().parents[1]
background_path = BASE_DIR / "assets" / "background.png"

if background_path.exists():
    bg = base64.b64encode(background_path.read_bytes()).decode("utf-8")
    background_css = f"""
        linear-gradient(90deg, rgba(2, 6, 23, 0.78), rgba(15, 23, 42, 0.42)),
        url("data:image/png;base64,{bg}")
    """
else:
    background_css = "linear-gradient(90deg, rgba(2, 6, 23, 0.88), rgba(15, 23, 42, 0.62))"

st.markdown(
    f"""
    <style>
        .stApp {{
            background: {background_css};
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
            background-repeat: no-repeat;
        }}

        [data-testid="stMain"],
        [data-testid="stMainBlockContainer"] {{
            background: transparent;
        }}

        [data-testid="stHeader"] {{
            background: rgba(15, 23, 42, 0.30);
            backdrop-filter: blur(8px);
        }}

        .block-container {{
            max-width: 1100px;
            padding-top: 1.5rem;
            padding-bottom: 2rem;
        }}

        .chat-shell {{
            background: rgba(17, 24, 39, 0.55);
            border: 1px solid rgba(255,255,255,0.09);
            border-radius: 22px;
            padding: 1rem 0.5rem 0.5rem 0.5rem;
            box-shadow: 0 18px 60px rgba(15, 23, 42, 0.25);
            backdrop-filter: blur(10px);
        }}

        .chat-message {{
            max-width: 780px;
            margin: 0 auto 0.8rem auto;
            border-radius: 18px;
            padding: 0.8rem 1rem;
        }}

        .stChatMessage {{
            border-radius: 18px;
        }}

        .stChatMessage[data-testid="stChatMessage"] {{
            border: 1px solid rgba(255,255,255,0.06);
            backdrop-filter: blur(6px);
        }}

        .stChatMessage [data-testid="stChatMessageContent"] {{
            background: rgba(15, 23, 42, 0.62);
            border-radius: 18px;
            padding: 0.9rem 1rem;
            border: 1px solid rgba(148, 163, 184, 0.12);
        }}

        .stChatMessage[data-testid="user"] [data-testid="stChatMessageContent"] {{
            background: linear-gradient(135deg, rgba(59,130,246,0.35), rgba(168,85,247,0.30));
            border: 1px solid rgba(125, 211, 252, 0.18);
        }}

        .stChatMessage[data-testid="assistant"] [data-testid="stChatMessageContent"] {{
            background: rgba(15, 23, 42, 0.56);
        }}

        .stChatInput {{
            border-radius: 16px;
            border: 1px solid rgba(148, 163, 184, 0.28);
            background: rgba(15, 23, 42, 0.72);
            box-shadow: 0 10px 30px rgba(2, 6, 23, 0.18);
        }}

        .stChatInput > div {{
            border-radius: 16px;
        }}

        .stButton > button,
        .stDownloadButton > button,
        .stLinkButton > button {{
            border-radius: 12px;
            background: rgba(15, 23, 42, 0.72);
            border: 1px solid rgba(148, 163, 184, 0.22);
            color: white;
        }}

        .sidebar-content {{
            background: rgba(15, 23, 42, 0.45);
            border-radius: 16px;
            padding: 0.3rem;
        }}
    </style>
    """,
    unsafe_allow_html=True,
)

st.set_page_config(page_title="Portfolio Assistant", page_icon="🤖", layout="wide")

st.markdown('<div class="chat-shell">', unsafe_allow_html=True)
st.title("Portfolio Assistant 🤖")
st.caption("Gemini-powered chat, memory, and voice support for your portfolio")

if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "Hi! I can answer questions about Vansh, his skills, and his project work. Try asking about AI, web apps, data analysis, or Python projects.",
        }
    ]

if "pending_voice_text" not in st.session_state:
    st.session_state.pending_voice_text = ""

if "last_response" not in st.session_state:
    st.session_state.last_response = ""

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

with st.sidebar:
    st.subheader("Quick actions")
    if st.button("About Vansh"):
        st.session_state.messages.append({"role": "user", "content": "about me"})
        st.session_state.messages.append({"role": "assistant", "content": get_answer("about me", st.session_state.messages)})

    if st.button("AI Projects"):
        st.session_state.messages.append({"role": "user", "content": "AI projects"})
        st.session_state.messages.append({"role": "assistant", "content": get_answer("AI projects", st.session_state.messages)})

    if st.button("Web Projects"):
        st.session_state.messages.append({"role": "user", "content": "web projects"})
        st.session_state.messages.append({"role": "assistant", "content": get_answer("web projects", st.session_state.messages)})

    if st.button("Python Work"):
        st.session_state.messages.append({"role": "user", "content": "python projects"})
        st.session_state.messages.append({"role": "assistant", "content": get_answer("python projects", st.session_state.messages)})

    st.markdown("---")
    st.caption("Voice input")
    voice_input = st.audio_input("Speak your question", key="voice_assistant")
    if voice_input is not None:
        audio_bytes = voice_input.read()
        recognized = transcribe_audio(audio_bytes)
        if recognized:
            st.session_state.pending_voice_text = recognized
            st.success(f"Detected voice: {recognized}")
        else:
            st.warning("Voice transcription failed. Please type your question or try again.")

    if st.button("Use voice text") and st.session_state.pending_voice_text:
        user_input = st.session_state.pending_voice_text
        st.session_state.pending_voice_text = ""
        st.session_state.messages.append({"role": "user", "content": user_input})
        assistant_reply = get_answer(user_input, st.session_state.messages[:-1])
        st.session_state.messages.append({"role": "assistant", "content": assistant_reply})
        st.session_state.last_response = assistant_reply
        st.rerun()

text_input = st.chat_input("Ask about projects, skills, or profile...")

if text_input:
    st.session_state.messages.append({"role": "user", "content": text_input})
    assistant_reply = get_answer(text_input, st.session_state.messages[:-1])
    st.session_state.messages.append({"role": "assistant", "content": assistant_reply})
    st.session_state.last_response = assistant_reply
    st.rerun()

if st.session_state.last_response:
    with st.container():
        st.markdown("---")
        if st.button("🔊 Play last answer"):
            audio_data = speak_text(st.session_state.last_response)
            if audio_data:
                st.audio(audio_data, format="audio/mp3")
            else:
                st.warning("Voice output is unavailable in this environment.")

st.markdown("</div>", unsafe_allow_html=True)
