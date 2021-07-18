import datetime
import yaml
import locale

import base64
#import cStringIO
import io
import re

from flask import Flask, render_template, request, redirect, url_for
from flask_mysqldb import MySQL
from PIL import Image
from base64 import b64encode

from flask_nav import Nav
from flask_bootstrap import Bootstrap

from flask_nav.elements import Navbar, Subgroup, View

import flask_wtf
from flask_wtf import FlaskForm


from forms import SignUpForm

from processdb import insertregdetails

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Coreldraw1$'

#render_template('testimage.html')

Bootstrap(app)
nav = Nav(app)

@nav.navigation('mysite_navbar')

def create_navbar():
    home_view = View('Home', 'signup')
    register_view = View('Rigister', 'index')
    about_me_view = View('About_me_view', 'mario')
    return Navbar('Mysite', home_view, register_view, about_me_view)

def convertToBinaryData(filename):
    # Convert digital data to binary format
    with open(filename, 'rb') as file:
        binaryData = file.read()
    return binaryData

#/home/cisco/pythonflask/db.yaml

#db = yaml.load(open('/home/cisco/pythonflask/db.yaml'))

#app.config['MYSQL_HOST'] = db['mysql_host']
#app.config['MYSQL_USER'] = db['mysql_user']
#app.config['MYSQL_PASSWORD'] = db['mysql_password']
#app.config['MYSQL_DB'] = db['mysql_db']

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Coreldraw1$'
app.config['MYSQL_DB'] = 'marioproperty'

mysql = MySQL(app)

@app.route("/", methods = ['GET', 'POST'])
def signup():
    create_navbar()
    form = SignUpForm()
    if form.is_submitted():
    #print('request method = ',request.method)
    #if request.method == 'POST':
        result = request.form
        fromsinglefield = result['username']
        myusername = request.form['username']
        c = insertregdetails(request.form)
        print(c['username'])
        return render_template('user.html', result=result, myusername = myusername, namefield = fromsinglefield)
    return render_template('signup.html',form=form)

@app.route("/about_me_view", methods = ['GET', 'POST'])
def about_me_view():
    return


@app.route("/about", methods = ['GET', 'POST'])
def index():

    im = Image.open("/home/cisco/pythonflask/static/newpencil.png")  
  
    im.show() 

    render_template("property.html")
    if request.method == 'POST':
        userDetails = request.form
        name = userDetails['name']
        address = userDetails['address']
        #helenimg = Image.open("pythonflask/helen.jpg")
        #photo = convertToBinaryData('pythonflask/static/helen.jpg')
        photo = convertToBinaryData('/home/cisco/pythonflask/static/newpencil.png')

        #biodata = convertToBinaryData('pythonflask/images/helen.jpg')
        locale.setlocale(locale.LC_ALL, 'en_GB.utf8')
        localnow = datetime.datetime.now()
        now=localnow.strftime("%c")
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO Vendors(name,address,entrydatevendor,vendormainpicture) VALUES(%s,%s,%s,%s)",(name,address,now,photo))
        mysql.connection.commit()
        cur.close()
        return redirect('/users')

    #now = datetime.datetime.now()
    #new_year = now.month == 1 and now.day == 1
    #new_year = True
    return render_template("property.html")

@app.route('/users')
def users():
    cur = mysql.connection.cursor()
    resultValue = cur.execute("SELECT * FROM Vendors")
    if resultValue > 0:
        #@app.route("/show/<int:id>")
        #obj = A.query(A.id == id).fetch(1)[0]
        #image = b64encode(obj.image).decode("utf-8")
        userDetails = cur.fetchall()
        dummy = []
        filename = '/home/cisco/pythonflask/static/newpencil.png'
        loopcounter = 0
        for eachrow in userDetails:
            loopcounter = loopcounter + 1
            print("\nLoop Counter = ", loopcounter)
            venid = eachrow[0]
            vendoname=eachrow[1]
            vendoaddress=eachrow[2]
            vendordateandtime = eachrow[3]
            print("\n   ",venid,"   ",vendoname,"   ",vendoaddress,"   ",vendordateandtime)
            image = eachrow[4]
            dummy=eachrow[4]
            dummy=io.BytesIO(base64.b64decode(eachrow[4]))
            with open(filename, 'wb') as f:
                f.write(image)
            
            #image_data = re.sub('^data:image/.+;base64,', '', eachrow[4])
            #im = Image.open(io.BytesIO(base64.b64decode(image_data)))

            #eachrow[4]) = re.sub('^data:image/.+;base64,', '', eachrow[4])
            #imdata = Image.open(io.BytesIO(base64.b64decode(image_data)))

            #pre_img = io.BytesIO(image)
            #Image.open(pre_img)
            
            


            #file_like=io.BytesIO(base64.b64decode(eachrow[4]))
            #img1=Image.open(file_like,mode='r').convert('RGB')
            #img1.show()
        return render_template('users.html',userDetails=userDetails,dummy=dummy)

@app.route("/mario", methods = ['GET', 'POST'])
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