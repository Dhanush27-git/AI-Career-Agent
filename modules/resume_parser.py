
from pypdf import PdfReader

def extract_text(pdf_file):

    reader = PdfReader(pdf_file)

    text = ""

    for page in reader.pages:
        text += page.extract_text() or ""

    return text


def extract_skills(text):

    skills_list = [
        "Python", "Java", "C++", "SQL",
        "Machine Learning", "Deep Learning",
        "Artificial Intelligence", "Data Science",
        "Pandas", "NumPy", "Scikit-learn",
        "TensorFlow", "PyTorch", "React",
        "JavaScript", "HTML", "CSS",
        "FastAPI", "Flask", "Docker",
        "AWS", "Azure", "Google Cloud",
        "Git", "GitHub", "NLP",
        "Generative AI", "LLM", "RAG",
        "Power BI", "Excel"
    ]

    found_skills = []

    for skill in skills_list:
        if skill.lower() in text.lower():
            found_skills.append(skill)

    return found_skills
