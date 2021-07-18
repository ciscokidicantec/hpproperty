
from flask import Flask, render_template, request, redirect, url_for
from flask_mysqldb import MySQL


def insertregdetails(result):

    print(result['username'])

    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'Coreldraw1$'


    app.config['MYSQL_HOST'] = 'localhost'
    app.config['MYSQL_USER'] = 'root'
    app.config['MYSQL_PASSWORD'] = 'Coreldraw1$'
    app.config['MYSQL_DB'] = 'marioproperty'

    mysql = MySQL(app)

    #uname = "Tom Finney"
    #regem = "kidicantec@googlemail.com"
    #psw = "Coreldraw2$"

    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO registration(regusername,regemail,password) VALUES(%s,%s,%s)",(result['username'],result['email'],result['password']))
    mysql.connection.commit()
    cur.close()


    return result