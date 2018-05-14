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
    different_key = {}
    for key in dict_related_word:
        different_key[key] = []
        count = 0.0
        sum = 0.0
        for i in range(len(each["center"])):
            if find_word(i,each["word_dic_temp"]) in dict_related_word[key]:
                count += 1
                difference = each["center"][i] - each["fre"][i]
                if difference < 0:
                    sum += 0.0
                    different_key[key].append[0.0]
                elif difference == 0:
                    if each["center"][i] > 0:
                        sum += 0.0
                        different_key[key].append[0.0]
                    else:
                        sum += 1.0
                        different_key[key].append[1.0]
                else:
                    sum += difference/each["center"][i]
        result[key + " different_array"] = different_key
        result[key + " avg"] = sum/count
    return result
def average_cluster(array):
    dict_related_word = load_related_words()
    result = {}
    for key in dict_related_word:
        result[key] = 0
        count = 0.0
        for i in range(len(array)):
            if find_word(i,each["word_dic_temp"]) in dict_related_word[key]:
                result[key] += array[i]
                count += 1
        result[key] = result[key]/count
    return result
def check_center_value(prediction_array):
    dict_related_word = load_related_words()
    center_fre = []
    each_one = {}
    avg_aspect = {}
    index_array = {}
    result = {}
    restuarant = []
    avg_center = []
    different_center_data = []
    avg_center_data = []
    avg_data = []
    for i in range(len(prediction_array["cluster_centers"])):
        avg_center.append(prediction_array["cluster_centers"][i])
    for i in range(6):
        different_center_data[i] = []
        avg_data[i] = 0
    for i in range(len(prediction_array["prediction_array"])):
        each_one["index_review"] = i
        each_one["center"] = prediction_array["cluster_centers"][i]
        each_one["fre"] = prediction_array["fre_array"][i]
        each_one["word_dic_temp"] = prediction_array["word_dic_temp"]
        avg_per_review = difference_center_fre(each_one)
        for key in dict_related_word:
            different_center_data[prediction_array["prediction_array"][i]].append(avg_per_review)
    for i in range(len(different_center_data)):
        aver_key = {}
        for key in dict_related_word:
            sum = 0
            for x in different_center_data[i]:
                sum += x[key + " avg"]
            aver_key[key] = sum/len(x[key + " avg"])
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
def run():
    kmeans, word_dic_temp = main()
    txt = [["name0",["I am good","I hate the food"],"url",kmeans,word_dic_temp],["name1",["I am good","I love the food"],"url",kmeans,word_dic_temp]]
    each_score = get_each_scores(txt)
    add_score_array(txt,each_score)
    #print(txt[0][5])
    #print(txt[1][5])
    prediction_array = all_prediction(txt)
    result = get_all_aspect(prediction_array)
    return result
test = run()
print(test)
