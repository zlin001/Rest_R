name = "restuarant"
final_score_container = {}
review_score_container = {}

with open("reviews_score.txt",'r',encoding='windows-1252') as f_reviews_score, open("final_score.txt",'r',encoding='windows-1252') as f_final_score:
    review_scores = f_reviews_score.read().splitlines()
    final_scores = f_final_score.read().splitlines()
    for i in range(31):
        final_score_container[name + str(i)] = float(final_scores[i])
        #for x in review_scores:
        review_score_convt = review_scores[i][1:-1]
        review_score_convt = review_score_convt.split(',')
        for x in range(len(review_score_convt)):
            review_score_convt[x] = float(review_score_convt[x])
        review_score_container[name + str(i)] = review_score_convt

#print(final_score_container)
print(review_score_container["restuarant0"])
