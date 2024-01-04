import MySQLdb.cursors
import secrets
from flask import render_template, url_for, redirect


class ApiKeyHandler:
    @classmethod
    def api_key(cls):
        from app import session, mysql, request

        print(session)
        if session.get('logged'):
            print("User logged")
            if request.method == 'POST':

                cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                user_id = session['id']

                cursor.execute('SELECT api_key FROM api_keys WHERE user_id = %s', (user_id,))
                existing_api_key_data = cursor.fetchone()

                # get api key from db
                if existing_api_key_data:
                    api_key = existing_api_key_data['api_key']

                # generate new api key
                else:
                    api_key = cls.generate_api_key()

                    cursor.execute('INSERT INTO api_keys (user_id, api_key) VALUES (%s, %s)', (user_id, api_key))
                    mysql.connection.commit()

                return render_template('api_key.html', api_key=api_key)
            else:
                return render_template('api_key.html')

        else:
            print("User didnt log")
            return redirect(url_for('login'))

    @staticmethod
    def generate_api_key(length=32):
        return secrets.token_hex(length // 2)
