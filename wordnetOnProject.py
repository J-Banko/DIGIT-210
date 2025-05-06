import os
import re
import json
import nltk
from nltk.corpus import wordnet as wn


nltk.download('wordnet', quiet=True)


BASE_DIR = os.path.dirname(os.path.abspath(__file__))


texts = {}
for fname in os.listdir(BASE_DIR):
    if fname.lower().endswith('.txt'):
        path = os.path.join(BASE_DIR, fname)
        with open(path, 'r', encoding='utf-8') as f:
            texts[fname] = f.read()

if not texts:
    raise RuntimeError(f"No .txt files found in {BASE_DIR}")


target_words = ['state', 'congress', 'shall']


results = {}
for word in target_words:
    count = sum(
        len(re.findall(rf"\b{re.escape(word)}\b", txt.lower()))
        for txt in texts.values()
    )
    synsets = wn.synsets(word)
    results[word] = {
        'occurrences': count,
        'senses': len(synsets),
        'synset_names': [s.name() for s in synsets]
    }


output_dir = os.path.join(BASE_DIR, 'output')
os.makedirs(output_dir, exist_ok=True)


json_path = os.path.join(output_dir, 'wordnet_ambiguity.json')
with open(json_path, 'w', encoding='utf-8') as jf:
    json.dump(results, jf, indent=2, ensure_ascii=False)
print(f"JSON report written to: {json_path}")


print("\nSummary:")
for w, info in results.items():
    print(f" - {w}: occurrences={info['occurrences']}, senses={info['senses']}")
