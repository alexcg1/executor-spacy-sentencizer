from jina import Executor, requests
from typing import Any, Dict, Optional, Sequence
from docarray import Document, DocumentArray
from spacy.lang.en import English
import re


class SpacySentencizer(Executor):
    """
    Splits text at doc-level into sentences using spaCy's sentencizer and stores as doc.chunks.
    """

    def __init__(self, min_sent_len=20, max_sent_len=77, max_len_overlap=0.5, traversal_paths: str = "@r", *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.min_sent_len = min_sent_len
        self.traversal_paths = traversal_paths
        self.max_sent_len = max_sent_len
        self.step_size = int(max_sent_len * (1 - max_len_overlap))
        self.nlp = English()
        self.nlp.add_pipe("sentencizer")

    def _break_sentence(self, sent):
        """
        breaks a sentence into chunks of max_sent_len with overlap of max_len_overlap
        """
        chunks = []
        for i in range(0, len(sent), self.step_size):
            chunks.append(sent[i : i + self.max_sent_len])
        return chunks
        
        
    
    @requests(on="/index")
    def segment(self, docs: DocumentArray, parameters: Dict[str, Any], **kwargs):
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
                    elif len(str(sent)) > self.max_sent_len:
                        text_chunks = self._break_sentence(str(sent))
                        for c in text_chunks:
                            doc.chunks.append(Document(text=c))
                    else:
                        pass


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
