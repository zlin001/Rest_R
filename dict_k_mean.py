from nltk import ngrams
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from sklearn.cluster import KMeans
from nltk import pos_tag
import numpy as np
from multiprocessing import Pool
import time
start_time = time.time()
# getting all reviews
def load_reviews():
    f_reviews = open('all_reviews/all_reviews.txt','r',encoding='utf-8')
    # all review in one string
    all_review = f_reviews.read()
    f_reviews.close()
    all_review = all_review.replace("."," ")
    all_review = all_review.replace(","," ")
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
    #words_dic_bi = {}
    # load the stopword from the library of nltk
    stop_words = set(stopwords.words('english'))
    # string to list
    word_tokens = word_tokenize(all_review)
    #test = pos_tag(word_tokens)
    # filter out the review
    filtered_review = [w for w in word_tokens if not w in stop_words]
    return filtered_review,all_review,reviews
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
def create_frequency_dict(data):
    words_dic = {}
    for i in range(len(data)):
        if data[i] in words_dic:
            words_dic[data[i]] += 1
        else:
            words_dic[data[i]] = 1
    return words_dic

#gram_generator(filtered_review, 2, words_dic_bi)
filtered_review,all_review,reviews = load_reviews()
words_dic = create_frequency_dict(filtered_review)
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
def find_frequency_dict(data,container):
    for i in range(len(data)):
        if data[i] in container:
            container[data[i]] += 1

def review_to_train_data(reviews, container_gram):
    for review in reviews:
        # string to list
        review = review.replace("."," ")
        review = review.replace(","," ")
        review_word_tokens = word_tokenize(review)
        # filter out the review
        stop_words = set(stopwords.words('english'))
        filtered_review_each = [w for w in review_word_tokens if not w in stop_words]
        # set to zero for all keys
        mofi_to_zero(word_dic_temp)
        # call the function to generate the gram vector
        find_frequency_dict(filtered_review_each,word_dic_temp)
        # normalization
        normalization(word_dic_temp)
        #print(len(word_dic_temp))
        # if count == 0:
        #     test = word_dic_temp.copy()
        # count += 1
        # and save in an array
        container_gram.append(word_dic_temp.copy())
review_to_train_data(reviews,container_gram)
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
kmeans = KMeans(n_clusters=6, random_state=0)
kmeans.fit(fre_array)
#print(kmeans.labels_)
#print(kmeans.cluster_centers_)
# def find_SSE(clusters,labels_,fre_array):
#     sse = {}
#     average_cluster = []
#     for i in range(len(clusters)):
#         sum = 0
#         sse[i] = 0
#         for value in clusters[i]:
#             sum += value
#         average = sum/len(clusters[i])
#         average_cluster.append(average)
#     for i in range(len(fre_array)):
#         for datapoint in fre_array[i]:
#             sse[labels_[i]] += (average_cluster[labels_[i]] - datapoint) ** 2
#     sum_sse = 0
#     for x in sse:
#         sum_sse += sse[x]
#     return sse, sum_sse/len(sse)
# sse,avg_sse = find_SSE(kmeans.cluster_centers_,kmeans.labels_,fre_array)
# print(sse)
# print(avg_sse)
def filter_zero_centers_index(cluster_centers):
    result = []
    for i in cluster_centers:
        cluster_index = {}
        for j in range(len(i)):
            if i[j] != 0:
                cluster_index[j] = i[j]
        result.append(cluster_index.copy())
    return result
non_zero_index_center = filter_zero_centers_index(kmeans.cluster_centers_)
#print(non_zero_index_center[1])
#print(len(non_zero_index_center[0]),len(non_zero_index_center[1]),len(non_zero_index_center[2]),len(non_zero_index_center[3]),len(non_zero_index_center[4]))

def find_words_index(index_array):
    result = []
    for i in index_array:
        words = {}
        for key_i in i:
            for key in words_dic:
                if words_dic[key] == key_i:
                    words[key] = i[key_i]
        result.append(words.copy())
    return result
feature_words = find_words_index(non_zero_index_center)
#print(len(feature_words[0]),len(feature_words[1]),len(feature_words[2]),len(feature_words[3]),len(feature_words[4]))
#print(feature_words[0])
# print(len(feature_words))

def filter_feature_word(feature_words):
    f_pronoun_conj = open("Directionary/pronouns_and_conj.txt","r")
    pronoun_conj = f_pronoun_conj.read().splitlines()
    f_pronoun_conj.close()
    f_verb = open("Directionary/verbs/31K verbs.txt","r")
    verbs = f_verb.read().splitlines()
    f_verb.close()
    f_adverb = open("Directionary/adverbs/6K adverbs.txt","r")
    adverbs = f_adverb.read().splitlines()
    f_adverb.close()
    f_adj = open("Directionary/adjectives/28K adjectives.txt","r")
    adjs = f_adj.read().splitlines()
    f_adj.close()
    result = []
    for feature_list in feature_words:
        new_feature_list = {}
        for key in feature_list:
            if key.lower() not in pronoun_conj and key.lower() not in verbs and key.lower() not in adverbs and key.lower() not in adjs:
                new_feature_list[key] = feature_list[key]
        result.append(new_feature_list.copy())
    return result

filter_features = filter_feature_word(feature_words)
f_nk = open("features_words/six_k.txt",'w')
for feature in filter_features:
    for i in feature:
        f_nk.write(str(i) + "\n")
    f_nk.write("----------------------------------------------------------------------------------------\n")
f_nk.close()

print(time.time() - start_time)
#print(filter_features[0])
# print(len(feature_words[0]),len(feature_words[1]),len(feature_words[2]),len(feature_words[3]),len(feature_words[4]),len(feature_words[5]))
# f_feature = open("feature_words.txt","w")
# for feature_list in feature_words:
#     f_feature.write(str(feature_list) + "\n")
# f_feature.close()
# test = True
# for i in range(len(feature_words)):
#     if len(feature_words[i]) != len(non_zero_index_center[i]):
#         test = False
# print(test)
