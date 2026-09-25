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
    document_scores = {}

    for document, keywords in document_keywords.items():
        score = 0

        for keyword in keywords:
            if keyword in question:
                score += 1

        document_scores[document] = score

        if score > 0:
            relevant_documents.append(document)

    return relevant_documents, document_scores


print("\n=== Customer Service Assistant ===")

question = input("\nWhat is your question? ")

relevant_documents, document_scores = find_relevant_documents(question)

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

selected_score = document_scores[selected_filename]

total_score = sum(document_scores.values())

confidence = (selected_score / total_score) * 100


prompt = f"""
You are a customer service assistant.

Answer the customer's question using ONLY the information
provided in the document below and don't make up things
that aren't mentioned in the document.

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

print(f"\n\nRetrieval confidence: {confidence:.0f}%")
print(f"Document used: {display_name}")