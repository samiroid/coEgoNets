DATA_PATH="/Users/samir/Dev/projects/coEgoNets/DATA/txt/wellness"
OUTPUT_PATH="/Users/samir/Dev/projects/coEgoNets/DATA/pkl/wellness.zip"
# TARGET_WORD="#wellness"
# -target_word $TARGET_WORD
python src/coegonets.py -data_path $DATA_PATH -output $OUTPUT_PATH --cooc

