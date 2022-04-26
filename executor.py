from jina import Executor, DocumentArray, requests, Document
from spacy.lang.en import English

nlp = English()
nlp.add_pipe("sentencizer")


class SpacySentencizer(Executor):
    @requests(on="/index")
    def segment(self, docs: DocumentArray, **kwargs):
        min_length = 20  # minimum sentence length

        # First do some cleanup of unwanted linebreaks
        substitutions = [
            # Convert deliberate paragraph breaks into sentence-ends so they dont get caught by next entry in the list
            {"old": "\n\n", "new": ". "},
            {"old": "\r\r", "new": ". "},
            # Remove incidental linebreaks caused by conversion
            {"old": "\n", "new": " "},
            {"old": "\r", "new": " "},
        ]

        for doc in docs:
            if doc.text:
                for sub in substitutions:
                    doc.text = doc.text.replace(sub["old"], sub["new"])

                # Sentencize
                text = nlp(doc.text)

                for sent in text.sents:
                    if len(str(sent)) >= min_length:
                        doc.chunks.append(Document(text=str(sent)))
