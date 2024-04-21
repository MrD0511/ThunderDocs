from app import app,db,User,login_user,logout_user,current_user,Files,login_required
from flask import render_template,redirect,request,url_for,jsonify,send_file
import uuid as uuid
from firebase_admin import credentials, initialize_app, storage


cred = credentials.Certificate("C:/Users/DELL/Documents/ThunderDocs/important/thunderdocs-52311-d7e8d2d32861.json")

initialize_app(cred, {'storageBucket': 'thunderdocs-52311.appspot.com'})

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

@app.route('/about',methods=['GET'])
def about():
    return render_template('about_us.html')

@app.route('/')
@app.route('/home')
@login_required
def index():
    if current_user.is_authenticated==False:
        return redirect(url_for('login'))
    files=Files.query.filter_by(user_id=current_user.id).all()
    if files:
        return render_template('home.html',files=files)
    return render_template('home.html')

@app.route('/upload',methods=['POST'])
def upload():
    if request.method=='POST':
        file=request.files['file']
        file_type=request.form['fileType']
        file_name=str(uuid.uuid1())+file.filename
        user_id=current_user.id
        file_path="C:/Users/DELL/Documents/ThunderDocs/static/files/"+file_name
        file.save(file_path)
        file=Files(
            file_name=file_name,
            file_path = file_path,
            user_id=user_id,
            file_type=file_type
        )
        db.session.add(file)
        db.session.commit()
        return jsonify({"message":"File uploaded successfully"})

@app.route('/download/<id>')
def downloadFile(id):
    file=Files.query.filter_by(id=id).first()
    if file:
        return send_file(file.file_path,as_attachment=True)
    return jsonify({"message":"File not found"})

@app.route('/file/preview/<file_id>')
@login_required
def preview(file_id):
    file=Files.query.filter_by(id=file_id).first()
    if file:
        return render_template('preview.html',id=file.id,file_name=file.file_name,file_path=file.file_path,file_type=file.file_type)
    return jsonify({"message":"File not found"})
