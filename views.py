from flask import Blueprint, render_template, request, url_for, redirect, session
import csv
from werkzeug.security import generate_password_hash, check_password_hash
from db import db_connection

#sessions are nonpermanent, are stored on the device and will be lost when the browser is closed
views = Blueprint("views", __name__)

@views.route("/")
def menu():
    return render_template("menu.html")

@views.route("/browse/")
def browse():
    return render_template("browse.html")

@views.route("/news/")
def news():
    return render_template("news.html")

@views.route("/lists/")
def my_list():
    #add an input box to the html to access the list of a certain user or a button that says "my favourites/my list", and add a checker here so that the program knows if the user is the owner of the list as only the owner of the list should have permissions to remove songs from the list
    return render_template("lists.html")

@views.route("/contact/")
def contact():
    return render_template("contact.html")

@views.route("/signup/", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
       #capturing data from the signup form
       username = request.form["regUsername"]
       email = request.form["regEmail"]
       password = request.form["regPassword"]
       password_hash = generate_password_hash(password)
       #parsing submitted information into the database
       connection = db_connection()
       connection.execute("INSERT INTO users (username, email, password_hash) VALUES (?, ?, ?)", (username, email, password_hash))
       connection.commit()
       connection.close()
       return redirect(url_for("views.login"))
    elif "username" in session:
        return redirect(url_for("views.account"))
    else:
       return render_template("signup.html")


@views.route("/login/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["nm"] #takes the user input from the form on the page
        password = request.form["regPassword"]
        connection = db_connection()
        username = connection.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone() #fetchone - retrieves the one entry that contains exactly ? fetchall - retrieves all that contains ?
        connection.close()
        if username and check_password_hash(username["password_hash"], password):
            session.permanent = True #session is not actually permanent, as a time can be, and is, set
            session["username"] = username["username"]
            return redirect(url_for("views.account"))
        return redirect(url_for("views.account")) #takes the user input as the username
    elif "username" in session:
        return redirect(url_for("views.account"))
    else:
        return render_template("login.html")

#edit account information on profile page:

@views.route("/account") #change this to /lists/mylist/ everywhere
def account():
    if "username" in session:
       return render_template("userlists.html", username=session["username"]) #EDIT THIS, needs to lead to THE USERS OWN LIST WITH edit permissions on
    else:
        return redirect(url_for("views.login"))

@views.route("/logout")
def logout():
    session.pop("username", None) #removes the input username from the session
    return redirect(url_for("views.login"))

@views.route("/go_myaccount")
def go_myaccount():
    return redirect(url_for("views.profile", name="Cal"))
