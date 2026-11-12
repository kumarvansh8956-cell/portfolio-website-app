
import streamlit as st

st.title("My Projects 🚀")
st.write(
    """
    A collection of things I've built, explored, and experimented with using Python,
    AI, and modern tooling.
    """
)

st.markdown("---")

category = st.selectbox(
    "Explore by category",
    [
        "All Projects",
        "AI & Machine Learning",
        "Python Development",
        "Data Analysis",
        "Web Applications",
        "Computer Vision",
    ],
)

projects = [
    {
        "name": "Personal AI Assistant",
        "description": "A local-first voice assistant using speech recognition and speech generation.",
        "tech": "Python, Whisper, Piper",
        "category": "AI & Machine Learning",
        "status": "In Progress",
        "project": (
            "https://github.com/kumarvansh8956-cell/Python_project/blob/main/Jarvis_v3.py",
            "https://github.com/kumarvansh8956-cell/Text_to_Speak_with_piper/blob/main/Speaking.py",
            "https://github.com/kumarvansh8956-cell/Speak-to-Text/blob/main/Listening.py",
        ),
    },
    {
        "name": "EDA Projects",
        "description": "Exploratory data analysis on multiple real-world datasets.",
        "tech": "Python, Pandas, NumPy, Matplotlib, seaborn",
        "category": "Data Analysis",
        "status": "Completed",
        "project": (
            "https://github.com/kumarvansh8956-cell/Amazon-E-Commerce-Data-Analysis/blob/main/Amazon_E-Commerce_Dataset_Analysis.ipynb",
            "https://github.com/kumarvansh8956-cell/HR-Data-Analysis-with-Python/blob/main/HR_Analytics_dataset.ipynb",
            "https://github.com/kumarvansh8956-cell/Titanic-Survival-EDA/blob/main/The_Titanic_notebook.ipynb",
            "https://github.com/kumarvansh8956-cell/Car-Sales-Analysis-by-Pandas-and-numpy/blob/main/Car-Sales-Analysis.ipynb",
        ),
    },
    {
        "name": "Streamlit Portfolio",
        "description": "A multipage developer portfolio with custom backgrounds and AI integration plans.",
        "tech": "Python, Streamlit",
        "category": "Web Applications",
        "status": "In Progress",
    },
    {
        "name": "Face Detection System",
        "description": "Real-time face, eye and smile detection using a webcam.",
        "tech": "Python, OpenCV, Haar Cascade",
        "category": "Python Development",
        "status": "Completed",
        "project": (
            "https://github.com/kumarvansh8956-cell/Open_CV-Python/blob/main/face_detection.py",
            "https://github.com/kumarvansh8956-cell/Open_CV-Python/blob/main/mini_assesment_4.py",
            "https://github.com/kumarvansh8956-cell/Open_CV-Python/blob/main/Mini_assesment_3.py",
            "https://github.com/kumarvansh8956-cell/Open_CV-Python/blob/main/Mini_Assesment_2.py",
            "https://github.com/kumarvansh8956-cell/Open_CV-Python/blob/main/Mini_assesment.py",
        ),
    },
]

if category == "All Projects":
    filtered_projects = projects
else:
    filtered_projects = [p for p in projects if p["category"] == category]

for project in filtered_projects:
    with st.container(border=True):
        st.subheader(project["name"])
        st.write(project["description"])
        st.caption("Technologies: " + project["tech"])
        st.caption("Status: " + project["status"])

        if st.button("View Project Links", key=project["name"]):
            with st.expander("Project links", expanded=True):
                for pro in project.get("project", ()):
                    st.markdown(f"[View on GitHub]({pro})")

if not filtered_projects:
    st.info("No projects found in this category.")
