from flask import Flask, render_template, request, session, redirect
import requests
import ibm_db
import re
import json
import webbrowser

app = Flask(__name__)
app.secret_key = 'a'
conn = ibm_db.connect("DATABASE=bludb;HOSTNAME=54a2f15b-5c0f-46df-8954-7e38e612c2bd.c1ogj3sd0tgtu0lqde00.databases.appdomain.cloud;PORT=32733;SECURITY=SSL;SSLServerCertificate=DigiCertGlobalRootCA.crt;UID=rgs84912;PWD=Su2nEUErWddmAoQU;", "", "")
print("connected")


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/home')
def home1():
    return render_template('index.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/meme')
def mem():
    return render_template('meme_input.html')


@app.route('/login')
def login_page():
    return render_template('login.html')


@app.route('/register')
def register():
    return render_template('register.html')


@app.route('/logout')
def logout():
    return render_template('index.html')


@app.route('/reg', methods=['POST', 'GET'])
def signup():
    msg = ''
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        sql = "SELECT * FROM NITHEESH_REGISTER WHERE EMAIL = ?"
        stmt = ibm_db.prepare(conn, sql)
        ibm_db.bind_param(stmt, 1, email)
        ibm_db.execute(stmt)
        account = ibm_db.fetch_assoc(stmt)
        print(account)
        if account:
            return render_template('login.html', error=True)
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = "Invalid Email Address!!"
        else:
            insert_sql = "INSERT INTO NITHEESH_REGISTER (EMAIL, PASSWORD) VALUES (?, ?)"
            prep_stmt = ibm_db.prepare(conn, insert_sql)
            ibm_db.bind_param(prep_stmt, 1, email)
            ibm_db.bind_param(prep_stmt, 2, password)
            ibm_db.execute(prep_stmt)
            msg = "You have successfully registered"
    return render_template('login.html', msg=msg)


@app.route('/log', methods=['POST', 'GET'])
def login_user():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        sql = "SELECT * FROM NITHEESH_REGISTER WHERE EMAIL=? AND PASSWORD=?"
        stmt = ibm_db.prepare(conn, sql)
        ibm_db.bind_param(stmt, 1, email)
        ibm_db.bind_param(stmt, 2, password)
        ibm_db.execute(stmt)
        account = ibm_db.fetch_assoc(stmt)
        print(account)
        if account:
            session['loggedin'] = True
            session['id'] = account['EMAIL']
            session['email'] = account['EMAIL']
            return redirect('/test')
        else:
            msg = "Incorrect Email/password"
            return render_template('login.html', msg=msg)
    else:
        return render_template('login.html')


@app.route('/test', methods=['POST', 'GET'])
def meme():
    op1 = ""  # Declare with default values
    op2 = ""

    if request.method == 'POST':
        keywords = request.form["key"]
        print(keywords)
        url = "https://humor-jokes-and-memes.p.rapidapi.com/jokes/search"
        querystring = {
            "exclude-tags": "nsfw",
            "keywords": keywords,
            "min-rating": "7",
            "include-tags": "one_liner",
            "number": "3",
            "max-length": "200"
        }
        headers = {
            "X-RapidAPI-Key": "b9768e88eamsheadfc1a1e560272p1aed75jsn17c60762162c",
            "X-RapidAPI-Host": "humor-jokes-and-memes.p.rapidapi.com"
        }
        response = requests.get(url, headers=headers, params=querystring)
        print(response.text)
        output = json.loads(response.text)
        print(output)
        op1 = output['memes'][0]['url']
        webbrowser.open(op1)
        op2 = output['memes'][1]['url']
        webbrowser.open(op2)

    return render_template('meme_input.html', output1=op1, output2=op2)


if __name__ == '__main__':
    app.run(debug=True)
