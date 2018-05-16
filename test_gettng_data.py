# a test with local run
from closest_30_rests import find_all_rests
from all_reviews.pool_review_scraper import get_all_reviews
from aspect_v2 import run
zip_code = 11355
all_restaurant_urls = find_all_rests(str(zip_code))
all_reviews = get_all_reviews(all_restaurant_urls)
#print(len(all_reviews))
result = run(all_reviews)
print(result)
