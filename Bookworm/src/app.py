from flask import Flask, render_template, redirect, url_for, session, abort, request, flash
import requests
from bs4 import BeautifulSoup
import psycopg2
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
import os
import glob
import pandas as pd
import random

app = Flask(__name__ , static_url_path='/static')

# set your own database name, username and password
db = "dbname='XXXX' user='postgres' host='localhost' password='XXXXX'" #potentially wrong password
conn = psycopg2.connect(db)
cursor = conn.cursor()


bcrypt = Bcrypt(app)

@app.route("/createaccount", methods=['POST', 'GET'])
def createaccount():
    cur = conn.cursor()
    if request.method == 'POST':
        new_username = request.form['username']
        new_password = request.form['password']
        cur.execute(f'''select * from users where username = '{new_username}' ''')
        unique = cur.fetchall()
        flash('Account created!')
        if  len(unique) == 0:
            cur.execute(f'''INSERT INTO users(username, password) VALUES ('{new_username}', '{new_password}')''')
            flash('Account created!')
            conn.commit()

            return redirect(url_for("home"))
        else: 
            flash('Username already exists!')


    return render_template("createaccount.html")




@app.route("/", methods=["POST", "GET"])
def home():
    cur = conn.cursor()
    #Getting 10 random rows from Books
    tenrand = '''select * from Books order by random() limit 10;'''
    cur.execute(tenrand)
    punks = list(cur.fetchall())
    length = len(punks)

    #Getting random id from table Books
    randint = '''select id from Books order by random() limit 1;'''
    cur.execute(randint)
    randomNumber = cur.fetchone()[0]
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        if request.method == "POST":
            input_gender = request.form["radio"].lower()
            input_type = request.form["radiotype"].lower()
            input_skin = request.form["radioskin"].lower()

            input_count = request.form["accessCount"] or -1
            input_access = request.form["access"].lower() or "NaN"

            input_id = request.form["punkid"].lower() or ""

            if input_id != "":
                input_id = input_id.zfill(4)
                return redirect(url_for("punkpage", punkid=input_id))
            return redirect(url_for("querypage", gender=input_gender, types=input_type, skin=input_skin, access=input_access, count=input_count))
            
        length = len(punks)
        return render_template("index.html", content=punks, length=length, randomNumber = randomNumber)

@app.route("/punks/<gender>/<types>/<skin>/<count>/<access>")
def querypage(gender, types, skin, count, access):
    cur = conn.cursor()
    rest = 0

    sqlcode = f'''select * from Books where '''
    if gender != "both":
        sqlcode += f''' gender = '{gender}' and'''
        rest += 1

    if types != "all":
        sqlcode += f''' type = '{types}' and'''
        rest += 1

    if skin != "all":
        sqlcode += f''' skin_tone = '{skin}' and'''
        rest += 1

    if access != "NaN":
        rest += 1
        sqlcode += f''' accessories ~* '{access}' and'''
    
    if int(count) != -1:
        rest += 1
        sqlcode += f''' count = '{count}' and'''

    if rest == 0: 
        sqlcode = f''' select * from Books'''

    else: 
        sqlcode  = sqlcode[:-3]

    cur.execute(sqlcode)
    ct = list(cur.fetchall())


    length = len(ct)

    return render_template("cryptoquery.html", content=ct, length=length)


@app.route('/login', methods=['POST'])
def do_admin_login():
    cur = conn.cursor()
    username = request.form['username']
    password = request.form['password'] 

    insys = f''' SELECT * from users where username = '{username}' and password = '{password}' '''

    cur.execute(insys)

    ifcool = len(cur.fetchall()) != 0

    if ifcool:
        session['logged_in'] = True
        session['username'] = username
    else:
        flash('wrong password!')
    return redirect(url_for("home"))


@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route("/logout")
def logout():
    session['logged_in'] = False
    return home()

@app.route("/profile")
def profile():
    cur = conn.cursor()
    if not session.get('logged_in'):
        return render_template('login.html')
    
    username = session['username']

    sql1 = f'''select id, type, gender, skin_tone, count, accessories from favorites natural join books where username = '{username}' '''
    cur.execute(sql1)
    favs = cur.fetchall()
    length = len(favs)
    return render_template("profile.html", content=favs, length=length, username = username)


@app.route("/punk/<punkid>", methods=["POST", "GET"])
def punkpage(punkid):
    cur = conn.cursor()
    """
    Instead of PunkID we would have our database content
    for 1 cryptopunk instead.
    """
    if not session.get('logged_in'):
        return render_template('login.html')

    if request.method == "POST":
        # Add til favourite
        username = session['username']
        try: 
            sql1 = f'''insert into favorites(id, username) values ('{punkid}', '{username}') '''
            cur.execute(sql1)
            conn.commit()
        except:
            conn.rollback()



    req = "https://cryptopunks.app/cryptopunks/details/"+ punkid
    response = requests.get(req)
    soup = BeautifulSoup(response.content, 'html.parser')
    rows = soup.select("table.ms-rteTable-default tr")
    pricelist = str(soup.find(class_="punk-history-row-bid")).split('\n')
    if len(pricelist) < 5:
        price = "10Ξ ($18,000)"
    else:
        price =pricelist[4].replace('</td>', '').replace('<td>','')

    sql1 = f''' select * from books where id = '{punkid}' '''

    cur.execute(sql1)

    ct = cur.fetchone()

    return render_template("cryptopunk.html", content=ct, price=price)

if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.run(debug=True)
