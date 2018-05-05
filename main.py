name = "restuarant"
final_score_container = {}
review_score_container = {}

with open("reviews_score.txt",'r',encoding='windows-1252') as f_reviews_score, open("final_score.txt",'r',encoding='windows-1252') as f_final_score:
    review_scores = f_reviews_score.read().splitlines()
    final_scores = f_final_score.read().splitlines()
    for i in range(31):
        final_score_container[name + str(i)] = final_scores[i]
        review_score_container[name + str(i)] = review_scores[i]

print(final_score_container)
print(review_score_container)
