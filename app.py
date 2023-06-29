from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
# from sqlalchemy import create_engine
# from sqlalchemy.orm import scoped_session, sessionmaker

# from passlib.hash import sha256_crypt
# engine = create_engine("mysql+pymysql://root:1234567@localhost/register")


# db =  scoped_session(sessionmaker(bind=engine))
# from flask_login import UserMixin

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///ToDo.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Todo(db.Model):
    SrNo = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    desc = db.Column(db.String(500), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"{self.SrNo} - {self.title}"
with app.app_context():
    db.create_all()

# class User(db.Model, UserMixin):
# #     id = db.Column(db.Integer(),primary_key= True )
# #     email = db.Column(db.String(100), unique=True)
# #     password = <PASSWORD>(db.<PASSWORD>)
# # todos = db.relationship('Todo', backref='user', lazy=True)




@app.route('/', methods=['GET', 'POST'])
def hello_world():
    if request.method == 'POST':
        title = request.form['title']
        desc = request.form['desc']
        todo = Todo(title=title, desc=desc)
        db.session.add(todo)
        db.session.commit()
    
    allTodo = Todo.query.all()
    return render_template("test.html", allTodo=allTodo)




# @app.route('/show')
# def products():
#     allTodo = Todo.query.all()
#     print(allTodo)
#     return 'This is Product Page'

@app.route('/update/<int:SrNo>', methods=['GET', 'POST'])
def update(SrNo):
    if request.method=='POST':
        title = request.form['title']
        desc = request.form['desc']
        todo = Todo.query.filter_by(SrNo=SrNo).first()
        todo.title = title
        todo.desc = desc
        db.session.add(todo)
        db.session.commit()
        return redirect("/")

    todo = Todo.query.filter_by(SrNo=SrNo).first()
    return render_template("update.html", todo=todo)

@app.route('/delete/<int:SrNo>')
def delete(SrNo):
    todo = Todo.query.filter_by(SrNo=SrNo).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect("/")

# # Register Form

# @app.route("/register", methods=["GET", "POST"])
# def register():
#     # if request.method == "POST":
#     #     name = request.form.get("name")
#     #     username = request.form.get("username")
#     #     password = request.form.get("password")
#     #     c_password = request.form.get("c_password")
#     #     secure_password = sha256_crypt.encrypt(str(password))

#         # if

#     return render_template("register.html")

# # Login 

# @app.route("/login")
# def login():
#     return render_template("login.html")



if __name__=="__main__":
    app.run(debug = True)

