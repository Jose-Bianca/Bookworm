from flask import Flask, render_template, redirect, url_for, session, abort, request, flash
import requests
from bs4 import BeautifulSoup
import psycopg2
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask import request
import os
import glob
import pandas as pd
import random

app = Flask(__name__ , static_url_path='/static')
app.secret_key = 'meatball'

# set your own database name, username and password
db = "dbname='Bookworm' user='postgres' host='localhost' password='Bianca-2904'" #potentially wrong password
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


# The random books function
@app.route("/", methods=["POST", "GET"])
def home():
    cur = conn.cursor()
    #Getting 10 random rows from Attributes
    tenrand = '''select * from Books order by random() limit 10;'''
    cur.execute(tenrand)
    books = list(cur.fetchall())
    length = len(books)
    randomNumber = random.randint(1, 100)
    
    return render_template("index.html", content=books, length=length, randomNumber = randomNumber)


#The search function
import re
from psycopg2.extensions import AsIs

import re

@app.route('/search', methods=['POST'])
def search():
    search_text = request.form['search_text']  # Get the search query from the form
    cur = conn.cursor()

    # Use the search query to find match in the database, we need a regex for this

    sqlcode = '''SELECT * FROM Books WHERE type ~* %s OR gender ~* %s'''
    regex_pattern = ".*" + re.escape(search_text) + ".*"

    cur.execute(sqlcode, (regex_pattern, regex_pattern))
    content = list(cur.fetchall())

    length = len(content)

    return render_template("cryptoquery.html", content=content, length=length)


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

    # Query to find the rating of the book
    sql1 = f''' select accessories from books where id = '{punkid}' '''

    cur.execute(sql1)
    price = cur.fetchone()[0]
    # Query to find the book details
    sql2 = f''' select * from books where id = '{punkid}' '''

    cur.execute(sql2)
    ct = cur.fetchone()

    return render_template("cryptopunk.html", content=ct, price=price)

if __name__ == "__main__":
    app.run(debug=True)
