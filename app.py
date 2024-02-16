from flask import Flask, render_template, url_for, request, redirect,session, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

app=Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"

class Base(DeclarativeBase):
  pass


db = SQLAlchemy(model_class=Base)
db.init_app(app)

app.secret_key = "??nIkBQAnE9bp3@qGKj3h6i#71!h/j"

class Users(db.Model):
    role = db.Column(db.String(50),nullable=False)
    uname = db.Column(db.String(100), nullable = False)
    reg_no = db.Column(db.Integer, primary_key=True)
    password = db.Column(db.String(100),nullable=False)
    club = db.Column(db.String(100),nullable=False)
    dept = db.Column(db.String(100),nullable=False)

class Roles(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200),nullable=False, unique=True)
    

class Posts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200),nullable=False)
    posted_by = db.Column(db.String(100),nullable=False)
    date = db.Column(db.DateTime,nullable=False)
    contents = db.Column(db.String(4294000000),nullable=False)
    attachments = db.Column(db.String(4294000000))

class News(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200),nullable=False)
    posted_by = db.Column(db.String(100),nullable=False)
    date = db.Column(db.DateTime,nullable=False)
    register_by = db.Column(db.DateTime)
    contents = db.Column(db.String(4294000000),nullable=False)
    attachments = db.Column(db.String(4294000000))

with app.app_context():
    db.create_all()
    try:
        db.session.add(Users(role="Admin",uname="abc",password="123"))
        db.session.commit()
    except:
        pass


@app.route("/",methods=["GET","POST"])
@app.route("/login",methods=["GET","POST"])
def login():
     
    if not session.get("loggedin"):
        if request.method=="POST":
            uname = request.form.get("uname")
            password = request.form.get("password")
            user = Users.query.filter_by(uname = uname).first()
            # add username and password to the db

            if (user and (password == user.password)):
                session['reg_no'] = user.reg_no
                session['uname'] = user.uname
                session['role']=user.role
                session["loggedin"]=True
                session['club'] = user.club
                return redirect(url_for("dash"))
            else:
                #print(uname,user.uname,password,user.password)
                flash("INCORRECT password")
                # to be completed

        return render_template("login.html")
    else:
        return redirect(url_for("dash"))

@app.route("/dashboard",methods=['POST','GET'])
def dash():
    if session.get("loggedin"):
        all_tasks = None
        #all_tasks = Posts.query.filter_by(assigned_by=session.get("uname"))
        return render_template("blank-page.html",all_tasks=all_tasks,uname=session['uname'],role=session['role'])
    else:
        return redirect(url_for("login"))
    
@app.route("/addPost",methods=["GET","POST"])
def addTask():
    if request.method == "POST":
        task_title = request.form.get("task_title")
        assigned_by=session.get("uname")
        assigned_to = request.form.get("assigned_to")
        start_date = datetime.strptime(request.form.get("start_date"),"%Y-%m-%d")
        end_date = datetime.strptime(request.form.get("end_date"),"%Y-%m-%d")
        contents = request.form.get("contents")
        attachments = request.form.get("attachments")
        
        if task_title:
            try:
                new_task= Posts(task_title=task_title,assigned_by=assigned_by,assigned_to=assigned_to,start_date=start_date,end_date=end_date,contents=contents,attachments=attachments)
                db.session.add(new_task)
                db.session.commit()
                print("Task added successfully")
                return redirect("/dashboard")
            except Exception as e:
                flash("Invalid input. Please try again.")
                print(e)
    return render_template("addTask.html")

@app.route("/post/<id>")
def task(id):
    post = Posts.query.filter_by(id=id).first()
    if task:
        return render_template("showTask.html",task=task)
    return "404 NO record found"

@app.route("/addNews",methods=["GET","POST"])
def addNews():
    if session.get("loggedin"):
        if request.method=="POST":
            title = request.form.get("title")
            cont = request.form.get("contents")
            e_date = request.form.get("Event_date")
            end_date = request.form.get("end_date")
            att = request.form.get("attachments")
            db.session.add(News(    title = title,    posted_by = session['reg_no'],    date = e_date,    register_by = end_date,    contents = cont,    attachments = att))


        return render_template("addNews.html")
    else:
        return redirect(url_for("login"))
    
@app.route("/register",methods=["GET","POST"])
def register():
    if request.method=="POST":
        uname=request.form.get("uname")
        regno=int(request.form.get("regno"))
        pwd=request.form.get("pwd")
        role="Member"
        club=request.form.get("club")
        if Users.query.filter_by(reg_no=regno) is not None:
            return "Account already exists for this Register Number."
        
        db.session.add(Users(role=role,uname=uname,password=pwd,club=club,reg_no=regno))
        return "User registered successfully. Please <a href='/login'>login</a> now."
    return render_template("register.html")

@app.route('/members')
def members():

    return render_template('members.html')

@app.route('/users/<reg_no>')
def user(reg_no):
    
    return render_template('user.html')

@app.route("/logout",methods=['POST','GET'])
def out():
    session.clear()
    return redirect(url_for("login"))

    
if __name__ == "__main__":
    app.run(debug=True)