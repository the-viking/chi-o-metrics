#!/usr/bin/env python
import codecs
from string import punctuation
import operator
import re
from couchdbkit import *
import numpy.numarray as na

class Paper(Document):
    author = StringProperty()
    url = StringProperty()
    words = DictProperty()

def clean(text):
    """
    Removes punctuation, numbers and newlines,
    and makes all letters lowercase.
    Returns a list of words
    """
    text = text.lower()
# split into a list of words
    for p in list(punctuation):
        text = text.replace(p,'')
    words = text.split(' ')
    to_remove = ('', '\n')
# remove empty strings, and new lines
    words = [w for w in words if w not in to_remove]
    regex = re.compile(r'\d+')
# remove numbers from the word list
    words = [w for w in words if not regex.search(w)]
    return words


def get_words(filename):
    """
    Returns a cleaned list of words from the 
    first paragraph of an introduction of the
    text file of a paper
    """
# load in text file to string
    f = codecs.open(filename, "r", encoding='utf-8')

    lines = list(f)
    f.close()
    lines = [l.encode('utf-8') for l in lines]

# list to store lines in the introduction
    intro_lines = []
# track index of line with first occurence of introduction
    c = 0
    start_key = 'introduction'
# cut string down to text between "introduction" (case insensitive) and first empty line
    for line in lines:
        if start_key in line.lower():
            lines = lines[c+1:]
            break
        c += 1
# add lines to intro_lines until an empty line is reached
    for line in lines:
        intro_lines.append(line)
# check for blank line, indicating possible end of paragraph
        if not line.strip():
# check for number, possibly in heading of next section
            if "1" in lines[c+1] or "2" in lines[c+1]:
                break 
        c += 1

    text = " ".join(intro_lines)
    words = clean(text)
    return words


def count(words):
    """
    Takes a list of words and returns a list of tuples 
    with the count of each word, 
    ignoring the 150 most common, sorted by 
    descending frequency
    """
# load in a list of the 150 most common words in the English language
    with open('common_words.txt', 'r') as f:
        common_words = [line.strip() for line in f]

# dictionary to store counts, where the key is the word and the value is the count
    counts = {}
# count occurrences of each word
    for w in words:
# ignore most common words
        if w not in common_words:
            if w in counts.keys():
                counts[w] += 1
            else:
                counts[w] = 1

# sort the dictionary by the values (counts) and return a list of tuples of words and counts
    sorted_counts = [(k,v) for v,k in sorted([(v,k) for k,v in counts.items()],reverse=True)]
    return sorted_counts

words = get_words("text/1307.2018.txt")
count =  count(words)
# set up connection to local couchDB
#server = Server()
#db = server.get_or_create_db("papers")
#Paper.set_db(db)
# Paper(author="bla blah", url="fsd").save

# add these counts to the corpus
