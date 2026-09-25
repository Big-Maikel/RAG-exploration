import numpy as np
import ollama

text1 = "How much does express shipping cost?"
text2 = "Express Shipping: 2-3 business days ($12.99)"
text3 = "Earn 1 point for every $1 spent"


def get_embedding(text):
    response = ollama.embed(
        model="nomic-embed-text",
        input=text
    )

    return response["embeddings"][0]


def cosine_similarity(vector_a, vector_b):
    a = np.array(vector_a)
    b = np.array(vector_b)

    return np.dot(a, b) / (
        np.linalg.norm(a) * np.linalg.norm(b)
    )


embedding1 = get_embedding(text1)
embedding2 = get_embedding(text2)
embedding3 = get_embedding(text3)

similarity_12 = cosine_similarity(embedding1, embedding2)
similarity_13 = cosine_similarity(embedding1, embedding3)

print(f"Question ↔ Shipping: {similarity_12:.4f}")
print(f"Question ↔ Loyalty:  {similarity_13:.4f}")