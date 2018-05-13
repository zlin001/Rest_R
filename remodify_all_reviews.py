from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
f_reviews = open('all_reviews/all_reviews.txt','r',encoding='utf-8')
all_review = f_reviews.read()
all_review = all_review.lower()
f_reviews.close()
all_review = all_review.replace("."," ")
all_review = all_review.replace(","," ")
all_review = all_review.replace("/"," ")
all_review = all_review.replace(":"," ")
all_review = all_review.replace("-"," ")

f_new_reviews = open('all_reviews/all_reviews_fix.txt','w')
f_new_reviews.write(all_review)
f_new_reviews.close()

stop_words = set(stopwords.words('english'))
# string to list
word_tokens = word_tokenize(all_review)
#test = pos_tag(word_tokens)
# filter out the review
def create_frequency_dict(data):
    words_dic = {}
    for i in range(len(data)):
        if data[i] in words_dic:
            words_dic[data[i]] += 1
        else:
            words_dic[data[i]] = 1
    return words_dic


f_pronoun_conj = open("Directionary/pronouns_and_conj.txt","r")
pronoun_conj = f_pronoun_conj.read().splitlines()
f_pronoun_conj.close()
f_verb = open("Directionary/verbs/31K verbs.txt","r")
verbs = f_verb.read().splitlines()
f_verb.close()
f_adverb = open("Directionary/adverbs/6K adverbs.txt","r")
adverbs = f_adverb.read().splitlines()
f_adverb.close()
f_adj = open("Directionary/adjectives/28K adjectives.txt","r")
adjs = f_adj.read().splitlines()
f_adj.close()
filtered_review = [w for w in word_tokens if not w in stop_words]
words_dic = create_frequency_dict(filtered_review)
f_feature = open('features_words/feature_words.txt','w')
for word in words_dic:
    if word not in pronoun_conj and word not in verbs and word not in adverbs and word not in adjs:
        f_feature.write(str(word) + "\n")
f_feature.close()
