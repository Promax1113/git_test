import os,pathlib
import webbrowser
import time
from markupsafe import escape
from flask import Flask, request, redirect, render_template, session
from flask_session import Session

import password_processing
import password_access


pathlib.Path.mkdir(pathlib.Path(f"{password_access.userpath}/passwords"), exist_ok=True)



app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

error = None
password = None
name = None



@app.route("/")
def goto_login():
    return redirect("/login")


@app.get("/login")
def hello_world():
    if session['name'] == None:
        return render_template('login.html')
    else:
        return redirect("/overview")


@app.post("/login")
def process_login():
    result = None
    username = None
    password_f = None
    username = request.form['ffx']
    password_f = request.form['ffl']
    result = password_processing.password_check(username, password_f)
    if result == "Access granted!" or result == None:
        session['name'] = username
        return redirect('/overview')
    elif result == "Fuck off! Access denied!":
        return redirect('/login')
    return f"<h2>Result: {escape(result)}</h2>"


@app.get("/overview")
def menu():
    file_list = []
    index = 0
    print(session['name'])
    for file in os.listdir(f"{password_access.userpath}/passwords"):
        if file.endswith('.passfile'):
            index += 1
            file_list.append({'id': index, 'name': file.split(".")[0]})
    print(file_list)
    return render_template('index.html', passlist = file_list)


@app.post("/overview")
def get_password():
    global error
    global password
    global name
    name = request.form['name']
    password = password_access.read_password(name)
    error = password
    print(password)
    if password == "Invalid Login! You did not login!" or password == "File not found!":
        return redirect('/invalid')
    else:
        return redirect('/details')

@app.get("/invalid")
def invalid_menu():
    return render_template('invalid.html', name = error)

@app.post("/invalid")
def process_invalid():
    return redirect("/login")

@app.get("/details")
def get_password_details():
    if password == "File not found!" or password == "Invalid login! You did not login!":
        return redirect("/invalid")
    else:
        return render_template('password.html', name = name, pass_details = password)

@app.get("/logout")
def logout_page():
    return render_template("logout.html", logout_data = session['name'])

@app.post("/logout")
def process_logout():
    session['name'] = None
    return redirect("/login")
