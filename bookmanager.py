#import flask
from functools import wraps
from flask import Flask, redirect, render_template, request, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from forms import SignupForm, LoginForm
#initializing the app
app = Flask(__name__)

#connect to postgress db
app.config['SQLALCHEMY_DATABASE_URI']='postgresql://postgres:8247@localhost/book_data'
db = SQLAlchemy(app)

#session seccret key to prevent attacks
app.config["SECRET_KEY"] ="b'e3ce76d4483bcce68ddf2067c443e43b87f02a304ab7a80e'"

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

#routes to signup page
@app.route('/signup/', methods=['GET','POST'])
def signup():
    form = SignupForm(request.form)
    if request.method == 'POST' and form.validate():
        username =request.form.data
        email = request.form.data
        password = request.form.data
        #get data and store in a variable post
        post= User(username = username, email=email, password=password )
        #add post variable to db
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('signup.html', form=form)
        
#route to index page
@app.route('/login/', methods=['GET','POST'])
def login():
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        name = request.form.data
        password = request.form.data
        post = User.query.get_by(username = username)
        if name != 

    return render_template("login.html", form=form)

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


@app.route('/editPost', methods=['POST'])
def editPost():
    if request.method == 'POST':
        title = request.form['title']
        subtitle  = request.form['subtitle']
        author = request.form['author']
        description =request.form['description']

        found_post =  Book.query.filter_by(id=id).first()
        Book.title = title
        Book.subtitle = subtitle
        Book.author = author
        Book.description = description
        #commit to db
        db.session.commit()
        return redirect (url_for('post'))

@app.route('/show/<int:id>')
def show(id):
    found_post =  Book.query.filter_by(id=id).first()
    return render_template("show.html", found_post= found_post)

#Route to delete a specific book by title
@app.route("/delete/<int:id>")
def delete(id):
    book = Book.query.filter_by(id=id).first()
    db.session.delete(book)
    db.session.commit()
    return redirect("post")

#runs the app
if __name__ == "__main__":
    app.run(debug=True)