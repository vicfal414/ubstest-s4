import os
import re

from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from flask import session
from flask import flash
# from flask_mysqldb import MySQL
# from flask_mysql import MySQL
# import pymysql
import MySQLdb
import pymysql.cursors

import random
from users import Users
#new import for custom challenge html page
from challenge import newChallenge

# mysql = MySQL()

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        # MYSQL_DATABASE_HOST='us-cdbr-east-02.cleardb.com',
        # MYSQL_PORT=15551,
        # MYSQL_DATABSE_USER='b33b6415873ff5',
        # MYSQL_DATABASE_PASSWORD='d1a1b9a1',
        # MYSQL_DATABASE_DB='heroku_1e2700f5b989c0b'
    )

    # mysql.init_app(app)
   

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    @app.route("/")
    def home():
        return render_template("index.html")

    @app.route("/dash")
    def dash():
        return render_template("userdashboard.html")

    @app.route("/challenge")
    def chall():
        return render_template("challenge_list.html")
    
    @app.route("/challenge1")
    def chall_pg1():
        return render_template("challenge_pages/challenge1.html")
    
    @app.route("/challenge2")
    def chall_pg2():
        return render_template("challenge_pages/challenge2.html")

    @app.route("/challenge3")
    def chall_pg3():
        return render_template("challenge_pages/challenge3.html")

    @app.route("/challenge4")
    def chall_pg4():
        return render_template("challenge_pages/challenge4.html")

    @app.route("/challenge5")
    def chall_pg5():
        return render_template("challenge_pages/challenge5.html")
    
    @app.route("/challenge6")
    def chall_pg6():
        return render_template("challenge_pages/challenge6.html")

    #Addition for Custom Challenge
    @app.route("/challengeCustom")
    def chall_pg7():
        return render_template("challenge_pages/custom_challenge.html")

    #Addition for new Custom Challenge specific page
    @app.route("/newChallengeCustom")
    def chall_pg8():
        return render_template("new_custom_challenge.html", newCC = newChallenge)

    @app.route("/friends")
    def friend():  
        return render_template("friends.html",
            friendList=Users['friends'],
            notFriendList=Users['notFriends'])

    @app.route("/publicProfileFriend")
    def publicProfileFriend():
        return render_template("publicProfileFriend.html")

    @app.route("/publicProfileNotFriend")
    def publicProfileNotFriend():
        return render_template("publicProfileNotFriend.html")


    @app.route("/login", methods = ['GET', 'POST'])
    def login():
        msg = ''
        if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
            username = request.form['username']
            password = request.form['password']
            # cur = mysql.connection.cursor()
            connection = pymysql.connect(host='us-cdbr-east-02.cleardb.com',
                             user='b2cb10b2b21b72',
                             password='1b8b9cc5',
                             db='heroku_318469e412eb0ae',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)
            with connection.cursor() as cursor:
                cursor.execute('SELECT * FROM accounts WHERE username = %s AND password = %s', (username, password, ))
            data = cursor.fetchone()
            print(data)
            if data:
                session['logged_in'] = True
                session['id'] = data['id']
                session['username'] = data['username']
                flash('You are logged in')
                return redirect(url_for('home'))
            else:
                msg = 'Invalid Credentials. Please try again.'
            connection.close()
        return render_template("login.html", msg = msg)
    
     
    @app.route('/logout')
    def logout():
        session.pop('logged_in', None)
        session.pop('id', None)
        session.pop('username', None)
        flash('You are logged out.')
        return redirect(url_for('home'))

    @app.route("/signup", methods = ['GET', 'POST'])
    def signup():
        msg = ''
        if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
            username = request.form['username']
            password = request.form['password']
            email = request.form['email']
            fname = request.form['fname']
            lname = request.form['lname']
            connection2 = pymysql.connect(host='us-cdbr-east-02.cleardb.com',
                             user='b2cb10b2b21b72',
                             password='1b8b9cc5',
                             db='heroku_318469e412eb0ae',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)
            with connection2.cursor() as cursor2:
                cursor2.execute('SELECT * FROM accounts WHERE username = %s', (username,))
            data = cursor2.fetchone()
            if data:
                # Account already exists
                msg = 'Account already exists.'
            elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
                # Invalid email address
                msg = 'Inavlid email address.'
            elif not re.match(r'[A-Za-z0-9]+', username):
                # Invalid username
                msg = 'Username must only contain characters and numbers.'
            elif not username or not password or not email:
                # Form was not filled out
                msg = 'Please enter your information.'
            else:
                with connection2.cursor() as cursor3:
                    cursor3.execute('INSERT INTO accounts VALUES (NULL, %s, %s, %s, %s, %s)', (fname, lname, username, password, email,))
                connection2.commit()
                msg = 'You have successfully registered!'
            connection2.close()
        elif request.method == 'POST':
            #Form is empty
            msg = 'Please enter your information.'
        
        return render_template("signup.html", msg = msg)

    #function for custom challenge form
    @app.route("/addingcustom", methods = ['GET', 'POST'])
    def addingcustom():
        msg = ''
        if request.method == 'POST' and 'challengeName' in request.form and 'shortDescription' in request.form and 'SelectDuration' in request.form and 'SelectCategory' in request.form and 'theImpact' in request.form and 'Suggestions' in request.form:
            challengeName = request.form['challengeName']
            shortDescription = request.form['shortDescription']
            SelectDuration = request.form['SelectDuration']
            SelectCategory = request.form['SelectCategory']
            theImpact = request.form['theImpact']
            suggestionsHelp = request.form['Suggestions']

            newChallenge['name'] = challengeName
            newChallenge['description'] = shortDescription 
            newChallenge['duration'] = SelectDuration 
            newChallenge['category'] = SelectCategory 
            newChallenge['impact'] = theImpact 
            newChallenge['suggestions'] = suggestionsHelp 
  
        elif request.method == 'POST':
            #Form is empty
            msg = 'Please enter all informaton for Custom Challenge.'
        
        #return render_template("challenge_pages/custom_challenge.html", msg = msg)
        return redirect(url_for('chall_pg8'))

    @app.route("/css")
    def css():
        return render_template("static/css/style.css") 
    
    @app.route("/random")
    def rand_chall():
        number = random.randint(1, 6)
        site = "chall_pg" + str(number)
        return redirect(url_for(site))
        
    def getUserName(name):
        for uType in Users:
            for user in Users[uType]:
                if user['name'] == name:
                    return user['username']
        return None

    def getProfilePic(name):
        for uType in Users:
            for user in Users[uType]:
                if user['name'] == name:
                    return user['profilePic']
        return None
    
    @app.route("/addFriend", methods = ['POST'])
    def addFriend():
        if request.method == 'POST':
            name = request.form['notFriend']
            newFriend = {'username': getUserName(name), 'name': name, 'profilePic':  getProfilePic(name)}
            Users['friends'].append(newFriend)
            Users['notFriends'].remove(newFriend)
        return redirect(url_for('friend'))
      
    @app.route("/remFriend", methods = ['POST'])
    def remFriend():
        if request.method == 'POST':
            name = request.form['friend']
            unFriend = {'username': getUserName(name), 'name': name, 'profilePic': getProfilePic(name)}
            Users['notFriends'].append(unFriend)
            Users['friends'].remove(unFriend)
        return redirect(url_for('friend'))
    return app
