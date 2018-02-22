import os,sys,re,csv
import pickle
from collections import Counter, defaultdict
import numpy as np
import scipy
import math
import random
import nltk
import time
from scipy.spatial.distance import cosine
from nltk.corpus import stopwords
from numba import jit
from nltk.tokenize import word_tokenize
import logging
from scipy import spatial
from nltk.tokenize import RegexpTokenizer
import matplotlib.pyplot as plt


#... (1) First load in the data source and tokenize into one-hot vectors.
#... Since one-hot vectors are 0 everywhere except for one index, we only need to know that index.


#... (2) Prepare a negative sampling distribution table to draw negative samples from.
#... Consistent with the original word2vec paper, this distribution should be exponentiated.


#... (3) Run a training function for a number of epochs to learn the weights of the hidden layer.
#... This training will occur through backpropagation from the context words down to the source word.


#... (4) Re-train the algorithm using different context windows. See what effect this has on your results.


#... (5) Test your model. Compare cosine similarities between learned word vectors.





#.................................................................................
#... global variables
#.................................................................................


random.seed(10)
np.random.seed(10)
randcounter = 10
np_randcounter = 10


vocab_size = 0
hidden_size = 100
uniqueWords = [""]                      #... list of all unique tokens
wordcodes = {}                          #... dictionary mapping of words to indices in uniqueWords
wordcounts = Counter()                  #... how many times each token occurs
samplingTable = []                      #... table to draw negative samples from






#.................................................................................
#... load in the data and convert tokens to one-hot indices
#.................................................................................



def loadData(filename):
	global uniqueWords, wordcodes, wordcounts
	override = True
	if override:
		#... for debugging purposes, reloading input file and tokenizing is quite slow
		#...  >> simply reload the completed objects. Instantaneous.
		fullrec = pickle.load(open("w2v_fullrec.p","rb"))
		wordcodes = pickle.load( open("w2v_wordcodes.p","rb"))
		uniqueWords= pickle.load(open("w2v_uniqueWords.p","rb"))
		wordcounts = pickle.load(open("w2v_wordcounts.p","rb"))
		return fullrec


	#... load in the unlabeled data file. You can load in a subset for debugging purposes.
	handle = open(filename, "r", encoding="utf8")
	fullconts =handle.read().split("\n")
	fullconts = [entry.split("\t")[1].replace("<br />", "") for entry in fullconts[1:(len(fullconts)-1)]]

	#... apply simple tokenization (whitespace and lowercase)
	fullconts = [" ".join(fullconts).lower()]





	print ("Generating token stream...")
	#... (TASK) populate fullrec as one-dimension array of all tokens in the order they appear.
	#... ignore stopwords in this process
	#... for simplicity, you may use nltk.word_tokenize() to split fullconts.
	#... keep track of the frequency counts of tokens in origcounts.
	stop_words = set(stopwords.words('english'))
	tokenizer = RegexpTokenizer(r'\w+')
	words = tokenizer.tokenize(fullconts[0])
	fullrec = list(filter(lambda x: x not in stop_words, words))
	min_count = 50
	origcounts = Counter(fullrec)




	print ("Performing minimum thresholding..")
	#... (TASK) populate array fullrec_filtered to include terms as-is that appeared at least min_count times
	#... replace other terms with <UNK> token.
	#... update frequency count of each token in dict wordcounts where: wordcounts[token] = freq(token)
	#... after filling in fullrec_filtered, replace the original fullrec with this one.

	fullrec_filtered = list(map(lambda x: x if origcounts[x] >= min_count else 'UNK', fullrec))

	#... after filling in fullrec_filtered, replace the original fullrec with this one.
	fullrec = fullrec_filtered
	wordcounts = Counter(fullrec)



	print ("Producing one-hot indicies")
	#... (TASK) sort the unique tokens into array uniqueWords
	#... produce their one-hot indices in dict wordcodes where wordcodes[token] = onehot_index(token)
	#... replace all word tokens in fullrec with their corresponding one-hot indices.
	uniqueWords = list(set(fullrec_filtered))
	wordcodes = {w: i for i, w in enumerate(uniqueWords)}
	#logging.debug("wordcodes: {}".format(wordcodes))
	fullrec = list(map(lambda x: wordcodes[x], fullrec))



	#... close input file handle
	handle.close()


	#... store these objects for later.
	#... for debugging, don't keep re-tokenizing same data in same way.
	#... just reload the already-processed input data with pickles.
	#... NOTE: you have to reload data from scratch if you change the min_count, tokenization or number of input rows

	pickle.dump(fullrec, open("w2v_fullrec.p","wb+"))
	pickle.dump(wordcodes, open("w2v_wordcodes.p","wb+"))
	pickle.dump(uniqueWords, open("w2v_uniqueWords.p","wb+"))
	pickle.dump(dict(wordcounts), open("w2v_wordcounts.p","wb+"))


	#... output fullrec should be sequence of tokens, each represented as their one-hot index from wordcodes.
	return fullrec

