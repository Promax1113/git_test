import os,pathlib
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

@app.route("/")
def goto_login():
    return redirect("/login")


@app.get("/login")
def hello_world():
    return render_template('login.html')


@app.post("/login")
def process_login():
    result = None
    username = None
    password = None
    username = request.form['ffx']
    password = request.form['ffl']
    result = password_processing.password_check(username, password)
    if result == "Access granted!" or None:
        return redirect('/overview')
    return f"<h2>Result: {escape(result)}</h2>"


@app.get("/overview")
def menu():
    return render_template('index.html')


@app.post("/overview")
def get_password():
    global error
    global password
    name = request.form['name']
    session['name'] = name
    password = password_access.read_password(name)
    error = password
    print(password)
    if password == "Invalid Login! You did not login!":
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
    print(password)
    return render_template('password.html', name = password['name'], pass_details = password)
