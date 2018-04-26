from flask import Flask, render_template
app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/enter_zip_code', methods=["GET",'POST'])
def enter_zip_code():
    zip_code = request.form.get("zip_code")
    return render_template("top_ten_rests.html", top10=None)



if __name__ == '__main__':
	app.run(debug=True)