def load_test(filename):
	handle = open(filename, "r", encoding="utf8")
	test_pair = handle.read().split("\n")
	test_pair = [entry.split("\t") for entry in test_pair[1:(len(test_pair) - 1)]]

	return test_pair



#.................................................................................
#... compute sigmoid value
#.................................................................................
@jit(nopython=True)
def sigmoid(x):
	return float(1)/(1+np.exp(-x))




#.................................................................................
#... generate a table of cumulative distribution of words
#.................................................................................


def negativeSampleTable(train_data, uniqueWords, wordcounts, exp_power=0.75):
	#global wordcounts
	#... stores the normalizing denominator (count of all tokens, each count raised to exp_power)
	# max_exp_count = 0

	override = True
	if override:
	#... for debugging purposes, reloading input file and tokenizing is quite slow
	#...  >> simply reload the completed objects. Instantaneous.
		cumulative_dict = pickle.load(open("w2v_sampletable.p","rb"))
		return cumulative_dict

	print ("Generating exponentiated count vectors")
	#... (TASK) for each uniqueWord, compute the frequency of that word to the power of exp_power
	#... store results in exp_count_array.
	exp_count_array = list(map(lambda x: math.pow(wordcounts[x], exp_power), uniqueWords))
	max_exp_count = sum(exp_count_array)



	print ("Generating distribution")

	#... (TASK) compute the normalized probabilities of each term.
	#... using exp_count_array, normalize each value by the total value max_exp_count so that
	#... they all add up to 1. Store this corresponding array in prob_dist
	prob_dist = list(map(lambda x: float(x/max_exp_count), exp_count_array))





	print ("Filling up sampling table")
	#... (TASK) create a dict of size table_size where each key is a sequential number and its value is a one-hot index
	#... the number of sequential keys containing the same one-hot index should be proportional to its prob_dist value
	#... multiplied by table_size. This table should be stored in cumulative_dict.
	#... we do this for much faster lookup later on when sampling from this table.
	cumulative_dict = {}
	table_size = 1e8


	for i, x in enumerate(prob_dist):
		for k in range(round(sum(prob_dist[:i])*table_size), round(sum(prob_dist[:i+1])*table_size)):
			cumulative_dict[k] = i

	pickle.dump(cumulative_dict, open("w2v_sampletable.p","wb+"))

	return cumulative_dict







#.................................................................................
#... generate a specific number of negative samples
#.................................................................................


def generateSamples(context_idx, num_samples):
	global samplingTable, uniqueWords, randcounter
	results = []

	#... (TASK) randomly sample num_samples token indices from samplingTable.
	#... don't allow the chosen token to be context_idx.
	#... append the chosen indices to results
	table_size = 1e8

	while len(results) != num_samples:
		sample = samplingTable[random.randint(0, table_size-1)]
		randcounter += 1
		if (sample != context_idx) and (sample not in results):
			results.append(sample)

	return results




