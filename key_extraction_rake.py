from rake_nltk import Rake
stoppath = "SmartStoplist.txt"
rake = Rake()
with open('reviews.txt', 'r') as f_reviews, open('keywords.txt', 'w') as f_keywords:
    reviews = f_reviews.read()
    rake.extract_keywords_from_text(reviews)
    result = rake.get_ranked_phrases_with_scores()
    print()
    for i in range(len(result)):
        for b in range(len(result[i])):
            f_keywords.write(str(result[i][b]))
            f_keywords.write(" ")
        f_keywords.write("\n")
