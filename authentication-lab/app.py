from flask import Flask, render_template, request, redirect, url_for, flash
from flask import session as login_session
import pyrebase

firebaseConfig = {
  "apiKey": "AIzaSyCE4jciSJDWWcSJORsd8GPBS_kmRCKCcU4",
  "authDomain": "fir-lab-ecc1d.firebaseapp.com",
  "projectId": "fir-lab-ecc1d",
  "storageBucket": "fir-lab-ecc1d.appspot.com",
  "messagingSenderId": "591618864518",
  "appId": "1:591618864518:web:d961eb5e55ec8cf7bb2807",
  "measurementId": "G-KQGQTHRZYB",
  "databaseURL": "https://fir-lab-ecc1d-default-rtdb.europe-west1.firebasedatabase.app/" }

firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()
db = firebase.database()


app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = 'super-secret-key'


@app.route('/', methods=['GET', 'POST'])
def signin():
    error = ""
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
    try:
        login_session['user'] = auth.sign_in_with_email_and_password(email, password)
        return redirect(url_for('add_tweet'))
    except:
        error = "Authentication failed"
    return render_template("signin.html")


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    error = ""
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
    try:
        login_session['user'] = auth.create_user_with_email_and_password(email, password)
        user = {"email": request.form["email"], "password": request.form["password"]}
        db.child("Users").child(login.session["user"]["localID"]).set(user)
        return redirect(url_for('add_tweet'))
    except:
        error = "Authentication failed"
    return render_template("signup.html")

@app.route('/signout')
def signout():
    login_session['user'] = None
    auth.current_user = None
    return redirect(url_for('signin'))

@app.route('/add_tweet', methods=['GET', 'POST'])
def add_tweet():
    if request.method == "POST":
        request.form["title"]
        request.form["text"]
    tweet = {"title": request.form["title"], "text": request.form["text"], "uid": login_session["user"]["localId"]}
    db.child("Tweet").push(tweet)
    return render_template("add_tweet.html")

@app.route('/all_tweets')
def all_tweets():
    alltweets = db.child("Tweet").get().val()
    return render_template("tweets.html", alltweets=alltweets)


if __name__ == '__main__':
    app.run(debug=False)