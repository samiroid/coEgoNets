import argparse
from collections import defaultdict
import datetime
import gzip
import json
from sklearn.feature_extraction.stop_words import ENGLISH_STOP_WORDS
from twokenize import tokenizeRawTweetText
import re
import sys
from ipdb import set_trace

URL_REGEX = r"""http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+] |[!*\(\), ]|(?:%[0-9a-fA-F][0-9a-fA-F]))+"""
USER_REGEX = r""".?@.+?( |$)|<@mention>"""

def preprocess(d, hashtags_only=False):       
    d = d.lower()    
    tokens = tokenizeRawTweetText(d)
    if hashtags_only:        
        d = u' '.join([t for t in tokens if t.startswith("#")])        
    else:
        d = u' '.join([t for t in tokens if t not in set(ENGLISH_STOP_WORDS)])
        #mask user mentions
        d = re.sub(USER_REGEX," @user ", d, flags=re.I)
        #mask urls
        d = re.sub(URL_REGEX," @url ", d, flags=re.I) 
    
    return d

def read_tweets(path, output, hashtags_only=False):
    data = defaultdict(list)
    with gzip.open(path,"r") as f:        
        print("[reading docs @ {} | hashtags:{})]".format(path, str(hashtags_only)))        
        for i,l in enumerate(f):
            t = json.loads(l)         
            year = datetime.datetime.strptime(t["created_at"],"%a %b %d %H:%M:%S +0000 %Y").year        
            text = preprocess(t["text"], hashtags_only)
            if len(text)>0:
                data[year].append(text)                      
            if i % 501 == 0:                    
                sys.stdout.write("\rdoc: {}".format(i))
                sys.stdout.flush()            
    print()    
    for year, tweets in data.items():
        sys.stdout.write("\r[writing files > year: {}]".format(str(year)))
        sys.stdout.flush()                
        with open(output+"/"+str(year)+".txt", "w") as f:
            for tweet in tweets:
                f.write("{}\n".format(tweet))
    print()
    
    return data  


def cmdline_args():
    par = argparse.ArgumentParser(description="parse tweets")
    par.add_argument('-data_path', type=str, required=True, help='input data')
    par.add_argument('-output', type=str, help='output path')	    
    par.add_argument('-hashtags', "--ht", action="store_true", help='just hashtags')        
    par.add_argument('-max_docs', type=int, help='max docs to be processed')
    par.add_argument('-parse_by', choices=["year"], help='time period by which counts are grouped')

    return par.parse_args()

if __name__ == "__main__":
    
    args = cmdline_args()
    read_tweets(args.data_path, output=args.output, hashtags_only=args.ht)
    