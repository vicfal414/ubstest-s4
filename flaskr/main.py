import os
import re

from flask import Flask, render_template, request, redirect, url_for, session, flash
import MySQLdb
import pymysql.cursors

import random

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


    @app.route("/getProfilePic")
    def getProfilePic(userid):
        connection = pymysql.connect(host='us-cdbr-east-02.cleardb.com',
                            user='b33b6415873ff5',
                            password='d1a1b9a1',
                            db='heroku_1e2700f5b989c0b',
                            charset='utf8mb4',
                            cursorclass=pymysql.cursors.DictCursor)
        with connection.cursor() as cursor:
            cursor.execute('SELECT picture FROM accounts where id = %s', (userid))
            pic = cursor.fetchone()
            connection.close()
        return pic

    @app.route("/getName")
    def getName(userid):
        connection = pymysql.connect(host='us-cdbr-east-02.cleardb.com',
            user='b33b6415873ff5',
            password='d1a1b9a1',
            db='heroku_1e2700f5b989c0b',
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor)
        with connection.cursor() as cursor:
            cursor.execute('SELECT fname FROM accounts where id = %s', (userid)) 
            fname = cursor.fetchone()
            rest = cursor.fetchall()
            cursor.execute('SELECT lname FROM accounts where id = %s', (userid))
            lname = cursor.fetchone()
            rest2 = cursor.fetchall()
        connection.close()
        fullName = str(fname) + str(lname)
                
        return fullName


    @app.route("/friends", methods=['GET','POST'])
    def friend():
        
        connection = pymysql.connect(host='us-cdbr-east-02.cleardb.com',
            user='b33b6415873ff5',
            password='d1a1b9a1',
            db='heroku_1e2700f5b989c0b',
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor)
        with connection.cursor() as cursor:
            cursor.execute('SELECT friendsList FROM accounts WHERE id = %s', (session['id']))
            fList = cursor.fetchone()
            session["friends"] = fList.split("|")
            rest = cursor.fetchall()
            cursor.execute('SELECT id FROM accounts WHERE id NOT IN %s AND WHERE id != %s LIMIT 10', (session["friends"], session['id'])) 
            nFList = cursor.fetchall()
            session["notFriends"] = nFList['id'].split("|")
        connection.close()

        if request.method == 'POST' and 'loadMoreFriend' in request.form:
            return redirect(url_for('loadMoreFriend'))

        if request.method == 'POST' and 'loadMoreNotFriend' in request.form:
            return redirect(url_for('loadMoreNotFriend'))

        if request.method == 'POST' and 'search' in request.form:
            search = request.form['search']
            session['search'] = search
            return redirect(url_for('search'))

        if request.method == 'POST' and 'user' in request.form :
            user = request.form['user']
            session['user'] = user
            return redirect(url_for('publicProfile'))

        if request.method == 'POST' and 'notFriend' in request.form :
            notFriend = request.form['notFriend']
            session['notFriend'] = notFriend
            return redirect(url_for('addFriend'))
        
        if request.method == 'POST' and 'friend' in request.form:
            friend = request.form['friend']
            session['friend'] = friend
            return redirect(url_for('remFriend'))

        return render_template("friends.html",
            loadMoreFriend = False,
            loadMoreNotFriend = False, 
            msg='')

    @app.route('/results')
    def search_results(search):

        #puts first and last name of search results in a list
        results = [(str(data[1]) + " " + str(data[2])) for data in search]

        # display results
        return render_template('results.html', results=results)

    @app.route('/search')
    def search():
            msg = ''
            connection = pymysql.connect(host='us-cdbr-east-02.cleardb.com',
                             user='b33b6415873ff5',
                             password='d1a1b9a1',
                             db='heroku_1e2700f5b989c0b',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)
            with connection.cursor() as cursor:
                cursor.execute('SELECT * FROM accounts WHERE username = %s OR email = %s OR fname = %s OR lname = %s', (session['search'], session['search'], session['search'], session['search']))
                data = cursor.fetchall()
            if data == []:
                msg = (str(session['search']) + ' is not a user in our system.')
            else:
                #render results template with data list
                search_results(data)
            connection.close()

            return render_template("friends.html",
                loadMoreFriend = False,
                loadMoreNotFriend = False, 
                msg=msg)
    
    @app.route("/publicProfile", methods = ['GET', 'POST'])
    def publicProfile():
            connection = pymysql.connect(host='us-cdbr-east-02.cleardb.com',
                user='b33b6415873ff5',
                password='d1a1b9a1',
                db='heroku_1e2700f5b989c0b',
                charset='utf8mb4',
                cursorclass=pymysql.cursors.DictCursor)
            with connection.cursor() as cursor:
                cursor.execute('SELECT friendsList FROM accounts WHERE id = %s', (session['user']))
                fList = cursor.fetchone()
                session["userFriends"] = fList.split("|")
                rest = cursor.fetchall()
                cursor.execute('SELECT progress, completed FROM dashboard WHERE user = %s', (session['user']))
                challs = cursor.fetchone()
                connection.close()
                if challs:
                    pro = challs['progress'].split("|")
                    com = challs['completed'].split("|")
                    session['progress'] = pro
                    session['completed'] = com

            if request.method == 'POST' and 'loadMorePub' in request.form:
                return redirect(url_for('loadMorePub'))

            if request.method == 'POST' and 'user' in request.form :
                user = request.form['user']
                session['user'] = user
                return redirect(url_for('publicProfile'))

            if request.method == 'POST' and 'notFriend' in request.form :
                notFriend = request.form['notFriend']
                session['notFriend'] = notFriend
                return redirect(url_for('addFriend'))
            
            if request.method == 'POST' and 'friend' in request.form:
                friend = request.form['friend']
                session['friend'] = friend
                return redirect(url_for('remFriend')) 
            return render_template("publicProfile.html",
                loadMore = False)

    @app.route("/login", methods = ['GET', 'POST'])
    def login():
        msg = ''
        if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
            username = request.form['username']
            password = request.form['password']
            # cur = mysql.connection.cursor()
            connection = pymysql.connect(host='us-cdbr-east-02.cleardb.com',
                             user='b33b6415873ff5',
                             password='d1a1b9a1',
                             db='heroku_1e2700f5b989c0b',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)
            with connection.cursor() as cursor:
                cursor.execute('SELECT * FROM accounts WHERE username = %s AND password = %s', (username, password ))
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
                    user='b33b6415873ff5',
                    password='d1a1b9a1',
                    db='heroku_1e2700f5b989c0b',
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

    @app.route("/css")
    def css():
        return render_template("static/css/style.css") 
    
    @app.route("/random")
    def rand_chall():
        number = random.randint(1, 6)
        site = "chall_pg" + str(number)
        return redirect(url_for(site))
        
    
    @app.route("/addFriend")
    def addFriend():
        
            connection = pymysql.connect(host='us-cdbr-east-02.cleardb.com',
                             user='b33b6415873ff5',
                             password='d1a1b9a1',
                             db='heroku_1e2700f5b989c0b',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)
            with connection.cursor() as cursor:
                cursor.execute('SELECT friendsList FROM accounts WHERE id = %s', (session['id']))
                fList = cursor.fetchone()
                session["friends"] = fList.split("|")
                rest = cursor.fetchall()
                session["friends"].append(session['notFriend'])

                cursor.execute('UPDATE TABLE accounts SET friendsList = %s WHERE id = %s', (session["friends"], session['id']))
                connection.commit()
            #add the user_id to the current user's friendList
            
            connection.close()
            return redirect(url_for('friend'))
      
    @app.route("/remFriend")
    def remFriend():
        
            connection = pymysql.connect(host='us-cdbr-east-02.cleardb.com',
                             user='b33b6415873ff5',
                             password='d1a1b9a1',
                             db='heroku_1e2700f5b989c0b',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)
            with connection.cursor() as cursor:
                cursor.execute('SELECT friendsList FROM accounts WHERE id = %s', (session['id']))
                fList = cursor.fetchone()
                session["friends"] = fList.split("|")
                rest = cursor.fetchall()
                session["friends"].remove(session['friend'])
                cursor.execute('UPDATE TABLE accounts SET friendsList = %s WHERE id = %s', (session["friends"], session['id']))
                connection.commit()
            #remove the user_id from the current user's friendList

            connection.close()
            return redirect(url_for('friend'))


    @app.route("/loadMoreFriend")
    def loadMoreFriend():
        return render_template("friends.html",
            loadMoreFriend = True,
            loadMoreNotFriend = False, 
            msg='')

    @app.route("/loadMoreNotFriend")
    def loadMoreNotFriend():
        return render_template("friends.html",
            loadMoreFriend = False,
            loadMoreNotFriend = True, 
            msg='')

    @app.route("/loadMorePub")
    def loadMorePub():
        return render_template("publicProfile.html",
            loadMore = True)

    return app