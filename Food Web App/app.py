# Taiyo Hayes, tjhayes@usc.edu
# ITP 216, Fall 2022
# Section: 32081
# Homework 11
# Description: Create web app based on food database

from flask import Flask, redirect, render_template, request, session, url_for
import os
import sqlite3 as sl

app = Flask(__name__)
db = "favouriteFoods.db"


# root end point
# routes to login unless client has already logged in
@app.route("/")
def home():
    """
    Checks whether the user is logged in and returns appropriately.

    :return: renders login.html if not logged in,
                redirects to client otherwise.
    """
    # TODO: your code goes here and replaces 'pass' below
    if not session.get("logged_in"):
        return render_template('login.html', message="Please Login to Continue")
    else:
        return redirect(url_for('client'))


# client endpoint
# renders appropriate template (admin or user)
@app.route("/client")
def client():
    """
    Renders appropriate template (admin or user)

    :return: redirects home if not logged in,
                renders admin.html if logged in as admin,
                user.html otherwise
    """
    # TODO: your code goes here and replaces 'pass' below
    if not session.get("logged_in"):
        return redirect(url_for('home'))
    else:
        if session.get("username") == "admin":
            return render_template('admin.html', username=session.get("username"), message="Welcome back.", result=db_get_user_list())
        else:
            return render_template('user.html', username=session.get("username"), fav_food=db_get_food(session.get("username")))


# create user endpoint (admin only)
# adds new user to db, then re-renders admin template
@app.route("/action/createuser", methods=["POST", "GET"])
def create_user():
    """
    Callable from admin.html only
    Adds a new user to db by calling db_create_user, then re-renders admin template

    :return: redirects to home if user not logged in,
                re-renders admin.html otherwise
    """
    # TODO: your code goes here and replaces 'pass' below
    if session["logged_in"]:
        db_create_user(request.form["username"], request.form["password"])
        return render_template('admin.html', username=session.get("username"), message="Welcome back.",
                               result=db_get_user_list())
    return redirect(url_for('home'))


# remove user endpoint (admin only)
# removes user from db, then re-renders admin template
@app.route("/action/removeuser", methods=["POST", "GET"])
def remove_user():
    """
    Callable from admin.html only
    Removes user from the db by calling db_remove_user, then re-renders admin template.

    :return: redirects to home if user not logged in,
                re-renders admin.html otherwise
    """
    # TODO: your code goes here and replaces 'pass' below
    if session["logged_in"]:
        db_remove_user(request.form["username"])
        return render_template('admin.html', username=session.get("username"), message="Welcome back.",
                               result=db_get_user_list())
    return redirect(url_for('home'))


# set food endpoint (user only)
# updates user food, then re-renders user template
@app.route("/action/setfood", methods=["POST", "GET"])
def set_food():
    """
    Callable from user.html only,
    Updates user food by calling db_set_food, then re-renders user template

    :return: redirects to home if user not logged in,
                re-renders user.html otherwise
    """
    # TODO: your code goes here and replaces 'pass' below
    if session.get("logged_in"):
        db_set_food(session.get("username"), request.form["set_fav_food"])
        return render_template('user.html', username=session.get("username"), fav_food=db_get_food(session.get("username")))
    return redirect(url_for('home'))


# login endpoint
# allows client to log in (checks creds)
@app.route("/login", methods=["POST", "GET"])
def login():
    """
    Allows client to log in
    Calls db_check_creds to see if supplied username and password are correct

    :return: redirects to client if login correct,
                redirects back to home otherwise
    """
    # TODO: your code goes here and replaces 'pass' below
    if request.method == "POST":
        if db_check_creds(request.form["username"], request.form["password"]):
            session["logged_in"] = True
            session["username"] = request.form["username"]
            session["password"] = request.form["password"]
            return redirect(url_for('client'))
    return redirect(url_for('home'))


# logout endpoint
@app.route("/logout", methods=["POST", "GET"])
def logout():
    """
    Logs client out, then routes to login
    Remove the user from the session
    :return: redirects back to home
    """
    # TODO: your code goes here and replaces 'pass' below
    if request.method == "POST":
        session['logged_in'] = False
        session.pop('username', None)
    return redirect(url_for('home'))


