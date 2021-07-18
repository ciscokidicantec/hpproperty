import mysql.connector
import datetime
import json

from flask import Flask, render_template, request, redirect, url_for
app = Flask(__name__)

@app.route("/c", methods = ['GET', 'POST'])
def c(): 
  now = datetime.datetime.now()
  new_year = now.month == 1 and now.day == 1
  print(new_year)

  return render_template("testimg.html")

@app.route("/", methods = ['GET', 'POST'])
def index(): 

  #print("mario python connector version : {0} " .format(mysql.connector.__version__))

  mydb = mysql.connector.connect(
    host='localhost',
    user='root',
    passwd='Coreldraw1$',
    auth_plugin='mysql_native_password'
    #database='w3school'
  )
  mycursor = mydb.cursor()
  sql = "DROP DATABASE IF EXISTS w3school"
  mycursor.execute(sql) 

  mycursor = mydb.cursor()
  mycursor.execute("CREATE DATABASE w3school")
  mycursor = mydb.cursor()
  mycursor.execute("SHOW DATABASES")
  for x in mycursor:
    print(x)

  mydbtb = mysql.connector.connect(
    host='localhost',
    user='root',
    passwd='Coreldraw1$',
    auth_plugin='mysql_native_password',
    database='w3school'
  )
  mycursor = mydbtb.cursor()
  mycursor.execute("CREATE TABLE Vendors (name VARCHAR(255), address VARCHAR(255), price INT, mydt DATETIME)")

  mycursor = mydbtb.cursor()

  myr_now = datetime.datetime.now()

  sql = "INSERT INTO Vendors (name, address,price,mydt) VALUES (%s, %s,%s,%s)"
  val = ("John", "Highway 21",687000,myr_now)
  mycursor.execute(sql, val)
  mydbtb.commit()
  print(mycursor.rowcount, "record inserted.")

  mycursor = mydbtb.cursor()

  sql = "INSERT INTO Vendors (name, address, price, mydt) VALUES (%s, %s, %s, %s)"
  val = [
    ('Peter', 'Lowstreet 4',-145000,myr_now),
    ('Helen', 'Central Drive 433a',180000,myr_now),
    ('Amy', 'Apple st 652',190000,myr_now),
    ('Hannah', 'Mountain 21',200000,myr_now),
    ('Michael', 'Valley 345',250000,myr_now),
    ('Sandy', 'Ocean blvd 2',275000,myr_now),
    ('Betty', 'Green Grass 1',335000,myr_now),
    ('Richard', 'Sky st 331',450000,myr_now),
    ('Susan', 'One way 98',500000,myr_now),
    ('Vicky', 'Yellow Garden 2',777000,myr_now),
    ('Ben', 'Park Lane 38',80000,myr_now),
    ('William', 'Central st 954',900000,myr_now),
    ('Chuck', 'Main Road 989',950000,myr_now),
    ('Mario','Ermin Street 29',999000,myr_now),
    ('Jade','West Swindon',1200000,myr_now),
    ('Viola', 'Sideway 1633',1500000,myr_now)
  ]
  mycursor.executemany(sql, val)
  mydbtb.commit()
  print(mycursor.rowcount, "rows were inserted.")

  mycursor = mydbtb.cursor()
  mycursor.execute("SELECT * FROM Vendors")
  myresult = mycursor.fetchall()

  for x in myresult:
    print(x)

  sql_select_Query = "SELECT * FROM Vendors"
  mydictcursor = mydbtb.cursor(dictionary=True)
  mydictcursor.execute(sql_select_Query)
  returndictrow = mydictcursor.fetchall()
  #for dictrow in returndictrow:
  #  print("dictinary row = ",dictrow)

  for dictitem in returndictrow:
    print("address = ", dictitem['address'],
        "date = ", dictitem['mydt'].strftime("%A") +
        " " + dictitem['mydt'].strftime("%d") +
        " " + dictitem['mydt'].strftime("%B") +
        " " + dictitem['mydt'].strftime("%Y") +
        " " + dictitem['mydt'].strftime("%H") +
        ":" + dictitem['mydt'].strftime("%M") +
        ":" + dictitem['mydt'].strftime("%S"),
        "name = ", dictitem['name'],
        "price = £{}".format(dictitem['price'])
    )  

  jsonrow = json.dumps(returndictrow, indent=4, sort_keys=True, default=str)
  print("json values = ", jsonrow)

  #for jsoneachrow in jsonrow:
  #  print("each row = ",jsoneachrow)

  mycursor = mydbtb.cursor()
  sql = "UPDATE Vendors SET address = 'Canyon 123' WHERE address = 'Valley 345'"
  mycursor.execute(sql)
  mydbtb.commit()
  print(mycursor.rowcount, "record(s) were affected with this update")

  mycursor = mydbtb.cursor()
  mycursor.execute("SELECT * FROM Vendors LIMIT 5 OFFSET 2")
  myresult = mycursor.fetchall()
  print(mycursor.rowcount, "record(s) were affected with this LIMIT 5 and OFFSET 2")
  for x in myresult:
    print(x)

  #new_year = True

#  return render_template("index.html", new_year=new_year)
  return render_template("testimg.html",jsonrow=jsonrow)


if __name__ == "__main__":
  app.run(debug=True)
