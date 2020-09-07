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

@app.route("/")
def index():
    if not request.cookies.get("series_id"):
        session.clear()
        return render_template("login.html")