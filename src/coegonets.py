import argparse
from collections import Counter
import gzip
from ipdb import set_trace
import itertools
import os
import pickle
import pandas as pd
from sklearn.feature_extraction.stop_words import ENGLISH_STOP_WORDS
from scipy.sparse import dok_matrix
import sys
MIN_COOC = 3
COUNTER_TOKEN = "OCCUR"

class Vocabulary(object):
    def __init__(self, min_word_len=4):
        self._V = {}
        self._iV = {}
        self.min_word_len = min_word_len
    def __len__(self):
        return self.size()
    
    def __getitem__(self, key):
        if isinstance(key,int):
            return self.idx2word(key)
        try:
            return self._V[key]
        except KeyError:
            return None

    def doc2idx(self, doc):
        m = [self.word2idx(w) for w in doc.split() if len(w) > self.min_word_len]
        return m

    def idx2word(self, idx):
        try:
            return self._iV[idx]
        except KeyError:
            return None

    def word2idx(self, w):
        try:
            return self._V[w]
        except KeyError:
            next_key = len(self._V) 
            self._V[w] = next_key
            self._iV[next_key] = w
            return next_key
    
    def size(self):
        return len(self._V)
    
    def vocabulary(self):
        v = [self._iV[i] for i in range(self.size())]
        return v

def build_coocurrences(docs):            
    K = Counter()
    V = Vocabulary()
    #add a special token to the vocabulary and to each doc to capture occurrences of singletons
    V.word2idx(COUNTER_TOKEN)
    total_tokens = 0
    for i,d in enumerate(docs):        
        #convert tokens to indices
        t = V.doc2idx(d)
        #get unique tokens (indices)
        t = list(set(t))
        total_tokens+=len(t)  
        #prepend counter token
        t = [V.word2idx(COUNTER_TOKEN)] + t
        #iterate over token idx combinations        
        coos = ["{},{}".format(co[0],co[1]) for co in itertools.combinations(t,2) ]
        #count co-occurrences
        K.update(coos)
        if i % 500 == 0:
            sys.stdout.write("\r > processed {} docs | {} tokens".format(len(docs), total_tokens))
            sys.stdout.flush()              
    #initialize co-ocurrence (sparse) matrix        
    M = dok_matrix((len(V), len(V)), dtype=int)
    #fill in the matrix with co-occurence counts 
    for k, v in K.items():
        word1,word2 = k.split(",")
        word1 = int(word1)
        word2 = int(word2)        
        #symmetric update
        M[word1,word2] = v
        M[word2,word1] = v    
    print("\n > done")
    #build dataframe
    C = pd.DataFrame(M.toarray(), columns=V.vocabulary(), index=V.vocabulary())
    return C

def read_data(path):    
    with open(path, "r") as f:
        data = [line for line in f]            
    return data

def cmdline_args():
    par = argparse.ArgumentParser(description="COOM")
    par.add_argument('-data_path', type=str, required=True, help='input data')
    par.add_argument('-output', type=str, help='output path')	
    par.add_argument('-target_word', type=str, help='target word')	    
    par.add_argument('-build_coocurrences', '--cooc', action="store_true", help='build co-occurrence matrix')	    
    return par.parse_args()

def save_cooc(data_path, output_path):
    #ensure output folder exists
    dirname = os.path.dirname(output_path)
    if not os.path.isdir(dirname):
        os.makedirs(dirname)    
    print("[reading data @ {}]".format(data_path))            
    T = read_data(data_path)        
    print("[building co-occurrence matrix]")
    C = build_coocurrences(T)         
    print("[saving @ {}]".format(output_path))            
    #pickle coocurrence matrix
    C.to_pickle(output_path)

if __name__ == "__main__":    
    args = cmdline_args()   
    if args.cooc:
        save_cooc(args.data_path, args.output)
