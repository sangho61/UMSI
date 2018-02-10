import os,sys,re,csv
import pickle
from collections import Counter, defaultdict
import numpy as np
import scipy
import math
import random
import nltk
from scipy.spatial.distance import cosine
from nltk.corpus import stopwords
from numba import jit
from nltk.tokenize import word_tokenize


min_count=2
stopwords = set(stopwords.words('english'))
fullconts = ["i am a boy boy girl", 'you are a girl bad bad good good korea korea bad boy girl']
fullrec = []

for i in fullconts:
	for k in word_tokenize(i):
		if k not in stopwords:
			fullrec.append(k)


origcounts = Counter(fullrec)


print(fullrec)
print(origcounts)

wordcounts = Counter()

fullrec_filtered = []

for i in fullrec:
	if origcounts[i] > min_count:
		fullrec_filtered.append(i)
		wordcounts[i] += 1
	else:
		fullrec_filtered.append('<UNK>')
		wordcounts['<UNK>'] += 1

print(fullrec_filtered)
print(wordcounts)

wordcodes = []
uniqueWords = list(wordcounts.keys())
uniqueWords.sort()

for i in range(len(uniqueWords)):
	a = np.zeros(len(uniqueWords))
	a[i] = 1
	wordcodes.append(a)

print(wordcodes)
