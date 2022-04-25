from jina import Executor, DocumentArray, requests, Document
from spacy.pipeline import Sentencizer
from spacy.lang.en import English

sentencizer = Sentencizer()
nlp = English()
nlp.add_pipe("sentencizer")


class SpacySentencizer(Executor):
    @requests(on="/index")
    def segment(self, docs: DocumentArray, **kwargs):
        sentencizer = Sentencizer()
        nlp = English()
        nlp.add_pipe("sentencizer")

        for doc in docs:
            sentences = DocumentArray()
            if doc.text:
                text = nlp(doc.text)

                for sent in text.sents:
                    sentences.append(Document(text=str(sent)))

            doc.chunks.extend(sentences)


def preproc(doc):
    sentences = DocumentArray()
    if doc.text:
        text = nlp(doc.text)

        for sent in text.sents:
            sentences.append(Document(text=str(sent)))

    doc.chunks.extend(sentences)
