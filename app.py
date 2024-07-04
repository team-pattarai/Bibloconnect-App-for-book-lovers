from flask import *
from PIL import Image
import gridfs
from bson import ObjectId
import io
import base64
app = Flask(__name__)
import pymongo
app.secret_key = 'bibloconnect'
uri = "mongodb+srv://Kabilan:nalibak@bibloconnect.64evmae.mongodb.net/?retryWrites=true&w=majority&appName=BIBLOCONNECT"
client=pymongo.MongoClient(uri)


db=client['Biblo-Connect']
fs=gridfs.GridFS(db,'post')
pfs=gridfs.GridFS(db,'profile_DP')
bfs=gridfs.GridFS(db,'bookmarks')
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
    cred['Init']='False'
    status=log.insert_one(cred)
    profile=db['profile']
    profile.insert_one({'username':username,'email':email,'dob':dob})
    print(status)
    return render_template("signup.html")
@app.route("/check",methods=['post'])
def check():
    email=request.form['email']
    password=request.form['pwd']
    log=db['login']
    mail_id=log.find_one({'email':email})
    print(mail_id)
    session['user_email'] = email 
    if mail_id:
        if mail_id['passw']==password:
            if mail_id["Init"]=="False":
                
                return render_template("new.html",user=email)
            return render_template("home.html")
        else:
            cred="Incorrect Credentials"
            return render_template("login.html",cred=cred)

    else:
        cred="Incorrect Credentials"
        return render_template("login.html",cred=cred)
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
    profile = db["profile"]
    user_email = session.get('user_email')
    post = db["post.files"]
    post_view=[]
    data = profile.find_one({'email': user_email})
    posts = list(post.find({'filename': user_email}))
    for i in range(len(posts)):
        post_view.append(posts[i]['_id'])
    
    name = data["username"]
    about = data["about"]
    location = f"{data['dist']}, {data['state']}, {data['country']}"
    profile_pic=db['profile_DP.files']
    try:
        pic_data=profile_pic.find_one({'filename': user_email})
        image_data = pfs.get(ObjectId(pic_data['_id']))
        image = Image.open(io.BytesIO(image_data.read()))
        if image.mode == 'RGBA':
            image = image.convert('RGB')
        
        img_io = io.BytesIO()
        image.save(img_io, format='JPEG')
        img_io.seek(0)
        img_base64 = base64.b64encode(img_io.getvalue()).decode('ascii')
        img_data = f"data:image/jpeg;base64,{img_base64}"
    except Exception as e:
        print(f"Error loading profile data or image: {e}")
        img_data=url_for('static', filename='public/ellipse-32@2x.png') 
    return render_template("profile.html", 
                           name=name,   
                           about=about, 
                           location=location, 
                           posts=post_view,
                           image=img_data)
@app.route("/getimg/<obj_id>")
def getimg(obj_id):
    try:
        fs=gridfs.GridFS(db,'post')
        print(obj_id)
        image_data = fs.get(ObjectId(obj_id))
        image = Image.open(io.BytesIO(image_data.read()))
        
        if image.mode == 'RGBA':
            image = image.convert('RGB')
        
        img_io = io.BytesIO()
        image.save(img_io, format='JPEG')

        img_io.seek(0)
        return send_file(img_io, mimetype='image/jpeg')
    except NoFile:
        print(f"File with id {obj_id} not found in GridFS")
        return "Image not found", 404
    except Exception as e:
        print(f"Error retrieving image: {str(e)}")
        return "Error retrieving image", 500

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
@app.route("/createprofile")
def createprofile ():
    return render_template("pop-up.html")
@app.route("/info",methods=['post'])
def info():
    log=db['profile']
    cred={}
    try:
        username=request.form['name']
        image=request.files['image']
        pfs.put(image,filename=session.get('user_email')) 
        cred['username']=username
    except Exception(e):
        print("except")
        print(e)    
        pass
    country=request.form['country']
    state=request.form['state']
    dist=request.form['district']
    ph=request.form['contact-number']
    about=request.form['about']
    user_email = session.get('user_email')
    cred['country']=country
    cred['state']=state
    cred['dist']=dist
    cred['ph_no']=ph
    cred['about']=about
    status=log.update_one({'email':user_email},{'$set':cred})
    logg=db['login']
    cred1={}
    cred1['Init']='True'
    if user_email:
        status1 = logg.update_one({'email': user_email}, {"$set": cred1})
    return redirect(url_for("profile"))
@app.route("/addpage")
def addpage ():
    return render_template("a-d-d-pages.html")
@app.route('/upload', methods=['POST'])
def upload():
    text = request.form['text']
    image = request.files['image']
    fs.put(image,filename=session.get('user_email'),text=text) 
    return redirect(url_for('profile'))
@app.route("/addbookmark")
def addbookmark ():
    return render_template("a-d-d-b-o-o-k-m-a-r-k.html")
@app.route('/uploadbm', methods=['POST'])
def uploadbm():
    image = request.files['image']
    bfs.put(image,filename=session.get('user_email')) 
    return render_template("home.html")
if __name__ == "__main__":
    app.run(debug=True)