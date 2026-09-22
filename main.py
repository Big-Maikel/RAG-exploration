from pathlib import Path
import ollama

DOCUMENTS_DIR = Path("documents")

documents = {}

for file_path in DOCUMENTS_DIR.glob("*.txt"):
    documents[file_path.name] = file_path.read_text(
        encoding="utf-8"
    )

selected_document = documents["return_policy.txt"]

question = "How long can I return an electronic item?"

prompt = f"""
You are a customer service assistant.

Answer the customer's question using ONLY the information
provided in the document below.

If the answer cannot be found in the document, say:
"I don't know based on the provided policy."

DOCUMENT:
{selected_document}

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

print(response["message"]["content"])