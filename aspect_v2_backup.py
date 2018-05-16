import ast
from dict_k_mean import main
from dict_k_mean import prediction
from multiprocessing import Pool
from dict_k_mean import mofi_to_index
from positive_negative_v2 import get_each_scores
from dict_k_mean import all_prediction
def load_related_words():
    f = open("all_reviews/aspect.txt",'r',encoding="windows-1252")
    summary = f.read()
    f.close()
    dict_related_word = ast.literal_eval(summary)
    for key in dict_related_word:
        dict_related_word[key] = dict_related_word[key].split(" ")
    return dict_related_word
#print("potato" in load_related_words()["food"])
# print(len(prediction(txt[0])["kmean_centers"]))
# print(len(prediction(txt[0])["fre_array"]))

def find_word(i,word_dic_temp):
    for key in word_dic_temp:
        if i == word_dic_temp[key]:
            return key
def difference_center_fre(each):
    dict_related_word = load_related_words()
    result = {}
    result["index_review"] = each["index_review"]
    result["cluster_number"] = each["cluster_number"]
    different_key = {}
    for key in dict_related_word:
        #different_key[key] = []
        count = 0.0
        sum = 0.0
        sum_difference = 0.0
        for i in range(len(each["center"])):
            if find_word(i,each["word_dic_temp"]) in dict_related_word[key]:
                count += 1
                if each["center"][i] < 0:
                    each["center"][i] = 0
                difference = each["center"][i] - each["fre"][i]
                sum_difference += difference
                if difference < 0:
                    sum += 0.0
                    #different_key[key].append[0.0]
                elif difference == 0:
                    if each["fre"][i] > 0:
                        sum += 0.0
                        #different_key[key].append[0.0]
                    else:
                        count -= 1
                        #different_key[key].append[1.0]
                else:
                    sum += difference/each["center"][i]
        #result[key + " different_array"] = different_key
        # this is average of one review on five aspect
        if count == 0:
            result[key + " avg"] = 0
        else:
            result[key + " difference"] = sum_difference/count
            result[key + " avg"] = sum/count
    return result
def average_cluster(array,word_dic_temp):
    dict_related_word = load_related_words()
    result = {}
    for key in dict_related_word:
        result[key] = 0
        count = 0.0
        for i in range(len(array)):
            if find_word(i,word_dic_temp) in dict_related_word[key]:
                if result[key] < 0:
                    result[key] += 0
                else:
                    result[key] += array[i]
                count += 1
        result[key] = result[key]/count
    return result

def check_center_value(prediction_array):
    dict_related_word = load_related_words()
    # this contain a dictionary of average for each cluster of each aspect
    avg_cluster_array = []
    # this contain array of different cluster of correspon average review of each aspect
    restuarant = []
    restuarant_avg = []
    restaurant_threshold = []
    each_one = {}
    for i in range(len(prediction_array["cluster_centers"])):
        avg_cluster_array.append(average_cluster(prediction_array["cluster_centers"][i], prediction_array["word_dic_temp"]).copy())
        restuarant.append([])
    for i in range(len(prediction_array["kmean_centers"])):
        each_one["index_review"] = i
        # each_one["center"] is an array of corresponding center
        each_one["center"] = prediction_array["kmean_centers"][i]
        each_one["cluster_number"] = prediction_array["prediction_result"][i]
        each_one["fre"] = prediction_array["fre_array"][i]
        each_one["word_dic_temp"] = prediction_array["word_dic_temp"]
        # each one is a dictionary which contain average of each aspect of one review
        restuarant[each_one["cluster_number"]].append(difference_center_fre(each_one).copy())
    for cluster in restuarant:
        # for each cluster
        sum_cluster = 0
        average_key = {}
        for key in dict_related_word:
            sum_key = 0
            average = 0
            if len(cluster) != 0:
                for review in cluster:
                    sum_key += review[key + " avg"]
                average = sum_key/len(cluster)
                average_key[key] = average
        restuarant_avg.append(average_key.copy())
    for i in range(len(restuarant_avg)):
        threshold_key = {}
        if len(restuarant_avg[i]) != 0:
            for key in dict_related_word:
                threshold_key[key] = restuarant_avg[i][key] * avg_cluster_array[i][key]
        restaurant_threshold.append(threshold_key.copy())
    result = {}
    for i in range(len(restuarant)):
        for key in dict_related_word:
            sum_key = 0
            count = 0
            average = 0
            if len(restaurant_threshold[i]) != 0:
                for review in restuarant[i]:
                    if review[key + " difference"] <= restaurant_threshold[i][key]:
                        count += 1
                        sum_key += prediction_array["score_array"]["review_score"][review["index_review"]]
                    if count != 0:
                        average = sum_key/count
                    else:
                        average = -1
                result[key] = average
    return result

def add_score_array(all_reviews,each_score):
    for i in range(len(all_reviews)):
        all_reviews[i].append(each_score[i])

def get_all_aspect(restuarants):
    with Pool(31) as p:
        result_all = p.map(check_center_value, restuarants)
        p.terminate()
        p.join()
    return result_all

f_reviews = open('all_reviews/file_name30.txt','r',encoding='windows-1252')
# all review in one string
all_review = f_reviews.read().splitlines()
f_reviews.close()
def run():
    kmeans, word_dic_temp = main()
    each_score = get_each_scores(txt)
    add_score_array(txt,each_score)
    txt = [["name0",all_review,"url",kmeans,word_dic_temp],["name1",["I am good","I love the food"],"url",kmeans,word_dic_temp]]
    #print(txt[0][5])
    #print(txt[1][5])
    prediction_array = all_prediction(txt)
    result = get_all_aspect(prediction_array)
    return result
test = run()
print(test)
