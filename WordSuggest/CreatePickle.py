# -*- coding: utf-8 -*-
"""
Created on Sat Jan 11 22:53:57 2020

@author: smattoo5
"""
import pickle as pk

list_of_doc=[]
file_name = 'whatsappdata.txt'
with open(file_name, 'rb') as f:
    for line in f:
        list_of_doc.append(line)
        
pk.dump(list_of_doc,open('wts_data.pkl','wb'))        