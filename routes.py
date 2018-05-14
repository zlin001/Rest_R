from flask import Flask, render_template, request
from closest_30_rests import find_all_rests
from all_reviews.pool_review_scraper import get_all_reviews
from positive_negative_v2 import get_all_scores
from get_rest_info import get_all_rest_info
app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/top_ten_rests', methods=["GET",'POST'])
def top_ten_rests():
    zip_code = request.form.get("zip_code")
    all_restaurant_urls = find_all_rests(str(zip_code))
    all_reviews = get_all_reviews(all_restaurant_urls)
    # print(all_reviews)
    all_scores = get_all_scores(all_reviews)
    all_scores_with_info = get_all_rest_info(all_scores)
    print(all_scores_with_info)

    top_10 = [{"rank": 1, "name": "Aria", "phone": 6461235344,"total_score": 3.3, "categories": {"taste": 3, "decor": 5, "style": 1.3}, "address": "135-34 booth memorial ave flushing ny 11355"}, {"rank": 1, "name": "Aria", "phone": 6461235344, "categories": {"taste": 3, "decor": 5, "style": 1.3}, "address": "135-34 booth memorial ave flushing ny 11355"}, {"rank": 1, "name": "Aria", "phone": 6461235344, "categories": {"taste": 3, "decor": 5, "style": 1.3}, "address": "135-34 booth memorial ave flushing ny 11355"}]
    return render_template("top_ten_rests.html", top_restaraunts=all_scores_with_info, zip_code=zip_code)

@app.route('/restaurant/<restaurant_info>')
def restaurant(restaurant_info):
    print(type(restaurant_info))
    return render_template("restaurant.html", restaurant_info=restaurant_info)


if __name__ == '__main__':
	app.run(debug=True)
