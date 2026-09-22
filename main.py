from pathlib import Path
import ollama

DOCUMENTS_DIR = Path("documents")

documents = {}

for file_path in DOCUMENTS_DIR.glob("*.txt"):
    documents[file_path.name] = file_path.read_text(
        encoding="utf-8"
    )

document_options = list(documents.keys())

print("\n=== Customer Service Assistant ===")
print("\nAvailable documents:")

for number, filename in enumerate(document_options, start=1):
    display_name = filename.replace("_", " ").replace(".txt", "").title()
    print(f"{number}. {display_name}")

while True:
    try:
        choice = int(input("\nChoose a document: "))

        if 1 <= choice <= len(document_options):
            break

        print("Please choose a valid document number.")

    except ValueError:
        print("Please enter a number.")

selected_filename = document_options[choice - 1]
selected_document = documents[selected_filename]

question = input("What is your question? ")

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
    ],
    stream=True
)

print("\nAssistant:")

for chunk in response:
    print(chunk["message"]["content"], end="", flush=True)

print(f"\n\nDocument used: {selected_filename}")