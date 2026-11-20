
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

from modules.embeddings import generate_embeddings


# Load job dataset
jobs = pd.read_csv("data/jobs.csv")


def recommend_jobs(candidate_skills, preferred_location="Any"):

    results = jobs.copy()

    # Convert candidate skills into text
    candidate_text = " ".join(candidate_skills)

    if not candidate_text.strip():
        return results.head(0)

    # Calculate skill matching score
    def calculate_skill_score(job_skills):

        required = [
            skill.strip().lower()
            for skill in job_skills.split(",")
        ]

        candidate = [
            skill.lower()
            for skill in candidate_skills
        ]

        matched = set(required) & set(candidate)

        return len(matched) / len(set(required)) if required else 0

    results["skill_score"] = results["skills"].apply(
        calculate_skill_score
    )

    # Generate job descriptions
    job_texts = (
        results["job_title"] + " " +
        results["skills"] + " " +
        results["description"]
    ).tolist()

    # Generate embeddings
    job_embeddings = generate_embeddings(job_texts)

    candidate_embedding = generate_embeddings(
        [candidate_text]
    )

    # Calculate semantic similarity
    semantic_scores = cosine_similarity(
        candidate_embedding,
        job_embeddings
    )[0]

    results["semantic_score"] = semantic_scores

    # Normalize semantic similarity
    results["semantic_score"] = (
        results["semantic_score"].clip(0, 1)
    )

    # Location preference score
    if preferred_location == "Any":
        results["location_score"] = 1.0
    else:
        results["location_score"] = (
            results["location"].str.lower()
            == preferred_location.lower()
        ).astype(float)

    # Calculate final weighted score
    results["match_score"] = (
        results["skill_score"] * 0.60 +
        results["semantic_score"] * 0.30 +
        results["location_score"] * 0.10
    )

    # Sort jobs by highest score
    results = results.sort_values(
        by="match_score",
        ascending=False
    )

    return results.head(5)
