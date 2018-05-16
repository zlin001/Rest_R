from sklearn.feature_extraction.text import CountVectorizer
# getting all reviews
f_reviews = open('Package/reviews_clean.txt','r',encoding='windows-1252')
# spit the review
reviews = f_reviews.read().splitlines()
f_reviews.close()
message = []
for review in reviews:
    message.append(review)

corpus = [
'All my cats in a row all',
'When my cat sits down, she looks like a Furby toy!',
'The cat from outer space',
'Sunshine loves to sit like this for some reason.'
]
vectorizer = CountVectorizer()
print( vectorizer.fit_transform(message).todense() )
print( vectorizer.vocabulary_ )
