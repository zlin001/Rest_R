with open('reviews_clean.txt', 'r') as f_reviews:
    lines = f_reviews.read().splitlines()
    for line in lines:
        print(line + '\n' + '\n')
