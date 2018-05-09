from nltk import ngrams
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from sklearn.cluster import KMeans
from nltk import pos_tag
import numpy as np
# getting all reviews
f_reviews = open('all_reviews/all_reviews.txt','r',encoding='utf-8')
# all review in one string
all_review = f_reviews.read()
f_reviews.close()

# getting all reviews
f_reviews = open('all_reviews/file_name30.txt','r',encoding='windows-1252')
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
#test = pos_tag(word_tokens)
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
            result += gram
            if n > 1:
                result += " "
            # check if it is in the container
        if n > 1:
            result = result[:-1]
        if result in container:
            # yes we add frequency
            container[result] += 1
        else:
            # no we set it as new index which value of frequency is 1
            container[result] = 1
# make the value of all key in dict to 0
def mofi_to_index(dict):
    count = 0
    for key in dict:
        dict[key] = count
        count = count + 1

def mofi_to_zero(dict):
    for key in dict:
        dict[key] = 0
gram_generator(filtered_review, 2, words_dic_bi)
gram_generator(filtered_review, 1, words_dic)
mofi_to_index(words_dic)
# print all words
# print(words_dic)
# print(len(words_dic))
# print bigrams
#print(words_dic_bi)
# print the words for unqigram
#print(words_dic)

"""Above the stuff are for all review, below are for each single review"""
def normalization(dic):
    for key in dic:
        if dic[key] > 0:
            dic[key] = dic[key] / len(dic)
container_gram = []
# get a copy from word_dic
word_dic_temp = words_dic.copy()
# count = 0
# print(len(word_dic_temp))
def review_array_generator(data, n, container):
    bigrams = ngrams(data, n)
    # loop the result from ngram function
    for grams in bigrams:
        # result in string
        result = ""
        # for more than one gram, we need to loop the grams for each word
        for gram in grams:
            # we add into result which it become a complete string with two words
            result += gram
            if n > 1:
                result += " "
            # check if it is in the container
        if n > 1:
            result = result[:-1]
        if result in container:
            # yes we add frequency
            container[result] += 1

for review in reviews:
    # string to list
    word_tokens = word_tokenize(review)
    # filter out the review
    filtered_review_each = [w for w in word_tokens if not w in stop_words]
    # set to zero for all keys
    mofi_to_zero(word_dic_temp)
    # call the function to generate the gram vector
    review_array_generator(filtered_review_each, 1, word_dic_temp)
    # normalization
    normalization(word_dic_temp)
    #print(len(word_dic_temp))
    # if count == 0:
    #     test = word_dic_temp.copy()
    # count += 1
    # and save in an array
    container_gram.append(word_dic_temp.copy())
# print(len(container_gram))
def get_frequncy_array(dict):
    frequency_array = []
    for i in dict:
        array = []
        for key in i:
            array.append(i[key])
        frequency_array.append(array.copy())
    return np.array(frequency_array)
fre_array = get_frequncy_array(container_gram)
#print(fre_array)
kmeans = KMeans(n_clusters=6, random_state=0).fit(fre_array)
#print(kmeans.labels_)
#for i in kmeans.cluster_centers_[0]:
     #print(i)
def filter_zero_centers_index(cluster_centers):
    result = []
    for i in kmeans.cluster_centers_:
        cluster_index = []
        for j in range(len(i)):
            if i[j] != 0:
                cluster_index.append(j)
        result.append(cluster_index.copy())
    return result
non_zero_index_center = filter_zero_centers_index(kmeans.cluster_centers_)
#print(non_zero_index_center[1])
def find_words_index(index_array):
    result = []
    for i in index_array:
        words = []
        for j in range(len(i)):
            for key in words_dic:
                if words_dic[key] == i[j]:
                    words.append(key)
        result.append(words.copy())
    return result
feature_words = find_words_index(non_zero_index_center)
#print(feature_words[1])
# test = True
# for i in range(len(feature_words)):
#     if len(feature_words[i]) != len(non_zero_index_center[i]):
#         test = False
# print(test)
