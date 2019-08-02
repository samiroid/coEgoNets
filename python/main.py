import argparse
import gzip
from collections import Counter
from sklearn.feature_extraction.stop_words import ENGLISH_STOP_WORDS
from scipy.sparse import dok_matrix
from ipdb import set_trace
import itertools
import sys
import pickle
import pandas as pd
MIN_COOC = 3

class Vocabulary:
    def __init__(self):
        self._V = {}

    def word2idx(self, w):
        try:
            return self._V[w]
        except KeyError:
            next_key = len(self._V) + 1
            self._V[next_key] = w
            return next_key
    
    def doc2idx(self, doc):
        m = [self.word2idx(w) for w in doc.split()]
        return m
    
    def size(self):
        return len(self._V)

def build_coocurrences(docs):    
    #initialize co-ocurrence (sparse) matrix        
    C = Counter()
    V = Vocabulary()
    for i,d in enumerate(docs):
        if i % 500 == 0:
            sys.stdout.write("\rdoc: {}/{}".format(i,len(docs)))
            sys.stdout.flush()
        #convert tokens to indices
        t = V.map(d)
        #iterate over token combinations        
        for co in itertools.combinations(t,2):
            set_trace()
            #symmetric update
            # C[co[0],co[1]]+=1
            # C[co[1],co[0]]+=1
    return C, V



# def get_vocabulary(docs, max_words=None):
#     """
#         Compute a dictionary index mapping words into indices
#     """
#     print("[building vocabulary]")
#     words = [w for m in docs for w in m.split()]
#     #keep only the 'max_words' most frequent tokens
#     if max_words:
#         top_words = sorted(Counter(words).items(), key=lambda x:x[1],reverse=True)[:max_words]
#         words = [w[0] for w in top_words]
#     #keep only the types
#     words = list(set(words))
#     print("[vocabulary size: {}]".format(len(words)))
#     w2i = {w:i for i, w in enumerate(words)}
#     return w2i

def get_coom(docs, V):    
    #initialize co-ocurrence (sparse) matrix        
    C = dok_matrix((len(V), len(V)), dtype=int)
    for i,d in enumerate(docs):
        if i % 500 == 0:
            sys.stdout.write("\rdoc: {}/{}".format(i,len(docs)))
            sys.stdout.flush()
        #convert tokens to indices
        t = [V[w] for w in d.split() if w in V]
        #iterate over token combinations        
        for co in itertools.combinations(t,2):
            #symmetric update
            C[co[0],co[1]]+=1
            C[co[1],co[0]]+=1
    return C

def read_data(path):
    data = []
    with open(path, "r") as f:
        for line in f:
            data.append(line)
    return data

def get_coos(C, V, target_word, min_cooc):          
    coos = C[V[target_word],:].toarray()
    ranked_coos = coos.argsort().tolist()[0][::-1]
    #invert vocabulary
    i2w = {i:w for w, i in V.items()}        
    coos_list = coos.tolist()[0]    
    #keep only words with at least 3 characters
    word_coos = [(i2w[w],coos_list[w]) for w in ranked_coos if len(i2w[w])>3]
    df = pd.DataFrame(word_coos,columns=["word","coo"])
    #keep only entries with at least min_cooc co-occurrences
    ol_size = len(df)
    df = df[df["coo"] >= min_cooc]    
    print("[getting cooc >= {}]".format(min_cooc))
    print("> {}: {}/{}".format(target_word,len(df),ol_size))
    return df

def cmdline_args():
    par = argparse.ArgumentParser(description="COOM")
    par.add_argument('-data_path', type=str, required=True, help='input data')
    par.add_argument('-output', type=str, help='output path')	
    par.add_argument('-target_word', type=str, help='target word')	    

    return par.parse_args()

def build(data_path, output_path):
    T = read_data(data_path)        
    print("[building co-occurrence matrix]")
    C, V = build_coocurrences(T)         
    print("\n[saving @ {}]".format(output_path))
    #pickle coocurrence matrix and vocabulary
    with open(output_path,"wb") as f:
        pickle.dump([C,V],f, -1)
    

if __name__ == "__main__":    
    args = cmdline_args()    
    build(args.data_path, args.output)
    
        
