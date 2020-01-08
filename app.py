import os
import werkzeug
from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, jsonify, url_for, make_response
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions
from werkzeug.security import check_password_hash, generate_password_hash
import re
import datetime
from flask_mail import Message, Mail
from itsdangerous import URLSafeTimedSerializer
import random
import string
from requests.models import Response
from flask_weasyprint import HTML, render_pdf
import json
from werkzeug.exceptions import HTTPException
from operator import itemgetter, attrgetter
from functions import has_duplicate, login_required, database, render_portfolio, term_tables, drop_tables, grade, assign_student_position, assign_subject_position, passwordGen, initials, add_student, remove_student, render_class, render_portfolio,  session_term_check, new_term, generate_pins,check_confirmed
from model import connect, select_all_from_id, select_all_from_table, create_ca_table, create_classlist_table, create_exam_table, create_grades_table, create_test_table, create_mastersheet_table, create_settings_table, create_subjects_table, create_subject_position_table, drop_table,delete_from_id
import psycopg2.extras
from psycopg2 import sql

# Configure application
app = Flask(__name__)


# generate confirmation token given email
def generate_confirmation_token(email):
    serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    return serializer.dumps(email, salt=app.config['SECURITY_PASSWORD_SALT'])

# return email given confirmation token
def confirm_token(token, expiration=3600):
    serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    try:
        email = serializer.loads(
            token,
            salt=app.config['SECURITY_PASSWORD_SALT'],
            max_age=expiration
        )
    except:
        return False
    return email
# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config["SECRET_KEY"] = "precious_two"
app.config["SECURITY_PASSWORD_SALT"] = "precious"



app.config.update(dict(
    DEBUG = True,
    MAIL_SERVER = 'smtp.gmail.com',
    MAIL_PORT = 587,
    MAIL_USE_TLS = True,
    MAIL_USE_SSL = False,
    MAIL_USERNAME = "schoolresultnigeria@gmail.com",
    MAIL_PASSWORD = "gmailvenuse123",
))

mail = Mail(app)

conn = connect()
db = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)



@app.errorhandler(werkzeug.exceptions.MethodNotAllowed)
def handle_error(e):
    return render_template("apology.html")


@app.errorhandler(werkzeug.exceptions.NotFound)
def handle_error2(e):
    return render_template("apology.html")

@app.route("/")
def index():
    if not request.cookies.get("series_id"):
        session.clear()
        return render_template("login.html")
    else:
        user = db.execute("SELECT * FROM school WHERE token_id = :series", series = request.cookies.get("series_id"))
        if len(user) != 1:
            session.clear()
            return render_template("login.html")
        if not check_password_hash(user[0]["token"], request.cookies.get("main_token")):
            session.clear()
            error = " theft dedicated, leave the site"
            return render_template("login.html", error = error)
        session["user_id"] = user[0]["id"]
        # if account is confirmed render this
        if(user[0]["confirmed"]== "true"):
            return render_portfolio()
        # else if account is not confirmed render unconfirmed view
        else:
            return redirect('/unconfirmed')
