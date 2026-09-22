from pathlib import Path

DOCUMENTS_DIR = Path("documents")

documents = {}

for file_path in DOCUMENTS_DIR.glob("*.txt"):
    documents[file_path.name] = file_path.read_text(
        encoding="utf-8"
    )

for filename, content in documents.items():
    print(f"\n--- {filename} ---")
    print(content[:100])

