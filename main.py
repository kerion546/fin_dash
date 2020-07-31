from flask import (
    Flask,
    request,
    Response,
    abort,
    render_template,
    redirect,
    url_for,
    jsonify,
    session,
)
import os
import pyrebase
import json

firebase_config_json_file = 'firebaseConfig.json'

with open(firebase_config_json_file) as f:
    firebaseConfig = json.loads(f.read())
firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = '/tmp'
app.config['SECRET_KEY'] = os.urandom(24)
app.config.from_object(__name__)

@app.route('/', methods=['GET'])
def index():
    usr = session.get('usr')
    if usr == None:    
        return redirect(url_for('login'))

    return render_template("index.html")

@app.route('/index.html', methods=['GET'])
def index2():
    usr = session.get('usr')
    if usr == None:    
        return redirect(url_for('login'))

    return render_template("index.html")

@app.route('/customer.html', methods=['GET'])
def customer():
    usr = session.get('usr')
    if usr == None:    
        return redirect(url_for('login'))

    return render_template("customer.html")

@app.route('/profile.html', methods=['GET'])
def profile():
    usr = session.get('usr')
    if usr == None:    
        return redirect(url_for('login'))

    return render_template("profile.html")

@app.route('/transaction.html', methods=['GET'])
def transaction():
    usr = session.get('usr')
    if usr == None:    
        return redirect(url_for('login'))

    return render_template("transaction.html")

@app.route('/transaction_2.html', methods=['GET'])
def transaction2():
    usr = session.get('usr')
    if usr == None:    
        return redirect(url_for('login'))

    return render_template("transaction_2.html")

@app.route('/transaction_3.html', methods=['GET'])
def transaction3():
    return render_template("invoice.html")

@app.route('/login.html', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template("login.html")

    email = request.form['email']
    password = request.form['password']
    print(email)
    print(password)

    user = auth.sign_in_with_email_and_password(email, password)
    local_id = user['localId']
    user = auth.refresh(user['refreshToken'])
    user_id = user['idToken']
    session['usr'] = user_id
    print(local_id)

    return redirect(url_for('index'))

@app.route('/logout', methods=['GET'])
def logout():
    try:
        del session['usr']
    except:
        pass
    return redirect('/login.html')

@app.route("/news")
def news():
    import feedparser
    import urllib
    import json

    s = '株価'
    s_quote = urllib.parse.quote(s)
    url = "https://news.google.com/news/rss/search/section/q/" + s_quote + "/" + s_quote + "?ned=jp&amp;hl=ja&amp;gl=JP"
    d = feedparser.parse(url)

    n = []

    for ditem in d.entries:
        jd = {}
        jd['link'] = ditem.link
        jd['published'] = ditem.published
        jd['title'] = ditem.title
        n.append(jd)

    news = json.dumps(n)
    return news

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=80, debug=True)