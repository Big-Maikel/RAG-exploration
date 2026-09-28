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


print(f"Number of chunks: {len(chunks)}")

for i, chunk in enumerate(chunks):
    print(f"\n--- Chunk {i + 1} ---")
    print(f"Document: {chunk['document']}")
    print(chunk["text"])