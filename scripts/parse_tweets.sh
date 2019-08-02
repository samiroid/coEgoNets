DATA_PATH="/Users/samir/Dev/projects/wellness/DATA/wellness_hashtag_all.json.gz"
OUTPUT="/Users/samir/Dev/projects/wellness/DATA/txt/"

python python/parse_tweets.py --ht -data_path $DATA_PATH -output $OUTPUT -parse_by "year"

