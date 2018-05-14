from postive_negative_v2 import get_all_scores
from dict_k_mean import main
from dict_k_mean import prediction
# txt = [["name",["you are good","food is bad"]],["name",["you are good","food is bad"]]]
# print(get_all_scores(txt))

kmeans, word_dic_temp = main()
print(kmeans.cluster_centers_[0])
