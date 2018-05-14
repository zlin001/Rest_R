import ast
from dict_k_mean import main
from dict_k_mean import prediction
from multiprocessing import Pool
from dict_k_mean import mofi_to_index
from positive_negative_v2 import get_each_scores
from dict_k_mean import all_prediction
from all_reviews.pool_review_scraper import get_all_reviews

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
    for key in dict_related_word:
        count = 0.0
        sum = 0.0
        for i in range(len(each["center"])):
            if find_word(i,each["word_dic_temp"]) in dict_related_word[key]:
                count += 1
                difference = each["center"][i] - each["fre"][i]
                if difference < 0:
                    sum += 0.0
                elif difference == 0:
                    if each["center"][i] > 0:
                        sum += 0.0
                    else:
                        sum += 1.0
                else:
                    sum += difference/each["center"][i]
        #result[key + " sum"] = sum
        #result[key + " count"] = count
        result[key + " avg"] = sum/count
    return result

def check_center_value(prediction_array):
    dict_related_word = load_related_words()
    center_fre = []
    each_one = {}
    avg_aspect = {}
    index_array = {}
    result = {}
    restuarant = []
    for i in range(len(prediction_array["kmean_centers"])):
        each_one["index_review"] = i
        each_one["center"] = prediction_array["kmean_centers"][i]
        each_one["fre"] = prediction_array["fre_array"][i]
        each_one["word_dic_temp"] = prediction_array["word_dic_temp"]
        restuarant.append(difference_center_fre(each_one))
    for key in dict_related_word:
        avg_aspect[key] = 0
        for review_aspect in restuarant:
            avg_aspect[key] += review_aspect[key + " avg"]
        avg_aspect[key] = avg_aspect[key]/len(restuarant)
    for key in dict_related_word:
        index_array[key] = []
        for review_aspect in restuarant:
            if review_aspect[key + " avg"] <= avg_aspect[key]:
                index_array[key].append(review_aspect["index_review"])
    for key in dict_related_word:
        result[key] = 0
        for x in index_array[key]:
            result[key] += prediction_array["score_array"]["review_score"][x]
        if len(index_array[key]) == 0:
            result[key] = 0
        else:
            result[key] = (1 - result[key]/len(index_array[key]))
    result["name"] = prediction_array["name"]
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
    all_reviews = get_all_reviews(all_restaurant_urls)
    #txt = [["name0",["I am good","I hate the food"],"url",kmeans,word_dic_temp],["name1",["I am good","I love the food"],"url",kmeans,word_dic_temp]]
    each_score = get_each_scores(all_reviews)
    add_score_array(all_reviews,each_score)
    #print(txt[0][5])
    #print(txt[1][5])
    prediction_array = all_prediction(all_reviews)
    result = get_all_aspect(prediction_array)
    return result
test = run()
print(test)
