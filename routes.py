from flask import Flask, render_template, request
from operator import itemgetter
from Package.closest_30_rests import find_all_rests # choose 30 restaurants from yelp based on zip code and import their info and url
from Package.pool_review_scraper import get_all_reviews #all reviews from the 30 restaurants
from Package.positive_negative_v2 import get_all_scores #import recalculated overall scores of the restaurants
from Package.get_rest_info import get_all_rest_info #get all available found restaurant info

app = Flask(__name__)

#home page
@app.route('/')
def home():
    return render_template('home.html')

#direct to restaurant ranking page
@app.route('/top_ten_rests', methods=["GET",'POST'])
def top_ten_rests():
    zip_code = request.form.get("zip_code") #catch zipcode
    all_restaurant_urls = find_all_rests(str(zip_code)) #catch restaurant link
    all_reviews = get_all_reviews(all_restaurant_urls) #catch reviews for restaurants
    # print(all_reviews)
    all_scores = get_all_scores(all_reviews) #catch calculated scores of restaurantt
    all_scores_with_info = get_all_rest_info(all_scores)#catch other restaurant info

	#sort score and put it in desc order and limit it to top 10 restaurant
    sorted_scores = sorted(all_scores_with_info, key=itemgetter('total_score'), reverse=True)
    # print(all_scores_with_info)
    top_10 = []
    count = 0
    for rest in sorted_scores:
        if count < 10:
            top_10.append(rest)
            print(rest["url"])
        count = count + 1

    return render_template("top_ten_rests.html", top_restaraunts=top_10, zip_code=zip_code)

#direct to yelp page for further restaurant_info
@app.route('/restaurant/<restaurant_info>')
def restaurant(restaurant_info):
    print(type(restaurant_info))
    return render_template("restaurant.html", restaurant_info=restaurant_info)


if __name__ == '__main__':
	app.run(debug=True)
