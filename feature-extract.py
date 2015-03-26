#!/usr/bin/env python
# coding=utf-8

import sys
import re
import unicodedata

# a useful alphabet detection library I found: https://github.com/EliFinkelshteyn/alphabet-detector
# supports latin, greek, arabic, hebrew, and cyrillic at least. Possibly more.
from alphabet_detector import AlphabetDetector # pip install alphabet-detector

import numpy


def extract_features(paragraph):
    features = {}

    alphabets = detect_alphabets(paragraph)
    alphabet_percentages = calculate_alphabet_percentages(paragraph, alphabets)
    for alphabet in alphabet_percentages:
        features["percent_"+str(alphabet).lower()] = alphabet_percentages[alphabet]

    features["vowel_cluster_size"] = find_vowel_cluster_size(paragraph)

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


def find_vowel_cluster_size(paragraph):
    vowels = [unicode("Æ", "UTF-8"), unicode("æ", "UTF-8"), unicode("A", "UTF-8"), unicode("a", "UTF-8"), unicode("E", "UTF-8"), unicode("e", "UTF-8"), unicode("I", "UTF-8"),
              unicode("i", "UTF-8"), unicode("O", "UTF-8"), unicode("o", "UTF-8"), unicode("U", "UTF-8"), unicode("u", "UTF-8") ,unicode("Y", "UTF-8"), unicode("y", "UTF-8"),
              unicode("е", "UTF-8"), unicode("ё", "UTF-8"), unicode("и", "UTF-8"), unicode("ю", "UTF-8"), unicode("я", "UTF-8"), unicode("ы", "UTF-8"), unicode("э", "UTF-8"),
              unicode("ё", "UTF-8"), unicode("α", "UTF-8"), unicode("ε", "UTF-8"), unicode("η", "UTF-8"), unicode("ι", "UTF-8"), unicode("ο", "UTF-8"), unicode("ω", "UTF-8"),
              unicode("υ", "UTF-8"), unicode("Α", "UTF-8"), unicode("Ε", "UTF-8"), unicode("Η", "UTF-8"), unicode("Ι", "UTF-8"), unicode("Ο", "UTF-8"), unicode("Ω", "UTF-8"),
              unicode("Υ", "UTF-8"), unicode("َ ", "UTF-8"), unicode(" ‎", "UTF-8"), unicode(" ", "UTF-8"), unicode("َا ", "UTF-8"), unicode("َى", "UTF-8"), unicode("ُو", "UTF-8"),
              unicode("ِي", "UTF-8"), unicode("ا", "UTF-8"), unicode("ى", "UTF-8"), unicode("و", "UTF-8"), unicode("ي", "UTF-8"), unicode("َي", "UTF-8"), unicode("َو", "UTF-8")]

    sentences = split_sentences(paragraph)
    vowel_cluster_sizes = []
    for sentence in sentences:
        words = split_words(sentence)
        for word in words:
            # print word
            cluster_size = 0
            for char in word:
                # print char
                if char in vowels:
                    cluster_size += 1
                else:
                    if cluster_size != 0:
                        vowel_cluster_sizes.append(cluster_size)
                        # print "Found cluster of size " + str(cluster_size)
                        cluster_size = 0
            if cluster_size != 0:
                # print "(End) Found cluster of size " + str(cluster_size)
                vowel_cluster_sizes.append(cluster_size)
    # print vowel_cluster_sizes
    return numpy.average(vowel_cluster_sizes)



def split_sentences(paragraph):
    terminators = "[\.!\?]"
    sentences = re.split(terminators, paragraph, flags=re.UNICODE)
    sentences = [sentence for sentence in sentences if sentence  != ""] # remove empty sentences
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