def db_get_user_list() -> dict:
    """
    Queries the DB's userfoods table to get a list
    of all the user and their corresponding favorite food for display on admin.html.
    Called to render admin.html template.

    :return: a dictionary with username as key and their favorite food as value
                this is what populates the 'result' variable in the admin.html template
    """
    # TODO: your code goes here and replaces 'pass' below
    conn = sl.connect('favouriteFoods.db')
    cursor = conn.cursor()
    stmt = "SELECT * FROM userfoods"
    data = dict(cursor.execute(stmt).fetchall())
    return data

def db_create_user(un: str, pw: str) -> None:
    """
    Add provided user and password to the credentials table
    Add provided user to the userfoods table
    and sets their favorite food to "not set yet".
    Called from create_user() view function.

    :param un: username to create
    :param pw: password to create
    :return: None
    """
    # TODO: your code goes here and replaces 'pass' below
    conn = sl.connect('favouriteFoods.db')
    curs = conn.cursor()
    stmt1 = "INSERT OR IGNORE INTO credentials (username, password) VALUES (?, ?)"
    v1 = (un, pw,)
    stmt2 = "INSERT OR IGNORE INTO userfoods (username, food) VALUES (?, ?)"
    v2 = (un, "not set yet")
    curs.execute(stmt1, v1)
    curs.execute(stmt2, v2)
    conn.commit()

def db_remove_user(un: str) -> None:
    """
    Removes provided user from all DB tables.
    Called from remove_user() view function.

    :param un: username to remove from DB
    :return: None
    """
    # TODO: your code goes here and replaces 'pass' below
    conn = sl.connect('favouriteFoods.db')
    curs = conn.cursor()
    v = (un,)
    stmt1 = "DELETE FROM credentials WHERE username = ?"
    stmt2 = "DELETE FROM userfoods WHERE username = ?"
    curs.execute(stmt1, v)
    curs.execute(stmt2, v)
    conn.commit()


def db_get_food(un: str) -> str:
    """
    Gets the provided user's favorite food from the DB.
    Called to render user.html fav_food template variable.

    :param un: username to get favorite food of
    :return: the favorite food of the provided user as a string
    """
    # TODO: your code goes here and replaces 'pass' below
    conn = sl.connect('favouriteFoods.db')
    curs = conn.cursor()
    stmt = "SELECT food FROM userfoods WHERE username = ?"
    v = (un,)
    food = curs.execute(stmt, v).fetchone()
    return food[0]

def db_set_food(un: str, ff: str) -> None:
    """
    Sets the favorite food of user, un param, to new incoming ff (favorite food) param.
    Called from set_food() view function.

    :param un: username to update favorite food of
    :param ff: user's new favorite food
    :return: None
    """
    # TODO: your code goes here and replaces 'pass' below
    conn = sl.connect('favouriteFoods.db')
    curs = conn.cursor()
    stmt = "UPDATE userfoods SET food = ? WHERE username = ? "
    v = (ff, un,)
    curs.execute(stmt, v)
    conn.commit()


def db_check_creds(un: str, pw: str) -> bool:
    """
    Checks to see if supplied username and password are in the DB's credentials table.
    Called from login() view function.

    :param un: username to check
    :param pw: password to check
    :return: True if both username and password are correct, False otherwise.
    """
    # TODO: your code goes here and replaces 'pass' below
    conn = sl.connect('favouriteFoods.db')
    cursor = conn.cursor()
    v = (un,)
    stmt = "SELECT password FROM credentials WHERE username=?"
    passw = cursor.execute(stmt, v).fetchone()
    if passw is None:
        return False
    elif pw == passw[0]:
        return True
    return False


if __name__ == "__main__":
    # Unit test of db_get_user_list()
    # TODO: Unit test your other db functions here
    assert db_check_creds('alice', 'alicesSecurePassWord') is True
    assert db_check_creds('admin', 'passwords') is True
    #db_get_user_list()
    #db_get_food()

    # Start flask app
    app.secret_key = os.urandom(12)
    app.run(debug=True)