@jit(nopython=True)
def performDescent(num_samples, learning_rate, center_token, sequence_chars,W1,W2,negative_indices):
	# sequence chars was generated from the mapped sequence in the core code
	nll_new = 0
	pos_target = 1
	neg_target = 0
	h = np.copy(W1[center_token])

	for k in range(0, len(sequence_chars)):
		#... (TASK) implement gradient descent. Find the current context token from sequence_chars
		#... and the associated negative samples from negative_indices. Run gradient descent on both
		#... weight matrices W1 and W2.
		#... compute the total negative log-likelihood and store this in nll_new.
		w1_error_t_np = np.zeros(len(h))
		w2_k = np.copy(W2[:, sequence_chars[k]])
		pos_ll = np.dot(h, w2_k)
		neg_ll_t = 0

		for j in range(num_samples*k, num_samples*(k+1)):
			w2_j = np.copy(W2[:, negative_indices[j]])
			neg_prob = np.dot(h, w2_j)
			neg_ll_t += math.log(sigmoid(-1 * neg_prob))


			error = sigmoid(neg_prob) - neg_target

			w1_error_t_np = w1_error_t_np + (error * w2_j)
			W2[:, negative_indices[j]] = np.subtract(w2_j, learning_rate * error * h)


		error = sigmoid(pos_ll) - pos_target
		W2[:, sequence_chars[k]] = np.subtract(w2_k, learning_rate * error * h)


		w1_error_t_np = w1_error_t_np + (error * w2_k)
		W1[center_token] = np.subtract(h, learning_rate * w1_error_t_np)

		new_pos_ll = np.dot(h, np.copy(W2[:, sequence_chars[k]]))
		new_neg_ll_t = 0
		for j in range(num_samples*k, num_samples*(k+1)):
		    w2_j = np.copy(W2[:, negative_indices[j]])
		    neg_prob = np.dot(h, w2_j)
		    new_neg_ll_t += math.log(sigmoid(-1 * neg_prob))
		nll = -1 * math.log(sigmoid(new_pos_ll)) - new_neg_ll_t
		nll_new += nll

	return [nll_new]






#.................................................................................
#... learn the weights for the input-hidden and hidden-output matrices
#.................................................................................


def trainer(curW1 = None, curW2=None):
	global uniqueWords, wordcodes, fullsequence, vocab_size, hidden_size,np_randcounter, randcounter
	vocab_size = len(uniqueWords)           #... unique characters
	hidden_size = 100                       #... number of hidden neurons
	context_window = [-1,+1]            #... specifies which context indices are output. Indices relative to target word. Don't include index 0 itself.
	nll_results = []                        #... keep array of negative log-likelihood after every 1000 iterations


	#... determine how much of the full sequence we can use while still accommodating the context window
	start_point = int(math.fabs(min(context_window)))
	end_point = len(fullsequence)-(max(max(context_window),0))
	mapped_sequence = fullsequence



	#... initialize the weight matrices. W1 is from input->hidden and W2 is from hidden->output.
	if curW1 is None:
		np_randcounter += 1
		W1 = np.random.uniform(-.5, .5, size=(vocab_size, hidden_size))
		W2 = np.random.uniform(-.5, .5, size=(hidden_size, vocab_size))
	else:
		#... initialized from pre-loaded file
		W1 = curW1
		W2 = curW2



	#... set the training parameters
	epochs = 5
	num_samples = 2
	learning_rate = 0.05
	nll = 0
	iternum = 0




	#... Begin actual training
	for j in range(0,epochs):
		print ("Epoch: ", j)
		prevmark = 0

		#... For each epoch, redo the whole sequence...
		for i in range(start_point,end_point):

			if (float(i)/len(mapped_sequence))>=(prevmark+0.1):
				print ("Progress: ", round(prevmark+0.1,1))
				prevmark += 0.1
			if iternum%10000==0:
				print ("Negative likelihood: ", nll)
				nll_results.append(nll)
				nll = 0


			#... (TASK) determine which token is our current input. Remember that we're looping through mapped_sequence
			center_token = mapped_sequence[i]
			#... (TASK) don't allow the center_token to be <UNK>. move to next iteration if you found <UNK>.
			iternum += 1
			if uniqueWords[center_token] == 'UNK':
				continue



			#... now propagate to each of the context outputs


			mapped_context = [mapped_sequence[i+ctx] for ctx in context_window]
			negative_indices = []
			for q in mapped_context:
				negative_indices += generateSamples(q, num_samples)
			#... implement gradient descent
			[nll_new] = performDescent(num_samples, learning_rate, center_token, mapped_context, W1,W2, negative_indices)
			nll += nll_new

	for nll_res in nll_results:
		print (nll_res)
	plot(nll_results)
	return [W1,W2]

