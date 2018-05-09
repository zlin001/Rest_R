# imports needed and set up logging
import gzip
import gensim
import logging

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
data_file="reviews_data.txt.gz"

with open ('reviews_data.txt', 'rb') as f:
    print(f.read())
