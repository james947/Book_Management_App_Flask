#import flask
from flask import Flask, redirect, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

#initializing the app
app = Flask(__name__)

#connect to postgress db
app.config['SQLALCHEMY_DATABASE_URI']='postgresql://postgres:8247@localhost/book_data'
db = SQLAlchemy(app)

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

@app.route('/post')
def post():
    books = Book.query.order_by(Book.date_posted.desc()).all()
    return render_template("posts.html", books=books)

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

#runs the app
if __name__ == "__main__":
    app.run(debug=True)