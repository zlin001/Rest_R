import ast
from dict_k_mean import main
from dict_k_mean import prediction
from multiprocessing import Pool
from dict_k_mean import mofi_to_index
from dict_k_mean import all_prediction
from Package.closest_30_rests import find_all_rests
from Package.positive_negative_v2 import get_each_scores
from dict_k_mean import all_prediction
from Package.pool_review_scraper import get_all_reviews
# previous steps are the same as aspect.py, the difference is get the average of ratios of each aspects and multpy with corresponding average aspect of center
# and use that as threshold, and save the average of difference, and compare them to determine the aspect and calculate the score
# try aspect_v2_back.py if this failed
# input: none
# output: a dictionary which each aspect containes their related words
def load_related_words():
    # open the file for information
    f = open("all_reviews/aspect.txt",'r',encoding="windows-1252")
    # read all
    summary = f.read()
    # close it
    f.close()
    # convert to dictionary
    dict_related_word = ast.literal_eval(summary)
    # loop the dictionary
    for key in dict_related_word:
        # split the work by space, therefore, they are individual
        dict_related_word[key] = dict_related_word[key].split(" ")
    # return result
    return dict_related_word
#print("potato" in load_related_words()["food"])
# print(len(prediction(txt[0])["kmean_centers"]))
# print(len(prediction(txt[0])["fre_array"]))

# input: index i, word_dic_temp(a copy of word list of kmean)
# output: return the key that match the index
def find_word(i,word_dic_temp):
    # loop the word_dic_temp
    for key in word_dic_temp:
        # if the index corresponding to the number of the word
        if i == word_dic_temp[key]:
            # we return the word
            return key

# input a dictionary contain index, center of keamns that this review belong, the frequency of review, word_dic_temp
# return a dictionary with average of ratios of each aspect to center
def difference_center_fre(each):
    # load the related words
    dict_related_word = load_related_words()
    # result
    result = {}
    # save the index review
    result["index_review"] = each["index_review"]
    # save the cluster number
    result["cluster_number"] = each["cluster_number"]
    # a dictionary to save difference of each aspect to center
    different_key = {}
    # loop each aspects
    for key in dict_related_word:
        #different_key[key] = []
        # count, difference, sum = 0 intial
        count = 0.0
        sum = 0.0
        sum_difference = 0.0
        # look the size of review
        for i in range(len(each["center"])):
            # check if the word in related list of aspect
            if find_word(i,each["word_dic_temp"]) in dict_related_word[key]:
                # add count if related
                count += 1
                # set all the negative center to 0 (negative become the mean of data is 0)
                if each["center"][i] < 0:
                    each["center"][i] = 0
                # take the difference of each relate word of aspect
                difference = each["center"][i] - each["fre"][i]
                # sum of difference
                sum_difference += difference
                # if difference less 0, mean data is bigger than center which is good
                if difference < 0:
                    # distance = 0
                    sum += 0.0
                    #different_key[key].append[0.0]
                # if difference is 0
                elif difference == 0:
                    # if data is not zero, mean they are the same
                    if each["fre"][i] > 0:
                        # distance is 0
                        sum += 0.0
                        #different_key[key].append[0.0]
                    # if it is zero, both are zero
                    else:
                        # we ignore it
                        count -= 1
                        #different_key[key].append[1.0]
                # for other cases
                else:
                    # add the ratios of distance between them
                    sum += difference/each["center"][i]
        #result[key + " different_array"] = different_key
        # make sure count != 0
        if count == 0:
            result[key + " avg"] = 0
        else:
            # add the average of difference and avg of ratios to result
            result[key + " difference"] = sum_difference/count
            result[key + " avg"] = sum/count
    # return them
    return result
# input:center of kmeans, and sample of word list
# output: dictionary of average of center for each aspects
def average_cluster(array,word_dic_temp):
    # laod the related words
    dict_related_word = load_related_words()
    # result
    result = {}
    # loop aspects
    for key in dict_related_word:
        # set result of each aspect and count = 0
        result[key] = 0
        count = 0.0
        # loop the value in center
        for i in range(len(array)):
            # find the word that is match of related list
            if find_word(i,word_dic_temp) in dict_related_word[key]:
                # if value is negative
                if array[i] < 0:
                    # we pass that
                    pass
                # otherwise
                else:
                    # we add them
                    result[key] += array[i]
                    # and count + 1
                    count += 1
        #save the the number by divide the count
        result[key] = result[key]/count
    # return result
    return result

