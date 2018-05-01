f_adverbs = open('Directionary/adverbs/6K adverbs.txt','r',encoding='windows-1252')
# spit the review
adverbs = f_adverbs.read().splitlines()
f_adverbs.close()

f_positive = open("positive_words.txt",'r',encoding='windows-1252')
# spit the review
positive_words = f_positive.read().splitlines()
f_positive.close()

f_negative = open("negative_words.txt",'r',encoding='windows-1252')
# spit the review
negative_words = f_negative.read().splitlines()
f_negative.close()

f_neutral_adverb = open("neutral_adverb.txt","w",encoding="windows-1252")
for adverb in adverbs:
    if adverb not in positive_words and adverb not in negative_words:
        f_neutral_adverb.write(adverb + "\n")
f_neutral_adverb.close()
