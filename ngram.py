from nltk import ngrams
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
review = "If you're looking to satisfy your craving for kebabs, but also feel like being a cheapo, this is the place for you!For about 10 bucks (or less!), you can get a super hearty meal with any protein of your choice, or you can even mix it up. I got the lamb kebab and beef kofta platter ($10), which comes with a total of 2 skewers of meat, a lot of brown rice, and a salad on the side. The lamb was super tender and delicious, and the beef was just as delicious! The food was certainly plentiful and left me more than satisfied. Definitely got the most bang for my buck!The place is far from fancy, and is more like an Afghan fast food joint where they have a variety of options besides kebabs such as cheeseburgers, wings, fries, etc. There's also a small parking lot right in front of the restaurant (enough for 5-6 cars).CASH ONLY!"

# load the stopword from the library of nltk
stop_words = set(stopwords.words('english'))
# string to list
word_tokens = word_tokenize(review)
# filter out the review
filtered_review = [w for w in word_tokens if not w in stop_words]
# print the size of review
#print(len(review))
# print the size of after removing stopword
#print(len(filtered_reivew))
# define a list for contain the stopword from file
stopword_from_file = []
# open the file and save the stopword into the list
with open('StopWordList.txt', 'r') as f_stopword:
    # read line by line
    all_stopwords = f_stopword.read().splitlines()
    # for loop each word
    for stopword in all_stopwords:
        # add to list
        stopword_from_file.append(stopword)
# filtering
filtered_review_file = [w for w in word_tokens if not w in stopword_from_file]
# print the size of review with removing stopword from file
#print(len(filtered_review_file))
# container of word and frequency
words_dic = {}
words_dic_bi = {}
# call the ngram function with n = 2 which represent bigrams
bigrams = ngrams(filtered_review, 2)
# loop the result from ngram function
for grams in bigrams:
    # result in string
    result = ""
    # since it is bigram, we need to loop the grams for each word
    for gram in grams:
        # we add into result which it become a complete string with two words
        result += gram + " "
    # check if it is in the container
    if result in words_dic_bi:
        # yes we add frequency
        words_dic_bi[result] += 1
    else:
        # no we set it as new index which value of frequency is 1
        words_dic_bi[result] = 1
print(words_dic_bi)
# same applied here for it is for unigram.
unigrams = ngrams(filtered_review, 1)
for grams in unigrams:
    result = ""
    result += grams[0]
    if result in words_dic:
        words_dic[result] += 1
    else:
        words_dic[result] = 1
print(words_dic)
