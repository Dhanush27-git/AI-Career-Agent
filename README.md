# 🚀 AI-Powered Career Agent

## 1. Project Overview

The AI-Powered Career Agent is an intelligent job assistance application designed to help job seekers discover suitable career opportunities based on their resumes, skills, interests, and preferences.

The application uses Natural Language Processing (NLP), semantic search, machine learning embeddings, personalized recommendation techniques, and conversational memory to improve the job-search experience.

## 2. Problem Statement

Job seekers often spend considerable time searching for suitable jobs across different platforms. Finding opportunities that match their skills, qualifications, and preferred locations can be difficult.

This project addresses the problem by providing an intelligent system that analyzes resumes, searches relevant jobs, and recommends suitable opportunities automatically.

## 3. Objectives

- Automatically extract information and skills from PDF resumes.
- Perform semantic job searches using natural-language queries.
- Recommend jobs based on candidate skills.
- Rank job opportunities using a recommendation score.
- Provide a conversational career assistant.
- Store chat history and user preferences using SQLite.
- Improve the job-search experience through personalization.

## 4. Main Features

### 4.1 Resume Parsing
- Upload resumes in PDF format.
- Extract text using PyPDF.
- Identify technical skills automatically.
- Display extracted resume information.

### 4.2 Semantic Job Search
- Accept natural-language job queries.
- Generate text embeddings using Sentence Transformers.
- Calculate cosine similarity.
- Rank jobs according to semantic relevance.

### 4.3 Personalized Job Recommendations
- Analyze candidate skills.
- Calculate skill matching scores.
- Calculate semantic similarity scores.
- Consider preferred job locations.
- Rank the top five job recommendations.

### 4.4 AI Career Conversational Agent
- Allow users to ask career-related questions.
- Search jobs through conversational queries.
- Recommend opportunities based on resume skills.
- Support tool-calling integration when an OpenAI API key is configured.
- Provide a rule-based local fallback without API charges.

### 4.5 Persistent Conversation Memory
- Store chat history using SQLite.
- Save preferred job roles.
- Remember preferred locations.
- Remember preferred job types.
- Retrieve saved preferences for future searches.

## 5. Technologies Used

| Category | Technologies |
|---|---|
| Programming Language | Python |
| Frontend | Streamlit |
| Machine Learning | Scikit-learn |
| NLP and Embeddings | Sentence Transformers |
| Data Processing | Pandas, NumPy |
| PDF Processing | PyPDF |
| Database | SQLite |
| Similarity Measurement | Cosine Similarity |
| Conversational AI | Python-based local agent, optional OpenAI API |
| Development Tool | Visual Studio Code |

## 6. System Architecture

The application follows this workflow:

1. User uploads a PDF resume.
2. Resume parser extracts text.
3. Skill extraction identifies candidate skills.
4. Embedding generation converts text into numerical vectors.
5. Semantic search finds relevant jobs.
6. Recommendation engine ranks jobs.
7. Conversational agent handles user queries.
8. SQLite stores conversation history and preferences.
9. Results are displayed through the Streamlit interface.

## 7. Recommendation Ranking

The application calculates an overall recommendation score using:

Overall Match Score =

(Skill Score × 0.60) + (Semantic Score × 0.30) + (Location Score × 0.10)

The highest-scoring jobs are displayed first.

## 8. Project Folder Structure

```text
AI-CAREER-AGENT/
│
├── data/
│   └── jobs.csv
│
├── modules/
│   ├── resume_parser.py
│   ├── embeddings.py
│   ├── job_search.py
│   ├── recommender.py
│   ├── career_agent.py
│   └── memory.py
│
├── app.py
├── .env
├── .gitignore
└── README.md
```

The SQLite database file is generated automatically when the memory module runs.

## 9. Installation and Execution

### Step 1: Clone the repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd AI-Career-Agent
```

### Step 2: Create a virtual environment

```bash
python -m venv venv
```

### Step 3: Activate the environment

Windows CMD:

```cmd
venv\Scripts\activate.bat
```

### Step 4: Install dependencies

```bash
pip install streamlit fastapi uvicorn pandas numpy sentence-transformers scikit-learn pypdf sqlalchemy python-multipart openai python-dotenv requests
```

### Step 5: Run the application

```bash
streamlit run app.py
```

### Step 6: Open the application

Open the local URL displayed in your terminal, usually:

```text
http://localhost:8501
```

## 10. Testing and Evaluation

The following functional tests were performed:

- PDF resume upload and text extraction.
- Automatic skill identification.
- Semantic job search using natural-language queries.
- Personalized job recommendation.
- Job ranking using weighted scores.
- Saving and retrieving user preferences.
- Persistent conversation history after restarting the application.
- Empty search and missing-resume handling.
- Clearing chat history while preserving saved preferences.

## 11. Limitations

- The current job dataset contains sample job listings.
- Resume skill extraction uses a predefined skill list.
- Local conversational responses use rule-based logic.
- Preference detection recognizes predefined job roles and locations.
- Recommendation scores are ranking indicators, not guaranteed measures of job suitability.
- Live job-platform integration is not currently implemented.

## 12. Future Enhancements

- Integrate live job portals and recruitment APIs.
- Improve resume understanding using advanced NLP models.
- Add advanced LLM-based conversational capabilities.
- Implement authentication and multiple user profiles.
- Develop advanced recommendation evaluation metrics.
- Deploy the application to a cloud platform.
- Add Docker-based deployment.

## 13. Conclusion

The AI-Powered Career Agent demonstrates how machine learning, semantic search, resume parsing, recommendation systems, and conversational memory can be combined to create an intelligent career assistance platform.

The system helps job seekers identify relevant opportunities, understand their skills, and discover personalized career recommendations through a user-friendly application.

---

**Project:** AI-Powered Career Agent  
**Domain:** Artificial Intelligence and Data Science  
**Programming Language:** Python  
**Interface:** Streamlit  
**Database:** SQLite