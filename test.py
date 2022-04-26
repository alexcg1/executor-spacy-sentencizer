from jina import Executor, Flow
from docarray import Document, DocumentArray
from executor import SpacySentencizer

with open("./data/rabbit.txt") as file:
    doc = Document(text=file.read())

docs = DocumentArray([doc])

# sentencizer = Executor.from_hub("jinahub://SpacySentencizer")
# sentencizer = SpacySentencizer

# sentencizer.segment(docs)

flow = Flow().add(uses="jinahub://SpacySentencizer", force_update=True)

with flow:
    docs = flow.index(docs)

for doc in docs:
    print(doc)
    for chunk in doc.chunks:
        print(chunk.text)
        print("---")
