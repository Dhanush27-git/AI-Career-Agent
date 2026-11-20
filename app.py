
import streamlit as st
from modules.job_search import search_jobs
from modules.career_agent import run_agent
from modules.resume_parser import extract_text, extract_skills
from modules.recommender import recommend_jobs
from modules.memory import (
    initialize_memory,
    save_message,
    get_chat_history,
    save_preference,
    get_preferences,
    clear_chat_history
)
initialize_memory()
# Page configuration
st.set_page_config(
    page_title="AI Career Agent",
    page_icon="🚀",
    layout="wide"
)

# Custom CSS for professional UI
st.markdown("""
<style>

.stApp {
    background-color: #101820;
}

h1 {
    color: #38BDF8;
    font-weight: bold;
}

h2, h3 {
    color: #7DD3FC;
}

.stButton > button {
    background-color: #0284C7;
    color: white;
    border-radius: 10px;
    border: none;
    padding: 10px 20px;
    font-weight: bold;
}

.stButton > button:hover {
    background-color: #0369A1;
    color: white;
}

.stTextInput input {
    border-radius: 8px;
}

.stTextArea textarea {
    border-radius: 8px;
}

div[data-testid="stFileUploader"] {
    border-radius: 10px;
}

</style>
""", unsafe_allow_html=True)

# Application title
st.title("🚀 AI Career Agent")
st.markdown("""
### Your Intelligent Career Companion

Upload your resume, discover your skills,
search jobs using AI semantic search,
and receive personalized job recommendations.

**Features:**
- Resume Parsing
- Semantic Job Search
- Personalized Job Recommendations
- AI Career Chatbot
- Persistent Memory using SQLite
""")
st.subheader("Your Personal AI Job Assistant")

st.write(
    "Upload your resume to discover your skills "
    "and find suitable job opportunities."
)

st.divider()

# Resume upload
uploaded_file = st.file_uploader(
    "Upload Your Resume (PDF)",
    type=["pdf"]
)

if uploaded_file is not None:

    st.success("Resume uploaded successfully!")

    # Extract resume text
    resume_text = extract_text(uploaded_file)

    # Extract skills
    skills = extract_skills(resume_text)

    st.subheader("📄 Resume Information")

    st.write("Total characters extracted:", len(resume_text))

    # Display skills
    st.subheader("💡 Skills Identified")

    if skills:

        st.write("Skills found in your resume:")

        cols = st.columns(3)

        for i, skill in enumerate(skills):
            cols[i % 3].success(skill)

    else:
        st.warning("No matching skills found.")

    # Display resume text
    st.subheader("Resume Preview")

    st.text_area(
        "Extracted Resume Text",
        resume_text,
        height=200
    )

st.divider()

st.header("🔍 AI Semantic Job Search")

st.write(
    "Describe the job you are looking for "
    "in your own words."
)

query = st.text_input(
    "Enter your job search query",
    placeholder="Example: I want a Python and AI internship"
)

if st.button("Search Jobs"):

    if query:

        with st.spinner("AI is searching for jobs..."):

            results = search_jobs(query)

        st.subheader("🎯 Recommended Jobs")

        for index, job in results.iterrows():

            st.markdown(
                f"### {job['job_title']}"
            )

            st.write("Company:", job["company"])
            st.write("Location:", job["location"])
            st.write("Job Type:", job["job_type"])
            st.write("Skills:", job["skills"])

            st.progress(
                max(0.0, min(1.0, float(job["match_score"])))
            )

            st.write(
                "Match Score:",
                round(float(job["match_score"]) * 100, 2),
                "%"
            )

            st.divider()

    else:

        st.warning("Please enter a search query.")

st.divider()

st.header("🎯 Personalized Job Recommendations")

st.write(
    "Find jobs based on the skills extracted "
    "from your uploaded resume."
)

if uploaded_file is not None and skills:

    preferred_location = st.selectbox(
        "Select your preferred location",
        ["Any", "Bengaluru", "Gurugram",
         "Chennai", "Hyderabad", "Remote"]
    )

    if st.button("Recommend Jobs For Me"):

        with st.spinner("Analyzing your profile..."):

            recommendations = recommend_jobs(
                skills,
                preferred_location
            )

        st.subheader("Your Top 5 Job Recommendations")

        for index, job in recommendations.iterrows():

            st.markdown(
                f"### {job['job_title']}"
            )

            st.write("Company:", job["company"])
            st.write("Location:", job["location"])

            st.write("Required Skills:", job["skills"])

            st.write(
                "Matching Skills:",
                round(job["skill_score"] * 100, 2),
                "%"
            )

            st.write(
                "Semantic Similarity:",
                round(job["semantic_score"] * 100, 2),
                "%"
            )

            st.write(
                "Overall Match:",
                round(job["match_score"] * 100, 2),
                "%"
            )

            st.progress(
                float(job["match_score"])
            )

            st.divider()

else:

    st.info(
        "Upload your resume first to receive "
        "personalized job recommendations."
    )
  
st.divider()

st.header("🤖 Chat with AI Career Agent")

st.write(
    "Ask questions about jobs, internships, "
    "your skills and career opportunities."
)

# Load previous conversations
if "chat_history" not in st.session_state:
    st.session_state.chat_history = get_chat_history()

candidate_skills = skills if uploaded_file is not None else []

# Display previous messages
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
user_message = st.chat_input(
    "Ask me about jobs or career opportunities..."
)

if user_message:

    save_message("user", user_message)

    with st.chat_message("user"):
        st.markdown(user_message)

    with st.chat_message("assistant"):

        with st.spinner("AI Career Agent is thinking..."):

            reply, updated_history = run_agent(
                user_message,
                st.session_state.chat_history,
                candidate_skills
            )

            st.session_state.chat_history = updated_history

            save_message("assistant", reply)

        st.markdown(reply)

# Clear chat
if st.button("Clear Chat"):

    clear_chat_history()

    st.session_state.chat_history = []

    st.rerun()
