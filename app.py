import os
import werkzeug
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
import json
from werkzeug.exceptions import HTTPException
from operator import itemgetter, attrgetter
from model import connect, select_all_from_table, create_ca_table, create_classlist_table,\
     create_exam_table, create_grades_table, create_test_table, create_mastersheet_table, create_settings_table,\
     create_subjects_table, create_subject_position_table, drop_table,delete_from_id, create_classes_table, create_terms_table,\
     create_settings_table, select_school_by_id, select_school_by_username,\
     select_school_by_email, insert_into_table, update_table, select_columns_by_attr, select_all_from_row, select_all_from_row_with_and, copy_table
from functions import random_string_generator, database, login_required

import base64
import logging

logging.basicConfig(level= logging.DEBUG)
logger = logging.getLogger()

# Configure application
app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config["SECRET_KEY"] = "precious_two"
app.config["SECURITY_PASSWORD_SALT"] = "precious"

@app.errorhandler(werkzeug.exceptions.MethodNotAllowed)
def handle_error(e):
    error = "Please Login to access link"
    flash(error)
    return render_template("login.html")


@app.errorhandler(werkzeug.exceptions.NotFound)
def handle_error2(e):
    error = "Sorry Link not available now"
    flash(error)
    return render_template("login.html")

# API
@app.route("/login", methods=["POST","GET"])
def login():
    try:
        if request.method == "POST":
            username = str(request.form.get("username"))
            password = str(request.form.get("password"))
            if username =="":
                error = "username field cannot be empty"
                # return render_template("login.html", error = error)
                return jsonify(message=error, data=False)
            if request.form.get("password")=="":
                error = "password field cannot be empty"
                # return render_template("login.html", error = error)
                return jsonify(message=error, data=False)
            # Query database for username
            rows = select_school_by_username(username)
            # Remember which user has logged in
            # Ensure username exists and password is correct
            if len(rows) == 0:
                error = "user does not exist"
                return jsonify(message=error, data=False)
            if not check_password_hash(rows[0]["admin_password"], password) and not check_password_hash(rows[0]["password"], password):
                error = "invalid username/password"
                # return render_template("login.html", error = error)
                return jsonify(message=error, status = 401, data=False)
            session["user_id"] = rows[0]["id"]
            # if rows[0]["username"] == "admin":
            #     # select all the schools
            #     all_schools = db.execute("SELECT * FROM school")
            #     # display them in admin portfolio
            #     return render_template("admin_page.html", schoolInfo = all_schools)
            # if account is confirmed render this
            if(rows[0]["confirmed"]== "true"):
                # tables = database(str(0))
                # classRows = select_all_from_table(tables["session_data"])
                # if remember me check box is checked
                if request.form.get("remember_me") == "checked":
                    # generate token
                    random_token = random_string_generator(12, string.ascii_letters+string.punctuation)
                    # generate series id
                    random_series = random_string_generator(12, string.ascii_letters+string.punctuation)
                    #set cookie
                    # resp = make_response(render_template("portfolio.html",schoolInfo = rows, clas = classRows))
                    resp = make_response(jsonify(message='success', data=True))
                    expire_date = datetime.datetime.now()
                    expire_date = expire_date + datetime.timedelta(days=90)
                    resp.set_cookie("series_id",random_series,expires=expire_date)
                    resp.set_cookie("main_token", random_token,expires=expire_date)
                    update_table('school', ["series", "token"], [random_series,generate_password_hash(random_token)], 'id', session["user_id"])
                    return resp
                    # return render portfolio
                # return render_template("portfolio.html", schoolInfo = rows, clas = classRows)
                return jsonify(message='success', data=True)

            # else if account is not confirmed render unconfirmed view
            else:
                return jsonify(message='success', data='unconfirmed_user')
        else:
            try:
                session["user_id"]
            except KeyError:
                # return render_template("login.html")
                return jsonify(message='fail', data=False)
            else:
                rows = select_school_by_id(session['user_id'])
                # if account is confirmed render this
                if(rows[0]["confirmed"]== "true"):
                    # tables = database(str(0))
                    rows = select_school_by_id(session['user_id'])
                    # classRows = select_all_from_table(tables['session_data'])
                    # return render portfolio
                    # return render_template("portfolio.html", schoolInfo = rows, clas = classRows)
                    return jsonify(message='success', data=True)

                # else if account is not confirmed render unconfirmed view
                else:
                    return jsonify(message='success', data='unconfirmed_user')
    except Exception as e:
        logger.error(e)
        return jsonify(message='fail', data=False)




#Webportal
@app.route("/")
def index():
    if not request.cookies.get("series_id"):
        session.clear()
        return render_template("login.html")

@app.route('/portfolio', methods=['GET'])
# @login_required
def portfolio():
    return render_template('portfolio.html')


