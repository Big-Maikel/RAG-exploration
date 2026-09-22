from pathlib import Path
import ollama

DOCUMENTS_DIR = Path("documents")

documents = {}

for file_path in DOCUMENTS_DIR.glob("*.txt"):
    documents[file_path.name] = file_path.read_text(
        encoding="utf-8"
    )

print("Available documents:")
for filename in documents:
    print(f"- {filename}")

document_choice = input("\nWhich document do you want to use? ")

if document_choice not in documents:
    print("Document not found.")
    exit()

question = input("What is your question? ")

selected_document = documents[document_choice]

prompt = f"""
You are a customer service assistant.

Answer the customer's question using ONLY the information
provided in the document below.

If the answer cannot be found in the document, say:
"I don't know based on the provided policy."

Clearly mention which document you used.

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

print("\nAssistant:")
print(response["message"]["content"])