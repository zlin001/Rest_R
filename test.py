from nltk import ngrams
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from sklearn.cluster import KMeans
from nltk import pos_tag
import numpy as np
from multiprocessing import Pool
# getting all reviews
f_reviews = open('all_reviews/all_reviews.txt','r',encoding='utf-8')
# all review in one string
all_review = f_reviews.read()
f_reviews.close()

# f_noun = open('Directionary/nouns/91K nouns.txt','r',encoding="windows-1252")
# all_nouns = f_noun.read()
# f_noun.close()
#
# all_review = all_nouns + all_review
# getting all reviews
f_reviews = open('all_reviews/all_reviews.txt','r',encoding='utf-8')
# spit the review
reviews = f_reviews.read().splitlines()
f_reviews.close()

# container of word and frequency
words_dic = {}
#words_dic_bi = {}
# load the stopword from the library of nltk
stop_words = set(stopwords.words('english'))
# string to list
word_tokens = word_tokenize(all_review)
#test = pos_tag(word_tokens)
# filter out the review
filtered_review = [w for w in word_tokens if not w in stop_words]
# print the size of review
#print(len(review))
# print the size of after removing stopword
#print(len(filtered_reivew))
# # call the ngram function with n = 2 which represent bigrams
# def gram_generator(data, n, container):
#     ngram = ngrams(data, n)
#     # loop the result from ngram function
#     for grams in ngram:
#         # result in string
#         result = ""
#         # for more than one gram, we need to loop the grams for each word
#         for gram in grams:
#             # we add into result which it become a complete string with two words
#             result += gram
#             if n > 1:
#                 result += " "
#             # check if it is in the container
#         if n > 1:
#             result = result[:-1]
#         if result in container:
#             # yes we add frequency
#             container[result] += 1
#         else:
#             # no we set it as new index which value of frequency is 1
#             container[result] = 1
# make the value of all key in dict to 0
def mofi_to_index(dict):
    count = 0
    for key in dict:
        dict[key] = count
        count = count + 1

def mofi_to_zero(dict):
    for key in dict:
        dict[key] = 0
def create_frequency_dict(data,container):
    for i in range(len(data)):
        if data[i] in container:
            container[data[i]] += 1
        else:
            container[data[i]] = 1

#gram_generator(filtered_review, 2, words_dic_bi)
create_frequency_dict(filtered_review, words_dic)
#print(len(words_dic))
"""A small check to see if we can replace word_tokens to unigram"""
# test_container = {}
# test(filtered_review,test_container)
# result = True
# for key in words_dic:
#     if key not in test_container:
#         result = False
#     else:
#         if words_dic[key] != test_container[key]:
#             result = False
# print(result)
mofi_to_index(words_dic)
# print all words
# print(words_dic)
# print(len(words_dic))
# print bigrams
#print(words_dic_bi)
# print the words for unqigram
#print(words_dic)
