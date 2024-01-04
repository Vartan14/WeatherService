import re
from flask import render_template, url_for, redirect, request
import MySQLdb.cursors


class LoginHandler:
    @staticmethod
    def index():
        return redirect(url_for('login'))

    @staticmethod
    def login():
        msg = ''
        print(request.form)
        if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
            from app import mysql, bcrypt, session
            username = request.form['username']
            password = request.form['password']

            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('SELECT * FROM users WHERE username = %s', [username])
            account = cursor.fetchone()

            if account:

                if bcrypt.check_password_hash(account['password'], password):

                    session['logged'] = True
                    session['id'] = account['id']
                    session['username'] = account['username']
                    print(session)
                    return redirect(url_for('apikey'))
                else:
                    msg = 'Invalid password'

            else:
                msg = 'Invalid username'

        return render_template('login.html', msg=msg)

    @staticmethod
    def logout():
        from app import mysql, bcrypt, session
        session.pop('logged', None)
        session.pop('id', None)
        session.pop('username', None)
        print(session)
        return redirect(url_for('login'))

    @staticmethod
    def register():
        msg = ''
        print(request.form)
        if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
            from app import mysql, bcrypt, session
            username = request.form['username']
            password = request.form['password']
            confirm_password = request.form['confirm_password']

            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('SELECT * FROM users WHERE username = %s', (username,))
            account = cursor.fetchone()
            if account:
                msg = 'Account already exists!'
            elif not username or not password or not confirm_password:
                msg = 'Please fill out the form !'
            elif not re.match(r'[A-Za-z0-9]+', username):
                msg = 'Username must contain only characters and numbers!'
            elif len(password) < 8:
                msg = 'Password must be at least 8 characters long!'
            elif not re.search("[a-z]", password) or not re.search("[A-Z]", password):
                msg = 'Password must contain both lowercase and uppercase letters!'
            elif not re.search("[0-9]", password):
                msg = 'Password must contain at least one digit!'
            elif password != confirm_password:
                msg = 'Passwords do not match!'
            else:
                hashed_password = bcrypt.generate_password_hash(password)
                cursor.execute('INSERT INTO users VALUES (NULL, %s, %s)', (username, hashed_password))
                mysql.connection.commit()
                msg = 'You have successfully registered !'

                return redirect(url_for('login'))

        elif request.method == 'POST':
            msg = 'Please fill out the form!'

        return render_template('register.html', msg=msg)
