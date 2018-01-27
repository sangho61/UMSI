import csv
import math
import re
from sklearn.metrics import f1_score
import matplotlib.pyplot as plt

dat = []
dev = []
testarr =[]

with open('train.tsv') as tsvfile:
  reader = csv.DictReader(tsvfile, dialect='excel-tab', quoting=csv.QUOTE_NONE)
  for i in reader:
      dat.append(i)

with open('dev.tsv') as tsvfile:
  reader2 = csv.DictReader(tsvfile, dialect='excel-tab', quoting=csv.QUOTE_NONE)
  for i in reader2:
      dev.append(i)

stop_words = []

with open('stopwords.txt', 'r') as file:
    for line in file.readlines():
        stop_words.append(line.strip())


def tokenize(review):
    return review.split()

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


def train(data, alpha = 0):
    dct_xi_0 = {}
    dct_xi_1 = {}
    dct_pxi_0 = {}
    dct_pxi_1 = {}
    pos_tot = 0
    neg_tot = 0

    for i in data:
        if i['class'] == '0':
            pos_tot += len(tokenize(i['text']))
            for k in tokenize(i['text']):
                dct_xi_0[k] = dct_xi_0.get(k,0) + 1
        else:
            for k in tokenize(i['text']):
                dct_xi_1[k] = dct_xi_1.get(k,0) + 1
            neg_tot += len(tokenize(i['text']))

    tot = pos_tot + neg_tot
    py0 = pos_tot / tot
    py1 = neg_tot / tot
    words = set(list(dct_xi_0.keys()) + list(dct_xi_1.keys()))
    v = len(words)

    for i in words:
        dct_pxi_0[i] = (dct_xi_0.get(i, 0) + alpha) / (pos_tot+v * alpha)
        dct_pxi_1[i] = (dct_xi_1.get(i, 0) + alpha) / (neg_tot+v * alpha)

    dct_tot = {'py0': py0, 'py1':py1, 'pxi_0':dct_pxi_0,'pxi_1':dct_pxi_1, 'words_set':words}
    return dct_tot


def classify(words, dct_tot, alpha = 0):
    w = tokenize(words)
    words_set = dct_tot['words_set']
    py0 = dct_tot['py0']
    py1 = dct_tot['py1']
    pxi_0 = dct_tot['pxi_0']
    pxi_1 = dct_tot['pxi_1']
    pos = 1
    neg = 1
    for i in w:
        if i not in words_set :
            continue
        pos = pos * pxi_0[i]
        neg = neg * pxi_1[i]
    if alpha == 0:
        py0_x = pos * py0
        py1_x = neg * py1
        if py0_x >= py1_x:
            return 0
        else:
            return 1
    else:
        py0_x = math.log10(pos * py0)
        py1_x = math.log10(neg * py1)
        if py0_x >= py1_x:
            return 0
        else:
            return 1


def f1_check(deve, data, alpha):
    y_pred = []
    y_true = []
    dct = train(data, alpha)
    for i in deve:
        y_pred.append(classify(i['text'], dct, alpha))
        y_true.append(int(i['class']))
    F1 = f1_score(y_true, y_pred)
    return F1

alp_list = [0, 0.1, 0.3, 0.7, 1, 1.5, 2, 2.5, 3]
per_list = []

for i in alp_list:
    per_list.append(f1_check(dev, dat, i))
plt.plot(alp_list, per_list)
plt.show()
print(alp_list)
print(per_list)

y_instanceids = []
y_pred = []
traindic = train(dat, 0.3)

with open('test.unlabeled.tsv') as tsvfile:
    reader3 = csv.DictReader(tsvfile, dialect='excel-tab', quoting=csv.QUOTE_NONE)
    for i in reader3:
        testarr.append(i)

csvfile = open("kaggle2.csv", 'w')


for i in testarr:
    y_instanceids.append(i['instance_id'])
    y_pred.append(classify(i['text'], traindic, 0.3))


with csvfile:
    titlerow = ['instance_id', 'class']
    writer = csv.writer(csvfile)
    writer.writerow(titlerow)

    for i in range(len(y_instanceids)):
        writer.writerow([y_instanceids[i], y_pred[i]])
