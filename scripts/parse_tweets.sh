DATA_PATH="/Users/samir/Dev/projects/coEgoNets/DATA/wellness_hashtag_all.json.gz"
# DATA_PATH="/Users/samir/Dev/projects/coEgoNets/DATA/11593882.tweets.gz"
# DATA_PATH="/Users/samir/Dev/projects/coEgoNets/DATA/wellness_tweets.txt.gz"
# OUTPUT="/Users/samir/Dev/projects/coEgoNets/DATA/txt/wellness"
OUTPUT="/Users/samir/Dev/projects/coEgoNets/DATA/txt/wellness_all"
KW_FILTER="#wellness"

python src/parse_tweets.py --ht -data_path $DATA_PATH -output $OUTPUT --kw $KW_FILTER

