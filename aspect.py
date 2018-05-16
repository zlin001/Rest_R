import ast
from dict_k_mean import main
from dict_k_mean import prediction
from multiprocessing import Pool
from dict_k_mean import mofi_to_index
from Package.positive_negative_v2 import get_each_scores
from dict_k_mean import all_prediction
from Package.pool_review_scraper import get_all_reviews

# this is the first type of calculation: filter based on the average of all the review split by aspect

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
    # save the index of review
    result["index_review"] = each["index_review"]
    # look the related words
    for key in dict_related_word:
        # count and sum = 0
        count = 0.0
        sum = 0.0
        # look the length of review
        for i in range(len(each["center"])):
            # check if the word in the related list of asecpt
            if find_word(i,each["word_dic_temp"]) in dict_related_word[key]:
                # yes, add count by 1s
                count += 1
                # take the difference of frequency
                difference = each["center"][i] - each["fre"][i]
                # if difference less 0, mean data is higher than center, which is good
                if difference < 0:
                    # this mean the distance is 0
                    sum += 0.0
                # if difference is 0
                elif difference == 0:
                    # if data is not zero
                    if each["fre"][i] > 0:
                        # mean data and center is the same
                        sum += 0.0
                    # else they both are zero
                    else:
                        # we don't count that
                        count -= 1
                # all other case
                else:
                    # difference divedes the center which we know the ratios of distance between them
                    sum += difference/each["center"][i]
        #result[key + " sum"] = sum
        #result[key + " count"] = count
        # make a sure that count is not = 0
        if count == 0:
            result[key + " avg"] = 0
        else:
            # save on result
            result[key + " avg"] = sum/count
    # output
    return result

# input a dictionary of name, review, url, kmean, word_dic_temp, score of each review
# out: a dictionary of score with each aspect
def check_center_value(prediction_array):
    # load related work
    dict_related_word = load_related_words()
    # define the variable that i needed
    center_fre = []
    each_one = {}
    avg_aspect = {}
    index_array = {}
    result = {}
    restuarant = []
    # loop the lenght of reviews
    for i in range(len(prediction_array["kmean_centers"])):
        # get the information need for the difference_center_fre function
        # name
        each_one["index_review"] = i
        # kmeans center to the review
        each_one["center"] = prediction_array["kmean_centers"][i]
        # the review frequency
        each_one["fre"] = prediction_array["fre_array"][i]
        # the word list of k mean
        each_one["word_dic_temp"] = prediction_array["word_dic_temp"]
        # add to array
        restuarant.append(difference_center_fre(each_one).copy())
    # this for loop compute the average of ratios of each aspect in one restuarant
    # loop each aspect
    for key in dict_related_word:
        # def inital as 0
        avg_aspect[key] = 0
        # loop the restuarant
        for review_aspect in restuarant:
            # we add the average split by aspect
            avg_aspect[key] += review_aspect[key + " avg"]
        # divide by the len of restuarant
        avg_aspect[key] = avg_aspect[key]/len(restuarant)
    # after we got the average of ratios of each aspect (that is our threshod)
    # loop each aspect
    for key in dict_related_word:
        # grab the index of which review will pass threshold
        index_array[key] = []
        # loop the review
        for review_aspect in restuarant:
            # if it is lower than threshod (mean close to center)
            if review_aspect[key + " avg"] <= avg_aspect[key]:
                # we add the index of review
                index_array[key].append(review_aspect["index_review"])
    # this will calculate the score for restuarant for each aspect
    # look the aspects
    for key in dict_related_word:
        # set result of each key = 0
        result[key] = 0
        # look index array
        for x in index_array[key]:
            # add the score based on the index
            result[key] += prediction_array["score_array"]["review_score"][x]
        # check if the size of index array based on difference aspect
        if len(index_array[key]) == 0:
            result[key] = 0
        else:
            # get the average of each aspect
            result[key] = result[key]/len(index_array[key])
    # save the name
    result["name"] = prediction_array["name"]
    # return result
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

# f_reviews = open('all_reviews/file_name30.txt','r',encoding='windows-1252')
# # all review in one string
# all_review = f_reviews.read().splitlines()
# f_reviews.close()

#txt = [["name0",all_review,"url"],["name1",["I am good","I love the food"],"url"]]
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
