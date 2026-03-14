import os
import re
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

RESUME_FOLDER = "resumes"
DB_PATH = "resume_db"


def extract_metadata(text):

    skills = re.findall(
        r"(Python|Java|Machine Learning|SQL|AWS|Docker|TensorFlow)",
        text,
        re.IGNORECASE
    )

    experience = re.findall(r"(\d+)\+?\s+years", text)

    return {
        "skills": list(set(skills)),
        "experience_years": int(experience[0]) if experience else 0
    }


def load_resumes():

    docs = []

    for file in os.listdir(RESUME_FOLDER):

        if file.endswith(".txt"):

            path = os.path.join(RESUME_FOLDER, file)

            with open(path) as f:
                text = f.read()

            metadata = extract_metadata(text)

            metadata["source"] = file

            docs.append(Document(
                page_content=text,
                metadata=metadata
            ))

    return docs


def chunk_documents(docs):

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100
    )

    chunks = splitter.split_documents(docs)

    return chunks


def create_vector_db(chunks):

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    db = Chroma.from_documents(
        chunks,
        embeddings,
        persist_directory=DB_PATH
    )

    db.persist()

    print("Vector database created.")


if __name__ == "__main__":

    print("Loading resumes...")
    docs = load_resumes()

    print("Chunking resumes...")
    chunks = chunk_documents(docs)

    print("Generating embeddings...")
    create_vector_db(chunks)