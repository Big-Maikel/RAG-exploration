from pathlib import Path
import ollama

DOCUMENTS_DIR = Path("documents")

documents = {}

for file_path in DOCUMENTS_DIR.glob("*.txt"):
    documents[file_path.name] = file_path.read_text(
        encoding="utf-8"
    )

document_keywords = {
    "return_policy.txt": [
        "return",
        "refund",
        "exchange",
        "returning",
        "damaged",
        "defective"
    ],

    "delivery_policy.txt": [
        "delivery",
        "shipping",
        "package",
        "carrier",
        "shipment",
        "deliver"
    ],

    "loyalty_program.txt": [
        "loyalty",
        "points",
        "reward",
        "birthday",
        "membership",
        "member",
        "bonus"
    ]
}

def find_relevant_documents(question):
    question = question.lower()

    relevant_documents = []

    for document, keywords in document_keywords.items():
        score = 0

        for keyword in keywords:
            if keyword in question:
                score += 1

        if score > 0:
            relevant_documents.append(document)

    return relevant_documents

print("\n=== Customer Service Assistant ===")

question = input("\nWhat is your question? ")

relevant_documents = find_relevant_documents(question)

if len(relevant_documents) == 0:
    print(
        "\nI'm sorry, I can only answer questions about "
        "our returns, delivery, or loyalty program."
    )
    exit()

if len(relevant_documents) > 1:
    print(
        "\nYour question is too complex and spans multiple "
        "policy areas. Please ask about one topic at a time."
    )
    exit()

selected_filename = relevant_documents[0]
selected_document = documents[selected_filename]

prompt = f"""
You are a customer service assistant.

Answer the customer's question using ONLY the information
provided in the document below and dont make-up things that aren't mentioned in the document.

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
    ],
    stream=True
)

print("\nAssistant:")

for chunk in response:
    print(chunk["message"]["content"], end="", flush=True)

display_name = (
    selected_filename
    .replace("_", " ")
    .replace(".txt", "")
    .title()
)

print(f"\n\nDocument used: {display_name}")