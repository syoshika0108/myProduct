from flask import render_template, redirect, Flask, request
import pyrebase
import json
import os
import math

from constant import *
import input, calc

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)
sign_err_f = False
user_name = "guest"

with open("./instance/firebaseConfig.json") as firebaseConfigJson:
    firebaseConfig = json.loads(firebaseConfigJson.read())
firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()


def ft_sign_in(email, passwd):
	sign_err_f = False
	try:
		user = auth.sign_in_with_email_and_password(email, passwd)
		user_name = user["email"]
	except:
		user_name = "user name not found."
		sign_err_f = True
	return user_name, sign_err_f

def ft_sign_up(email, passwd):
	sign_err_f = False
	try:
		user = auth.create_user_with_email_and_password(email, passwd)
		user_name = user["email"]
	except:
		user_name = "cannot create"
		sign_err_f = True
	return user_name, sign_err_f

@app.route("/")
@app.route("/index")
def ft_welcome_path():
	return render_template("welcome.html", msg = "success!!!")

@app.route("/select_sign_in", methods = ["GET", "POST"])
def ft_select_sign_in_path():
	global user_name
	if request.method == "GET":
		return render_template("select.html", user_name = user_name, guest_f = True)
	elif request.method == "POST":
		input_email = request.form.get("input_email")
		input_password = request.form.get("input_password")
		user_name, sign_err_f = ft_sign_in(input_email, input_password)
		if sign_err_f:
			return render_template("sign_in.html", error_f = True)
		return render_template("select.html", user_name = user_name, success_f = True)

@app.route("/select_sign_up", methods = ["GET", "POST"])
def ft_select_sign_up_path():
	global user_name
	if request.method == "GET":
		return render_template("select.html", user_name = user_name)
	elif request.method == "POST":
		input_email = request.form.get("input_email")
		input_password = request.form.get("input_password")
		user_name, sign_err_f = ft_sign_up(input_email, input_password)
		if sign_err_f:
			return render_template("sign_up.html", error_f = True)
		return render_template("select.html", user_name = user_name, success_f = True)

@app.route("/calc_word", methods = ["GET", "POST"])
def ft_calc_word_path():
	if request.method == "GET":
		return render_template("word2vec.html")
	elif request.method == "POST":
		input_pos_str = request.form.get("input_pos_str")
		input_neg_str = request.form.get("input_neg_str")
		input_err_f, pos_str, neg_str = input.ft_input_word(input_pos_str, input_neg_str)
		if input_err_f:
			err_msg = "無効な入力です"
			return render_template("word2vec.html", err_msg = err_msg)
		l_name, l_prob, err_f = calc.ft_calc_word(pos_str, neg_str)
		if err_f:
			err_msg = "キーワードが見つかりませんでした。"
			return render_template("word2vec.html", err_msg = err_msg)
		return render_template("word2vec.html", l_name = l_name, l_prob = l_prob, input_pos_str = input_pos_str, input_neg_str = input_neg_str)

@app.route("/calc_doc", methods = ["GET", "POST"])
def ft_calc_doc_path():
	if request.method == "GET":
		return render_template("doc2vec.html")
	elif request.method == "POST":
		input_str = request.form.get("input_str")
		input_err_f, str = input.ft_input_doc(input_str)
		if input_err_f:
			err_msg = "入力が正しくありません"
			return render_template("doc2vec.html", err_msg = err_msg)
		ans, prob = calc.ft_calc_doc(str)
		prob = math.floor(100 * prob)
		return render_template("doc2vec.html", ans = ans, prob = prob)

@app.route("/word2vec", methods = ["GET", "POST"])
def ft_word2vec_path():
	if request.method == "GET":
		return render_template("word2vec.html")


@app.route("/doc2vec", methods = ["GET", "POST"])
def ft_doc2vec_path():
	if request.method == "GET":
		return render_template("doc2vec.html")

@app.route("/sign_in")
def ft_sign_in_path():
	global sign_err_f
	if sign_err_f:
		return render_template("sign_in.html", error_msg = ERROR_MSG_EMAIL_PASSWD)
	return render_template("sign_in.html")

@app.route("/sign_up")
def ft_sign_up_path():
	global sign_err_f
	if sign_err_f:
		return render_template("sign_up.html", error_msg = ERROR_MSG_EMAIL_PASSWD)
	return render_template("sign_up.html")

@app.route("/inquire")
def ft_inquire_path():
	return render_template("inquire.html")

@app.errorhandler(404)
def page_not_found(error):
    return render_template('error404.html', error = error), 404

if __name__ == MAIN:
	app.run(debug=True)
