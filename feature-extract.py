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


MIN_LEN = 25


def extract_features(paragraph):
    features = {}

    alphabets = detect_alphabets(paragraph)
    alphabet_percentages = calculate_alphabet_percentages(paragraph, alphabets)
    for alphabet in alphabet_percentages:
        if alphabet not in set(["MODIFIER", "CJK", "HEBREW", "DEVANAGARI"]):
            features["percent_"+str(alphabet).lower()] = alphabet_percentages[alphabet]

    features["vowel_cluster_size"], features["consonant_cluster_size"] = find_cluster_sizes(paragraph)

    features["avg_diacritics_per_word"], diacritics_percentages = find_diacritics(paragraph)

    for key in diacritics_percentages:
        features["percent_diacritics_" + key] = diacritics_percentages[key]

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

    # print features
    return features


def detect_alphabets(paragraph):
    detector = AlphabetDetector()
    return detector.detect_alphabet(paragraph)

def find_diacritics(paragraph):
    number_of_diacritics_per_word = []
    counts = {}
    counts["acute"] = 0
    counts["caron"] = 0
    counts["grave"] = 0
    counts["circumflex"] = 0
    counts["tilde"] = 0
    counts["cedilla"] = 0
    counts["breve"] = 0
    counts["diaeresis"] = 0
    counts["ring_above"] = 0
    counts["ogonek"] = 0
    counts["horn"] = 0
    counts["hook_above"] = 0
    counts["dot_below"] = 0
    counts["macron"] = 0
    total_diacritics = 0
    sentences = split_sentences(paragraph)
    for sentence in sentences:
        words = split_words(sentence)
        for word in words:
            number_of_diacritics = 0
            for char in word:
                if "COMBINING" in unicodedata.name(char):
                    number_of_diacritics += 1
                    total_diacritics += 1
                    # print unicodedata.name(char)
                    if "ACUTE" in unicodedata.name(char):
                        counts["acute"] += 1
                    elif "CARON" in unicodedata.name(char):
                        counts["caron"] += 1
                    elif "GRAVE" in unicodedata.name(char):
                        counts["grave"] += 1
                    elif "DIAERESIS" in unicodedata.name(char):
                        counts["diaeresis"] += 1
                    elif "CIRCUMFLEX" in unicodedata.name(char):
                        counts["circumflex"] += 1
                    elif "TILDE" in unicodedata.name(char):
                        counts["tilde"] += 1
                    elif "CEDILLA" in unicodedata.name(char):
                        counts["cedilla"] += 1
                    elif "BREVE" in unicodedata.name(char):
                        counts["breve"] += 1
                    elif "RING ABOVE" in unicodedata.name(char):
                        counts["ring_above"] += 1
                    elif "OGONEK" in unicodedata.name(char):
                        counts["ogonek"] += 1
                    elif "HORN" in unicodedata.name(char):
                        counts["horn"] += 1
                    elif "HOOK ABOVE" in unicodedata.name(char):
                        counts["hook_above"] += 1
                    elif "DOT BELOW" in unicodedata.name(char):
                        counts["dot_below"] += 1
                    elif "MACRON" in unicodedata.name(char):
                        counts["macron"] += 1
            number_of_diacritics_per_word.append(number_of_diacritics)

    for key in counts:
        counts[key] = float(counts[key])/total_diacritics if total_diacritics else 0
    return numpy.average(number_of_diacritics_per_word), counts



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
    avcs = numpy.average(vowel_cluster_sizes) if vowel_cluster_sizes else 0
    accs = numpy.average(consonant_cluster_sizes) if consonant_cluster_sizes else 0
    return avcs, accs



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

    print "@RELATION"

    # I'm looping through and saving to variables, then printing in case we later decide we want this function to return a string or something.
    for feature in features:
        if feature == "language":
            print "@ATTRIBUTE language { GREEK, DUTCH, BOSNIAN, UKRAINIAN, VIETNAMESE, NORWEGIAN, CZECH, AFRIKAANS, RUSSIAN, WELSH, GAELIC, ESPERANTO, ARABIC, FRENCH, SWAHILI, TAGALOG, PORTUGUESE, FINNISH, ITALIAN, SPANISH, POLISH, DANISH, GERMAN, KURDISH, SERBIAN, SWEDISH, ENGLISH }"
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
        # print "%% processing file %s" % fname
        if fname == "data/plaintext/GERMAN-Gert-Peter_Reichert.txt":
            continue
        with open(fname, "r") as f:
            for lnum, line in enumerate(f):
                paragraph = line.strip()
                if len(paragraph) > MIN_LEN:
                    paragraph = unicodedata.normalize("NFKD", unicode(paragraph, "UTF-8")).lower()
                    if " ".join([unicodedata.name(c).split()[0] for c in paragraph[:3]]) != "LATIN LATIN COLON": #skip language links
                        features.append(extract_features(paragraph))
                        features[-1]["language"] = fname.split("-")[0].split("/")[-1]
                        #features[-1]["fname"] = fname.split("/")[-1]
                        #features[-1]["lnum"] = lnum + 1
                        #print features[-1]

    convert_features_to_arff(features)


if __name__ == "__main__":
    main()
