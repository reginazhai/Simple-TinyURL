# import flast module
from flask import Flask, redirect, jsonify, render_template, request, abort
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from urllib.parse import urlparse, urljoin
import sqlite3
import string

# instance of flask application
app = Flask(__name__)

# Rate limiting
limiter = Limiter(app=app, key_func=get_remote_address,
                  default_limits=["1000 per day", "100 per hour"])

# Constants
CHARACTERS = string.digits + string.ascii_letters
CHAR_TO_IND = {c: i for i, c in enumerate(CHARACTERS)}

# Reference: https://www.geeksforgeeks.org/how-to-build-a-web-app-using-flask-and-sqlite-in-python/;
# https://www.sqlitetutorial.net/sqlite-python/;
# https://www.geeksforgeeks.org/how-to-return-a-json-response-from-a-flask-api/

# SQLite database connection
conn = sqlite3.connect('urls.db')
# Create table if not exists
cur = conn.cursor()
cur.execute('''CREATE TABLE IF NOT EXISTS url_mappings
             (id integer PRIMARY KEY AUTOINCREMENT, 
		     long_url TEXT NOT NULL)''')

print("Database connected!")

# Using Base62 encoding to generate short URL
def generate_short_url(id):
    short_url = ""
    while id > 0:
        short_url = CHARACTERS[id % 62] + short_url
        id = id // 62

    # Add padding to make the short URL length 6
    short_url = "0" * (6 - len(short_url)) + short_url
    return short_url

def decode_short_url(short_url):
    print(f"Decoding {short_url}")
    # Remove padding
    short_url = short_url.lstrip("0")
    id = 0
    for char in short_url:
        id = id * 62 + CHAR_TO_IND[char]
    return id

# Possible Improvement: add error pages for different errors

# home route that returns below text when root url is accessed
@app.route('/') 
def index():
	return render_template('index.html') 

# API endpoint to shorten URL
@app.route('/shorten', methods=['POST'])
def shorten_url_api():
    data = request.json
    long_url = data.get('url')

    # Check if the long URL is provided
    if not long_url:
        return jsonify({"error": "URL is required"}), 400
    
    # Check if the URL is valid
    final_url = urlparse(urljoin(long_url, "/"))
    is_correct = (all([final_url.scheme, final_url.netloc, final_url.path]) 
                and len(final_url.netloc.split(".")) > 1)
    if not is_correct:
        return jsonify({"error": "Invalid URL"}), 400
	
    with sqlite3.connect("urls.db") as conn: 
        cursor = conn.cursor() 

        # Check if the URL already exists in the database
        find_short_url_query = "SELECT id FROM url_mappings WHERE long_url=?"
        cursor.execute(find_short_url_query, (long_url,))
        exist_short_url = cursor.fetchone()
        if exist_short_url:
            return jsonify({"shortened_url": exist_short_url[0]})

        # Insert new mapping into the database
        insert_query = "INSERT INTO url_mappings (long_url) VALUES (?)"
        cursor.execute(insert_query, (long_url,))
        id = cursor.lastrowid
        conn.commit()

        # Generate a new short code
        short_url = generate_short_url(id)

        return jsonify({"shortened_url": short_url})

# Reference: https://www.geeksforgeeks.org/redirecting-to-url-in-flask/
@app.route('/<short_url>')
def redirect_to_long_url(short_url):
    with sqlite3.connect("urls.db") as conn:
        id = decode_short_url(short_url)
        cursor = conn.cursor()
        find_long_url_query = "SELECT long_url FROM url_mappings WHERE id=?"
        cursor.execute(find_long_url_query, (id,))
        row = cursor.fetchone()

        if row:
            long_url = row[0]
            print(f"Redirecting to {long_url}")
            return redirect(long_url)
        else:
            abort(404)


if __name__ == '__main__': 
	app.run(debug=True) 
