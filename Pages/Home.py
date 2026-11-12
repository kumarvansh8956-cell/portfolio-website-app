
import streamlit as st

st.title("Hello, I'm Vansh Kumar! 👋")
st.subheader("Aspiring AI Engineer | Python Developer")

st.write(
    """
    I'm a Computer Science Engineering student specializing in Artificial Intelligence and
    Machine Learning. I enjoy creating Python-based solutions, experimenting with AI systems,
    and turning ideas into practical, real-world tools.
    """
)

st.markdown("---")

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("Explore Projects", use_container_width=True):
        st.switch_page("Pages/projects.py")

with col2:
    if st.button("About Me", use_container_width=True):
        st.switch_page("Pages/about.py")

with col3:
    if st.button("Open Assistant", use_container_width=True):
        st.switch_page("Chatbot/chatbot.py")

st.markdown("---")

st.write("Want to explore my code and projects?")
st.link_button("Visit my GitHub", "https://github.com/kumarvansh8956-cell")

st.subheader("Building Intelligence.")