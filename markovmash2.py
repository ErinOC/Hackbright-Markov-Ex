#!/usr/bin/env python

import sys

from operator import itemgetter

import random

from sys import argv

import string

first_pick = []
split_words = []
word_tuples = []
word_tuples2 = []

def make_chains(corpus, corpus2):
#Takes an input text as a string; returns dictionary of Markov chains.

    global first_pick
    global split_words
    words = corpus
    words2 = corpus2
    #make strings of words into lists
    split_words = words.split() 
    split_words2 = words2.split()

    chains1 = {}
    #make a list of every word pairing in the first list of words
    for word_index in range(len(split_words)): 
        if word_index < (len(split_words) - 4): 
        #if the word isn't the last word in the list, then make the word and the subsequent word into a tuple
            the_tuple = (split_words[word_index], split_words[word_index + 1])
            word_tuples.append(the_tuple)
            if the_tuple not in chains1:
                chains1[the_tuple] = [split_words[word_index + 2]]
            else:
                chains1[the_tuple].append(split_words[word_index + 2])

    chains2 = {}
    for word_index in range(len(split_words2)): 
        if word_index < (len(split_words2) - 4): 
            the_tuple = (split_words2[word_index], split_words2[word_index + 1])
            word_tuples2.append(the_tuple)
            if the_tuple not in chains2:
                chains2[the_tuple] = [split_words2[word_index + 2]]
            else:
                chains2[the_tuple].append(split_words2[word_index + 2])

    chains = [chains1, chains2]
    return chains

def make_text(chains):
    #this function will bring in the Markov chains from the first function
    #it will find a word to follow a given word tuple.
    
    chains1 = chains[0] 
    chains2 = chains[1]
    caps_list = {}

    #make a list of tuples starting with capital letters (from the first corpus only)
    for key, value in chains1.iteritems(): 
    #for each item in dictionary e.g. ('time,', 'souls,'): ['from']  
        if ((key[0])[0]).isupper(): 
        #if the first letter of the first key tuple is uppercase, then add it to a list of caps words to start sentences
            caps_list[key] = value

    pick = random.choice(list(caps_list.keys()))
    first_word = pick[0]
    sentence = []
    while len(sentence) < 10:
        the_value = random.choice(chains1[pick]) #the value is a random value for the key previously chosen 
        pick = (pick[1], the_value) 
        #the pick now starts with what had been the second word in the key
        sentence.append(pick[1]) 

    while len(sentence) >= 10 and len(sentence) <= 25: 
    #after the sentence has reached a certain length, look for a key tuple in corpus 1 that is also in corpus2
        if (pick[1])[-1] == "." and len(sentence) >= 15:
            break
        elif pick in chains2: 
        #if we can find a key tuple in both, pick that tuple (encouraging mashing from two sources)
            the_value = random.choice(chains2[pick])
            pick = (pick[1], the_value) 
            sentence.append(pick[1]) 
        else:
        #otherwise, continue working with the first list of words
            the_value = random.choice(chains1[pick]) 
            pick = (pick[1], the_value) 
            sentence.append(pick[1]) 

    sentence2 = first_word
    for word in sentence:
        sentence2 += " " + word

    print sentence2


def main():
    args = sys.argv #this refers to a list of the two arguments entered on the command line (script and filename)
    script, filename, filename2 = argv

    text = open(filename)
    input_text = text.read()
    text.close()

    text2 = open(filename2)
    input_text2 = text2.read()
    text2.close()

    chain_dict = make_chains(input_text, input_text2)
    #this variable is what is returned from the make_chains function (the Markov chains dictionary)

    random_text = make_text(chain_dict)
    #this variable takes the Markov chains dictionary and runs it through the second function, make_text

if __name__ == "__main__":
    main()

