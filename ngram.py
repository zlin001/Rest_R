from nltk import ngrams
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
sentence = "If you're looking to satisfy your craving for kebabs, but also feel like being a cheapo, this is the place for you!For about 10 bucks (or less!), you can get a super hearty meal with any protein of your choice, or you can even mix it up. I got the lamb kebab and beef kofta platter ($10), which comes with a total of 2 skewers of meat, a lot of brown rice, and a salad on the side. The lamb was super tender and delicious, and the beef was just as delicious! The food was certainly plentiful and left me more than satisfied. Definitely got the most bang for my buck!The place is far from fancy, and is more like an Afghan fast food joint where they have a variety of options besides kebabs such as cheeseburgers, wings, fries, etc. There's also a small parking lot right in front of the restaurant (enough for 5-6 cars).CASH ONLY!"

stop_words = set(stopwords.words('english'))
word_tokens = word_tokenize(sentence)
filtered_sentence = [w for w in word_tokens if not w in stop_words]
print(len(sentence))
print(len(filtered_sentence))
stopword_from_file = []
with open('StopWordList.txt', 'r') as f_stopword:
    all_stopwords = f_stopword.read().splitlines()
    for stopword in all_stopwords:
        stopword_from_file.append(stopword)
filtered_sentence_file = [w for w in word_tokens if not w in stopword_from_file]
print(len(filtered_sentence_file))
n = 2
sixgrams = ngrams(filtered_sentence, n)
#for grams in sixgrams:
  #print(grams)
