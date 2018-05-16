from nltk import ngrams
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from sklearn.cluster import KMeans
from nltk import pos_tag
import numpy as np
from multiprocessing import Pool
import time
# getting all reviews

def load_reviews():
    f_reviews = open('all_reviews/all_reviews_fix.txt','r',encoding='utf-8')
    # all review in one string
    all_review = f_reviews.read()
    f_reviews.close()
    # f_noun = open('Directionary/nouns/91K nouns.txt','r',encoding="windows-1252")
    # all_nouns = f_noun.read()
    # f_noun.close()
    # all_review = all_nouns + all_review
    # getting all reviews
    f_reviews = open('all_reviews/all_reviews_fix.txt','r',encoding='utf-8')
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
    return filtered_review,reviews
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

# input: a dictionary of different word
# out: an dictionary of difference word with their corresponding index
def mofi_to_index(dict):
    # count as index
    count = 0
    # loop dict
    for key in dict:
        # set count to each key
        dict[key] = count
        # and count ++ since index start with 0 we add count after assigned
        count = count + 1

# input dictionary of word with their frequency
# output make all frequency to zero
def mofi_to_zero(dict):
    # loop dict
    for key in dict:
        # set them to zero
        dict[key] = 0
# input: data, list of words(tokenize)
# output: dictionary with words and their frequency of word
def create_frequency_dict(data):
    # result
    words_dic = {}
    # loop the data
    for i in range(len(data)):
        # check if the word already in the result
        if data[i] in words_dic:
            # yes, we increase the frequency of that word
            words_dic[data[i]] += 1
        else:
            # no, we add them into it and set to 1
            words_dic[data[i]] = 1
    #return result
    return words_dic

#gram_generator(filtered_review, 2, words_dic_bi)


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

# print all words
# print(words_dic)
# print(len(words_dic))
# print bigrams
#print(words_dic_bi)
# print the words for unqigram
#print(words_dic)

"""Above the stuff are for all review, below are for each single review"""
# input: a dictionary with word and their frequency
# output: a dictionary with word and after average by the size of dictionary
def normalization(dic):
    for key in dic:
        if dic[key] > 0:
            dic[key] = dic[key] / len(dic)
# print(len(word_dic_temp))
# input: data the list of word, container, container = word_dic_temp which the list of word in the kmean
def find_frequency_dict(data,container):
    # loop the words
    for i in range(len(data)):
        # if find the word
        if data[i] in container:
            # we increase the frequency
            container[data[i]] += 1

# input: reviews as array of review, container_gram as result, word_dic_temp for sample of word list in kmeans
# output: an array contain dictionaries which contained word and frequency of each review
def review_to_train_data(reviews, container_gram,word_dic_temp):
    #loop the reivew
    for review in reviews:
        # string to list
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

# print(len(container_gram))
# the input is a array of Directionary, each dictionary is represent the frequency of one review
# [{word: frequency,...}, .... ]
# the output is a array of frequency [frequency,frequency,frequency,,x,x,x,x]

# input a array of dictionary of word and frequency
# output a array of array contains frequency without the word
def get_frequncy_array(array_of_reivews):
    # result
    frequency_array = []
    # loop the input
    for i in array_of_reivews:
        # define a empty arry
        array = []
        # loop each dictionary of input
        for key in i:
            # add the frequency into array
            array.append(i[key])
        # add back to the result
        frequency_array.append(array.copy())
    # return the array
    return np.array(frequency_array)
#print(fre_array)


#print(kmeans.labels_)
#print(kmeans.cluster_centers_)

# input: clusters: each center of kmeans, the labels_ of kmeans, the array contined frequency
# output: sse: an array of sse of each cluster, and overall sse
def find_SSE(clusters,labels_,fre_array):
    # result
    sse = {}
    # container of contains average of each clusters SSE
    average_cluster = []
    # loop the cluster
    for i in range(len(clusters)):
        # declare sum, and set the sse of each cluster to 0
        sum = 0
        sse[i] = 0
        # loop the number of each center
        for value in clusters[i]:
            # get the sum of them
            sum += value
        # take the average
        average = sum/len(clusters[i])
        # we add adverage to container
        average_cluster.append(average)
    # loop the frequency array
    for i in range(len(fre_array)):
        # the number in the frequency
        for datapoint in fre_array[i]:
            # the format of sse is center - datapoint and to the power of 2
            sse[labels_[i]] += (average_cluster[labels_[i]] - datapoint) ** 2
    # sum of sse to 0
    sum_sse = 0
    # loop the sse
    for x in sse:
        # add to sum
        sum_sse += sse[x]
    # return the results
    return sse, sum_sse/len(sse)

# this function give prediction of one restaurant
# input restaurant: a dictionary:name, reviews, url, kmean, word_dic_temp
def prediction(restuarant):
    # the output
    result = {}
    # the array of dictionary of each dictionary of words and frequency
    container_gram = []
    # run the review_to_train_data to get the trainning data in a array
    review_to_train_data(restuarant[1],container_gram,restuarant[4].copy())
    # grab the frequency only by calling get_frequncy_array
    fre_array = get_frequncy_array(container_gram)
    # use keman to predict
    prediction_result = restuarant[3].predict(fre_array)
    # to contain the center of each label from prediction
    center_container = []
    # loop the result of predict
    for i in prediction_result:
        # add the corresponding center
        center_container.append(restuarant[3].cluster_centers_[i])
    # adding the infomration of other function use
    result["name"] = restuarant[0]
    result["kmean_centers"] = center_container
    result["prediction_result"] = prediction_result
    result["fre_array"] = fre_array
    result["word_dic_temp"] = restuarant[4]
    result["score_array"] = restuarant[5]
    result["cluster_centers"] = restuarant[3].cluster_centers_
    # return result
    return result

