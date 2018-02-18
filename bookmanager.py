#import flask
from functools import wraps
from flask import Flask, redirect, render_template, request, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

#initializing the app
app = Flask(__name__)

#connect to postgress db
app.config['SQLALCHEMY_DATABASE_URI']='postgresql://postgres:8247@localhost/book_data'
db = SQLAlchemy(app)

#user auth checks if user is logged_in
def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('Unauthorized,Plese login', 'danger') 
            return redirect(url_for('login'))  
    return wrap

#class for creating table book
class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    subtitle = db.Column(db.String(80), nullable=False)
    author =db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(80), nullable=False)
    date_posted = db.Column(db.DateTime)

    def __repr__(self):
        return "<Title: {}>".format(self.title)

#session seccret key
app.config["SECRET_KEY"] ="b'e3ce76d4483bcce68ddf2067c443e43b87f02a304ab7a80e'"

#route to index page
@app.route('/index/')
def index():
    return render_template("index.html")
#routes to post
@app.route('/post')
def post():
    books = Book.query.order_by(Book.date_posted.desc()).all()
    return render_template("posts.html", books=books)
#stores form data to db
@app.route('/addPost', methods=['POST'])
def addPost():
    #request form data
    title = request.form['title']
    subtitle = request.form['subtitle']
    author = request.form['author']
    description = request.form['description']

    #create variable post to add data to db
    post = Book(title=title, subtitle=subtitle, author=author, description=description, date_posted=datetime.now())

    #commit to db and end session
    db.session.add(post)
    db.session.commit()
    return redirect (url_for('post'))


@app.route('/editPost', methods=['GET','POST'])
def editPost():
    book = Book.query.get(Book.id)
    #request form data
    book.title = 'title'
    book.subtitle = 'subtitle'
    title = request.form['title']
    subtitle = request.form['subtitle']
    author = request.form['author']
    description = request.form['description']

    #create variable post to add data to db
    post = Book(title=title, subtitle=subtitle, author=author, description=description, date_posted=datetime.now())

    #commit to db and end session
    db.session.add(post)
    db.session.commit()
    return redirect (url_for('post'))
    
#Route to delete a specific book by title
@app.route("/delete", methods=["POST"])
def delete():
    title = request.form.get("title")
    book = Book.query.filter_by(title=title).first()
    db.session.delete(book)
    db.session.commit()
    return redirect("post")

#runs the app
if __name__ == "__main__":
    app.run(debug=True)