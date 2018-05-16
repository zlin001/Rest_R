from nltk import ngrams
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from multiprocessing import Pool
"""Citation:Minqing Hu and Bing Liu. "Mining and Summarizing Customer Reviews."
;       Proceedings of the ACM SIGKDD International Conference on Knowledge
;       Discovery and Data Mining (KDD-2004), Aug 22-25, 2004, Seattle,
;       Washington, USA,
"""
# function: collecting the score for each review (postive and negative)
# input: array_words: array of word, f_name: the file u want to check (positve or negative), f_inc/f_dec the file contained inc adverb/dec adverb
# output: is the score of the negative or positive based on the input file, inv_score is the score that get converted by not or no
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
# input: the score of postive, negative and inverted score from postiive and negative
# output: return the rotios of postive score to sum of postive and negative
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
# this is main function. Input the array word tokens and return score of each array and a final score
# input: array of work that tokenizeself.
# output: a array of score present each review, and one total score present this restaurant
def score_reviews(array_word_tokens):
    # a container to contain the score
    score_container = []
    sum = 0
    if len(array_word_tokens) == 0:
        return score_container, 0
    #we loop them
    for i in range(len(array_word_tokens)):
        # call the positve popularity function
        p_score, p_invi = scan_popularity(array_word_tokens[i],"positive_words.txt","inc_words.txt","dec_words.txt")
        # call the negative popularity function
        n_score, n_invi = scan_popularity(array_word_tokens[i],"negative_words.txt","inc_words.txt","dec_words.txt")
        # add result to container.
        sum += scoring_one(p_score,n_score,p_invi,n_invi)
        score_container.append(scoring_one(p_score,n_score,p_invi,n_invi))
    # return the final score and the container that contained score of each review
    return score_container, sum/len(array_word_tokens)

# review_score_containter_all = []
# final_score_container_all = []

# input: array of information of restaurant index 0 = name, 1 = array of reviews, 2 = url
# output: a dictionary contained name and the total score
def all_scores(restuarant):
    # the output
    result_all = {}
    # a array to contain all the tokenize review
    array_word_tokens = []
    # loop each review
    for review in restuarant[1]:
        # tokenize each review
        word_tokens = word_tokenize(review)
        # add to array
        array_word_tokens.append(word_tokens.copy())
    # call the score review to get the score
    score_container, all_score = score_reviews(array_word_tokens)
    #print(all_score,restuarant)
    # need to mark each total to the name of restaurant
    result_all["name"] = restuarant[0]
    # save the total score
    result_all["total_score"] = all_score
    # return result
    result_all["url"] = restuarant[2] 
    return result_all

# f_reviews = open("all_reviews/file_name30.txt","r",encoding="windows-1252")
# reviews = f_reviews.read().splitlines()
# f_reviews.close()
# text = [["abc",reviews],["god",["i am good student"]]]

# this is parallel process to reduce the time
# input is an array of containes all restaurant
# output is an array of dictionary which contained all score and name
def get_all_scores(restuarants):
    # 31 is the threshold
    with Pool(31) as p:
        # we map the function and input
        result_all = p.map(all_scores, restuarants)
        # stop
        p.terminate()
        # merge them
        p.join()
    # return result
    return result_all
# result_all = get_all_scores(text)
# print(result_all)

# input: array of information of restaurant index 0 = name, 1 = array of reviews, 2 = url
# output: a dictionary contained name and the array of score to each review
def each_scores(restuarant):
    # the output
    result_each = {}
    # array of work tokenized
    array_word_tokens = []
    # loop each review
    for review in restuarant[1]:
        # tokenize each review
        word_tokens = word_tokenize(review)
        # add them into array
        array_word_tokens.append(word_tokens.copy())
    # call the function of score review
    score_container, all_score = score_reviews(array_word_tokens)
    #print(all_score,restuarant)
    # save the name of restuarant
    result_each["name"] = restuarant[0]
    # save the array of score of each review
    result_each["review_score"] = score_container
    # return result
    return result_each

# this is same as get_all_scores, but it called the each scores
# to get the parallel process to run each scores of all restaurant
def get_each_scores(restuarants):
    with Pool(31) as p:
        result_each = p.map(each_scores, restuarants)
        p.terminate()
        p.join()
    return result_each

# result_each = get_each_scores(text)
# print(result_each)
#print(result_each)
#print(all_score)
# with open("reviews_score.txt",'w',encoding='windows-1252') as f_reviews_score, open("final_score.txt",'w',encoding="windows-1252") as f_final_score:
#     for i in range(31):
#         score_container, all_score = all_scores(i)
#         f_reviews_score.write(str(score_container) + "\n")
#         f_final_score.write(str(all_score) + "\n")
#         review_score_containter_all.append(score_container)
#         final_score_container_all.append(all_score)
# print(review_score_containter_all[0])
# print(final_score_container_all[0])
