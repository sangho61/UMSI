import csv
from sklearn.metrics import f1_score
import matplotlib.pyplot as plt
import re
import numpy as np
from scipy.sparse import csr_matrix, hstack
import logging, sys
import math



dat = []
dev = []
stop_words = []
with open('train.tsv') as tsvfile:
  reader = csv.DictReader(tsvfile, dialect='excel-tab', quoting=csv.QUOTE_NONE)
  for i in reader:
      dat.append(i)

with open('dev.tsv') as tsvfile:
  reader2 = csv.DictReader(tsvfile, dialect='excel-tab', quoting=csv.QUOTE_NONE)
  for i in reader2:
      dev.append(i)

with open('stopwords.txt', 'r') as file:
    for line in file.readlines():
        stop_words.append(line.strip())


def tokenize(text):
    return text.split()

def better_tokenize(text):
    text = text.lower()
    text = re.sub(r"(@[a-zA-Z0-9_]+)|(\w+:\/\/\S+)", " ", text)
    text = re.sub('[^A-Za-z0-9 ]+', '', text)
    features = text.split()
    filtered_features = []
    for feature in features:
        if feature not in stop_words:
            filtered_features.append(feature)
    return filtered_features

def create_matrix(lst):
    indptr = [0]
    indices = []
    data = []
    vocabulary = {}
    y_true = []

    for i in lst:
        y_true.append(int(i['class']))

        text = better_tokenize(i['text'])
        for k in text:
            index = vocabulary.setdefault(k, len(vocabulary))
            indices.append(index)
            data.append(1)
        indptr.append(len(indices))
    a = csr_matrix((data, indices, indptr))
    return [a, np.array([y_true]).T, vocabulary]

def sigmoid(z):
    return 1/(1+np.exp(-z))



def log_likelihood(x, yt, w):
    scores = x.dot(w)
    ll = np.sum(yt * scores - np.log(1 + np.exp(scores)))
    return ll



def logistic_regression(x, yt, num_steps, learning_rate, add_intercept = False):
    steps = []
    ll_lst = []

    if add_intercept:
        intercept = np.ones((x.shape[0], 1))
        x = hstack((intercept, x))

    w = np.zeros((x.shape[1], 1))

    for step in range(num_steps):
        scores = x.dot(w)
        predictions = sigmoid(scores)
        output_error_signal = yt - predictions
        gradient = x.T.dot(output_error_signal)
        w += learning_rate * gradient

        if step % 10000 == 0:
            steps.append(step)
            ll = log_likelihood(x, yt, w)
            ll_lst.append(ll)
            print('step: ',step, '', 'll: ', ll)
    return {'w': w, 'step': steps, 'll': ll_lst}



def predict(x, w):
    scores = x.dot(w)
    yp = sigmoid(scores)
    ytr = np.round(yp)
    return ytr

def predict2(d, w, vocabulary, label = True, add_intercept = False):
    yp = []
    yt = []
    inst =[]

    for i in d:
        inst.append(i['instance_id'])
        if label:
            yt.append(int(i['class']))


        if add_intercept:
            x = np.zeros((1, len(vocabulary)+1))
            x[0, 0] = 1
            text = better_tokenize(i['text'])
            for k in text:
                if k in vocabulary:
                    index = vocabulary[k]
                    x[0, index] += 1
        else:
            x = np.zeros((1, len(vocabulary)))
            text = better_tokenize(i['text'])
            for k in text:
                if k in vocabulary:
                    index = vocabulary[k]
                    x[0, index] += 1

        scores = int(predict(x,w))
        yp.append(scores)

    return {'yp': yp, 'yt': yt, 'inst_id': inst}


def f1_check(yte, ytr):
    return f1_score(yte, ytr, average = 'micro')


train_set = create_matrix(dat)
train_x = train_set[0]
train_y = train_set[1]
train_v = train_set[2]

print(train_x.shape, train_y.shape)

w1 = logistic_regression(train_x, train_y, num_steps = 300000, learning_rate = 5e-5, add_intercept = True)
w1_step = w1['step']
w1_ll = w1['ll']

w2 = logistic_regression(train_x, train_y, num_steps = 300000, learning_rate = 5e-3, add_intercept = True)
w2_ll = w2['ll']
w2_w = w2['w']

w3 = logistic_regression(train_x, train_y, num_steps = 300000, learning_rate = 5e-7, add_intercept = True)
w3_ll = w3['ll']
w3_w = w3['w']


plt.plot(w1_step, w1_ll, label='lr=5e-5', 'b')
plt.plot(w1_step, w2_ll, label='lr=5e-3', 'r')
plt.plot(w1_step, w3_ll, label = 'lr=5e-7', 'g')
plt.show()


p1 = predict(dev, w1, train_v, label = True, add_intercept = True )
yp1 = p1['yp']
yt1 = p2['yt']

f1 = f1_check(yt1,yp1)
print(f1)


testarr =[]
with open('test.unlabeled.tsv') as tsvfile:
    reader3 = csv.DictReader(tsvfile, dialect='excel-tab', quoting=csv.QUOTE_NONE)
    for i in reader3:
        testarr.append(i)
