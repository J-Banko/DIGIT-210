import spacy
import os
from collections import Counter

nlp = spacy.load('en_core_web_md')
CollPath = r'C:\Users\justi\Documents\GitHub\Banko210\python-nlp'

def lexical_diversity(tokens):
    return len(set(tokens)) / len(tokens) if tokens else 0

def readTextFiles(filepath):
    with open(filepath, 'r', encoding='utf8') as f:
        text = f.read()
    doc = nlp(text)
    tokens = [t.text.lower() for t in doc if not t.is_stop and not t.is_punct]
    div = lexical_diversity(tokens)
    freq = Counter(tokens)
    most_common, count = freq.most_common(1)[0] if freq else (None, 0)
    print(f"{os.path.basename(filepath):<20} → lexical diversity = {div:.3f}")
    print(f"    Most common word: '{most_common}' ({count} occurrences)")

if not os.path.isdir(CollPath):
    raise FileNotFoundError(f"Folder not found: {CollPath!r}")

for file in os.listdir(CollPath):
    if file.lower().endswith('.txt'):
        readTextFiles(os.path.join(CollPath, file))
