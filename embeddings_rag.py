from pathlib import Path
import ollama

DOCUMENTS_DIR = Path("documents")

documents = {}

for file_path in DOCUMENTS_DIR.glob("*.txt"):
    documents[file_path.name] = file_path.read_text(
        encoding="utf-8"
    )

chunks = []

for filename, content in documents.items():
    document_chunks = content.split("\n\n")

    for chunk in document_chunks:
        chunk = chunk.strip()

        if chunk:
            chunks.append({
                "document": filename,
                "text": chunk
            })


def get_embedding(text):
    response = ollama.embed(
        model="all-minilm",
        input=text
    )

    return response["embeddings"][0]


for chunk in chunks:
    chunk["embedding"] = get_embedding(chunk["text"])


question = "How much does express shipping cost?"

question_embedding = get_embedding(question)


def cosine_similarity(vector_a, vector_b):
    import numpy as np

    a = np.array(vector_a)
    b = np.array(vector_b)

    return np.dot(a, b) / (
        np.linalg.norm(a) * np.linalg.norm(b)
    )


for chunk in chunks:
    chunk["similarity"] = cosine_similarity(
        question_embedding,
        chunk["embedding"]
    )


chunks = sorted(
    chunks,
    key=lambda chunk: chunk["similarity"],
    reverse=True
)


best_chunk = chunks[0]


prompt = f"""
You are a customer service assistant.

Answer the customer's question using ONLY the information
provided in the document below and don't make up things
that aren't mentioned in the document.

If the answer cannot be found in the document, say:
"I don't know based on the provided policy."

RETRIEVED DOCUMENT:
{best_chunk["text"]}

CUSTOMER QUESTION:
{question}
"""


response = ollama.chat(
    model="llama3.2",
    messages=[
        {
            "role": "user",
            "content": prompt
        }
    ]
)


print("\nQuestion:")
print(question)

print("\nBest chunk:")
print(best_chunk["text"])

print("\nAssistant:")
print(response["message"]["content"])