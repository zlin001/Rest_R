from nltk import ngrams
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
# getting all reviews
f_reviews = open('Package/reviews_clean.txt','r',encoding='windows-1252')
# all review in one string
all_review = f_reviews.read()
f_reviews.close()

# getting all reviews
f_reviews = open('Package/reviews_clean.txt','r',encoding='windows-1252')
# spit the review
reviews = f_reviews.read().splitlines()
f_reviews.close()

# container of word and frequency
words_dic = {}
words_dic_bi = {}
# load the stopword from the library of nltk
stop_words = set(stopwords.words('english'))
# string to list
word_tokens = word_tokenize(all_review)
# filter out the review
filtered_review = [w for w in word_tokens if not w in stop_words]
# print the size of review
#print(len(review))
# print the size of after removing stopword
#print(len(filtered_reivew))
# call the ngram function with n = 2 which represent bigrams
def gram_generator(data, n, container):
    bigrams = ngrams(data, n)
    # loop the result from ngram function
    for grams in bigrams:
        # result in string
        result = ""
        # for more than one gram, we need to loop the grams for each word
        for gram in grams:
            # we add into result which it become a complete string with two words
            result += gram + " "
            # check if it is in the container
        if result in container:
            # yes we add frequency
            container[result] += 1
        else:
            # no we set it as new index which value of frequency is 1
            container[result] = 1
# make the value of all key in dict to 0
def mofi_to_zero(dict):
    for key in dict:
        dict[key] = 0
gram_generator(filtered_review, 2, words_dic_bi)
gram_generator(filtered_review, 1, words_dic)
# print bigrams
#print(words_dic_bi)
# print the words for unqigram
#print(words_dic)

"""Above the stuff are for all review, below are for each single review"""
for review in reviews:
    print(review)
