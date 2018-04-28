from nltk import ngrams
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from sklearn.cluster import KMeans
"""Citation:Minqing Hu and Bing Liu. "Mining and Summarizing Customer Reviews."
;       Proceedings of the ACM SIGKDD International Conference on Knowledge
;       Discovery and Data Mining (KDD-2004), Aug 22-25, 2004, Seattle,
;       Washington, USA,
"""
# getting all reviews
f_reviews = open('Package/reviews_clean.txt','r',encoding='windows-1252')
# spit the review
reviews = f_reviews.read().splitlines()
f_reviews.close()

array_word_tokens = []
for review in reviews:
    word_tokens = word_tokenize(review)
    array_word_tokens.append(word_tokens.copy())

def scan_popularity(array_words,f_name):
    f_popularity = open(f_name,'r',encoding='windows-1252')
    # spit the review
    popularity_words = f_popularity.read().splitlines()
    f_popularity.close()
    score = 0
    for word in array_words:
        if word in popularity_words:
            score = score + 1
            #print(word)
    return score
def scoring_one(p_score,n_score):
    score = p_score / (p_score + n_score)
    return score
def scoring_all(score_array):
    sum = 0
    for i in range(len(score_array)):
        sum += score_array[i]
    return sum/len(score_array)
def score_reviews(array_word_tokens):
    score_container = []
    for i in range(len(array_word_tokens)):
        p_score = scan_popularity(array_word_tokens[i],"positive_words.txt")
        n_score = scan_popularity(array_word_tokens[i],"negative_words.txt")
        score_container.append(scoring_one(p_score,n_score))
    return score_container, scoring_all(score_container)

score_container, all_score = score_reviews(array_word_tokens)
print(score_container)
print(all_score)