def plot(nlls):
	x_coordinate = [i for i in range(len(nlls))]
	plt.plot(x_coordinate[::50], nlls[::50])
	plt.show()



#.................................................................................
#... Load in a previously-saved model. Loaded model's hidden and vocab size must match current model.
#.................................................................................

def load_model():
	handle = open("saved_W1.data","rb")
	W1 = np.load(handle)
	handle.close()
	handle = open("saved_W2.data","rb")
	W2 = np.load(handle)
	handle.close()
	return [W1,W2]






#.................................................................................
#... Save the current results to an output file. Useful when computation is taking a long time.
#.................................................................................

def save_model(W1,W2):
	handle = open("saved_W1.data","wb+")
	np.save(handle, W1, allow_pickle=False)
	handle.close()

	handle = open("saved_W2.data","wb+")
	np.save(handle, W2, allow_pickle=False)
	handle.close()






#... so in the word2vec network, there are actually TWO weight matrices that we are keeping track of. One of them represents the embedding
#... of a one-hot vector to a hidden layer lower-dimensional embedding. The second represents the reversal: the weights that help an embedded
#... vector predict similarity to a context word.






#.................................................................................
#... code to start up the training function.
#.................................................................................
word_embeddings = []
proj_embeddings = []
def train_vectors(preload=False):
	global word_embeddings, proj_embeddings
	if preload:
		[curW1, curW2] = load_model()
	else:
		curW1 = None
		curW2 = None
	[word_embeddings, proj_embeddings] = trainer(curW1,curW2)
	save_model(word_embeddings, proj_embeddings)


def cosine_sim(vec1, vec2):
	result = 1 - spatial.distance.cosine(vec1, vec2)

	return result






#.................................................................................
#... for the averaged morphological vector combo, estimate the new form of the target word
#.................................................................................

# def morphology(word_seq):
# 	global word_embeddings, proj_embeddings, uniqueWords, wordcodes
# 	embeddings = word_embeddings
# 	target = wordcodes[word_pair[0]] # technique idx
# 	imputed_vec = get_or_impute_vector(morph_type, word_pair, morph_code) # suffix averaged
# 	#... find whichever vector is closest to vector_math
# 	#... (TASK) Use the same approach you used in function prediction() to construct a list
	#... of top 10 most similar words to vector_math. Return this list.





#.................................................................................
#... for the triplet (A,B,C) find D such that the analogy A is to B as C is to D is most likely
#.................................................................................

def analogy(word_seq):
	global word_embeddings, proj_embeddings, uniqueWords, wordcodes
	embeddings = word_embeddings
	vectors = [embeddings[wordcodes[word_seq[0]]],
	embeddings[wordcodes[word_seq[1]]],
	embeddings[wordcodes[word_seq[2]]]]
	vector_math = -vectors[0] + vectors[1] - vectors[2] # + vectors[3] = 0
	# ... find whichever vector is closest to vector_math
	# ... (TASK) Use the same approach you used in function prediction() to construct a list
	# ... of top 10 most similar words to vector_math. Return this list.




#.................................................................................
#... find top 10 most similar words to a target word
#.................................................................................


