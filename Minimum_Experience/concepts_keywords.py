# -*- coding: utf-8 -*-
"""
Created on Tue Dec  3 10:57:52 2019

@author: smattoo5
"""
import time   
import os
import sys
import traceback
import string

import pandas as pd
from collections import defaultdict

import re
import requests
import json

import spacy
import en_core_web_sm
nlp = en_core_web_sm.load()


def FindPos(SearchSentence):
    """ Find the different tags to identify POS of search Sentence using Spacy
    --- parameters -- 
    SearchSentence is the input Search query from user
    """
    datadictionary = {}
    for token in nlp(SearchSentence):
        datadictionary.update({token.text : [token.lemma_, token.pos_, token.tag_, token.dep_, token.ent_type_, token.shape_, 
                                             token.is_alpha, token.is_stop, token.head.text, token.head.pos_, [child for child in token.children]]})
    return datadictionary

## Transform the dictionary into DataFrame
def Trans_to_dataframe(datadictionary):
    """ Convert the Dictionary into DataFrame 
    parameters
    --- datadictionary is a dictionary having different token entities"""
    df = pd.DataFrame()
    df = pd.DataFrame(datadictionary).transpose()
    df.columns=['Lemma', 'Pos', 'Tag', 'Dep', 'Ent','Shape', 'ISAlpha', 'Is_StopWord', 'Head_Text', 'Head_Pos','Children']
    return df

def RunSearch(SearchSentence):
    """ Nested Function which will run TWO different functions and return Data Frame
        This Data Frame will be iterated and Main Concept and Sub Concept will be identified 
    """
    dicta = FindPos(SearchSentence)
    DF = Trans_to_dataframe(dicta)
    return(DF)

def NounPhrasing(SearchSentence):
    """ Use Spacy Noun Chunking to identify Noun Phrases and keywords"""
    #print(SearchSentence)
    NounPhrasing, keyword = [], []
    D = FindPos(SearchSentence)
    odd_List = ['WP', 'WRB', 'PRP'] # Avoid Which/What to be identified as Concepts
    doc = nlp(SearchSentence)
    for chunk in doc.noun_chunks:
        if len(chunk.text.split(' ')) == 1:
            if D[chunk.text][2] not in odd_List:
                NounPhrasing.append(chunk.text)
                keyword.append(chunk.root.text)
            else:
                pass
        else:
            NounPhrasing.append(chunk.text)
            keyword.append(chunk.root.text)
        

        #print(chunk.text, chunk.label_)
    
    return NounPhrasing, keyword

def FindIntent(RS):
    """ In a unique scenario keywords does not highlight the required intent
        Ex: ML accounts in asia
    """
    # traverse through dataframe:
    #Intent=''
    Intent = ''
    Intent = [ getattr(row, "Index") for row in RS.itertuples(index=True, name='Pandas') 
    if getattr(row, "Dep") == 'ROOT' and getattr(row, 'Is_StopWord') == False]
    if Intent == '':
        Intent = [ getattr(row, "Index") for row in RS.itertuples(index=True, name='Pandas') 
        if getattr(row, "Pos") == 'VERB' and getattr(row, 'Is_StopWord') == False]
    
    return Intent
    
def List_of_Prepositional_objects(DataFrame):
    """ This function will identify which phrase belongs to Main Concept"""
    List_of_Prepositional_objects = []
    for row in DataFrame.itertuples(index=True, name='Pandas'):
            Dep  = getattr(row, "Dep")
            if Dep == 'pobj':
                List_of_Prepositional_objects.append(getattr(row,'Index'))
    return List_of_Prepositional_objects

       
def FindMainConcept(NP,LPObj):
    """ This Function will identify Main Concept, Single Concept, Single Phrase"""
    MainConcepts, SubConcepts =[], []
    SingularPhrase = ''
    if len(NP) >1:
        MainConcepts = [each for each in NP for e2 in each.split() if e2 in LPObj]
        SubConcepts = [each for each in NP if each not in MainConcepts ]
        return SingularPhrase, MainConcepts, SubConcepts
    else:
        SingularPhrase=NP
        MainConcepts,SubConcepts = [''], ['']
        return SingularPhrase, MainConcepts, SubConcepts

#inputtext = "case-study in DTC"    
def Main(inputtext):
    SearchSentence = re.sub('-', '', inputtext)
    
    DISPLAY ={}
    #SearchSentence = "case study in DTC"
    RS = RunSearch(SearchSentence)
    NP,KW = NounPhrasing(SearchSentence)
    I = FindIntent(RS)
    KW = list(set(I+KW))
    LPObj = List_of_Prepositional_objects(RS)
    Sp, Mc, Sc = FindMainConcept(NP,LPObj)
      
      
    #print("Intent is::::",I)
    #RS
    ## Print for Single Phase
	
    Intent = ''
    if len(Sp)>0:
        AllPhrases = list(set(Sp+Mc+Sc))
        DISPLAY.update({'Phrases': AllPhrases})
        # for each in AllPhrases:
        #     if I[0] in AllPhrases:
        #         Intent = each
        #     else:
        #         Intent = I
        
        #New Code 7th Dec
		      
        #DISPLAY.update({'SinglePhrase': NP, 'Relation': I, 'Keyword': KW})
        #DISPLAY.update({'SinglePhrase': NP, 'Relation': Intent})
    else:
        AllPhrases = list(set(Mc+Sc))
        DISPLAY.update({'Phrases': AllPhrases})
        # for each in AllPhrases:
        #     if I[0] in each:
        #         Intent = each
        #     else:
        #         Intent = I
   
        #DISPLAY.update({'Phrases': AllPhrases})
        #DISPLAY.update({'mainConcepts': Mc, 'subConcepts': Sc, 'Relation': I, 'Keyword': KW})
        #DISPLAY.update({'mainConcepts': Mc, 'subConcepts': Sc, 'Relation': Intent})
    #return DISPLAY
    return AllPhrases

   
##########################################################################################
   

#from flask import Flask,request,Response
#from requests.auth import HTTPBasicAuth
#import pickle as pk
#from nltk import everygrams
#import local_semantic_words as simword
#import PoolParty as PP
#import Poolparty_multiprocess as pmp
### Comment this when saved in AWS box
#os.chdir(r'C:\Users\smattoo5\Desktop\DXC-NLP\Sprint13\Deploy1')
#####