# input a dictionary contain index, center of keamns that this review belong, the frequency of review, word_dic_temp
# return a dictionary with average of ratios of each aspect to center
def check_center_value(prediction_array):
    # load the related words
    dict_related_word = load_related_words()
    # define the variable i needed
    avg_cluster_array = []
    restuarant = []
    restuarant_avg = []
    restaurant_threshold = []
    each_one = {}
    # loop centers
    for i in range(len(prediction_array["cluster_centers"])):
        # save the average of each aspects for each centers
        avg_cluster_array.append(average_cluster(prediction_array["cluster_centers"][i], prediction_array["word_dic_temp"]).copy())
        # declare empty array for restuarant
        restuarant.append([])
    # loop the size of reviews
    for i in range(len(prediction_array["kmean_centers"])):
        # get the information for calling difference_center_fre
        # name
        each_one["index_review"] = i
        # each_one["center"] is an array of corresponding center
        # corresponding center
        each_one["center"] = prediction_array["kmean_centers"][i]
        # corresponding number of cluster
        each_one["cluster_number"] = prediction_array["prediction_result"][i]
        # the frequency array
        each_one["fre"] = prediction_array["fre_array"][i]
        # word_dic_temp, the sample word lsit of kmeans
        each_one["word_dic_temp"] = prediction_array["word_dic_temp"]
        # each one is a dictionary which contain average of each aspect of one review
        # add the result in  corresponding cluster number
        restuarant[each_one["cluster_number"]].append(difference_center_fre(each_one).copy())
    # loop the each cluster of restuarant
    for cluster in restuarant:
        # for each cluster
        # define sum and average
        sum_cluster = 0
        average_key = {}
        # loop each aspect
        for key in dict_related_word:
            # sum of each key and average = 0
            sum_key = 0
            average = 0
            # check if that custer didn't contain any thing
            if len(cluster) != 0:
                # loop review in the cluster
                for review in cluster:
                    # add the value
                    sum_key += review[key + " avg"]
                # find the average by divide the size
                average = sum_key/len(cluster)
                # and save the average
                average_key[key] = average
        # save the result
        restuarant_avg.append(average_key.copy())
    # loop the average array
    for i in range(len(restuarant_avg)):
        # the dictionary for each aspect
        threshold_key = {}
        # make sure it is not empty
        if len(restuarant_avg[i]) != 0:
            # loop aspect
            for key in dict_related_word:
                # multpy to corresponding average of center to grab the threshod
                threshold_key[key] = restuarant_avg[i][key] * avg_cluster_array[i][key]
        # add the array
        restaurant_threshold.append(threshold_key.copy())
    # result
    result = {}
    # loop each restuarant
    for i in range(len(restuarant)):
        # loop aspects
        for key in dict_related_word:
            # define sum of each key, count and average
            sum_key = 0
            count = 0
            average = 0
            # check if it is not empty
            if len(restaurant_threshold[i]) != 0:
                # for each result of restuarant from the fucntion difference_center_fre
                for review in restuarant[i]:
                    # check if it pass the threshod
                    if review[key + " difference"] <= restaurant_threshold[i][key]:
                        # increase the count
                        count += 1
                        # add the corresponding score
                        sum_key += prediction_array["score_array"]["review_score"][review["index_review"]]
                    # make sure the count is not 0
                    if count != 0:
                        # get the average
                        average = sum_key/count
                    # else mean the aspect is not avilable to this restuarant
                    else:
                        # average = -1
                        average = -1
                # save the average
                result[key] = average
    # save the name
    result["name"] = prediction_array["name"]
    # return
    return result

# input array of all restuarant, kmeans object, word_dic_temp, array of each score of each restuarant
# output no, it is modify the input
def add_information(all_reviews,kmeans,word_dic_temp,each_score):
    # loop each restuarant
    for i in range(len(all_reviews)):
        # add the information, kemans
        all_reviews[i].append(kmeans)
        # word_dic_temp
        all_reviews[i].append(word_dic_temp)
        # score of the restuarant
        all_reviews[i].append(each_score[i])

# pallel running
# input the array of all restuarant with all information
# output the array of aspects of each restuarant
def get_all_aspect(restuarants):
    # 31 threshod
    with Pool(31) as p:
        # map the function with input
        result_all = p.map(check_center_value, restuarants)
        # stops
        p.terminate()
        # merge
        p.join()
    # return result
    return result_all


f_reviews = open('all_reviews/file_name30.txt','r',encoding='windows-1252')
# all review in one string
all_review = f_reviews.read().splitlines()
f_reviews.close()
txt = [["name0",["I am good","I love the food"],"url"],["name1",["I am good","I love the food"],"url"]]
# main function to call
# input a array of all restuarant
# output: output the array of aspects of each restuarant
def run(restuarants):
    # define and train the kmean
    kmeans, word_dic_temp = main()
    # calculate the score for each review of all restuarant
    each_score = get_each_scores(restuarants)
    # add information to inpunt
    add_information(restuarants,kmeans,word_dic_temp,each_score)
    #print(txt[0][5])
    #print(txt[1][5])
    # call the parallel of all prediction to get the label and center for each review
    prediction_array = all_prediction(restuarants)
    # call the paralle to get the all aspects
    result = get_all_aspect(prediction_array)
    # result
    return result
test = run(txt)
print(test)
