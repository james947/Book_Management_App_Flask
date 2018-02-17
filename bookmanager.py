#import flask
from flask import Flask, redirect, render_template
#initializing the app
app = Flask(__name__)
#route to index page
@app.route('/index/')
def index():
    return render_template("index.html")
#runs the app
if __name__ == "__main__":
    app.run(debug=True)