def prediction(target_word):
	global word_embeddings, uniqueWords, wordcodes

	#... (TASK) search through all uniqueWords and for each token, compute its similarity to target_word.
	#... you will compute this using the absolute cosine similarity of the word_embeddings for the word pairs.
	#... Note that the cosine() function from scipy.spatial.distance computes a DISTANCE so you need to convert that to a similarity.
	#... return a list of top 10 most similar words in the form of dicts,
	#... each dict having format: {"word":<token_name>, "score":<cosine_similarity>}

	k = 10
	target_vec = word_embeddings[wordcodes[target_word]]
	sim = [cosine_sim(target_vec, word_embeddings[i]) for i in range(len(uniqueWords))]
	pred = sorted(range(len(sim)), key=lambda k: sim[k], reverse=True)[:k+1]
	pred_str = list(map(lambda x: {"word": uniqueWords[x], "score": sim[x]}, pred))
	return pred_str[1:]


def write_output(result, columns, filename):
	with open(filename, 'w') as file:
		writer = csv.writer(file, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL, lineterminator='\n')
		writer.writerow(columns)
		writer.writerows(result)

def eval_pred():
    # … we've got the trained weight matrices. Now we can do some predictions
	targets = ["good", "bad", "scary", "funny"]
	pred_flattened = []
	for targ in targets:
		bestpreds = prediction(targ)
		for pred in bestpreds:
			pred_flattened.append([targ, pred["word"], pred["score"]])
		print ("\n")
	filename = "p9_output.txt"
	write_output(pred_flattened, ['target_word', 'similar_word', 'similar_score'], filename)

def eval_intrinsic(test_data):
	global word_embeddings, wordcodes
	eval = [[data[0], cosine_sim(word_embeddings[wordcodes[data[1]]], word_embeddings[wordcodes[data[2]]])] for data in test_data]
	write_output(eval, ['id', 'similarity'], "intrinsic-test.csv")



if __name__ == '__main__':
	nltk.download('stopwords')
	if len(sys.argv)==2:
		filename = sys.argv[1]
		#... load in the file, tokenize it and assign each token an index.
		#... the full sequence of characters is encoded in terms of their one-hot positions

		fullsequence= loadData(filename)
		print ("Full sequence loaded...")
		#print(uniqueWords)
		#print (len(uniqueWords))



		#... now generate the negative sampling table
		print ("Total unique words: ", len(uniqueWords))
		print("Preparing negative sampling table")
		samplingTable = negativeSampleTable(fullsequence, uniqueWords, wordcounts)


		#... we've got the word indices and the sampling table. Begin the training.
		#... NOTE: If you have already trained a model earlier, preload the results (set preload=True) (This would save you a lot of unnecessary time)
		#... If you just want to load an earlier model and NOT perform further training, comment out the train_vectors() line
		#... ... and uncomment the load_model() line

		train_vectors(preload=False)
		# [word_embeddings, proj_embeddings] = load_model()


		#... we've got the trained weight matrices. Now we can do some predictions
		eval_pred()



		#... try an analogy task. The array should have three entries, A,B,C of the format: A is to B as C is to ?
		# print (analogy(["son", "daughter", "man"]))
		# print (analogy(["thousand", "thousands", "hundred"]))
		# print (analogy(["amusing", "fun", "scary"]))
		# print (analogy(["terrible", "bad", "amazing"]))



		#... try morphological task. Input is averages of vector combinations that use some morphological change.
		#... see how well it predicts the expected target word when using word_embeddings vs proj_embeddings in
		#... the morphology() function.

		# s_suffix = [word_embeddings[wordcodes["stars"]] - word_embeddings[wordcodes["star"]]]
		# others = [["types", "type"],
		# ["ships", "ship"],
		# ["values", "value"],
		# ["walls", "wall"],
		# ["spoilers", "spoiler"]]
		# for rec in others:
		# 	s_suffix.append(word_embeddings[wordcodes[rec[0]]] - word_embeddings[wordcodes[rec[1]]])
		# s_suffix = np.mean(s_suffix, axis=0)
		# print (morphology([s_suffix, "techniques"]))
		# print (morphology([s_suffix, "sons"]))
		# print (morphology([s_suffix, "secrets"]))





		# Task4 intrinsic evaluation
		test_data = load_test("intrinsic-test_v2.tsv")
		eval_intrinsic(test_data)



	else:
		print ("Please provide a valid input filename")
		sys.exit()
