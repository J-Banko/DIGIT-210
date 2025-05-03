import spacy
import os
from collections import Counter
import matplotlib.pyplot as plt

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
    shall_count = freq.get('shall', 0)
    print(f"{os.path.basename(filepath):<20} → lexical diversity = {div:.3f}")
    print(f"    Most common word: '{most_common}' ({count} occurrences)")
    print(f"    'shall' frequency: {shall_count}\n")
    return os.path.basename(filepath), shall_count

if not os.path.isdir(CollPath):
    raise FileNotFoundError(f"Folder not found: {CollPath!r}")

file_names = []
shall_counts = []
for file in os.listdir(CollPath):
    if file.lower().endswith('.txt'):
        name, count = readTextFiles(os.path.join(CollPath, file))
        file_names.append(name)
        shall_counts.append(count)

plt.figure()
plt.bar(file_names, shall_counts)
plt.title('Frequency of "shall" in each document')
plt.xlabel('Document')
plt.ylabel('Count of "shall"')
plt.tight_layout()
plt.show()
