# SpacySentencizer

SpacySentencizer takes a DocumentArray, and for each Document:

1. Checks if it has `.text` attribute
2. If so, sentencize it
3. Store each sentence as a chunk of the Document

## Why SpacySentencizer over "Vanilla" Sentencizer?

- In English a `.` (full stop/period) comes at the end of every sentence.
- However, `.` is also used in:
  - URLs: `docs.jina.ai`
  - Decimals: `3.14`
  - Initials: `J.R.R Tolkien`, `H. Sapiens`
  - Abbreviations: `Turn to p. 13`
- This means that Vanilla Sentencizer tries to split things that aren't sentences

SpacySentencizer *should* also work for other languages, though I haven't yet tested that

## Usage

#### via Docker image (recommended)

```python
from jina import Flow
	
f = Flow().add(uses='jinahub+docker://SpacySentencizer')
```

#### via source code

```python
from jina import Flow
	
f = Flow().add(uses='jinahub://SpacySentencizer')
```

- To override `__init__` args & kwargs, use `.add(..., uses_with: {'key': 'value'})`
- To override class metas, use `.add(..., uses_metas: {'key': 'value})`
