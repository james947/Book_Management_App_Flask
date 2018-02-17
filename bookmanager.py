#import flask
from flask import Flask, redirect, render_template
#initializing the app
app = Flask(__name__)

#session seccret key
app.config["SECRET_KEY"] ="b'e3ce76d4483bcce68ddf2067c443e43b87f02a304ab7a80e'"

#route to index page
@app.route('/index/', methods=['GET','POST'])
def index():

    return render_template("index.html")
#runs the app
if __name__ == "__main__":
    app.run(debug=True)