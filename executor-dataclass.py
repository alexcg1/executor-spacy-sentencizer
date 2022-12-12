from jina import Executor, requests
from typing import Any, Dict, Optional, Sequence
from docarray import Document, DocumentArray
from spacy.lang.en import English
from dataclasses import dataclass
import re
from time import sleep


@dataclass
class SpacySentencizer(Executor):
    """
    Splits text at doc-level into sentences using spaCy's sentencizer and stores as doc.chunks.
    """

    # everything in this block is loaded like under `def __init__()`
    # ref https://docs.python.org/3/library/dataclasses.html
    min_sent_len: int = 5
    traversal_paths = "@r"
    nlp = English()
    nlp.add_pipe("sentencizer")
    print("Loading __init__ stuff. Well not really, but faking it by sleeping for 10")
    sleep(10)

    @requests(on="/index")
    def segment(self, docs: DocumentArray, parameters: Dict[str, Any], **kwargs):
        print("Using segment function. This is fast")
        traversal_paths = parameters.get("traversal_paths", self.traversal_paths)
        # First do some cleanup of unwanted linebreaks
        substitutions = [
            # Convert deliberate paragraph breaks into sentence-ends so they dont get caught by next entry in the list
            {"old": "\n\n.*", "new": ". "},
            {"old": "\r\r.*", "new": ". "},
            # Remove incidental linebreaks caused by conversion
            {"old": "\n", "new": " "},
            {"old": "\r", "new": " "},
            {"old": "\\s+", "new": " "},  # collapse white-spaces into one space
        ]

        for doc in docs[traversal_paths]:
            if doc.text:
                for sub in substitutions:
                    doc.text = re.sub(sub["old"], sub["new"], doc.text)

                # Sentencize
                text = self.nlp(doc.text)

                for sent in text.sents:
                    if len(str(sent)) >= self.min_sent_len:
                        doc.chunks.append(Document(text=str(sent)))


if __name__ == "__main__":
    docs = DocumentArray(
        [
            Document(text="J.R.R. Tolkien turns to p.3 on www.google.com"),
            Document(text="Doe a deer, a female deer"),
            Document(text="The cat sits on a mat. The dog sits in a tree"),
        ]
    )

    SpacySentencizer().segment(docs, parameters={})

    for doc in docs:
        print(doc.text)
        for chunk in doc.chunks:
            print("\t", chunk.text)
