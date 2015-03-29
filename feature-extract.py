#!/usr/bin/env python
# coding=utf-8

import sys
import re
import unicodedata

# a useful alphabet detection library I found: https://github.com/EliFinkelshteyn/alphabet-detector
# supports latin, greek, arabic, hebrew, and cyrillic at least. Possibly more.
from alphabet_detector import AlphabetDetector # pip install alphabet-detector

import glob

import numpy


def extract_features(paragraph):
    features = {}

    alphabets = detect_alphabets(paragraph)
    alphabet_percentages = calculate_alphabet_percentages(paragraph, alphabets)
    for alphabet in alphabet_percentages:
        features["percent_"+str(alphabet).lower()] = alphabet_percentages[alphabet]

    features["vowel_cluster_size"], features["consonant_cluster_size"] = find_cluster_sizes(paragraph)

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


def find_cluster_sizes(paragraph):
    vowels = [unicode("Æ", "UTF-8"), unicode("æ", "UTF-8"), unicode("A", "UTF-8"), unicode("a", "UTF-8"), unicode("E", "UTF-8"), unicode("e", "UTF-8"), unicode("I", "UTF-8"),
              unicode("i", "UTF-8"), unicode("O", "UTF-8"), unicode("o", "UTF-8"), unicode("U", "UTF-8"), unicode("u", "UTF-8") ,unicode("Y", "UTF-8"), unicode("y", "UTF-8"),
              unicode("е", "UTF-8"), unicode("ё", "UTF-8"), unicode("и", "UTF-8"), unicode("ю", "UTF-8"), unicode("я", "UTF-8"), unicode("ы", "UTF-8"), unicode("э", "UTF-8"),
              unicode("ё", "UTF-8"), unicode("α", "UTF-8"), unicode("ε", "UTF-8"), unicode("η", "UTF-8"), unicode("ι", "UTF-8"), unicode("ο", "UTF-8"), unicode("ω", "UTF-8"),
              unicode("υ", "UTF-8"), unicode("Α", "UTF-8"), unicode("Ε", "UTF-8"), unicode("Η", "UTF-8"), unicode("Ι", "UTF-8"), unicode("Ο", "UTF-8"), unicode("Ω", "UTF-8"),
              unicode("Υ", "UTF-8"), unicode("َ ", "UTF-8"), unicode(" ‎", "UTF-8"), unicode(" ", "UTF-8"), unicode("َا ", "UTF-8"), unicode("َى", "UTF-8"), unicode("ُو", "UTF-8"),
              unicode("ِي", "UTF-8"), unicode("ا", "UTF-8"), unicode("ى", "UTF-8"), unicode("و", "UTF-8"), unicode("ي", "UTF-8"), unicode("َي", "UTF-8"), unicode("َو", "UTF-8")]

    sentences = split_sentences(paragraph)
    vowel_cluster_sizes = []
    consonant_cluster_sizes = []
    for sentence in sentences:
        words = split_words(sentence)
        for word in words:
            # print word
            vowel_cluster_size = 0
            consonant_cluster_size = 0;

            for char in word:
                # print char
                if char in vowels:
                    vowel_cluster_size += 1
                    if consonant_cluster_size:
                        consonant_cluster_sizes.append(consonant_cluster_size)
                        consonant_cluster_size = 0
                else:
                    consonant_cluster_size += 1
                    if vowel_cluster_size:
                        vowel_cluster_sizes.append(vowel_cluster_size)
                        # print "Found cluster of size " + str(cluster_size)
                        vowel_cluster_size = 0
            if vowel_cluster_size:
                # print "(End) Found cluster of size " + str(cluster_size)
                vowel_cluster_sizes.append(vowel_cluster_size)
            if consonant_cluster_size:
                consonant_cluster_sizes.append(consonant_cluster_size)

    # print vowel_cluster_sizes
    return numpy.average(vowel_cluster_sizes), numpy.average(consonant_cluster_sizes)



def split_sentences(paragraph):
    terminators = "[\.!\?]"
    sentences = re.split(terminators, paragraph, flags=re.UNICODE)
    sentences = [sentence for sentence in sentences if sentence  != ""] # remove empty sentences
    return sentences


def split_words(sentence):
    words = sentence.split(" ")
    words = [word for word in words if word != ""] #remove empty words
    return words


def convert_features_to_arff(instances):
    # loop through all of the features in the vector once to see what all of the columns are.
    features = []
    for instance in instances:
        for key in instance:
            if key not in features and key != "language":
                features.append(key)
    # make sure that language is our last feature
    features.append("language")

    # I'm looping through and saving to variables, then printing in case we later decide we want this function to return a string or something.
    for feature in features:
        if feature == "language":
            print "@ATTRIBUTE language class @ATTRIBUTE language class { GREEK, DUTCH, BOSNIAN, UKRAINIAN, VIETNAMESE, NORWEGIAN, CZECH, AFRIKAANS, RUSSIAN, WELSH, GAELIC, ESPERANTO, ARABIC, FRENCH, SWAHILI, TAGALOG, PORTUGUESE, FINNISH, ITALIAN, SPANISH, POLISH, DANISH, GERMAN, KURDISH, SERBIAN, SWEDISH }"
        else:
            print "@ATTRIBUTE %s Continuous" % feature

    print "@DATA"

    # and now loop through a second time to extract the data
    formatted_instances = []
    for instance in instances:
        formatted_instance = ""
        for feature in features:
            if feature in instance:
                formatted_instance += str(instance[feature]) + ", "
            else:
                formatted_instance += "0, "
        formatted_instance = formatted_instance[:-2]
        formatted_instances.append(formatted_instance)

    for formatted_instance in formatted_instances:
        print formatted_instance

def main():
    paragraph = None

    # support matching a whole bunch of files, instead of just a single file.
    filenames = glob.glob(sys.argv[1])

    features = []
    for fname in filenames:
        print "processing file %s" % fname
        if fname == "data/plaintext/GERMAN-Gert-Peter_Reichert.txt":
            continue
        with open(fname, "r") as f:
            for line in f:
                paragraph = line.strip()
                if paragraph:
                    paragraph = unicodedata.normalize("NFKD", unicode(paragraph, "UTF-8"))
                    features.append(extract_features(paragraph))
                    features[len(features) - 1]["language"] = fname.split("-")[0].split("/")[-1]

    convert_features_to_arff(features)


if __name__ == "__main__":
    main()