# input a array of contain all restuarants
# output a array of contain result of prediction function of all restuarant
def all_prediction(restuarants):
    # pallerel process
    with Pool(31) as p:
        # map function and input
        result_all = p.map(prediction, restuarants)
        # stop
        p.terminate()
        # merge them
        p.join()
    # return result
    return result_all
"""below functions for filter out the word that is useless to determine the aspect"""
#print(kmeans.cluster_centers_[0])
#input: array of centers from k mean
#output: array of dictionary with index and frequency
def filter_zero_centers_index(cluster_centers):
    # result
    result = []
    # loop the centers
    for i in cluster_centers:
        # define a dictionary to contain index and frequency
        cluster_index = {}
        # loop the center
        for j in range(len(i)):
            # if the value is greater than 0 or not
            if i[j] > 0:
                # yes we add to the dictionary and his frequency
                cluster_index[j] = i[j]
        # add to result
        result.append(cluster_index.copy())
    # retrun the result
    return result
#print(non_zero_index_center[1])
#print(len(non_zero_index_center[0]),len(non_zero_index_center[1]),len(non_zero_index_center[2]),len(non_zero_index_center[3]),len(non_zero_index_center[4]))

#input: index array: array containes dictionary of index and frequency, a sample dictionary of word of kmean
#output: a array contain dictionary of word
def find_words_index(index_array,words_dic):
    # result
    result = []
    # loop the index array
    for i in index_array:
        # word dictionary
        words = {}
        # loop the each element
        for key_i in i:
            # loop the word in sameple array
            for key in words_dic:
                # check the ward
                if words_dic[key] == key_i:
                    # if match to the index, we add them
                    words[key] = i[key_i]
        # add to result
        result.append(words.copy())
    return result

#print(len(feature_words[0]),len(feature_words[1]),len(feature_words[2]),len(feature_words[3]),len(feature_words[4]))
#print(feature_words[0])
# print(len(feature_words))

#input the feature word (a array of array of word)
# a array of array of word (remove useless word)
def filter_feature_word(feature_words):
    # load the files contained the word that is not useful to find aspect
    # conjunction and pronoun
    f_pronoun_conj = open("Directionary/pronouns_and_conj.txt","r")
    pronoun_conj = f_pronoun_conj.read().splitlines()
    f_pronoun_conj.close()
    # verbs
    f_verb = open("Directionary/verbs/31K verbs.txt","r")
    verbs = f_verb.read().splitlines()
    f_verb.close()
    # adverb
    f_adverb = open("Directionary/adverbs/6K adverbs.txt","r")
    adverbs = f_adverb.read().splitlines()
    f_adverb.close()
    # adjective
    f_adj = open("Directionary/adjectives/28K adjectives.txt","r")
    adjs = f_adj.read().splitlines()
    f_adj.close()
    # result
    result = []
    # loop the feature array
    for feature_list in feature_words:
        # dict for container
        new_feature_list = {}
        # loop the feature list
        for key in feature_list:
            # check the word
            if key.lower() not in pronoun_conj and key.lower() not in verbs and key.lower() not in adverbs and key.lower() not in adjs:
                # if not, we add into array
                new_feature_list[key] = feature_list[key]
        # add back to result
        result.append(new_feature_list.copy())
    # return
    return result

# main function to call
# output: kmean(trained), same array of word in kmean
def main():
    # load review
    filtered_review,reviews = load_reviews()
    # create the dict of word for k mean
    words_dic = create_frequency_dict(filtered_review)
    # modfi them with index
    mofi_to_index(words_dic)
    # container for each reviews
    container_gram = []
    # get a copy
    word_dic_temp = words_dic.copy()
    # reviews to trainning data
    review_to_train_data(reviews,container_gram,word_dic_temp)
    # grab the frequency only
    fre_array = get_frequncy_array(container_gram)
    # run the kmeans with best 6
    kmeans = KMeans(n_clusters=6, random_state=0)
    # train the data
    kmeans.fit(fre_array)
    # mode back to index
    mofi_to_index(word_dic_temp)
    # non_zero_index_center = filter_zero_centers_index(kmeans.cluster_centers_)
    # feature_words = find_words_index(non_zero_index_center,words_dic)
    # filter_features = filter_feature_word(feature_words)
    # f_nk = open("features_words/six_k.txt",'w')
    # for feature in filter_features:
    #     for i in feature:
    #         f_nk.write(str(i) + "\n")
    #     f_nk.write("----------------------------------------------------------------------------------------\n")
    # f_nk.close()
    # sse,avg_sse = find_SSE(kmeans.cluster_centers_,kmeans.labels_,fre_array)
    # print(sse)
    # print(avg_sse)
    # return the object kmean and word_dic_temp
    return kmeans,word_dic_temp
#kmeans, word_dic_temp = main()
# print(time.time() - start_time)
# print(prediction(txt,kmeans,word_dic_temp))

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
