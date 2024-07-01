from flask import *

app = Flask(__name__)
import pymongo
uri = "mongodb+srv://Kabilan:nalibak@bibloconnect.64evmae.mongodb.net/?retryWrites=true&w=majority&appName=BIBLOCONNECT"
client=pymongo.MongoClient(uri)
db=client['Biblo-Connect']
#@app.route("/")
#def landing():
    #return render_template("landing_page.html")
@app.route("/")
def account():
    return render_template("login-page.html")
@app.route("/login")
def login():
    return render_template("login.html")
@app.route("/signup")
def signup():
    return render_template("signup.html")
@app.route("/create",methods=['post'])
def create():
    log=db['login']
    cred={}
    username=request.form['username']
    email=request.form['email']
    password=request.form['pwd']
    dob=request.form['birthday']
    print(username,dob)
    cred['email']=email
    cred['passw']=password
    log.insert_one(cred)
    return render_template("signup.html")
@app.route("/check",methods=['post'])
def check():
    email=request.form['email']
    password=request.form['pwd']
    log=db['login']
    mail_id=log.find_one({'email':email})
    print(mail_id)
    if mail_id:
        if mail_id['passw']==password:
            return render_template("home.html")
        else:
            return render_template("login.html")

    else:
        return render_template("login.html")
@app.route("/home")
def home():
    return render_template("home.html")
@app.route("/bookmark")
def bookmark():
    return render_template("bookmark.html")
@app.route("/search")
def search():
    return render_template("search.html")
@app.route("/feed")
def feed():
    return render_template("feed-from-search.html")
@app.route("/profile")
def profile():
    return render_template("profile.html")
@app.route("/editprofile")
def editprofile():
    return render_template("edit-profile.html")
@app.route("/lending")
def lending():
    return render_template("lending.html")
@app.route("/message")
def message():
    return render_template("message.html")
@app.route("/chat")
def chat():
    return render_template("message-1.html")
if __name__ == "__main__":
    app.run(debug=True)