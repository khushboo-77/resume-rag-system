from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

import json

DB_PATH = "resume_db"


def load_db():

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    db = Chroma(
        persist_directory=DB_PATH,
        embedding_function=embeddings
    )

    return db


def keyword_score(jd, text):

    keywords = ["Python", "Machine Learning", "SQL", "AWS"]

    score = 0

    for k in keywords:

        if k.lower() in jd.lower() and k.lower() in text.lower():
            score += 10

    return score


def search_candidates(job_description, k=10):

    db = load_db()

    results = db.similarity_search_with_score(job_description, k=k)

    matches = []

    for doc, score in results:

        semantic_score = int((1 - score) * 100)

        keyword = keyword_score(job_description, doc.page_content)

        final_score = semantic_score + keyword

        candidate = {
            "candidate_name": doc.metadata.get("source"),
            "resume_path": f"resumes/{doc.metadata.get('source')}",
            "match_score": min(final_score, 100),
            "matched_skills": doc.metadata.get("skills"),
            "relevant_excerpts": [doc.page_content[:200]],
            "reasoning": "Resume matched with job description using semantic + keyword search"
        }

        matches.append(candidate)

    return matches


if __name__ == "__main__":

    jd = open("jobs/job1.txt").read()

    results = search_candidates(jd)

    output = {
        "job_description": jd,
        "top_matches": results
    }

    print(json.dumps(output, indent=2))