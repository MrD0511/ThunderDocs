from app import app,db,User,login_user,logout_user,current_user,Files
from flask import render_template,redirect,request,url_for,jsonify
import uuid as uuid
from firebase_admin import credentials, initialize_app, storage
cred = credentials.Certificate("C:/Users/DELL/Documents/ThunderDocs/important/thunderdocs-52311-d7e8d2d32861.json")
initialize_app(cred, {'storageBucket': 'thunderdocs-52311.appspot.com'})
from base64 import b64encode

@app.route('/register',methods=['GET','POST'])
def register():
    if request.method=='POST':
        name=request.form['name']
        email=request.form['email']
        password=request.form['password']
        conf_password=request.form['confirm-password']
        if password==conf_password:
            user=User(
                name=name,
                email=email,
                password=password,
            )
            db.session.add(user)
            db.session.commit()
            print("successfull")
            return redirect(url_for('login'))
    return render_template("registration.html")

@app.route('/login',methods=['GET','POST'])
def login():
    if request.method=="POST":
        email=request.form['email']
        password=request.form['password']
        user=User.query.filter_by(email=email).first()
        if user is not None and user.verify_password(password):
            login_user(user)
            print("logged in")
            return redirect(url_for('index'))
    return render_template("login.html")

@app.route('/logout',methods=['GET'])
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/')
@app.route('/home')
def index():
    return render_template('home.html')

@app.route('/upload',methods=['POST'])
def upload():
    if request.method=='POST':
        file=request.files['file']
        file_type=file.content_type
        user_id=current_user.id
        bucket = storage.bucket()
        blob = bucket.blob(str(uuid.uuid1())+file.filename)
        blob.upload_from_string(
            file.read(),
            content_type=file.content_type
        )
        url = blob.public_url
        file=Files(
            file_name=str(uuid.uuid1())+file.filename,
            file_path = url,
            user_id=user_id,
            file_type=file_type
        )
        db.session.add(file)
        db.session.commit()
        return jsonify({"message":"File uploaded successfully"})
