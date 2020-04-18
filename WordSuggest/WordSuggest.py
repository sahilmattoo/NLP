# -*- coding: utf-8 -*-
"""
Created on Sat Jan 11 22:53:09 2020

@author: smattoo5
"""

import nltk
from nltk import word_tokenize

import re
from collections import Counter
import pickle as pk

from flask import jsonify
from flask import request
from flask import Flask
app = Flask(__name__)
import json
app.url_map.strict_slashes = False

import requests


def RunSpellCheck(SearchSentence):
    
    WWS = pk.load(open('wts_data.pkl', 'rb'))
    res = (" ".join(map(str, WWS)))
    
    def words(text): return re.findall(r'\w+', text.lower())
    WORDS  = Counter(words(res))
    
    def P(word, N=sum(WORDS.values())):
        "Probability of `word`."
        return WORDS[word] / N
    
    def correction(word): 
        "Most probable spelling correction for word."
        return max(candidates(word), key=P)

    def candidates(word):
        "Generate possible spelling corrections for word."
        return (known([word]) or known(edits1(word)) or known(edits2(word)) or [word])
    
    

    def known(words): 
        "The subset of `words` that appear in the dictionary of WORDS."
        return set(w for w in words if w in WORDS)
    
    def edits1(word):
        "All edits that are one edit away from `word`."
        letters    = 'abcdefghijklmnopqrstuvwxyz'
        splits     = [(word[:i], word[i:])    for i in range(len(word) + 1)]
        deletes    = [L + R[1:]               for L, R in splits if R]
        transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R)>1]
        replaces   = [L + c + R[1:]           for L, R in splits if R for c in letters]
        inserts    = [L + c + R               for L, R in splits for c in letters]
        return set(deletes + transposes + replaces + inserts)
    
    def edits2(word): 
        "All edits that are two edits away from `word`."
        return (e2 for e1 in edits1(word) for e2 in edits1(e1))

    def CorrectSentence(SearchSentence):
        tokens = SearchSentence.split()
        SpellCheckString = ''
        counterflag = False
    
        for token in tokens:
            SpellCheckString = SpellCheckString+' '+''.join(correction(token))
            newword = correction(token)
            
            if newword != token:
                counterflag = True
    
    
    
        return SpellCheckString, counterflag
    
    
    SearchSentence, flag = CorrectSentence(SearchSentence)
    if flag == True:
        DISPLAY = {'Do you Mean': SearchSentence}
    else:
        DISPLAY = {'Suggestion': 'No Suggestion'}
    
    wordsuggests = {}
    wordsuggests.update({'Word Suggestion':list(candidates(SearchSentence))})
    return DISPLAY, wordsuggests

@app.route('/wordsuggest',methods=['GET'])  
def Get_SpellCheck():
    SearchSentence = request.args.get("input")
    #SearchSentence = ' dxtc is technology'
    #print(SearchSentence)
    Suggested, WordSuggestions = RunSpellCheck(SearchSentence)
    return jsonify(Suggested)

if __name__ == "__main__":
    app.run(host='0.0.0.0') 