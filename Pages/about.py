
import streamlit as st

st.title("About Me 👋")
st.subheader("A curious builder with a practical approach to technology.")

st.write(
    """
    Hey! I'm Vansh Kumar, a Computer Science Engineering student specializing in
    Artificial Intelligence and Machine Learning.

    I enjoy learning by building. I like to break down ideas, prototype them quickly,
    debug through real problems, and turn concepts into useful projects that actually work.
    """
)

st.markdown("---")

st.header("What Interests Me")

col1, col2 = st.columns(2)

with col1:
    with st.container(border=True):
        st.subheader("🧠 AI Engineering")
        st.write("""
        - Artificial Intelligence
        - Machine Learning
        - Local AI Systems
        - AI Agents
        """)

with col2:
    with st.container(border=True):
        st.subheader("⚙️ Development")
        st.write("""
        - Python Development
        - Automation
        - Research & Analysis
        - Intelligent Applications
        """)

st.markdown("---")

st.header("How I Learn")

st.write(
    """
    I believe the best way to understand technology is by experimenting with it.
    I enjoy exploring different approaches, debugging problems, and building practical solutions
    that teach me why something works—not just that it works.
    """
)

st.markdown("---")

st.header("Beyond Technology 🎌")

st.write(
    """
    Outside programming, I'm an anime enthusiast. I enjoy stories built around strategy,
    problem-solving, complex characters, and unconventional ideas.

    Technology isn't my only curiosity.
    """
)

st.markdown("---")

st.header("What I'm Working Towards 🚀")

st.write(
    """
    My long-term goal is to become an AI Engineer and build meaningful systems that create real impact.
    I’m continuously learning, experimenting, and creating projects one step at a time.
    """
)

st.markdown("---")

st.subheader("Explore My Work")

col1, col2 = st.columns(2)

with col1:
    st.link_button("Visit My GitHub", "https://github.com/kumarvansh8956-cell")

with col2:
    st.link_button("Email Me", "mailto:Kumarvansh8956@gmail.com")

st.caption("Still exploring. Still building. Always learning.")
