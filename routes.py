from flask import Flask, render_template, request
from closest_30_rests import find_all_rests
app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/top_ten_rests', methods=["GET",'POST'])
def top_ten_rests():
    zip_code = request.form.get("zip_code")
    all_restaurant_urls = find_all_rests(str(zip_code))
    return render_template("top_ten_rests.html", top10=all_restaurant_urls)

@app.route('/restaurant')
def restaurant(restaurant_info):

    return render_template("restaurant.html", restaurant_info=restaurant_info)





if __name__ == '__main__':
	app.run(debug=True)
