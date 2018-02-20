import sys
import math
import numpy as np
from nltk.tree import *



def get_grammar(grammar):
    grammar_text = open(grammar, 'r')
    tmp = []
    tot_p = {}
    grammar = {}
    for i in grammar_text:
        tmp.append(i.split())
    for j in tmp:
        try:
            if j[1] in tot_p:
                tot_p[j[1]] += float(j[0])
            else:
                tot_p[j[1]] = float(j[0])
        except:
            pass
    for k in tmp:
        if len(k) == 4:
            grammar[(k[1], (k[2], k[3]))] = float(k[0])/tot_p[k[1]]
        elif len(k) == 3:
            grammar[(k[1], k[2])] = float(k[0])/tot_p[k[1]]

    return grammar

a = get_grammar('example.gr')
print(a)
