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
MIN_WORD_LEN = 4
COUNTER_TOKEN = "[COUNTS]"

class Vocabulary(object):
    def __init__(self):
        self._V = {}
        self._iV = {}
        
    def __len__(self):
        return len(self._V)
        
    def __getitem__(self, key):
        if isinstance(key,int):
            return self.idx2word(key)
        try:
            return self._V[key]
        except KeyError:
            return None

    def doc2idx(self, doc, min_word_len=1):
        m = [self.word2idx(w) for w in doc.split() if len(w) > min_word_len]
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

    def vocabulary(self):
        v = [self._iV[i] for i in range(len(self._iV))]
        return v

def getDF(C=None, V=None, path=None):
    assert (C is not None and V is not None) or path is not None, "Please pass path or C and V"
    if path is not None:
        with gzip.GzipFile(path, "r") as f:
            C, V = pickle.load(f)    
    #build dataframe
    df = pd.DataFrame(C.toarray(), columns=V, index=V)
    return df

def build_COOM(docs):            
    K = Counter()
    V = Vocabulary()
    #add a special token to the vocabulary and to each doc to capture occurrences 
    ctr_idx = V.word2idx(COUNTER_TOKEN)
    total_tokens = 0
    for i,d in enumerate(docs):        
        #convert tokens to indices
        t = V.doc2idx(d, min_word_len=MIN_WORD_LEN)
        #get unique tokens (indices)
        t = list(set(t))
        total_tokens+=len(t)  
        #prepend counter token
        t = [ctr_idx] + t
        #iterate over token idx combinations        
        coos = ["{},{}".format(co[0],co[1]) for co in itertools.combinations(t,2) ]
        #count co-occurrences
        K.update(coos)
        if i % 501 == 0:
            sys.stdout.write("\r > processed {}\{} docs | {} tokens".format(i, len(docs), 
                            total_tokens))
            sys.stdout.flush()              
    sys.stdout.write("\r > processed {}\{} docs | {} tokens".format(i, len(docs), 
                        total_tokens))
    sys.stdout.flush()   
    print()
    #initialize co-ocurrence (sparse) matrix        
    C = dok_matrix((len(V), len(V)), dtype=int)
    #fill in the matrix with co-occurence counts 
    for k, v in K.items():
        word1,word2 = k.split(",")
        word1 = int(word1)
        word2 = int(word2)        
        #symmetric update
        C[word1,word2] = v
        C[word2,word1] = v    
    print(" > done")
    return C, V.vocabulary()

def read_data(path):    
    with open(path, "r") as f:
        data = [line.strip("\n") for line in f]            
    return data

def keyword_filter_all(docs, filters):
    filtered = filter(lambda doc: all(w in doc.split() for w in filters), docs)
    return list(filtered)

def keyword_filter_any(docs, filters):
    filtered = filter(lambda doc: any(w in doc.split() for w in filters), docs)
    return list(filtered)

def cmdline_args():
    par = argparse.ArgumentParser(description="COOM")
    par.add_argument('-data_path', type=str, required=True, help='input data')
    par.add_argument('-output', type=str, help='output path')	    
    return par.parse_args()

def main(data_path, output_path):
    #ensure output folder exists
    dirname = os.path.dirname(output_path)
    if not os.path.isdir(dirname):
        os.makedirs(dirname)    
    print("[reading data @ {}]".format(data_path))            
    T = read_data(data_path)        
    print("[building co-occurrence matrix]")
    C, V = build_COOM(T)         
    output_path+=".gz"
    print("[saving @ {}]".format(output_path))            
    #pickle coocurrence matrix
    with gzip.GzipFile(output_path, "w") as f:
        pickle.dump([C, V], f, -1)

if __name__ == "__main__":    
    args = cmdline_args()       
    main(args.data_path, args.output)