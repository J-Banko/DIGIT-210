import os
import json
import argparse
import collections

import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

import matplotlib.pyplot as plt


def ensure_nltk_resources():
    try:
        nltk.data.find('tokenizers/punkt')
    except LookupError:
        nltk.download('punkt')
    try:
        nltk.data.find('corpora/stopwords')
    except LookupError:
        nltk.download('stopwords')


def write_output(path, content, mode='w'):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, mode, encoding='utf-8') as f:
        f.write(content)


def read_texts_from_dir(directory, ext='.txt'):
    texts = {}
    for fname in os.listdir(directory):
        if fname.lower().endswith(ext):
            with open(os.path.join(directory, fname), 'r', encoding='utf-8') as f:
                texts[fname] = f.read()
    return texts


def most_common_words(text, n=5):
    tokens = word_tokenize(text.lower())
    sw = set(stopwords.words('english'))
    words = [t for t in tokens if t.isalpha() and t not in sw]
    return collections.Counter(words).most_common(n)


def count_word(text, word):
    tokens = word_tokenize(text.lower())
    return tokens.count(word.lower())


def plot_word_frequencies(freqs, word, output_path):
    files = list(freqs.keys())
    counts = [freqs[f] for f in files]
    plt.figure()
    plt.bar(files, counts)
    plt.ylabel(f'Frequency of "{word}"')
    plt.xlabel('Document')
    plt.title(f'Word Frequency of "{word}"')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()


def main():
    parser = argparse.ArgumentParser(description="Smoke-test NLP script")
    parser.add_argument('--input-dir', default=os.getcwd(), help='Directory to scan for .txt files')
    parser.add_argument('--word', default='shall', help='Word to count frequency')
    args = parser.parse_args()

    ensure_nltk_resources()
    texts = read_texts_from_dir(args.input_dir)


    common_results = {
        name: most_common_words(txt)
        for name, txt in texts.items()
    }
    write_output('output/most_common_words.json', json.dumps(common_results, indent=2))

    word_freqs = {
        name: count_word(txt, args.word)
        for name, txt in texts.items()
    }
    write_output(f'output/word_freq_{args.word}.json', json.dumps(word_freqs, indent=2))


    plot_path = f'output/{args.word}_frequency.png'
    plot_word_frequencies(word_freqs, args.word, plot_path)

    print("Results:")
    print(f" - Most common words per document written to output/most_common_words.json")
    print(f" - Word frequencies written to output/word_freq_{args.word}.json")
    print(f" - Plot saved to {plot_path}")


if __name__ == '__main__':
    main()
