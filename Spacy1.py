import os
import re
from collections import Counter
import spacy
from nltk.corpus import wordnet as wn
import pygal
from pygal.style import Style

# Load spaCy model (install with `pip install spacy en_core_web_sm` in your venv)
nlp = spacy.load("en_core_web_sm")

# Locate this script's directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Read all .txt files alongside this script
texts = {}
for fname in os.listdir(BASE_DIR):
    if fname.lower().endswith('.txt'):
        with open(os.path.join(BASE_DIR, fname), 'r', encoding='utf-8') as f:
            texts[fname] = f.read()
if not texts:
    raise RuntimeError(f"No .txt files found in {BASE_DIR}")

# Collect verb lemmas from all texts
verb_freq = Counter()
for content in texts.values():
    doc = nlp(content)
    for token in doc:
        if token.pos_ == 'VERB':
            verb_freq[token.lemma_.lower()] += 1

# Top 10 verbs
top_ten = verb_freq.most_common(10)

# Compute WordNet synset counts per verb
synset_counts = {w: len(wn.synsets(w, pos='v')) for w, _ in top_ten}
max_syn = max(synset_counts.values())
min_syn = min(synset_counts.values())

def synset_to_color(syn_count):
    """Map synset count to a shade of blue."""
    if max_syn == min_syn:
        blue = 150
    else:
        blue = int(50 + 205 * (syn_count - min_syn) / (max_syn - min_syn))
    return f'#0000{blue:02x}'

# Pygal bar chart setup (minimal change)
custom_style = Style(
    background='white',
    plot_background='white',
    foreground='black',
    foreground_strong='black',
    foreground_subtle='gray',
    opacity='.8',
    opacity_hover='.9',
    transition='400ms ease-in',
    colors=('#cccccc',)
)
chart = pygal.Bar(style=custom_style)
chart.title = 'Top 10 Verb Frequencies Colored by Ambiguity'
for word, freq in top_ten:
    syns = synset_counts[word]
    color = synset_to_color(syns)
    chart.add(word, [{
        'value': freq,
        'label': f'{word} has {syns} synsets',
        'style': f'fill:{color}'
    }])

# Save SVG
svg_path = os.path.join(BASE_DIR, 'top_verbs_colored_by_synsets.svg')
chart.render_to_file(svg_path)

# Write text report
txt_path = os.path.join(BASE_DIR, 'verbFreq.txt')
with open(txt_path, 'w', encoding='utf-8') as o:
    o.write('Verb\tFrequency\tSynsetCount\n')
    for word, freq in top_ten:
        o.write(f"{word}\t{freq}\t{synset_counts[word]}\n")

# Summary
print(f"Text report written to: {txt_path}")
print(f"SVG chart written to: {svg_path}")