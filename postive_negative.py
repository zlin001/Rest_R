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
# this arary to contain the word token for each review
array_word_tokens = []
# token all the reviews, and put them in to array_word_tokens
for review in reviews:
    word_tokens = word_tokenize(review)
    array_word_tokens.append(word_tokens.copy())

# function: collecting the score for each review (postive and negative)
def scan_popularity(array_words,f_name):
    # based on the input, collect the score for positive of negative
    f_popularity = open(f_name,'r',encoding='windows-1252')
    # spit the review
    popularity_words = f_popularity.read().splitlines()
    f_popularity.close()
    # score of popularity
    score = 0
    # score of inverted popularity
    inv_score = 0
    # loop the array
    for i in range(len(array_words)):
        # if the word in the corresponding file of popularity
        if array_words[i] in popularity_words:
            # check if the word before it is match of inverted rule
            if array_words[i-1] == "not" or array_words[i-1] == "no":
                # if it is we add the inv_score
                inv_score = inv_score + 1
            # else
            else:
                # adding the score by 1
                score = score + 1
            #print(word)
    return score, inv_score
# this function does calculation of score
def scoring_one(p_score,n_score,p_invi,n_invi):
    # total positive score = positve score plus inverted negative words
    p_total = p_score + n_invi
    # total negative score = negative score plus inverted postive words
    n_total = n_score + p_invi
    # take the ratios of them
    score = p_total  / (p_total + n_total)
    # the output is our score of each review
    return score
# this is function collect score of all reivews and return a score for this restuarant
def scoring_all(score_array):
    # the result
    sum = 0
    # loop the score arrey and add them
    for i in range(len(score_array)):
        sum += score_array[i]
        #return the result by taking average
    return sum/len(score_array)
#this is main function. Input the array word tokens and return score of each array and a final score
def score_reviews(array_word_tokens):
    # a container to contain the score
    score_container = []
    #we loop them
    for i in range(len(array_word_tokens)):
        # call the positve popularity function
        p_score, p_invi = scan_popularity(array_word_tokens[i],"positive_words.txt")
        # call the negative popularity function
        n_score, n_invi = scan_popularity(array_word_tokens[i],"negative_words.txt")
        # add result to container.
        score_container.append(scoring_one(p_score,n_score,p_invi,n_invi))
    # return the final score and the container that contained score of each review
    return score_container, scoring_all(score_container)

# called
score_container, all_score = score_reviews(array_word_tokens)
# the container of score of each reviews
print(score_container)
# the final score of this restuarant
print(all_score)
