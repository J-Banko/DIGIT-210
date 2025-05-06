import os
import nltk
import pandas as pd
import spacy
from nltk.corpus import wordnet as wn

nltk.download('wordnet', quiet=True)

nlp = spacy.load('en_core_web_sm')

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def wordCollector(doc, unit_name):
    words = []
    types = []
    counts = []
    units = []
    for token in doc:
        if token.pos_ == 'ADJ':
            lemma = token.lemma_.lower()
            syn_count = len(wn.synsets(lemma, pos=token.pos_[0].lower()))
            words.append(lemma)
            types.append(token.pos_)
            counts.append(syn_count)
            units.append(unit_name)
    return pd.DataFrame({
        'word': words,
        'nodeType': types,
        'synsetCount': counts,
        'unit': units
    })

all_dfs = []
for fname in os.listdir(BASE_DIR):
    if fname.lower().endswith('.txt'):
        path = os.path.join(BASE_DIR, fname)
        with open(path, 'r', encoding='utf-8') as f:
            text = f.read()
        doc = nlp(text)
        unit_name = os.path.splitext(fname)[0]
        df = wordCollector(doc, unit_name)
        all_dfs.append(df)

if not all_dfs:
    raise RuntimeError(f"No .txt files found in {BASE_DIR}")
full_df = pd.concat(all_dfs, ignore_index=True)

out_path = os.path.join(BASE_DIR, 'networkData.tsv')
full_df.to_csv(out_path, sep='\t', index=False)
print(f"TSV network data written to: {out_path}")