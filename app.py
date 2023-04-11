from flask import Flask
from flask import Flask, request, redirect, jsonify
import redis
import string
import random

app = Flask(__name__)
r = redis.StrictRedis(host='localhost', port=6379, db=0)

@app.route('/', methods=['GET', 'POST'])
def index():
    short_url = ""
    if request.method == 'POST':
        url = request.form['url']
        short_id = generate_short_id()

        while r.get(short_id) is not None:
            short_id = generate_short_id()

        r.set(short_id, url)
        short_url = f'http://127.0.0.1:5000/{short_id}'

    return f'''
    <!doctype html>
    <html>
      <head>
        <title>URL Shortener</title>
        <style>
          body {{
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 0;
            background-color: #f5f5f5;
          }}
          .container {{
            max-width: 800px;
            margin: 0 auto;
            padding: 30px;
            background-color: white;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
            border-radius: 8px;
          }}
          h1 {{
            font-size: 30px;
            color: #333;
            margin-bottom: 30px;
          }}
          form {{
            display: flex;
            justify-content: space-between;
            align-items: center;
          }}
          input {{
            flex-grow: 1;
            padding: 10px 15px;
            font-size: 16px;
            border: 1px solid #ccc;
            border-radius: 4px;
          }}
          button {{
            font-size: 16px;
            color: white;
            background-color: #007bff;
            border: none;
            padding: 10px 20px;
            margin-left: 10px;
            cursor: pointer;
            border-radius: 4px;
          }}
          button:hover {{
            background-color: #0056b3;
          }}
          p {{
            font-size: 18px;
            color: #333;
            margin-top: 30px;
          }}
          a {{
            color: #007bff;
            text-decoration: none;
          }}
          a:hover {{
            text-decoration: underline;
          }}
        </style>
      </head>
      <body>
        <div class="container">
          <h1>URL Shortener</h1>
          <form method="post">
            <input type="url" name="url" placeholder="Enter URL" required>
            <button type="submit">Shorten URL</button>
          </form>
          {f'<p>Shortened URL: <a href="{short_url}" target="_blank">{short_url}</a></p>' if short_url else ""}
        </div>
      </body>
    </html>
    '''



def generate_short_id(length=6):
    characters = string.ascii_letters + string.digits
    short_id = ''.join(random.choice(characters) for _ in range(length))
    return short_id



@app.route('/<short_id>', methods=['GET'])
def redirect_url(short_id):
    url = r.get(short_id)

    if url is None:
        return "URL not found", 404

    return redirect(url.decode('utf-8'), code=302)

if __name__ == "__main__":
    app.run(debug=True)
