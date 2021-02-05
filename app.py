from os import environ
from flask import Flask, render_template, request, redirect, session, url_for
from dotenv import load_dotenv 
import tweepy
import tweetsplitter

load_dotenv()

app = Flask(__name__)

app.config['SECRET_KEY'] = environ['SECRET_KEY']
consumer_key = environ['CONSUMER_KEY'] # Also known as API key
consumer_secret = environ['CONSUMER_SECRET'] # Also known as API secret
callback = environ['CALLBACK']

tweets = []

@app.route("/", methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        tweet_content = request.form['tweet_content']
        tweets = tweetsplitter.tweet_splitter(tweet_content, True)
        session['tweets'] = tweets
        return render_template('index.html', tweets=tweets)
    else:
        session.pop('tweets', None)
        tweets = []
        return render_template('index.html', tweets=tweets)

@app.route("/login")
def login():
    if 'username' in session:
        return redirect(url_for('tweet'))
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret, callback)
    redirect_url = auth.get_authorization_url()
    
    session['request_token'] = auth.request_token
    return redirect(redirect_url)

@app.route("/callback")
def twitter_callback():
    request_token = session["request_token"]
    del session["request_token"]

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret, callback)
    auth.request_token = request_token
    verifier = request.args.get('oauth_verifier')
    auth.get_access_token(verifier)
    session['token'] = (auth.access_token, auth.access_token_secret)
    api = tweepy.API(auth)
    session['username'] = api.me().screen_name
    return redirect(url_for('tweet'))

@app.route("/tweet")
def tweet():
    if 'username' not in session:
        return redirect(url_for('login'))
    if 'tweets' in session:
        tweets = session['tweets']
        token, token_secret = session['token']
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret, callback)
        auth.set_access_token(token, token_secret)
        api = tweepy.API(auth)
        
        for tweet in tweets:
            api.update_status(tweet)
        
        session.pop('tweets', None)

    return redirect(url_for('index'))

@app.route('/disclaimer')
def disclaimer():
    return render_template('disclaimer.html')

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)