#!/usr/bin/env python

import sys
import re


def extract_features(paragraph):
    features = {}

    sentences = split_sentences(paragraph)

    total_words = 0
    total_chars = 0
    for sentence in sentences:
        words = split_words(sentence)
        total_words += len(words)

        print len(words), words

        for word in words:
            total_chars += len(word)

        features["avg_words_per_sentence"] = (total_words * 1.0) / len(sentences)
        features["avg_chars_per_word"] = (total_chars * 1.0) / total_words

    return features


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
        paragraph = f.readline().strip()

    print extract_features(paragraph)


if __name__ == "__main__":
    main()
