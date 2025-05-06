import os
import json
from collections import Counter
import spacy

nlp = spacy.load("en_core_web_sm")

collection = os.getcwd()

target_term = 'liberty'
threshold = 0.4

target_token = nlp(target_term)

def readTextFiles(filepath):
    with open(filepath, 'r', encoding='utf8') as f:
        text = f.read()

    tokens = nlp(text)
    highSimilarityDict = {}
    wordCounts = Counter()

    for token in tokens:
        if token.has_vector and token.is_alpha:
            sim = target_token.similarity(token)
            if sim > threshold:
                wordCounts[token.text] += 1

                if token.text not in highSimilarityDict or sim > highSimilarityDict[token.text]:
                    highSimilarityDict[token.text] = sim

    results = [
        {'token': tok, 'similarity': highSimilarityDict[tok], 'count': wordCounts[tok]}
        for tok in highSimilarityDict
    ]
    return results

all_reports = {}
for fname in os.listdir(collection):
    if fname.lower().endswith('.txt'):
        path = os.path.join(collection, fname)
        data = readTextFiles(path)
        unit = os.path.splitext(fname)[0]
        all_reports[unit] = data
        # write per-file JSON
        out_file = os.path.join(collection, f"{unit}_sim.json")
        with open(out_file, 'w', encoding='utf-8') as out:
            json.dump(data, out, indent=2)
        print(f"Wrote similarity report for {unit} to {unit}_sim.json")

summary_path = os.path.join(collection, f"corpus_{target_term}_similarity.json")
with open(summary_path, 'w', encoding='utf-8') as summary:
    json.dump(all_reports, summary, indent=2)
print(f"Consolidated report written to {summary_path}")