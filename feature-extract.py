#!/usr/bin/env python

import sys
import re
import unicodedata

# a useful alphabet detection library I found: https://github.com/EliFinkelshteyn/alphabet-detector
# supports latin, greek, arabic, hebrew, and cyrillic at least. Possibly more.
from alphabet_detector import AlphabetDetector # pip install alphabet-detector


def extract_features(paragraph):
    features = {}

    alphabets = detect_alphabets(paragraph)
    alphabet_percentages = calculate_alphabet_percentages(paragraph, alphabets)
    for alphabet in alphabet_percentages:
        features["percent_"+str(alphabet).lower()] = alphabet_percentages[alphabet]

    sentences = split_sentences(paragraph)

    total_words = 0
    total_chars = 0
    for sentence in sentences:
        words = split_words(sentence)
        total_words += len(words)

        #print len(words), words

        for word in words:
            #total_chars += len(word)
            total_chars += len([unicodedata.name(c) for c in word if unicodedata.name(c).split()[0] != "COMBINING"])

        features["avg_words_per_sentence"] = (total_words * 1.0) / len(sentences)
        features["avg_chars_per_word"] = (total_chars * 1.0) / total_words

    return features

def detect_alphabets(paragraph):
    detector = AlphabetDetector()
    return detector.detect_alphabet(paragraph)

def calculate_alphabet_percentages(paragraph, alphabets):
    # TODO - re-work this so that we're not duplicating the code
    detector = AlphabetDetector()
    sentences = split_sentences(paragraph)
    words_in_alphabet = dict.fromkeys(alphabets, 0)
    total_word_count = 0
    for sentence in sentences:
        words = split_words(sentence)
        # get number of words in each alphabet
        for word in words:
            total_word_count += 1
            for alphabet in alphabets:
                if detector.only_alphabet_chars(word, alphabet):
                    words_in_alphabet[alphabet] += 1
    # convert counts to percentages
    for alphabet in words_in_alphabet:
        words_in_alphabet[alphabet] /= float(total_word_count)
    return words_in_alphabet


def split_sentences(paragraph):
    terminators = "[\.!\?]"
    sentences = re.split(terminators, paragraph, flags=re.UNICODE)
    sentences = [sentence for sentence in sentences if sentence  != ""] #remove empty sentences
    return sentences


def split_words(sentence):
    words = sentence.split(" ")
    words = [word for word in words if word != ""] #remove empty words
    return words


def main():
    paragraph = None

    fname = sys.argv[1]
    with open(fname, "r") as f:
        for line in f:
            paragraph = line.strip()
            if paragraph:
                paragraph = unicodedata.normalize("NFKD", unicode(paragraph, "UTF-8"))
                print extract_features(paragraph)
                print


if __name__ == "__main__":
    main()
