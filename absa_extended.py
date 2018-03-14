from aylienapiclient import textapi

client = textapi.Client(" 51c406ea", " 06f281d46fe40eac69fcbd4170ca9b33")

# input: array with index will be 1 string review
# output: dictionary
# [{Review: "...", Sentiment: "0 or 1", confidence: ".54"}, {...}, ...]

all_sentiments = []

with open('reviews_clean.txt', 'rb') as f_reviews:
    all_reviews = f_reviews.read().splitlines()
    for review in all_reviews:
        indiv_sentiment = []
        try:
            absa = client.AspectBasedSentiment({'domain': 'restaurants', 'text': review })
            for aspect in absa['aspects']:
                indiv_sentiment.append(aspect)
            all_sentiments.append(indiv_sentiment)
        except:
            print(type(review))

for sentiment in all_sentiments:
    print(sentiment)
    print("\n")
    print("\n")
