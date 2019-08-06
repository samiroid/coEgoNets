# DATA_PATH="/Users/samir/Dev/projects/coEgoNets/DATA/11593882.tweets.gz"

# DATA_PATH="/Users/samir/Dev/projects/coEgoNets/DATA/wellness_tweets.txt.gz"
# OUTPUT="/Users/samir/Dev/projects/coEgoNets/DATA/txt/wellness"

DATA_PATH="/Users/samir/Dev/projects/coEgoNets/DATA/wellness_hashtag_all.json.gz"
OUTPUT="/Users/samir/Dev/projects/coEgoNets/DATA/txt/wellness_all_tmp"

python src/parse_tweets.py -data_path $DATA_PATH -output $OUTPUT

