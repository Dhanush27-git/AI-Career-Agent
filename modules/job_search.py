
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

from modules.embeddings import generate_embeddings


# Load job dataset
jobs = pd.read_csv("data/jobs.csv")


def search_jobs(query):

    job_texts = (
        jobs["job_title"] + " " +
        jobs["skills"] + " " +
        jobs["description"]
    ).tolist()

    # Generate embeddings
    job_embeddings = generate_embeddings(job_texts)

    query_embedding = generate_embeddings([query])

    # Calculate similarity
    scores = cosine_similarity(
        query_embedding,
        job_embeddings
    )[0]

    # Rank jobs
    jobs["match_score"] = scores

    results = jobs.sort_values(
        by="match_score",
        ascending=False
    )

    return results.head(5)
