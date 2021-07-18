import datetime

from flask import Flask, render_template
app = Flask(__name__)

@app.route("/")
def index(): 
    now = datetime.datetime.now()
    new_year = now.month == 1 and now.day == 1
    new_year = True
    return render_template("index.html", new_year=new_year)

@app.route("/mario")
def mario():
    names = ["Alice","Bob","Charlie"]
    return render_template("index.html",names=names)

@app.route("/more")
def more():
    return render_template("more.html")

@app.route("/<string:name>")
def hello(name):
    name = name.capitalize()
    return f"<h1>Hello,{name}!</h1>"

if __name__ == "__main__":
    app.run(debug=True)