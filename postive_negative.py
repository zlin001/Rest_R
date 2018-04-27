from nltk import ngrams
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from sklearn.cluster import KMeans
"""Citation:Minqing Hu and Bing Liu. "Mining and Summarizing Customer Reviews."
;       Proceedings of the ACM SIGKDD International Conference on Knowledge
;       Discovery and Data Mining (KDD-2004), Aug 22-25, 2004, Seattle,
;       Washington, USA,
"""
#text = "AMAZING authentic food, great service, has a very homey/family feel to it. Definitely recommend and will definitely be coming back, with friends."
text = "What can I say about this place. The staff of the restaurant is nice and the eggplant is not bad. Apart from that, very uninspired food, lack of atmosphere and too expensive. I am a staunch vegetarian and was sorely dissapointed with the veggie options on the menu. Will be the last time I visit, I recommend others to avoid."
word_tokens = word_tokenize(text)

#print(word_tokens)

def scan_popularity(array_words,f_name):
    f_popularity = open(f_name,'r',encoding='windows-1252')
    # spit the review
    popularity_words = f_popularity.read().splitlines()
    f_popularity.close()
    score = 0
    for word in word_tokens:
        if word in popularity_words:
            print(word)
            score = score + 1
            #print(word)
    return score
positive_score = scan_popularity(word_tokens,"positive_words.txt")
negative_score = scan_popularity(word_tokens,"negative_words.txt")
print(positive_score)
print(negative_score)
