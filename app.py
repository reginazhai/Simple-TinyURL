# import flast module
from flask import Flask, redirect, jsonify, render_template, request, abort
import sqlite3
import string
import random

# instance of flask application
app = Flask(__name__)


# Reference: https://www.geeksforgeeks.org/how-to-build-a-web-app-using-flask-and-sqlite-in-python/;
# https://www.sqlitetutorial.net/sqlite-python/;
# https://www.geeksforgeeks.org/how-to-return-a-json-response-from-a-flask-api/

# SQLite database connection
conn = sqlite3.connect('urls.db')
# Create table if not exists
cur = conn.cursor()
cur.execute('''CREATE TABLE IF NOT EXISTS url_mappings
             (id integer PRIMARY KEY, 
		     long_url TEXT, short_url TEXT)''')

print("Database connected!")

# TODO: find appropriate URL shortening system
def generate_short_url(long_url):
    characters = string.ascii_letters + string.digits
    short_url = ''.join(random.choices(characters, k=6))
    return short_url

# TODO: add a 404 error page

# home route that returns below text when root url is accessed
@app.route('/') 
def index():
	return render_template('index.html') 

# API endpoint to shorten URL
@app.route('/shorten', methods=['POST'])
def shorten_url_api():
    data = request.json
    long_url = data.get('url')
	
    with sqlite3.connect("urls.db") as conn: 
        cursor = conn.cursor() 
        # Check if the URL already exists in the database
        find_short_url_query = "SELECT short_url FROM url_mappings WHERE long_url=?"
        cursor.execute(find_short_url_query, (long_url,))
        exist_short_url = cursor.fetchone()
        if exist_short_url:
            return jsonify({"shortened_url": exist_short_url[0]})
        
        # Generate a new short code
        short_url = generate_short_url(long_url)
        # Insert new mapping into the database
        insert_query = "INSERT INTO url_mappings (long_url, short_url) VALUES (?, ?)"
        cursor.execute(insert_query, (long_url, short_url))
        conn.commit()
	
        return jsonify({"shortened_url": short_url})

# Reference: https://www.geeksforgeeks.org/redirecting-to-url-in-flask/
@app.route('/<short_url>')
def redirect_to_long_url(short_url):
    with sqlite3.connect("urls.db") as conn:
        cursor = conn.cursor()
        find_long_url_query = "SELECT long_url FROM url_mappings WHERE short_url=?"
        cursor.execute(find_long_url_query, (short_url,))
        row = cursor.fetchone()

        if row:
            long_url = row[0]
            print(f"Redirecting to {long_url}")
            return redirect(long_url)
        else:
            abort(404)


if __name__ == '__main__': 
	app.run(debug=True) 
