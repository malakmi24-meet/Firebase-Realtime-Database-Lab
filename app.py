from flask import Flask, render_template, request, redirect, url_for, flash
from flask import session as login_session
import pyrebase

app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = 'super-secret-key'

config = {
  "apiKey": "AIzaSyAuzGOh4rg4mVOjtJbdItvZuJeIGOQyY28",
  "authDomain": "real-time-database-lab.firebaseapp.com",
  "projectId": "real-time-database-lab",
  "storageBucket": "real-time-database-lab.appspot.com",
  "messagingSenderId": "499670971901",
  "appId": "1:499670971901:web:4c52b2dd6db4d61bb85594",
  "databaseURL": "https://real-time-database-lab-default-rtdb.europe-west1.firebasedatabase.app/"
};

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
db = firebase.database()

@app.route('/', methods=['GET', 'POST'])
def signin():
    error=''
    if request.method=='POST':
        email=request.form['email']
        password=request.form['password']
        try:
            login_session['user']=auth.sign_in_with_email_and_password(email, password)
            return redirect (url_for('add_tweet'))
        except:
            error='Authentication failed'
            return render_template('signin.html')
    else:
        return render_template('signin.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    error=''
    if request.method=='POST':
        email=request.form['email']
        password=request.form['password']
        fullname=request.form['full_name']
        username=request.form['username']
        bio=request.form['bio']
        try:
            login_session['user']=auth.create_user_with_email_and_password(email, password)
            UID = login_session['user']['localId']
            user={'email':email,'password':password,'full_name':fullname,'username':username,'bio':bio}
            db.child('users').child(UID).set(user)
            return redirect (url_for('add_tweet'))
        except:
            error='Authentication failed'
            return render_template('signup.html')
    else:
        return render_template('signup.html')


@app.route('/logout')
def logout():
    login_session['user'] =None
    auth.current_user=None
    return redirect (url_for('signup'))



@app.route('/add_tweet', methods=['GET', 'POST'])
def add_tweet():
    error=''
    if request.method=='POST':

        title=request.form['title']
        text=request.form['text']
        try:
            uid=login_session['user']['localId']
            tweet={'title':title,'text':text}
            db.child('tweets').push(tweet)
            return redirect(url_for('all_tweets'))
        except:
            error='ERROR'
    return render_template('add_tweet.html', error=error)

@app.route('/all_tweets')
def all_tweets():
    tweets=db.child('tweets').get().val()
    return render_template('all_tweets.html',tweets=tweets)

if __name__ == '__main__':
    app.run(debug=True)