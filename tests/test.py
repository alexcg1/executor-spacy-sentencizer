from jina import Executor
from docarray import Document, DocumentArray

with open("./data/rabbit.txt") as file:
    doc = Document(text=file.read())

docs = DocumentArray([doc])

sentencizer = Executor.from_hub("jinahub://SpacySentencizer")

sentencizer.segment(docs)

for doc in docs:
    print(doc)
    for chunk in doc.chunks:
        print(chunk.text)
