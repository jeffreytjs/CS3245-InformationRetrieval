#!/usr/bin/python3

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
from collections import Counter
from nltk.util import ngrams

import re
import nltk
import sys
import getopt

# Initialization of variables
N_SIZE = 4
CHAR_SET = set()
OBSERVED_GRAM = []
def build_LM(in_file):
    """
    Build language models for each label
    Each line in in_file contains a label and a string separated by a space
    """
    print('building language models...')
    # Pls implement your code in below
    inputs = preprocess(in_file)
    return ngram_language_model(inputs)

def ngram_language_model(inputs):
    """
    Takes a list of ngrams and associated language, and outputs a tuple of the
    frequency count table, and the total count for each category.
    """
    all_lang = {}
    prob_count = {}
    for each_gram, lang in entries:
        if lang not in all_lang: # Build a dictionary containing dictionary for each language
            all_lang[lang] = {}
        else:
            all_lang[lang] = all_lang[lang]

        if lang not in prob_count: # Tracking no. of times the lang appears
            prob_count[lang] =  1
        else:
            prob_count[lang] = prob_count[lang] + 1

        for i in range(len(each_gram)): # Store all possible n-grams with its counter
            end = i + N_SIZE
            lang_dict = all_lang[lang]
            if end <= len(each_gram):
                ngram = each_gram[i:end]
                if ngram not in lang_dict: # Tracking no. of times the ngram appears
                    lang_dict[ngram] = 1
                else:
                    lang_dict[ngram] = lang_dict[ngram] + 1
                CHAR_SET.add(ngram) # To ensure no duplicates
    return all_lang, prob_count

def preprocess(in_file):
    """
    Takes in_file, and outputs a list of all observed ngrams and its language.
    """
    infile = open(in_file,'r',encoding='utf8')
    in_file_lines = infile.readlines()
    for line in in_file_lines:
        (lang, l) = line.split(" ", 1)
        l = re.sub("\d+","",l)
        for gram in list(ngrams(list(l),N_SIZE)):
            OBSERVED_GRAM.append((gram, lang))
    infile.close()
    return OBSERVED_GRAM

#######################################################################################

def test_string(string,orig_string,LM):
    '''
    Multiplication of the probabilities of the 4-grams for each string,
    and return the label that gives the highest product.

    To implement:
    Ignore the four-gram if it is not found in the LMs.
    Remove numbers (Done)
    Remove punctuations
    Convert to lowercase
    Try different N-SIZEs
    '''
    freq_counts,prob_count = LM
    max_prob, category = 0, None
    for lang in freq_counts:
        combined_prob = 1
        for i in range(len(string)-N_SIZE):
            last = i + N_SIZE
            ngram = tuple(string[i:last])
            if ngram in freq_counts[lang]:
                prob = (freq_counts[lang][ngram] + 1.0)/float(prob_count[lang] + len(CHAR_SET))
            elif ngram in CHAR_SET:
                prob = 1.0/float(prob_count[lang] + len(CHAR_SET))
            else:
                prob = 1
            combined_prob *= prob
        max_prob = max(combined_prob,max_prob)
        if  combined_prob < max_prob:
            category = category
        else:
            category = lang
    return category + ' ' + orig_string

def test_LM(in_file, out_file, LM):
    """
    Test the language models on new strings
    Each line of in_file contains a string
    You should print the most probable label for each string into out_file
    """
    print("testing language models...")
    # Pls implement your code in below
    infile = open(in_file,'r')
    output = open(out_file,'w')
    in_file_lines = infile.readlines()
    all_lang = []
    for line in in_file_lines:
        (lang, l) = line.split(" ", 1)
        l = re.sub("\d+","",l) # Removed numbers
        all_lang.append(l)
    infile.close()
    for i in range(len(all_lang)):
        print(test_string(all_lang[i],in_file_lines[i],LM))
        output.write(test_string(all_lang[i],in_file_lines[i],LM))
    output.close()

def usage():
    print("usage: " + sys.argv[0] + " -b input-file-for-building-LM -t input-file-for-testing-LM -o output-file")

input_file_b = input_file_t = output_file = None
try:
    opts, args = getopt.getopt(sys.argv[1:], 'b:t:o:')
except getopt.GetoptError:
    usage()
    sys.exit(2)
for o, a in opts:
    if o == '-b':
        input_file_b = a
    elif o == '-t':
        input_file_t = a
    elif o == '-o':
        output_file = a
    else:
        assert False, "unhandled option"
if input_file_b == None or input_file_t == None or output_file == None:
    usage()
    sys.exit(2)

LM = build_LM(input_file_b)
test_LM(input_file_t, output_file, LM)
