from flask import Flask, url_for, request, render_template #import flask and the url_for, request, and render template function
from app import app #import app variable from the app.py file
import datetime
import sys
#import PyMySQL
import sqlite3

#SQLdatabase for the entries
conn = sqlite3.connect('blog.db') #create a connection to the sql database
c = conn.cursor() #create a new cursor object from that connection
#build the table
c.execute("""CREATE TABLE IF NOT EXISTS entries (
                NUM REAL,
                DATE TEXT NOT NULL, 
                TITLE TEXT NOT NULL, 
                ENTRY TEXT NOT NULL) 
                """)

'''
#SQLdatabase for the number of entries to avoid global variabls(?)
conn_two = sqlite3.connect('number.db')
c_two = conn_two.cursor()
#build the table
c_two.execute("""CREATE TABLE IF NOT EXISTS number (
                value REAL)
                """)
#put the number 0 in the table already
temp = 0
c_two.execute("INSERT INTO number (value) VALUES (?)", (0.0))
'''


#db = PyMySQL.connect("localhost","testuser","test123","TESTDB" )

#server/
@app.route('/')
def hello():
    newentry_link = "<a href='" + url_for('new_entry') + "'>Write a new entry</a>"
    return """<html>
                    <head>
                        <title>Welcome!</title>
                    </head>
                    <body>
                        """ + newentry_link + """
                    </body>
              </html>"""

#server/new

@app.route('/new', methods = ['GET', 'POST'])
def new_entry():
    if request.method == 'GET': #if the user is trying to GET info
        return render_template('newentry.html') #send the user the new entry page
    elif request.method == 'POST':
        try:
            num = 0
            '''
            #get the number from the number database
            c_two.execute("SELECT MAX(value) FROM number")
            temp = c_two.fetchone()
            num = temp[0]
            num = num + 1
            '''

            #get the data from the form
            date = str(datetime.date.today())
            title = str(request.form['title'])
            entry = str(request.form['entry'])

            #store the title and entry in the database
            c.execute("INSERT INTO entries VALUES (?,?,?,?)", (num, date, title, entry))
            conn.commit()
            msg = "Your entry has been published."
        except:
            conn.rollback()
            msg = "There was an error publishing your entry."

        finally: 
            return render_template('submitentry.html', msg = msg)
    else:
        return "<h2> Invalid </h2>"

#server/entry/<title>
@app.route('/entry/<name>', methods = ['GET', 'POST'])
def view_entry(name):
    if request.method == 'GET':
        #get the data from the database
        c.execute("SELECT TITLE, DATE, ENTRY FROM entries WHERE TITLE = ?", (name,))
        row = c.fetchone()

        title = row[3] #read title from database
        data = row[2] #read date from the database
        entry = row[4] #read entry for database

        return render_template('viewentry.html', title = title, date = date, entry = entry)
    elif request.method == 'POST':
        return "<h2> Invalid </h2>"
    else:
        return "<h2> Invalid </h2>"


@app.route('/number')
def view_number():
    return "<h2>" + str(num) + "</h2>"

@app.route('/viewall')
def view_all():
   con = sqlite3.connect("blog.db")
   con.row_factory = sqlite3.Row
   
   cur = con.cursor()
   cur.execute("select * from entries")
   
   rows = cur.fetchall();
   return render_template("viewall.html",rows = rows)