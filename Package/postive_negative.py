from nltk import ngrams
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
"""Citation:Minqing Hu and Bing Liu. "Mining and Summarizing Customer Reviews."
;       Proceedings of the ACM SIGKDD International Conference on Knowledge
;       Discovery and Data Mining (KDD-2004), Aug 22-25, 2004, Seattle,
;       Washington, USA,
"""
# function: collecting the score for each review (postive and negative)
def scan_popularity(array_words,f_name,f_inc,f_dec):
    # getting different words from folder that we need
    # postive word or negative word based on the input f_name
    f_popularity = open(f_name,'r',encoding='windows-1252')
    # spit the review
    popularity_words = f_popularity.read().splitlines()
    f_popularity.close()
    # getting inc adverb
    f_inc_abverbs = open(f_inc,'r',encoding='windows-1252')
    # get each word
    inc_abverbs = f_inc_abverbs.read().splitlines()
    f_inc_abverbs.close()
    # getting dec adverb
    f_dec_abverbs = open(f_dec,'r',encoding='windows-1252')
    # spit the words
    dec_abverbs = f_dec_abverbs.read().splitlines()
    f_dec_abverbs.close()
    # score of popularity
    score = 0
    # score of inverted popularity
    inv_score = 0
    # loop the array
    for i in range(len(array_words)):
        # if the word in the corresponding file of popularity
        if array_words[i].lower() in popularity_words:
            # check if the word before it is match of inverted rule
            if array_words[i-1] == "not" or array_words[i-1] == "no":
                # if it is we add the inv_score
                inv_score = inv_score + 1
            # else
            else:
                # if the previous word is inc abverbs, +2(1*2)
                if array_words[i-1].lower() in inc_abverbs:
                    # add 2
                    score = score + 2
                # if this preview word is dec adverbs, +0.5(1/2)
                elif array_words[i-1].lower() in dec_abverbs:
                    # add 0.5
                    score = score + 0.5
                else:
                    # else pure degree
                    # adding the score by 1
                    score = score + 1
            #print(word)
    return score, inv_score
# this function does calculation of score
def scoring_one(p_score,n_score,p_invi,n_invi):
    score = 0
    try:
        # total positive score = positve score plus inverted negative words
        p_total = p_score + n_invi
        # total negative score = negative score plus inverted postive words
        n_total = n_score + p_invi
        # take the ratios of them
        score = p_total  / (p_total + n_total)
        # the output is our score of each review
    except ZeroDivisionError:
        score = 0
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
        p_score, p_invi = scan_popularity(array_word_tokens[i],"positive_words.txt","inc_words.txt","dec_words.txt")
        # call the negative popularity function
        n_score, n_invi = scan_popularity(array_word_tokens[i],"negative_words.txt","inc_words.txt","dec_words.txt")
        # add result to container.
        score_container.append(scoring_one(p_score,n_score,p_invi,n_invi))
    # return the final score and the container that contained score of each review
    return score_container, scoring_all(score_container)

review_score_containter_all = []
final_score_container_all = []
def all_scores(i):
    f_name = "all_reviews/file_name"
    # getting all reviews
    array_word_tokens = []
    try:
        f_reviews = open(f_name + str(i) + ".txt","r",encoding="windows-1252")
        reviews = f_reviews.read().splitlines()
        f_reviews.close()
    except UnicodeDecodeError:
        f_reviews = open(f_name + str(i) + ".txt","r",encoding="utf-8")
        reviews = f_reviews.read().splitlines()
        f_reviews.close()
    for review in reviews:
        word_tokens = word_tokenize(review)
        array_word_tokens.append(word_tokens.copy())
    score_container, all_score = score_reviews(array_word_tokens)
    return score_container, all_score

with open("reviews_score.txt",'w',encoding='windows-1252') as f_reviews_score, open("final_score.txt",'w',encoding="windows-1252") as f_final_score:
    for i in range(31):
        score_container, all_score = all_scores(i)
        f_reviews_score.write(str(score_container) + "\n")
        f_final_score.write(str(all_score) + "\n")
        review_score_containter_all.append(score_container)
        final_score_container_all.append(all_score)
# print(review_score_containter_all[0])
# print(final_score_container_all[0])
