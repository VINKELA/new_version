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
from functions import has_duplicate, login_required, database, render_portfolio, term_tables, drop_tables, grade, \
    assign_student_position, assign_subject_position, passwordGen, initials, add_student, remove_student, render_class, \
        render_portfolio,  session_term_check, new_term, generate_pins,check_confirmed
from model import connect, select_all_from_table, create_ca_table, create_classlist_table,\
     create_exam_table, create_grades_table, create_test_table, create_mastersheet_table, create_settings_table,\
     create_subjects_table, create_subject_position_table, drop_table,delete_from_id, create_classes_table, create_terms_table,\
     create_settings_table, select_school_by_id, select_school_by_username,\
     select_school_by_email, insert_into_table, update_table, select_columns_by_attr, \
         select_all_from_row, alter_table, drop_column, select_current_term,update_term_settings
import psycopg2.extras
from psycopg2 import sql

# Configure application
app = Flask(__name__)

# send message to email
def send_email(to, subject, template, sender_email):
    msg = Message(
        subject,
        recipients=[to],
        html=template,
        sender=sender_email
    )
    mail.send(msg)

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


@app.errorhandler(werkzeug.exceptions.MethodNotAllowed)
def handle_error(e):
    return render_template("apology.html", error = e)


@app.errorhandler(werkzeug.exceptions.NotFound)
def handle_error2(e):
    return render_template("apology.html", error = e)

@app.route("/")
def index():
    # if user do not have cookies clear and existing session and serve homepage
    if not request.cookies.get("series_id"):
        session.clear()
        return render_template("login.html")
    else:
        # if user has cookies, select user detail from database
        user = select_all_from_row('school', 'token_id', request.cookies.get('series_id'))
        #if cookies has expired, serve home page
        if len(user) != 1:
            session.clear()
            return render_template("login.html")
        # if token doesn't match warn against hack attempt
        if not check_password_hash(user[0]["token"], request.cookies.get("main_token")):
            session.clear()
            error = " theft dedicated, leave the site"
            return render_template("login.html", error = error)
        # else auticate user and begin session
        session["user_id"] = user[0]["id"]
        # if account is confirmed render this
        if(user[0]["confirmed"]== "true"):
            return render_portfolio()
        # else if account is not confirmed render unconfirmed view
        else:
            return redirect('/unconfirmed')
    

@app.route("/register", methods=["GET", "POST"])
def register():
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure email was submitted
        if not request.form.get("email"):
            error = "you must provide email"
            return render_template("register.html", error = error)
        if not request.form.get("school_name"):
            error = "you must provide school name"
            return render_template("register.html", error = error)
        # Ensure term was submitted
        if not request.form.get("term"):
            error = "you must provide current term"
            return render_template("register.html", error = error)
        # ensure session was submitted
        if not request.form.get("school_session"):
            error = "you must provide current session"
            return render_template("register.html", error = error)
        # ensure username was submitted
        if not request.form.get("username"):
            error = "you must provide a unique username"
            return render_template("register.html", error = error)
        # ensure the username is not taken
        username_check = select_school_by_username(request.form.get('username').lower())
        if  username_check:
            error = "username: "+request.form.get("username")+" already taken, choose another one"
            return render_template("register.html", error = error)
        email_check = select_school_by_email(request.form.get('email').lower())
        if  email_check:
            error = "Another account has been opened with email: "+request.form.get("email")
            return render_template("register.html", error = error)

        # Ensure password was submitted
        if not request.form.get("password"):
            error = "you must provide password"
            return render_template("register.html", error = error)

        # Ensure confirmation was submitted
        if not request.form.get("confirmation"):
            error = "you must provide confirmation"
            return render_template("register.html", error = error)

        # Ensure password and confirmation match
        if (request.form.get("password") != request.form.get("confirmation")):
            error = "password and confirmation do not match"
            return render_template("register.html", error = error)

        password = request.form.get("password")
        if len(password) < 8:
            error = "Make sure your password is at lest 8 letters"
            return render_template("register.html", error = error)
        general_password = passwordGen()
        session['general_password'] = general_password
        insert_into_table('school',\
        ['school_name', 'email', 'username', 'password', 'admin_password', 'current_session', 'current_term','registered_on'],\
        [request.form.get('school_name').upper(), request.form.get("email").lower(),request.form.get("username").lower(),generate_password_hash(general_password),generate_password_hash(request.form.get("password")),request.form.get("school_session"),request.form.get("term"),datetime.datetime.now()])
        # Query database for username
        rows = select_school_by_username(request.form.get('username'))
        print('row is {}'.format(rows))
        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]
        tables = database(0)
        create_terms_table(tables['terms'])
        create_classes_table(tables['classes'])
        create_settings_table(tables['settings'], tables['classes'])
        token = generate_confirmation_token(request.form.get("email"))
        confirm_url = url_for('confirm_email', token=token, _external=True)
        html = render_template('confirm_email.html', confirm_url=confirm_url, password = general_password)
        subject = "Please confirm your Account"
        try:
            send_email(request.form.get("email"), subject, html, 'schoolresultnigeria@gmail.com')
        except Exception as e:
            print(e)
        return render_template("unconfirmed.html", schoolInfo=rows)
    else:
        return render_template("register.html")

@app.route("/username_check", methods=["POST"])
def register_check():
    if request.method == "POST":
        # Query database for username
        rows = select_school_by_username(request.form.get('username'))
        if not rows:
            return "true"
        else:
            return "false"


@app.route("/email_check", methods=["POST"])
def email_check():
    if request.method == "POST":
        # Query database for email
        rows = select_school_by_email(request.form.get('email'))
        if not rows:
            return "true"
        else:
            return "false"

@app.route("/confirm_email", methods=["GET", "POST"])
def confirm_email():
    token = request.args.get('token')
    email = confirm_token(token)
    if  not email:
        error = 'The confirmation link is invalid or has expired.'
    else:
        user = select_school_by_email(email)
        if user[0]["confirmed"]:
            error = 'Account already confirmed. Please login.'
        else:
            update_table('school',['confirmed', 'confirmed_on'], [1, 'NOW()'], 'email', email)
            error = 'You have confirmed your account.  Thanks!'
    session.clear()
    flash(error)
    return render_template('login.html')

@app.route("/resend_confirmation", methods=["GET", "POST"])
@login_required
def resend_confirmation():
    user = select_school_by_id(session['user_id'])
    general_password = passwordGen()
    update_table('school', 'password', generate_password_hash(general_password),'id', session['user_id'])
    token = generate_confirmation_token(user[0]["email"])
    confirm_url = url_for('confirm_email', token=token, _external=True)
    html = render_template('confirm_email.html', confirm_url=confirm_url, password=general_password)
    subject = "Please confirm your Account"
    try:
        send_email(user[0]["email"], subject, html,'Schoolresultnigeria@gmail.com')
    except Exception as e:
        print(e)
    flash('A new confirmation email has been sent.', 'success')
    return redirect('/unconfirmed')

@app.route("/login", methods=["POST","GET"])
def login():
    if request.method == "POST":
        if request.form.get("username")=="":
            error = "username field cannot be empty"
            return render_template("login.html", error = error)
        if request.form.get("password")=="":
            error = "password field cannot be empty"
            return render_template("login.html", error = error)
        # Query database for username
        rows = select_school_by_username(request.form.get("username"))
        # Remember which user has logged in
        # Ensure username exists and password is correct
        if len(rows):
            error = "user does not exist"
            return render_template ("login.html", error=error)
        if not check_password_hash(rows[0]["admin_password"], request.form.get("password")) and not check_password_hash(rows[0]["password"], request.form.get("password")):
            error = "invalid username/password"
            return render_template("login.html", error = error)
        session["user_id"] = rows[0]["id"]
        if rows[0]["username"] == "admin":
            # select all the schools
            all_schools = select_all_from_table('school')
            # display them in admin portfolio
            return render_template("admin_page.html", schoolInfo = all_schools)
        # if account is confirmed render this
        if(rows[0]["confirmed"]):
            tables = database(0)
            classRows = select_all_from_table(tables['classes'])
            # if remember me check box is checked
            if request.form.get("remember_me") == "checked":
                # generate token
                random_token = random_string_generator(12, string.ascii_letters+string.punctuation)
                # generate series id
                random_series = random_string_generator(12, string.ascii_letters+string.punctuation)
                #set cookie
                resp = make_response(render_template("portfolio.html",schoolInfo = rows, clas = classRows))
                expire_date = datetime.datetime.now()
                expire_date = expire_date + datetime.timedelta(days=90)
                resp.set_cookie("series_id",random_series,expires=expire_date)
                resp.set_cookie("main_token", random_token,expires=expire_date)
                update_table('school', ['token_id', 'token'], \
                [random_series,generate_password_hash(random_token)], 'id', session['user_id'])
                return resp
                # return render portfolio
            return render_template("portfolio.html", schoolInfo = rows, clas = classRows)
        # else if account is not confirmed render unconfirmed view
        else:
            return redirect('/unconfirmed')
    else:
        try:
            session["user_id"]
        except KeyError:
            return render_template("login.html")
        else:
            rows = select_school_by_id(session['user_id'])
            # if account is confirmed render this
            if(rows[0]["confirmed"]):
                tables = database(str(0))
                rows = select_school_by_id(session['user_id'])
                classRows = select_all_from_table(tables['classes'])
                # return render portfolio
                return render_template("portfolio.html", schoolInfo = rows, clas = classRows)

            # else if account is not confirmed render unconfirmed view
            else:
                return redirect('/unconfirmed')


@app.route("/subject_check", methods=["POST"])
@login_required
@check_confirmed
def subject_check():
    tables = database(int(request.form.get("class_id")))
    # Query database for username
    subject_row = select_all_from_row(tables['subjects'], 'name', request.form.get('subject_name').lower())
    if len(subject_row) > 0:
        return "false"
    else:
        return "true"

@app.route("/subject_name_check", methods=["POST"])
@login_required
@check_confirmed
def subject_name_check():
    tables = database(int(request.form.get("class_id")))
    if request.form.get("previous") == request.form.get("subject_name"):
        return "true"
    else:
        # Query database for subject name
        subject_row = select_all_from_row(tables['subjects'],'name', request.form.get('subject_name').lower())
        if len(subject_row) > 0:
            return "false"
        else:
            return "true"



@app.route("/editclass_check", methods=["POST"])
@login_required
@check_confirmed
def editclass_check():
    class_id = str(request.form.get("class_id"))
    password = request.form.get("password")
    tables = database(class_id)
    # Query database for username
    class_row = select_all_from_row(tables['classes'], 'id', class_id)
    rows = select_school_by_id(session['user_id'])
    if not check_password_hash(rows[0]["admin_password"],password) and not check_password_hash(class_row[0]["password"],password ):
        return "false"
    else:
        return "true"


@app.route("/change_password", methods=["POST", "GET"])
def change_password():
    if request.method == "POST":
        # Query database for email
        if request.form.get("email") == "":
            error = "provide the email your account was registered with"
            flash(error)
            return render_template("change_password_form.html", error = error)
        rows = select_school_by_email(request.form.get("email").lower())
        if len(rows) != 1:
            error = request.form.get("email")+" not associated with any registered account"
            flash(error)
            return render_template("change_password_form.html", error = error)
        token = generate_confirmation_token(request.form.get("email"))
        confirm_url = url_for('password_changed', token=token, _external=True)
        html = render_template('password.html', confirm_url=confirm_url)
        subject = "change password"
        try:
            send_email(request.form.get("email"), subject, html, 'Schoolresultest@gmail.com')
        except Exception as e:
            print(e)
        error = "follow the link sent to "+request.form.get("email") +" to change password"
        flash(error)
        return render_template("login.html", error=error)
    else:
        return render_template("change_password_form.html")


@app.route("/password_changed", methods=["GET", "POST"])
def password_changed():
    if request.method == "POST":
        email = request.form.get("email")
        if request.form.get("password") == "":
            error = "password is empty"
            return render_template("password_changed.html", error = error, email = email)
        if len(request.form.get("password")) < 8:
            error = "Make sure your password is at lest 8 letters"
            return render_template("password_changed.html", error = error)

        if request.form.get("confirmation") == "":
            error = "confirmation is empty"
            return render_template("password_changed.html", error = error, email = email)
        if request.form.get("password") != request.form.get("confirmation"):
            error = "password and confirmation do not match"
            return render_template("password_changed", error = error, email = email)
        #change the password
        update_table('school', 'admin_password',generate_password_hash(request.form.get("password")), 'email', email )
        error = 'You have changed your password.  Thanks!'
        session.clear()
        flash(error)
        return render_template('login.html',error=error)
    else:
        token = request.args.get('token')
        email = confirm_token(token)
        if  not email:
            error = 'The  link is invalid or has expired.'
            flash(error)
            return render_template("login.html", error = error)
        else:
            return render_template("password_changed.html", email = email)


@app.route("/login_check", methods=["POST"])
def login_check():
    if request.method == "POST":
        # Query database for username
        rows = select_school_by_username(request.form.get('username').lower())
        if len(rows) == 0:
            return "fail"
        # Ensure username exists and password is correct
        if check_password_hash(rows[0]["password"], request.form.get("password")):
            return "true"
        elif check_password_hash(rows[0]["admin_password"], request.form.get("password")):
            return "true"
        else:
            return "fail"

@app.route("/email_ajax", methods=["POST"])
def email_ajax():
    if request.method == "POST":
        # Query database for username
        rows = select_school_by_email(request.form.get('email'))
        # Remember which user has logged in
        # Ensure username exists and password is correct
        if len(rows) < 1:
            return "fail"
        else:
            return "pass"


@app.route("/class_name", methods=["POST"])
@login_required
@check_confirmed
def class_name():
    if request.method == "POST":
        tables = database(str(0))
        class_name=request.form.get("classname").lower()
        old_name = request.form.get("oldname").lower()
        if class_name != old_name:
            row_class = select_all_from_row(tables['classes'],'classname', class_name)
            if len(row_class) < 1: 
                return jsonify(value="pass")
            else:
                return jsonify(value="fail")
        return jsonify(value="pass")

@app.route("/class_name2", methods=["POST"])
def class_name2():
    if request.method == "POST":
        tables = database(str(0))
        # Query database for username
        rows = select_all_from_row(tables['classes'],'classname', request.form.get('classname').lower() )
        if len(rows) == 0:
            return "pass"
        else:
            return "fail"

        

@app.route("/class_name_check", methods=["POST"])
@login_required
@check_confirmed
def class_name_check():
    if request.method == "POST":
        new_name = request.form.get("new_name")
        formerly = request.form.get("former")
        tables = database(str(0))
        if new_name != formerly:
            # Query database for username
            rows = select_all_from_row(tables['classes'],'classname', request.form.get('new_name').lower() )
            if len(rows) == 0:
                return "pass"
            else:
                return "fail"
        else:
            return "pass"

@app.route("/createClass", methods=["GET", "POST"])
@login_required
@check_confirmed
def createClass():
    session["info"]={}
    tables = database(str(0))
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        schoolrow = select_school_by_id(session['user_id'])
        # Ensure schoolname was submitted
        if not request.form.get("class_name"):
            error = "Provide a class name"
            return render_template("createClassForm.html", error=error, school=schoolrow)
        row = select_all_from_row(tables['classes'], 'classname', request.form.get('class_name').lower())
        if len(row) > 0:
            error = "class already exist"
            return render_template("createClassForm.html", error=error, schoolInfo=schoolrow)
        if not request.form.get("section"):
            error = "Provide your section"
            return render_template("createClassForm.html", error=error, schoolInfo=schoolrow)
        if not request.form.get("firstname"):
            error = "Provide your firstname"
            return render_template("createClassForm.html", error=error, schoolInfo=schoolrow)
        if not request.form.get("surname"):
            error = "Provide your surname"
            return render_template("createClassForm.html", error=error, schoolInfo=schoolrow)
        if not request.form.get("no_of_students"):
            error = "Provide the number of students in class"
            return render_template("createClassForm.html", error=error, schoolInfo=schoolrow)
        try:
            int(request.form.get("no_of_students"))
        except ValueError:
            error = "Provide a number for the students in class"
            return render_template("createClassForm.html", error=error, schoolInfo=schoolrow)
        if not request.form.get("ca"):
            error = "Provide the maximum ca score"
            return render_template("createClassForm.html", error=error, schoolInfo=schoolrow)
        if not request.form.get("test"):
            error = "Provide the maximum test score"
            return render_template("createClassForm.html", error=error, schoolInfo=schoolrow)
        if not request.form.get("exam"):
            error = "Provide the maximum exam score"
            return render_template("createClassForm.html", error=error, schoolInfo=schoolrow)
        try:
            int(request.form.get("ca"))
        except ValueError:
            error = "Provide a number for the class maximum ca"
            return render_template("createClassForm.html", error=error, schoolInfo=schoolrow)
        try:
            int(request.form.get("test"))
        except ValueError:
            error = "Provide a number for the class maximum test"
            return render_template("createClassForm.html", error=error, schoolInfo=schoolrow)
        try:
            int(request.form.get("exam"))
        except ValueError:
            error = "Provide a number for the class maximum exam"
            return render_template("createClassForm.html", error=error, schoolInfo=schoolrow)
        sum = int(request.form.get("ca"))+int(request.form.get("exam"))+int(request.form.get("test"))
        if sum != 100:
            error = "ca + exam + test must be equal to 100"
            return render_template("createClassForm.html", error=error)
        if not request.form.get("password"):
            error = "Provide a class password"
            return render_template("createClassForm.html", error=error)
        if len(request.form.get("password")) < 6:
            error = "password should be at least 6 digit long"
            return render_template("createClassForm.html", error=error)
        if not request.form.get("confirmation"):
            error = "Provide a password confirmation"
            return render_template("createClassForm.html", error=error)
        # Ensure password and confirmation match
        if (request.form.get("password") != request.form.get("confirmation")):
            error = "Provide a password is not equal to  confirmation"
            return render_template("createClassForm.html", error=error)
        session["info"]["surname"] = request.form.get("surname")
        session["info"]["firstname"] = request.form.get("firstname")
        session["info"].update({"className":request.form.get("class_name").upper()})
        session["info"]["ca_max"] = request.form.get("ca")
        session["info"]["test_max"] = request.form.get("test")
        session["info"]["exam_max"] = request.form.get("exam")
        session["info"]["noOfStudents"] = request.form.get("no_of_students")
        session["info"]["password"] = request.form.get("password")
        session["info"]["section"] = request.form.get("section")
        schoolrow = select_school_by_id(session['user_id'])
        return render_template("classListForm.html",n = int(request.form.get("no_of_students")), schoolInfo = schoolrow, class_name=session["info"]["className"] )
    else:
        schoolId = session['user_id']
        schoolrow = select_school_by_id(schoolId)
        return render_template("createClassForm.html",schoolInfo = schoolrow)

@app.route("/confirm_classlist", methods=["POST"])
@check_confirmed
@login_required
def confirm_classlist():
    session["all_students"]=[]
    #declare an array of dicts
    rows = select_school_by_id(session[user_id])
    #fill classlist
    g = int(session["info"]["noOfStudents"])
    # each student will be an element of the array
    for i in range(g):
        surname = "s"+str(i)
        firstname = "f"+str(i)
        othername = "o"+str(i)
        sex = "g"+str(i)
        session["all_students"].append((request.form.get(surname), request.form.get(firstname), request.form.get(othername), request.form.get(sex)))
    session["creating_class"]= False
    #return classlist.html
    return render_template("confirm_classlist.html",schoolInfo = rows, students= session["all_students"], classinfo=session['info'])


@app.route("/classCreated", methods=["POST"])
@check_confirmed
@login_required
def classCreated():
    if session['creating_class']:
        error = session["info"]["className"]+" has been created"
        return render_portfolio(error)
    session["creating_class"] = True
    tables = database(str(0))
    class_data = select_all_from_row(tables[classes], 'classname', session["info"]["className"].lower())
    if len(class_data) > 0:
        error = session["info"]["className"]+" already exist"
        flash(error)
        return render_portfolio()
    class_settings = select_all_from_table(tables['settings'])
    rows = select_school_by_id(session['user_id'])
    classId = insert_into_table(tables['classes'],['surname','firstname','classname', 'password','section','ca', 'test', 'exam'],[session["info"]["surname"],session["info"]["firstname"], session["info"]["className"].lower(),generate_password_hash(session["info"]["password"]),session["info"]["section"],session["info"]["ca_max"],session["info"]["test_max"],session["info"]["exam_max"]])
    
    term_tables(classId)
    tables = database(classId)
    # fill classlist
    sort_names = sorted(session["all_students"], key=itemgetter(0))
    #generate pins
    pins = generate_pins(10,len(sort_names))
    # fill classlist
    i = 0
    for name in sort_names:
        student_id = insert_into_table(tables['classlist'],\
        ['surname', 'firstname', 'othername','sex','pin'],\
        [name[0].upper(),name[1].upper(), name[2].upper(),name[3], pins[i]])
        insert_into_table(tables['ca'], 'id', student_id)
        insert_into_table(tables['test'], 'id', student_id)
        insert_into_table(tables['exam'], 'id', student_id)
        insert_into_table(tables['mastersheet'], 'id', student_id)
        insert_into_table(tables['subject_position'], 'id', student_id)
        insert_into_table(tables['grades'], 'id', student_id)
        i = i + 1

    no_classlist = select_all_from_table(tables['classlist'])
    # the first class
    if len(class_settings) < 1 :
        insert_into_table(tables['settings'], 'id', class_id)
    else:
        insert_into_table(tables['settings'],['grading_type' ,'background_color' ,'text_color' ,'line_color','background_font','ld_position','l_font' ,'l_weight' ,'l_color' ,'l_fontsize','sd_font','sd_color','sd_fontsize' ,'sd_position' ,'sd_email','admin_email' , 'address' ,'po_box' ,'phone','next_term' ,'sd_other' ,'std_color','std_font','std_fontsize','std_position','table_type','shadow','watermark', 'email_notification'], [ class_settings[0]["grading_type"] ,class_settings[0]["background_color"],class_settings[0]["text_color"] ,class_settings[0]["line_color"], class_settings[0]["background_font"], class_settings[0]["ld_position"], class_settings[0]["l_font"], class_settings[0]["l_weight"] , class_settings[0]["l_color"],class_settings[0]["l_fontsize"], class_settings[0]["sd_font"], class_settings[0]["sd_color"], class_settings[0]["sd_fontsize"] ,class_settings[0]["sd_position"], class_settings[0]["sd_email"], class_settings[0]["admin_email"], class_settings[0]["address"], class_settings[0]["po_box"], class_settings[0]["phone"], class_settings[0]["phone"], class_settings[0]["phone"],class_settings[0]["std_color"], class_settings[0]["std_font"],class_settings[0]["std_fontsize"],class_settings[0]["std_position"],class_settings[0]["table_type"] ,class_settings[0]["shadow"],class_settings[0]["watermark"], class_settings[0]["email_notification"]])

    classRow = select_all_from_row(tables['classes'], 'id', classId)
    class_settings = select_all_from(tables['settings'], 'id', classId)

    if class_settings[0]["email_notification"] == 'on':
        # send email to admin about subject scoresheet
        html = render_template('new_class.html',classInfo = classRow)
        subject = classRow[0]["classname"].upper()+" created for  "+ classRow[0]["section"]+" section"
        try:
            send_email(rows[0]["email"], subject, html, 'classclass_term_dataest@gmail.com')
        except Exception as e:
            print(e)
    # return classlist.html
    flash(subject)
    return render_class(classId)

@app.route("/how_to_use", methods=["GET"])
def how_to_use():
        try:
            session["user_id"]
        except KeyError:
            return render_template("how_to_use.html")
        schoolrow = select_all_from_row(session['user_id'])
        return render_template("how_to_use.html", schoolInfo = schoolrow )

@app.route("/about_us", methods=["GET"])
def about_us():
        try:
            session["user_id"]
        except KeyError:
            return render_template("about_us.html")
        schoolrow = select_all_from(session['user_id'])
        return render_template("about_us.html", schoolInfo = schoolrow )
@app.route("/submit_score", methods =["POST","GET"])
@login_required
@check_confirmed
def submit_score():
    session["subject_info"] = {}
    tables = database(str(0))

    if request.method == "POST":
        classes = select_all_from_table(tables['classes'])
        schoolId = session['user_id']
        schoolrow = select_school_by_id(session['user_id'])

        if not request.form.get("subject_name"):
            error = " provide the subject name"
            return render_template("submit_score_form.html",classes = classes, schoolInfo = schoolrow, error = error)
        if not request.form.get("the_class"):
            error = "select one class"
            return render_template("submit_score_form.html",classes = classes, schoolInfo = schoolrow)
        tables = database(str(request.form.get("the_class")))
        subject_row = select_all_from_row(tables['subjects'], 'name', request.form.get("subject_name").lower())
        if len(subject_row) > 0:
            error = "subject already have a scoresheet"
            return render_template("submit_score_form.html",classes = classes, schoolInfo = schoolrow, error = error)
        if not request.form.get("subject_teacher"):
            error = "provide your name"
            return render_template("submit_score_form.html",classes = classes, schoolInfo = schoolrow, error = error)
        session["subject_info"]["subject"] = request.form.get("subject_name").lower()
        session["subject_info"]["subject_teacher"] = request.form.get("subject_teacher")
        class_id= int(request.form.get("the_class"))
        tables = database(class_id)
        session["subject_info"]["class_id"] = class_id
        current_setting = select_all_from_row(tables['settings'], 'id', tables['class_id'])
        session_setting = select_all_from_row(tables['classes'],'id', tables['class_id'] )
        class_names = select_all_from_table(tables['classlist'])
        sort(class_name, key = 'surname', reverse = False)

        return render_template("empty_scoresheet.html",schoolInfo = schoolrow, subject_info = session["subject_info"],class_names = class_names ,classinfo = class_row[0], setting = session_setting, result = current_setting)
    else:
        tables = database(str(0))
        classes = select_all_from_table(tables['classes'])
        schoolId = session['user_id']
        schoolrow = select_school_by_id(session['user_id'])
        return render_template("submit_score_form.html",classes = classes, schoolInfo = schoolrow)

@app.route("/confirm_scoresheet", methods=["POST"])
@login_required
@check_confirmed
def confirm_scoresheet():
    #declare an array of
    session["class_scores"] = []
    tables = database(session["subject_info"]["class_id"])
    rows = select_school_by_id(session['user_id'])
    session_setting = select_all_from_row(tables['settings'], 'id', tables['class_id'])
    class_list = select_all_from_table(tables['classlist'])
    # each student will be an element of the array
    for student  in class_list:
        ca = "cascore"+str(student["id"])
        test = "testscore"+str(student["id"])
        exam = "examscore"+str(student["id"])
        session["class_scores"].append((student["id"], student["firstname"], student["surname"],student["othername"], request.form.get(ca), request.form.get(test), request.form.get(exam)))
    session["submitting_scoresheet"] = False
    #return classlist.html
    return render_template("confirm_scoresheet.html",schoolInfo = rows, students=session["class_scores"], class_id = session["subject_info"]["class_id"], details=session_setting, details2 = session["subject_info"])

@app.route("/submitted", methods=["POST"])
@login_required
@check_confirmed
def submitted():
    if session["submitting_scoresheet"]:
        error = "scoresheet Already submitted"
        return render_portfolio(error)
    else:
        session["submitting_scoresheet"] = True
        tables = database(request.form.get("button"))
        c_subject = select_all_from_row(tables['subjects'],'name', session["subject_info"]["subject"].lower())
        if len(c_subject) > 0:
            error = session["subject_info"]["subject"]+" already submitted for this class"
            flash(error)
            return render_class(tables["class_id"])
        former_info = select_all_from_row(tables['settings'], 'id', tables['class_id'])
        insert_into_table(tables['subjects'], ['name, teachers_name'], [session["subject_info"]["subject"],session["subject_info"]["subject_teacher"]])
        subject_list = select_all_from_row(tables['subjects'], 'name', session["subject_info"]["subject"])
        subject_id = str(subject_list[0]["id"])
        alter_table(table['ca'], subject_id)
        alter_table(tables['test'], subject_id)
        alter_table(tables['exam'], subject_id)
        alter_table(tables['grade'], subject_id)
        alter_table(tables['subject_position'], subject_id)
        alter_table(tables['mastersheet'], subject_id)        
        rows = select_school_by_id(session['user_id'])
        class_info = select_all_from_row(tables['classes'], 'id', tables['class_id'])
        subject_total = 0
        term_failed = 0
        term_passed = 0
        subjects_no = select_all_from_table(subject['subjects'])
        student_row = select_all_from_table(tables['mastersheet'])
        no_of_grade = select_all_from_table(tables['grades'])
        i = 0
        for  student in session["class_scores"]:
            subject_list = select_all_from_row(tables['subjects'], 'name',session["subject_info"]["subject"])
            total_score = 0
            if student[4]:
                total_score = total_score + int(student[4])
            if student[5]:
                total_score = total_score + int(student[5])
            if student[6]:
                total_score = total_score + int(student[6])
            new_total = student_row[i]["total_score"] + total_score
            grading = grade(total_score, former_info[0]["grading_type"])
            student_grade = grading["score_grade"]
            subject_total = subject_total + total_score
            subject_grade = str(student_grade[0]).upper()
            #grade col in subjects
            grade_col = "no_of_"+subject_grade.lower()
            #student total score
            new_average = new_total /no_of_sub 
            # no of students that passed or failed for the term
            if int(new_average) >= int(grading["pass_mark"]):
                term_passed = term_passed + 1
            else:
                term_failed = term_failed + 1


            update_table(tables['ca'],subject_id, student[4], 'id', student[0])
            update_table(tables['test'],subject_id, student[5], 'id', student[0])
            update_table(tables['exam'],subject_id, student[6], 'id', student[0])


            update_table(tables['mastersheet'], [subject_id, 'total_score', 'average'][total_score, new_total, new_average], 'id', student[0] )
            update_table(tables['subjects'],grade_col,int(subject_list[0][grade_col]+1) )

            update_table(tables['grade'], [subject_id, grade_col], [grading['score_grade'],int(no_of_grade[i][str(grade_col)]) + 1], 'id', student[0])
            i = i + 1
        #sort students position
        assign_student_position(tables["class_id"])
        update_table(tables['classes'], [no_of_passes, no_of_failures], [term_passed, term_failed], 'id', tables['class_id'])
        classRows = select_all_from_row(tables['classes'], 'id', tables['class_id'])
        #sort subject position
        assign_subject_position(tables["class_id"],subject_id)
        no_of_students = len(session["class_scores"])
        subject_average = subject_total / no_of_students
        # calculate and insert ppass for subject and class and repair passed and failed for class 
        initial_array = str(session["subject_info"]["subject_teacher"]).split()
        teacher_initials = ""
        for name in initial_array:
            if teacher_initials == "":
                teacher_initials = initials(name)
            else:
                teacher_initials = teacher_initials+initials(name)
        update_table(tables['subjects'],['class_average','total_score', 'teachers_initial'],[subject_average, subject_total,teacher_initials], 'id', subject_id)
        if class_info[0]["email_notification"] == 'on':
            # send email to admin about subject scoresheet
            html = render_template('new_score.html',subject = session["subject_info"], class_info=classRows[0])
            subject = session["subject_info"]["subject"].upper()+" scoreesheet submitted for  "+ classRows[0]["classname"]
            try:
                send_email(rows[0]["email"], subject, html, 'Schoolresultnigeria@gmail.com')
            except Exception as e:
                print(e)
        classRows = select_all_from_table(tables['classes'])
        error = session["subject_info"]["subject"].upper()+" scoresheet submitted successfully"
        # return classlist.html
    return render_class(tables["class_id"],error)




@app.route("/veiwclass", methods=["post", "get"])
@login_required
@check_confirmed
def veiwclass():
    if request.form.get("veiw_class"):
        return render_class(request.form.get("veiw_class"))
    else:
        return redirect('/')


@app.route("/scoresheet", methods=["POST"])
@login_required
@check_confirmed
def scoresheet():
    array_id = str(request.form.get("scoresheet")).split("_")
    subject_id = int(array_id[0])
    class_id = int(array_id[1])
    tables=database(class_id)
    classrow = select_all_from(tables['classes'], 'id', class_id)
    schoolrow = select_school_by_id(session['user_id'])
    carow = select_all_from_table(tables['ca'])
    testrow = select_all_from_table(tables['test'])
    examrow = select_all_from_table(tables['exam'])
    classlistrow = select_all_from_table(tables['classlist'])
    grade_row = select_all_from_table(tables['grade'])
    subject_position_row = select_all_from_table(tables['subject_position'])
    subjectrow = select_all_from_row(tables['subjects'], 'id', subject_id)
    results = select_all_from_row(tables['classes'], 'id', class_id)
    return render_template("scoresheet.html",result = results[0],sub_id=subject_id, gradeData = grade_rows, schoolInfo = schoolrow, classData = classrow, caData = carow, testData = testrow, examData = examrow, subjectData = subjectrow,class_list = classlistrow, mastersheet = mastersheet_rows, subject_position = subject_position_row)

@app.route("/scoresheet_pdf", methods=["POST"])
@login_required
@check_confirmed
def scoresheet_pdf():
    array_id = str(request.form.get("scoresheet")).split("_")
    subject_id = int(array_id[0])
    class_id = int(array_id[1])
    tables=database(class_id)
    classrow = select_all_from(tables['classes'], 'id', class_id)
    schoolrow = select_school_by_id(session['user_id'])
    carow = select_all_from_table(tables['ca'])
    testrow = select_all_from_table(tables['test'])
    examrow = select_all_from_table(tables['exam'])
    classlistrow = select_all_from_table(tables['classlist'])
    grade_row = select_all_from_table(tables['grade'])
    subject_position_row = select_all_from_table(tables['subject_position'])
    subjectrow = select_all_from_row(tables['subjects'], 'id', subject_id)
    results = select_all_from_row(tables['classes'], 'id', class_id)
    html =  render_template("scoresheet.html",gradeData = grade_rows, result = results[0],sub_id=subject_id, schoolInfo = schoolrow, classData = classrow, caData = carow, testData = testrow, examData = examrow, subjectData = subjectrow,class_list = classlistrow, mastersheet = mastersheet_rows, subject_position = subject_position_row)
    return render_pdf(HTML(string=html))

@app.route("/result_sheet", methods=["POST"])
@login_required
@check_confirmed
def result_sheet():
    array_id = str(request.form.get("result_sheet")).split("_")
    student_id = int(array_id[0])
    class_id = int(array_id[1])
    tables= database(class_id)
    classrow = select_all_from(tables['classes'], 'id', class_id)
    schoolrow = select_school_by_id(session['user_id'])
    carow = select_all_from_table(tables['ca'])
    testrow = select_all_from_table(tables['test'])
    examrow = select_all_from_table(tables['exam'])
    classlistrow = select_all_from_table(tables['classlist'])
    grade_row = select_all_from_table(tables['grade'])
    subject_position_row = select_all_from_table(tables['subject_position'])
    subjectrow = select_all_from_row(tables['subjects'], 'id', subject_id)
    results = select_all_from_row(tables['classes'], 'id', class_id)
    return render_template("result_sheet.html",gradeRows = grades,result = results[0], schoolInfo = schoolrow, classData = classrow, caData = carow, testData = testrow, examData = examrow, subjectData = subjectrow,class_list = classlistrow, mastersheet = mastersheet_rows, subject_position = subject_position_row)


@app.route("/result_sheet_pdf", methods=["POST"])
@login_required
@check_confirmed
def result_sheet_pdf():
    array_id = str(request.form.get("result_sheet")).split("_")
    student_id = int(array_id[0])
    class_id = int(array_id[1])
    tables= database(class_id)
    classrow = select_all_from(tables['classes'], 'id', class_id)
    schoolrow = select_school_by_id(session['user_id'])
    carow = select_all_from_table(tables['ca'])
    testrow = select_all_from_table(tables['test'])
    examrow = select_all_from_table(tables['exam'])
    classlistrow = select_all_from_table(tables['classlist'])
    grade_row = select_all_from_table(tables['grade'])
    subject_position_row = select_all_from_table(tables['subject_position'])
    subjectrow = select_all_from_row(tables['subjects'], 'id', subject_id)
    results = select_all_from_row(tables['classes'], 'id', class_id)
    html =  render_template("result_sheet.html",gradeRows = grades,result = results[0], schoolInfo = schoolrow, classData = classrow, caData = carow, testData = testrow, examData = examrow, subjectData = subjectrow,class_list = classlistrow, mastersheet = mastersheet_rows, subject_position = subject_position_row)
    return render_pdf(HTML(string=html))


@app.route("/printall_pdf", methods=["POST"])
@login_required
@check_confirmed
def printall_pdf():
    class_id = request.form.get('class_id')
    tables= database(class_id)
    classrow = select_all_from(tables['classes'], 'id', class_id)
    schoolrow = select_school_by_id(session['user_id'])
    carow = select_all_from_table(tables['ca'])
    testrow = select_all_from_table(tables['test'])
    examrow = select_all_from_table(tables['exam'])
    classlistrow = select_all_from_table(tables['classlist'])
    grade_row = select_all_from_table(tables['grade'])
    subject_position_row = select_all_from_table(tables['subject_position'])
    subjectrow = select_all_from_row(tables['subjects'], 'id', subject_id)
    results = select_all_from_row(tables['classes'], 'id', class_id)
    html =  render_template("print_all.html",gradeRows = grades,result = results[0], schoolInfo = schoolrow, classData = classrow, caData = carow, testData = testrow, examData = examrow, subjectData = subjectrow,class_list = classlistrow, mastersheet = mastersheet_rows, subject_position = subject_position_row)
    return render_pdf(HTML(string=html))


@app.route("/printall_html", methods=["POST"])
@login_required
@check_confirmed
def printall_html():
    class_id = request.form.get('class_id')
    tables= database(class_id)
    classrow = select_all_from(tables['classes'], 'id', class_id)
    schoolrow = select_school_by_id(session['user_id'])
    carow = select_all_from_table(tables['ca'])
    testrow = select_all_from_table(tables['test'])
    examrow = select_all_from_table(tables['exam'])
    classlistrow = select_all_from_table(tables['classlist'])
    grade_row = select_all_from_table(tables['grade'])
    subject_position_row = select_all_from_table(tables['subject_position'])
    subjectrow = select_all_from_row(tables['subjects'], 'id', subject_id)
    results = select_all_from_row(tables['classes'], 'id', class_id)
    return render_template("print_all.html",gradeRows = grades,result = results[0], schoolInfo = schoolrow, classData = classrow, caData = carow, testData = testrow, examData = examrow, subjectData = subjectrow,class_list = classlistrow, mastersheet = mastersheet_rows, subject_position = subject_position_row)

@app.route("/edited_scoresheet", methods=["POST"])
@login_required
@check_confirmed
def edited_scoresheet():
    if session["edit_scoresheet"] or session["deleting_scoresheet"]:
        error = "scoresheet currently being updated please wait"
        return render_class(request.form.get("class_id"))
    session["edit_scoresheet"] = True
    schoolrow = select_school_by_id(school['user_id'])
    subject_id = request.form.get("subject_id")
    class_id = request.form.get("class_id")
    tables = database(class_id)
    class_list = tables["classlist"]
    cascore_table = tables["ca"]
    test_table = tables["test"]
    exam_table = tables["exam"]
    subject_table = tables["subjects"]
    class_list_row = select_all_from_table(table['classlist'])
    subject_row = select_all_from_row(tables['subjects'], 'id', subject_id)
    class_info = select_all_from_row(tables['classes'], 'id', class_id)
    #subject name check 
    if not request.form.get("subject_name"):
        mastersheet_row = select_all_from_table(tables['mastersheet'])
        class_data = select_all_from_row(tables['classes'], 'id', class_id)
        carow = select_all_from_table(tables['ca'])
        testrow = select_all_from_table(tables['test'])
        examrow = select_all_from_table(tables['mastersheet'])
        error = "subject do not have a name"
        flash(error)
        return render_template("edit_scoresheet.html",sub_id=subject_id, schoolInfo = schoolrow, classData = class_data, caData = carow, testData = testrow, examData = examrow, subjectData = subject_row,class_list = class_list_row, mastersheet = mastersheet_row, result = class_info)
    elif request.form.get("previous") != request.form.get("subject_name"):
        subject_data = select_all_from_row(subject_table, 'name', request.form.get("subject_name").lower())
        if len(subject_data) > 0:
            mastersheet_row = select_all_from_table(tables['mastersheet'])
            class_data = select_all_from_row(tables['classes'], 'id', class_id)
            carow = select_all_from_table(tables['ca'])
            testrow = select_all_from_table(tables['test'])
            examrow = select_all_from_table(tables['exam'])
            error = "subject with the same name already exist"
            flash(error)
            return render_template("edit_scoresheet.html",sub_id=subject_id, schoolInfo = schoolrow, classData = class_data, caData = carow, testData = testrow, examData = examrow, subjectData = subject_row,class_list = class_list_row, mastersheet = mastersheet_row, result = class_info)


    if not request.form.get("teachers_name") :
        mastersheet_row = select_all_from_table(tables['mastersheet'])
        class_data = select_all_from_row(tables['classes'], 'id', class_id)
        carow = select_all_from_table(tables['ca'])
        testrow = select_all_from_table(tables['test'])
        examrow = select_all_from_table(tables['exam'])
        error = "teacher name is empty"
        flash(error)
        return render_template("edit_scoresheet.html",sub_id=subject_id, schoolInfo = schoolrow, classData = class_data, caData = carow, testData = testrow, examData = examrow, subjectData = subject_row,class_list = class_list_row, mastersheet = mastersheet_row, result = class_info)

    #uniqueness of subject name check
    #teacher name check

    subject_total = 0
    # no of students that passed this term
    class_passing = int(class_info[0]["no_of_passes"])
    class_failing = int(class_info[0]["no_of_failures"])
    for  student in class_list_row:
        prev_grades = select_all_from_row(tables['grade'], 'id', student['id'])
        student_row = select_all_from_row(tables['mastersheet'], 'id', student['id'])
        ca_row = select_all_from_row(tables['ca'], 'id', student['id'])
        test_row = select_all_from_row(tables['test'], 'id', student['id'])
        exam_row = select_all_from_row(tables['exam'], 'id', student['id'])

        total_score = 0
        cascore = "cascore"+ str(student["id"])
        testscore = "testscore"+str(student["id"])
        examscore = "examscore"+str(student["id"])
        ca_score = request.form.get(cascore)
        test_score = request.form.get(testscore)
        exam_score = request.form.get(examscore)
        if  str(ca_score) != ca_row[0][str(subject_id)] and  ca_score != "None" : 
            update_table(cascore_table, str(subject_row[0]["id"]),ca_score, 'id', student['id']  )
        if  str(test_score) != test_row[0][str(subject_id)] and  test_score != "None"  : 
            update_table(test_table, str(subject_row[0]["id"]),test_score, 'id', student['id']  )
        if  str(exam_score) != exam_row[0][str(subject_id)] and  exam_score != "None": 
            update_table(exam_table, str(subject_row[0]["id"]),exam_score, 'id', student['id']  )
        if request.form.get(cascore) != '' and request.form.get(cascore) != 'None':
            total_score = total_score + int(ca_score)
        if request.form.get(testscore) != '' and request.form.get(testscore) != 'None':
            total_score = total_score + int(test_score)
        if request.form.get(examscore) != '' and request.form.get(examscore) != 'None':
            total_score = total_score + int(exam_score)
        subject_total = subject_total + total_score

        if float(total_score) !=  float(student_row[0][str(subject_id)]):
            all_subjects = select_all_from_table(str(tables['subjects']))
            subject_list = select_all_from_row(tables['subjects'], 'id',subject_id )
            previous_grade = prev_grades[0][str(subject_id)]
            current_grading = grade(0, str(class_info[0]["grading_type"]))
            new_total = float(student_row[0]["total_score"]) - float(student_row[0][str(subject_id)])
            new_total = new_total + total_score
            student_grad = grade(total_score, str(class_info[0]["grading_type"]))
            student_grade = student_grad["score_grade"]
            grade_col = 'no_of_'+str(student_grade[0]).lower()
            previous_grade_col = 'no_of_'+str(previous_grade[0]).upper()
            new_average = new_total / len(all_subjects)
            if grade_col != previous_grade_col:
                new_grade_no = int(subject_list[0][grade_col]) + 1
                previous_grade_no = int(subject_list[0][previous_grade_col]) - 1
                update_table(tables['subjects'], [grade_col, previous_grade_col],[new_grade_no, previous_grade_no], 'id', subject_id )
            
            update_table(tables['mastersheet'],[str(subject_id), 'total_score',average ][total_score, new_total, new_average], 'id', student['id'] )


            # if student passed now but failed previously for the term
            if float(new_average) >= float(current_grading["pass_mark"]) and float(student_row[0]["average"]) < float(current_grading["pass_mark"]) :
                class_failing = class_failing - 1
                class_passing = class_passing + 1
            elif float(new_average) < int(current_grading["pass_mark"]) and float(student_row[0]["average"]) >= float(current_grading["pass_mark"]) :
                class_failing = class_failing + 1
                class_passing = class_passing - 1
            if grade_col != previous_grade_col:
                new_sub_grade = int(prev_grades[0][grade_col]) + 1
                prev_sub_grade = int(prev_grades[0][previous_grade_col]) - 1
                update_table(tables['grade'], [str(subject_id), grade_col, previous_grade_col], [student_grade ,new_sub_grade, prev_sub_grade], 'id', student['id'])

    #sort students position
    assign_student_position(tables["class_id"])
    #sort subject position
    assign_subject_position(int(tables["class_id"]),subject_id)
    update_table(tables['classes'], ['no_of_failures', 'no_of_passes'],[class_failing, class_passing], 'id', class_id)
    if int(subject_row[0]["total_score"]) != subject_total:
        no_of_students = len(class_list_row)
        subject_average = subject_total / no_of_students
        # calculate and insert ppass for subject and class and repair passed and failed for class
        update_table(tables['subjects'], ['class_average', 'total_score'],[subject_average, subject_total], 'id', subject_id)
    if subject_row[0]["name"] != request.form.get("subject_name"):
        update_table(tables['subjects'], 'name',request.form.get("subject_name").upper(), 'id',subject_id  )
    if subject_row[0]["teachers_name"] != request.form.get("teachers_name"):
        update_table(tables['subjects'], 'teachers_name',request.form.get("teachers_name").upper(), 'id', subject_id )
        teacher_initials = initials(request.form.get("teachers_name"))
        update_table(tables['subjects'], 'teacher_initials', teacher_initials, 'id', subject_id)
    error = request.form.get("subject_name").upper()+" scoresheet edited successfully"
    # return class.html
    session["edit_scoresheet"] = False
    return render_class(tables["class_id"],error)


@app.route("/delete_scoresheet", methods=["POST"])
@login_required
@check_confirmed
def delete_scoresheet():
    if session["deleting_scoresheet"] or session["edit_scoresheet"]:
        error = "Deleting scoresheet in progress please wait"
        flash(error)
        return render_class(request.form.get("class_id"))
    session["deleting_scoresheet"] = True
    class_id = str(request.form.get("class_id"))
    subject_id = str(request.form.get("subject_id"))
    tables = database(class_id)
    subject = select_all_from_row(tables['subjects'],'id', subject_id )
    if len(subject) < 1:
        error = "Subject do not exist"
        flash(error)
        return render_class(class_id)
    class_details = select_all_from_row(tables['classes'], 'id', class_id)
    mastersheet = select_all_from_table(tables['mastersheet'])
    all_subject = select_all_from_table(tables['subjects'])

    no_of_subjects = len(all_subject) - 1
    student_pass = 0
    student_fail = 0
    for student in mastersheet:
        students_total = float(student["total_score"])
        subject_total = float(student[subject_id])
        new_total= students_total - subject_total
        grading = grade(subject_total,class_details[0]["grading_type"])
        student_grade = grading["score_grade"]
        if no_of_subjects != 0:
            new_average = new_total/no_of_subjects 
        else:
            new_average = 0

        if float(new_average) >= float(grading["pass_mark"]):
            student_pass = student_pass + 1
        else:
            student_fail = student_fail + 1
        grade_col = "no_of_"+student_grade[0]
        grades = select_all_from_row(tables['grade'], 'id', student['id'])
        update_table(tables['grade'], grade_col,int(grades[0][grade_col])-1, 'id', student['id'] )
        update_table(tables['mastersheet'], ['total_score', 'average'], [new_total,new_average], 'id', student['id'])
    drop_column(tables['ca'], subject_id)
    drop_column(tables['test'], subject_id)
    drop_column(tables['exam'], subject_id)
    drop_column(tables['mastersheet'], subject_id)
    drop_column(tables['subject_position'], subject_id)
    drop_column(tables['grade'], subject_id)
    if no_of_subjects == 0:
        update_table(table['classes'], ['no_of_passes','no_of_failures'], [0, 0], 'id', class_id)
        delete_from_id(table['subjects'], 'id', class_id)
        update_table(tables['mastersheet'], 'position', 'None' )
        error=subject[0]["name"]+" deleted successfully"
        return render_class(tables["class_id"],error)
    else:
        update_table(table['classes'], ['no_of_passes','no_of_failures'], [student_pass, student_fail], 'id', class_id)
        delete_from_id(tables['subjects'], 'id', subject_id)
        assign_student_position(class_id)
        error=subject[0]["name"].upper()+" deleted successfully"
        session["deleting_scoresheet"] = False
        return render_class(tables["class_id"],error)


@app.route("/cancel", methods=["POST"])
@login_required
@check_confirmed

def cancel():
    class_id = str(request.form.get("class_id"))
    return render_class(class_id)


@app.route("/cancel_portfolio", methods=["POST"])
@login_required
@check_confirmed
def cancel_portfolio():
    return render_portfolio()

@app.route("/verify_scoresheet", methods=["POST"])
@login_required
@check_confirmed
def verify_scoresheet():
    array_id = str(request.form.get("edit_scoresheet")).split("_")
    subject_id = int(array_id[0])
    class_id = int(array_id[1])
    tables= database(class_id)
    select_all_from_row(tables['classes'], 'id', tables['class_id'])
    schoolrow = select_school_by_id(session['user_id'])
    return render_template("verify_scoresheet.html",sub_id=subject_id,  classData = classrow, schoolInfo=schoolrow)
    
    
@app.route("/edit_student", methods=["POST"])
@login_required
@check_confirmed
def edit_student():
    password = request.form.get("password")
    student_id = request.form.get("student_id")
    class_id = request.form.get("class_id")
    tables= database(class_id)
    classrow = select_all_from_row(table['classes'], 'id', class_id)
    schoolrow = select_school_by_id(session['user_id'])
    if check_password_hash(classrow[0]["password"], password) or check_password_hash(schoolrow[0]["admin_password"], password ):
        studentrow = select_all_from_row(tables['classlist'],'id', class_id )
        session["edit_student"] = False
        session["deleting_student"] = False
        return render_template("edit_student.html",id=student_id, schoolInfo = schoolrow, classData=classrow,student=studentrow[0])
    else:
        error= ' The admin or class password is incorrect.'
        return render_class(class_id, error)

@app.route("/edit_scoresheet", methods=["POST"])
@login_required
@check_confirmed
def edit_scoresheet():
    password = request.form.get("password")
    subject_id = request.form.get("subject_id")
    class_id = request.form.get("class_id")
    tables= database(class_id)
    classrow = select_all_from_row(table['classes'], 'id', class_id)
    schoolrow = select_school_by_id(session['user_id'])
    if check_password_hash(classrow[0]["password"], password) or check_password_hash(schoolrow[0]["admin_password"], password ):
        carow = select_all_from_table(tables['ca'])
        testrow = select_all_from_table(tables['test'])
        examrow = select_all_from_table(tables['exam'])
        subjectrow = select_all_from_row(tables['subjects'], 'id', subject_id)
        classlistrow = select_all_from_table(tables['classlist'])
        mastersheet_rows = select_all_from_table(tables['mastersheet'])
        subject_position = select_all_from_table(tables['subject_position'])
        current_settings = select_all_from_row(tables[settings], 'id', class_id)
        setting = current_settings[0]
        session["edit_scoresheet"] = False
        session["deleting_scoresheet"] = False
        return render_template("edit_scoresheet.html",sub_id=subject_id, schoolInfo = schoolrow, classData = classrow, caData = carow, testData = testrow, examData = examrow, subjectData = subjectrow,class_list = classlistrow, mastersheet = mastersheet_rows, subject_position = subject_position_row, result = setting)
    else:
        error= ' The admin or class password is incorrect.'
        return render_class(class_id, error)


@app.route("/edited_student", methods=["POST"])
@login_required
@check_confirmed
def edited_student():
    if session["edit_student"] or session["deleting_student"]:
        error = "Edit student in progress"
        flash(error)
        return render_class(request.form.get("class_id"))
    session["edit_student"] = True
    student_id = request.form.get("student_id")
    class_id = request.form.get("class_id")
    tables= database(class_id)
    surname = "s"+str(student_id)
    schoolrow = select_school_by_id(session['user_id'])
    classrow = select_all_from_table(tables['classes'])
    sex = "g"+str(student_id)
    if not request.form.get(surname):
        error= "provide surname"
        studentrow = select_all_from_row(tables['classlist'], 'id', class_id)
        flash(error)
        return render_template("edit_student.html",id=student_id, schoolInfo = schoolrow, classData=classrow,student=studentrow[0])
    firstname = "f"+str(student_id)
    if not request.form.get(firstname):
        error= "provide firstname"
        studentrow = select_all_from_row(tables['classlist'], 'id', class_id)
        flash(error)
        return render_template("edit_student.html",id=student_id, schoolInfo = schoolrow, classData=classrow,student=studentrow[0])
    if not request.form.get(sex):
        error= "please select student's gender"
        studentrow = select_all_from_row(tables['classlist'], 'id', class_id)
        flash(error)
        return render_template("edit_student.html",id=student_id, schoolInfo = schoolrow, classData=classrow,student=studentrow[0])

    othername = "o"+str(student_id)
    update_table(tables['classlist'], ['surname', 'firstname', 'othername', 'sex'][request.form.get(surname).upper(),request.form.get(firstname).upper(),request.form.get(othername).upper(), request.form.get(sex).upper()], 'id', student_id)
    session["edit_student"] = False
    return render_class(class_id)

@app.route("/unregister_student", methods=["POST"])
@login_required
@check_confirmed
def unregister_student():
    if session["deleting_student"] or session["edit_student"]:
        error = "Currenting unregistering a student please wait"
        return render_class(request.form.get("class_id"))
    session["deleting_student"] = True
    student_id = request.form.get("student_id")
    class_id = request.form.get("class_id")
    tables =database(class_id)
    student_details = select_all_from_row(tables['classlist'], 'id',student_id )
    if len(student_details) < 1:
        error = "student does not exist"
        flash(error)
        return render_class(class_id)
    remove_student(student_id, class_id)
    error="student deleted successfully"
    session["deleting_student"] = False
    return render_class(class_id,error)

@app.route("/verify_customize", methods=["POST"])
@login_required
@check_confirmed
def verify_customize():
   class_id = request.form.get("class_id")
   tables= database(class_id)
   schoolrow = select_school_by_id(session['user_id'])
   classrow = select_all_from_row(tables['classes'], 'id', class_id)
   return render_template("verify_customize.html", classData = classrow, schoolInfo=schoolrow)

@app.route("/verified_customize", methods=["POST"])
@login_required
@check_confirmed
def verified_customize():
    class_id = request.form.get("class_id")
    tables = database(class_id)
    password = request.form.get("password")
    schoolrow = select_school_by_id(session['user_id'])
    classRows, class_info = select_all_from_row(tables['classes'], 'id', class_id)
    class_settings = select_all_from_row(tables['settings'], 'id', class_id)

    #select all the subjects
    subject = select_all_from_table(tables['subjects'])
    # return classlist.html
    if not password:
        error = "provide admin or class password"
        flash(error,'success')
        return render_template("verify_customize.html", classData = classRows, schoolInfo=schoolrow)

    if check_password_hash(classRows[0]["password"], password) or check_password_hash(schoolrow[0]["admin_password"], password):
        session["class_settings"] = False
        return render_template("customize.html", schoolInfo = schoolrow,classData=classRows,subjects = subject, classInfo=class_info[0], class_setting=class_settings[0])
    else:
        error = "admin or class password incorrect"
        return render_class(class_id, error)



@app.route("/verify_add_student", methods=["POST"])
@login_required
@check_confirmed
def verify_add_student():
   class_id = request.form.get("class_id")
   tables= database(class_id)
   schoolrow = select_school_by_id(session['user_id'])
   classrow = select_all_from_row(tables['classes'], 'id', class_id)
   return render_template("verify_add_student.html", classData = classrow, schoolInfo=schoolrow)


@app.route("/verified_add_student", methods=["POST"])
@login_required
@check_confirmed
def verified_add_student():
    class_id = request.form.get("class_id")
    tables = database(class_id)
    password = request.form.get("password")
    schoolrow = select_school_by_id(session['user_id'])
    classrow = select_all_from_row(tables['classes'], 'id', class_id)
    class_info = delete_from_id(tables['classes'], 'id', class_id)
    #select all the subjects
    subject = select_all_from_table(tables['subjects'])
    # return classlist.html
    if not password:
        error = "provide admin or class password"
        flash(error,'success')
        return render_template("verify_add_student.html", classData = classrow, schoolInfo=schoolrow)

    if check_password_hash(classrow[0]["password"], password) or check_password_hash(schoolrow[0]["admin_password"], password):
        return render_template("add_student.html", schoolInfo = schoolrow,clas=classrow,subjects = subject, classInfo=class_info[0])
    else:
        classrow = select_all_from_table(tables['classes'])
        error = "admin or class password incorrect"
        return render_class(class_id, error)
 
@app.route("/confirm_details", methods=["POST"])
@login_required
@check_confirmed
def confirm_details():
    session["single_details"]={}
    session["single_subject"]=[]
    class_id = request.form.get("class_id")
    tables= database(class_id)
    class_session = select_all_from_row(tables['classes'], 'id', class_id)
    session["single_details"]["class_id"] = class_id
    session["single_details"]["class_name"] = class_session[0]["classname"]
    if not request.form.get("surname"):
        error = "you must provide students surname"
        schoolrow = select_school_by_id(session['user_id'])
        classrow = select_all_from_row(tables['classes'], 'id', class_id)
        class_info = delete_from_id(tables['classes'], 'id', class_id)
        #select all the subjects
        subject = select_all_from_table(tables['subjects'])
        flash(error,'success')
        return render_template("add_student.html", schoolInfo = schoolrow,clas=classRows,subjects = subject, classInfo=class_info[0])
    if not request.form.get("firstname"):
        error = "you must provide students firstname"
        schoolrow = select_school_by_id(session['user_id'])
        classrow = select_all_from_row(tables['classes'], 'id', class_id)
        class_info = delete_from_id(tables['classes'], 'id', class_id)
        #select all the subjects
        subject = select_all_from_table(tables['subjects'])
        flash(error,'success')
        return render_template("add_student.html", schoolInfo = schoolrow,clas=classRows,subjects = subject, classInfo=class_info[0])
    session["single_details"]["surname"] = request.form.get("surname")
    session["single_details"]["firstname"] = request.form.get("firstname")
    session["single_details"]["othername"] = request.form.get("othername")
    if not request.form.get("sex"):
        session["single_details"]["sex"] = "male"
    else:
        session["single_details"]["sex"] = request.form.get("sex")
    class_subjects = select_all_from_table(tables['subjects'])
    for subject in class_subjects:
        sub = {}
        ca = "cascore"+str(subject["id"])
        test = "testscore"+str(subject["id"])
        exam = "examscore"+str(subject["id"])
        sub["name"] = subject["name"]
        sub["id"] = subject["id"]
        sub["ca"] = request.form.get(ca)
        sub["test"] = request.form.get(test)
        sub["exam"] = request.form.get(exam)
        session["single_subject"].append(sub)
    session["adding_student"] = False
    rows = select_school_by_id(session['user_id'])
    
    # return classlist.html
    return render_template("confirm_single_scoresheet.html", schoolInfo = rows, subjects= class_subjects, details = session["single_details"], student_subjects=session["single_subject"])

@app.route("/student_added", methods=["POST"])
@login_required
@check_confirmed
def student_added():
    if session["adding_student"]:
        error = session["single_details"]["firstname"] + " " +session["single_details"]["surname"]+ " already  added "
        flash(error)
        return render_class(session["single_details"]["class_id"])
    session["adding_student"] = True
    class_id = session["single_details"]["class_id"]
    tables= database(class_id)
    pins = generate_pins(10, 1)
    student_id = insert_into_table(tables['classlist'], ['surname', 'firstname', 'othername', 'sex', 'pin'],[session["single_details"]["surname"].upper(),session["single_details"]["firstname"].upper(),session["single_details"]["othername"].upper(),session["single_details"]["sex"].upper(),pins[0]])
    all_student = select_all_from_table(tables['classlist'])
    insert_into_table(tables['ca'], 'id', student_id)
    insert_into_table(tables['test'], 'id', student_id)
    insert_into_table(tables['exam'], 'id', student_id)
    insert_into_table(tables['mastersheet'], 'id', student_id)
    insert_into_table(tables['subject_position'], 'id', student_id)
    insert_into_table(tables['grade'], 'id', student_id)
    new = len(all_student)
    for subject in session["single_subject"]:
        ntotal = 0
        update_table(table['ca'], str(subject["id"]),subject["ca"], 'id', student_id )
        update_table(table['test'], str(subject["id"]),subject["test"], 'id', student_id )
        update_table(table['exam'], str(subject["id"]),subject['exam'], 'id', student_id )
        if subject["ca"]!= None:
            ntotal = ntotal + int(subject["ca"])
        if subject["test"] != None:
            ntotal = ntotal + int(subject["test"])
        if subject["exam"] != None:
            ntotal = ntotal + int(subject["exam"])                                                             
        update_table(tables['mastersheet'], str(subject['id']), ntotal, 'id', student_id)
        update_table(tables['grade'], str(subject['id']),  grade(ntotal)["score_grade"], 'id', student_id)

    add_student(student_id, class_id)
    
    # return classlist.html
    return render_class(class_id)

@app.route("/edit_class", methods=["GET"])
@login_required
@check_confirmed
def edit_class():
   class_id = str(request.args.get("class_id"))
   tables= database(class_id)
   classrow = select_all_from_row(tables['classses'], 'id', class_id)
   schoolrow = select_school_by_id(session['user_id'])
   return render_template("verify_admin.html", classData = classrow, schoolInfo=schoolrow)


@app.route("/verified_admin", methods=["POST"])
@login_required
@check_confirmed
def verified_admin():        
    class_id = request.form.get("class_id")
    password = request.form.get("password")
    tables= database(str(class_id))
    classrow = select_all_from_row(tables['classses'], 'id', class_id)
    schoolrow = select_school_by_id(session['user_id'])
    if check_password_hash(schoolrow[0]["admin_password"], password ):
        session["editing_class"] = False
        session["deleting_class"] = False
        return render_template("edit_class.html", schoolInfo = schoolrow, classData=classrow)
    else:
        error = "admin password incorrect"
        return render_portfolio(error)

@app.route("/edited_class", methods=["POST"])
@login_required
@check_confirmed
def edited_class():
    if session["editing_class"] or session["deleting_class"]:
        error = "Editing class in progress please wait"
        return render_portfolio(error)
    session["editing_class"] = True
    class_id = request.form.get("id")
    tables= database(class_id)
    firstname = request.form.get("firstname")
    surname = request.form.get("surname")
    class_name = request.form.get("class_name")
    section = request.form.get("section")
    password = request.form.get("password")
    classrow = select_all_from_row(tables['classses'], 'id', class_id)
    schoolrow = select_school_by_id(session['user_id'])
    if  firstname == " ":
        error = "class teachers firstname is empty"
        flash(error)
        return render_template("edit_class.html", schoolInfo = schoolrow, classData=classrow)
    if  surname == " ":
        error = "class teacher's surname is empty"
        flash(error)
        return render_template("edit_class.html", schoolInfo = schoolrow, classData=classrow)

    if  section == " ":
        error = "class section  is empty"
        flash(error)
        return render_template("edit_class.html", schoolInfo = schoolrow, classData=classrow)

    if  class_name == " ":
        error = "class name is empty"
        flash(error)
        return render_template("edit_class.html", schoolInfo = schoolrow, classData=classrow)
   
    if  password == " ":
        error = "password is empty"
        flash(error)
        return render_template("edit_class.html", schoolInfo = schoolrow, classData=classrow)
    class_name = class_name.lower()
    if class_name != classrow[0]["classname"]:
        row_class = select_all_from_row(tables["classes"], 'classname', request.form.get('class_name').lower())
        if len(row_class) < 1: 
            update_table(table['classes'],'classname', request.form.get("class_name").lower() )
        else:
            error = "class with name "+class_name+" already exist"
            flash(error)
            return render_template("edit_class.html", schoolInfo = schoolrow, classData=classrow)
    firstname = firstname.lower()
    if  firstname != classrow[0]["firstname"]:
        update_table(tables['classses'], 'firstname', firstname, 'id', tables['class_id'])
    
    if  password != classrow[0]["password"]:
        update_table(tables['classses'], 'password', generate_password_hash(password), 'id', tables['class_id'])

    surname = surname.lower()
    if surname != classrow[0]["surname"]:
        update_table(tables['classses'], 'surname', surname, 'id', tables['class_id'])

    section = section.lower()
    if section != classrow[0]["section"]:
        update_table(tables['classses'], 'section', section, 'id', tables['class_id'])

    session["editing_class"] = False
    error = "class edited successfully"
    return render_portfolio(error)

@app.route("/delete_class", methods=["POST"])
@login_required
@check_confirmed
def delete_class():
    if session["deleting_class"] or session["editing_class"]:
        error = "class currently being deleted please wait"
        flash(error)
        return render_portfolio()
    session["deleting_class"] = True
    class_id = request.form.get("delete_class")
    tables= database(class_id)
    class_details = select_all_from_row(tables['classes'], 'id', class_id)
    if len(class_details) < 1:
        error = "class does not exit"
        flash(error)
        return render_portfolio()
    drop_table(tables['ca'])
    drop_table(tables['test'])
    drop_table(tables['exam'])
    drop_table(tables['grade'])
    drop_table(tables['mastersheet'])
    drop_table(tables['subject_position'])
    drop_table(tables['subjects'])
    delete_from_id(tables['classes'], 'id', class_id)
    school = select_school_by_id(session['user_id'])
    error = class_details[0]["classname"].upper()+" successfully deleted from "+current_term+" term "+current_session+" academic session"
    session["deleting_class"] = False
    return render_portfolio(error)





@app.route("/verify_edit_student", methods=["GET"])
@login_required
@check_confirmed
def verify_edit_student():
    class_id = request.args.get("class_id")
    student_id = request.args.get("student_id")
    tables= database(class_id)
    classrow = select_all_from_row(tables['classses'], 'id', class_id)
    schoolrow = select_school_by_id(session['user_id'])
    return render_template("verify_teacher.html", classData = classrow, schoolInfo=schoolrow, id = student_id)


@app.route("/verify_edit_scoresheet", methods=["GET"])
@login_required
@check_confirmed
def verify_edit_scoresheet():
    class_id = request.args.get("class_id")
    subject_id = request.args.get("subject_id")
    tables= database(class_id)
    classrow = select_all_from_row(tables['classses'], 'id', class_id)
    schoolrow = select_school_by_id(session['user_id'])
    return render_template("verify_editor.html", classData = classrow, schoolInfo=schoolrow, id = subject_id)

@app.route("/mastersheet", methods=["POST"])
@login_required
@check_confirmed
def mastersheet():
    class_id = request.form.get("class_id")
    tables = database(class_id)
    classrow = select_all_from(tables['classes'], 'id', class_id)
    schoolrow = select_school_by_id(session['user_id'])
    carow = select_all_from_table(tables['ca'])
    testrow = select_all_from_table(tables['test'])
    examrow = select_all_from_table(tables['exam'])
    classlistrow = select_all_from_table(tables['classlist'])
    mastersheet_rows = select_all_from_table['mastersheet']
    grades = select_all_from_table(tables['grade'])
    subject_p = select_all_from_table(tables['subject_position'])
    subjectrow = select_all_from_table(tables['subjects'])
    results = select_all_from_row(tables['classes'], 'id', class_id)

    return render_template("printable_mastersheet.html",gradeData = grades,result = results[0], caData = carow, testData = testrow, examData = examrow, classData = classrow, schoolInfo = schoolrow, subjectData=subjectrow,class_list = classlistrow, mastersheet = mastersheet_rows, subject_position= subject_p)

@app.route("/mastersheet_pdf", methods=["POST"])
@login_required
@check_confirmed
def mastersheet_pdf():
    class_id = request.form.get("class_id")
    tables = database(class_id)
    classrow = select_all_from(tables['classes'], 'id', class_id)
    schoolrow = select_school_by_id(session['user_id'])
    carow = select_all_from_table(tables['ca'])
    testrow = select_all_from_table(tables['test'])
    examrow = select_all_from_table(tables['exam'])
    classlistrow = select_all_from_table(tables['classlist'])
    mastersheet_rows = select_all_from_table['mastersheet']
    grades = select_all_from_table(tables['grade'])
    subject_p = select_all_from_table(tables['subject_position'])
    subjectrow = select_all_from_table(tables['subjects'])
    results = select_all_from_row(tables['classes'], 'id', class_id)
    html =  render_template("mastersheet_pdf.html",gradeData=grades,result = results[0], caData = carow, testData = testrow, examData = examrow, classData = classrow, schoolInfo = schoolrow, subjectData=subjectrow,class_list = classlistrow, mastersheet = mastersheet_rows, subject_position= subject_p)
    return render_pdf(HTML(string=html))


@app.route("/customize", methods=["POST"])
@login_required
@check_confirmed
def customize():
    if session["class_settings"]:
        error = "Settings are currently being updated please wait"
        flash(error)
        return render_class(request.form.get("class_id"))
    session["class_settings"] = True
    class_id = request.form.get("class_id")
    tables = database(class_id)
    schoolrow = select_school_by_id(session['user_id'])
    current_settings = select_all_from_row(tables['settings'], 'id', class_id)
    setting = current_settings[0]
    classRows, class_info  = select_all_from_id(tables['classes'], 'id', class_id)
    if int(request.form.get("ca_score")) != int(classRows[0]["ca"]) or int(request.form.get("test_score")) != int(classRows[0]["test"]) or int(request.form.get("exam_score")) != int(classRows[0]["exam"]):
        sum_score = 0
        if request.form.get("ca"):
            sum_score = sum_score + int(request.form.get("ca_score"))
        if request.form.get("test"):
            sum_score = sum_score + int(request.form.get("test_score"))
        if request.form .get("exam"):
            sum_score = sum_score + int(request.form.get("exam_score"))
        if sum_score != 100:
            flash("ca score + test score  + exam score must be equal to 100")
            return render_template("customize.html", schoolInfo = schoolrow,classData=classRows, classInfo=class_info[0], class_setting=current_settings[0])
        else:
          
            update_table(tables['settings'], ['ca', 'test', 'exam', ], [int(request.form.get("ca_score")),request.form.get("test_score"), request.form.get("exam_score")], 'id', class_id)

    if request.form.get("table_type") and request.form.get("table_type") != setting["table_type"]:
        update_table(tables['settings'],'table_type', request.form.get("table_type"), 'id', class_id)

    if request.form.get("ca") != setting["ca"]:
        if request.form.get("ca"):
            update_table(tables['settings'], 'ca', 'on','id', class_id)
        else :
            update_table(tables['settings'], 'ca', 'off','id', class_id)


    if  request.form.get("test") != setting["test"]:
        if request.form.get("test"):
            update_table(tables['settings'], 'test', 'on','id', class_id)
        else:
            update_table(tables['settings'], 'test', 'off','id', class_id)

  
    if  request.form.get("combined") != setting["combined"]:
        if request.form.get("combined"):
            update_table(tables['settings'], 'combined', 'on','id', class_id)
        else:
            update_table(tables['settings'], 'combined', 'off','id', class_id)

    if  request.form.get("exam") != setting["exam"]:
        if request.form.get("exam"):
            update_table(tables['settings'], 'exam', 'on','id', class_id)
        else :
            update_table(tables['settings'], 'exam', 'off','id', class_id)

    if  request.form.get("subject_total") and setting["subject_total"] == 'off':
        update_table(tables['settings'], 'subject_total', 'on','id', class_id)
    elif not request.form.get('subject_total') and setting['subject_total'] == 'on' :
        update_table(tables['settings'], 'subject_total', 'off','id', class_id)
    
    if request.form.get("subject_comment") and setting['subject_comment'] == 'off':
        update_table(tables['settings'], 'subject_comment', 'on','id', class_id)
    elif not request.form.get('subject_comment') and setting['subject_comment'] == 'on' :
        update_table(tables['settings'], 'subject_comment', 'off','id', class_id)

    if request.form.get("class_average") and setting["class_average"] == 'off':
        update_table(tables['settings'], 'class_average', 'on','id', class_id)
    elif not request.form.get('class_average') and setting['class_average'] == 'on' :
        update_table(tables['settings'], 'class_average', 'off','id', class_id)

    if request.form.get("grade") and setting["grade"] == 'off':
        update_table(tables['settings'], 'grade', 'on','id', class_id)
    elif not request.form.get('grade') and setting['grade'] == 'on' :
        update_table(tables['settings'], 'grade', 'off','id', class_id)
    
    if  request.form.get("teachers_initials") != setting["teachers_initials"]:
        if request.form.get("teachers_initials"): 
            update_table(tables['settings'], 'teachers_initials', 'on','id', class_id)
        else:
            update_table(tables['settings'], 'teachers_initials', 'off','id', class_id)

    if request.form.get("total_score") != setting["total_score"]:
        if request.form.get("total_score"):
            update_table(tables['settings'], 'total_score', 'on','id', class_id)
        else:
            update_table(tables['settings'], 'total_score', 'off','id', class_id)

    if request.form.get("average_score") != setting["average"]:
        if request.form.get("average_score"):
            update_table(tables['settings'], 'average', 'on','id', class_id)
        else:
            update_table(tables['settings'], 'average', 'off','id', class_id)

    if  request.form.get("position") != setting["position"]:
        if request.form.get("position"): 
            update_table(tables['settings'], 'position', 'on','id', class_id)
        else :
            update_table(tables['settings'], 'position', 'off','id', class_id)


    if  request.form.get("teachers_line") != setting["teachers_line"] and request.form.get("teachers_line") != 'None':
        update_table(tables['settings'], 'teachers_line',request.form.get("teachers_line"), 'id', class_id )
    

    if  request.form.get("principal_line") != setting["principal_line"] and request.form.get("principal_line") != 'None':
        update_table(tables['settings'], 'principal_line',request.form.get("principal_line"), 'id', class_id )

    if  request.form.get("teachers_signature") != setting["teachers_signature"]:
        if request.form.get("teachers_signature"):
            update_table(tables['settings'], 'teachers_signature', 'on','id', class_id)
        else:
            update_table(tables['settings'], 'ca', 'off','id', class_id)
   
    if request.form.get("principal_signature") != setting["principal_signature"]:
        if request.form.get("principal_signature"):
            update_table(tables['settings'], 'principal_signature', 'on','id', class_id)
        else:
            update_table(tables['settings'], 'principal_signature', 'off','id', class_id)

    if request.form.get("subject_position") != setting["subject_position"]:
        if request.form.get("subject_position"):
            update_table(tables['settings'], 'subject_position', 'on','id', class_id)
        else:
            update_table(tables['settings'], 'subject_position', 'off','id', class_id)

    if request.form.get("average_score") != setting["average"]:
        if request.form.get("average_score"):
            update_table(tables['settings'], 'average', 'on','id', class_id)
        else:
            update_table(tables['settings'], 'average', 'off','id', class_id)


    if request.form.get("pandf") != setting["pandf"]:
        if request.form.get("pandf"):
            update_table(tables['settings'], 'pandf', 'on','id', class_id)
        else:
            update_table(tables['settings'], 'pandf', 'off','id', class_id)

    if request.form.get("grade_summary") != setting["grade_summary"]:
        if request.form.get("pandf"):
            update_table(tables['settings'], 'grade_summary', 'on','id', class_id)

        else:
            update_table(tables['settings'], 'grade_summary', 'off','id', class_id)
    
    if request.form.get("shadow") != setting["shadow"]:
        if request.form.get("shadow") == 'on':
            update_table(tables['settings'], 'shadow', 'on','id', class_id)       
        else:
            update_table(tables['settings'], 'shadow', 'off','id', class_id)
    if request.form.get("grading_type") and request.form.get("grading_type") != setting["grading_type"]:
        update_table(tables['settings'], 'grading_type',request.form.get("grading_type"),'id', class_id )
        update_grade(class_id)
    session["class_settings"] = False
    return render_class(class_id, error ="setting updated successfully")

@app.route("/admin_verification", methods=["POST"])
@login_required
@check_confirmed
def admin_verification():        
    password = request.form.get("password")
    tables= database(0)
    classrow = select_all_from_table(tables['classes'])
    schoolrow =  select_school_by_id(session['user_id'])
    settings = select_all_from_table(tables['settings'])
    if check_password_hash(schoolrow[0]["admin_password"], password ):
        session["school_setting"] = False
        return render_template("customize_school.html", schoolInfo = schoolrow, classData=classrow, class_setting = settings)
    else:
        error = "admin password incorrect"
        flash(error)
        return render_template("admin_verification.html",schoolInfo = schoolrow, error=error)


@app.route("/school_settings", methods=["GET"])
@login_required
@check_confirmed
def school_settings():        
    tables= database(0)
    classrow = select_all_from_table(tables['classes'])
    schoolrow =  select_school_by_id(session['user_id'])
    return render_template("admin_verification.html", schoolInfo = schoolrow, classData=classrow)

@app.route("/customize_school", methods=["POST"])
@login_required
@check_confirmed
def customize_school():
    if session["school_setting"]:
        error = "Setting is currently being updatede please wait"
        return render_portfolio(error)
    session["school_setting"] = True
    tables = database("0")
    classrow = select_all_from_table(tables['classes'])
    school_info =  select_school_by_id(session['user_id'])
    current_settings = select_current_term(tables['terms'], school_info[0]['current_term'], school_info[0]['current_session'])
    if len(current_settings) > 0:
        general_password = request.form.get("general_password")
        setting = current_settings[0]
        if general_password:
            if len(general_password) < 8:
                error = "General password must be up to 8 characters"
                flash(error)
                return render_template("customize_school.html", schoolInfo = school_info, classData=classrow, class_setting = current_settings)
            else:
                update_table('school', 'password',generate_password_hash(general_password), 'id', session['user_id'] )

        if  request.form.get("background_color") != setting["background_color"] :
            update_term_settings(tables['settings'], 'background_color',request.form.get("background_color"), school_info['current_term'], school_inf0['current_session'] )
        
        if request.form.get("line_color") != setting["line_color"]:
            update_term_settings(tables['settings'], 'line_color',request.form.get("line_color"), school_info['current_term'], school_inf0['current_session'] )
        
        if request.form.get("text_color") and request.form.get("text_color") != setting["text_color"]:
            update_term_settings(tables['settings'], 'text_color',request.form.get("text_color"), school_info['current_term'], school_inf0['current_session'] )

        if request.form.get("background_font") and request.form.get("background_font") != setting["background_font"]:
            update_term_settings(tables['settings'], 'background_font',request.form.get("background_font"), school_info['current_term'], school_inf0['current_session'] )
        
        if request.form.get("ld_position") and request.form.get("ld_position") != setting["ld_position"]:
            update_term_settings(tables['settings'], 'ld_position',request.form.get("ld_position"), school_info['current_term'], school_inf0['current_session'] )

        if request.form.get("l_font") and request.form.get("l_font") != setting["l_font"]:
            update_term_settings(tables['settings'], 'l_font',request.form.get("l_font"), school_info['current_term'], school_inf0['current_session'] )

        if request.form.get("l_color") and request.form.get("l_color") != setting["l_color"]:
            update_term_settings(tables['settings'], 'l_color',request.form.get("l_color"), school_info['current_term'], school_inf0['current_session'] )
    
        if request.form.get("l_font-size") and request.form.get("l_font-size") != setting["l_fontsize"]:
            update_term_settings(tables['settings'], 'l_fontsize',request.form.get("l_fontsize"), school_info['current_term'], school_inf0['current_session'] )

        if request.form.get("l_weight") and request.form.get("l_weight") != setting["l_weight"]:
            update_term_settings(tables['settings'], 'l_weight',request.form.get("l_weight"), school_info['current_term'], school_inf0['current_session'] )

        if request.form.get("sd_font") and request.form.get("sd_font") != setting["sd_font"]:
            update_term_settings(tables['settings'], 'sd_font',request.form.get("sd_font"), school_info['current_term'], school_inf0['current_session'] )

        if request.form.get("sd_color") and request.form.get("sd_color") != setting["sd_color"]:
            update_term_settings(tables['settings'], 'sd_color',request.form.get("sd_color"), school_info['current_term'], school_inf0['current_session'] )
    
        if request.form.get("sd_fontsize") and request.form.get("sd_fontsize") != setting["sd_fontsize"]:
            update_term_settings(tables['settings'], 'sd_fontsize',request.form.get("sd_fontsize"), school_info['current_term'], school_inf0['current_session'] )

        if request.form.get("sd_position") and request.form.get("sd_position") != setting["sd_position"]:
            update_term_settings(tables['settings'], 'sd_position',request.form.get("sd_position"), school_info['current_term'], school_inf0['current_session'] )

        if  request.form.get("sd_email") != setting["sd_email"] and request.form.get("sd_email") != 'None':
            update_term_settings(tables['settings'], 'sd_email',request.form.get("sd_email"), school_info['current_term'], school_inf0['current_session'] )
        
        if request.form.get("admin_email") != setting["admin_email"]:
            if request.form.get("admin_email") == 'on':
                update_term_settings(tables['settings'], 'admin_email','on', school_info['current_term'], school_inf0['current_session'] )
            else:
                update_term_settings(tables['settings'], 'admin_email','off', school_info['current_term'], school_inf0['current_session'] )

        if  request.form.get("address") != setting["address"] and request.form.get("address") != 'None' :
            update_term_settings(tables['settings'], 'address',request.form.get("address"), school_info['current_term'], school_inf0['current_session'] )

        if  request.form.get("po_box") != setting["po_box"] and request.form.get("po_box") != 'None':
            update_term_settings(tables['settings'], 'po_box',request.form.get("po_box"), school_info['current_term'], school_inf0['current_session'] )

        if  request.form.get("phone") != setting["phone"] and request.form.get("phone") != 'None':
            update_term_settings(tables['settings'], 'phone',request.form.get("phone"), school_info['current_term'], school_inf0['current_session'] )
        
        if  request.form.get("sd_other") != setting["sd_other"] and request.form.get("sd_other") != 'None':
            update_term_settings(tables['settings'], 'sd_other',request.form.get("sd_other"), school_info['current_term'], school_inf0['current_session'] )

        if  request.form.get("next_term") != setting["next_term"] and request.form.get("next_term") != 'None' :
            update_term_settings(tables['settings'], 'next_term',request.form.get("next_term"), school_info['current_term'], school_inf0['current_session'] )
    
        if  request.form.get("address") != setting["address"] and request.form.get("address") != 'None' :
            update_term_settings(tables['settings'], 'address',request.form.get("address"), school_info['current_term'], school_inf0['current_session'] )

        if request.form.get("std_font") and request.form.get("std_font") != setting["std_font"]:
            update_term_settings(tables['settings'], 'std_font',request.form.get("std_font"), school_info['current_term'], school_inf0['current_session'] )

        if request.form.get("std_color") and request.form.get("std_color") != setting["std_color"]:
            update_term_settings(tables['settings'], 'std_color',request.form.get("std_color"), school_info['current_term'], school_inf0['current_session'] )
    
        if request.form.get("std_fontsize") and request.form.get("std_fontsize") != setting["std_fontsize"]:
            update_term_settings(tables['settings'], 'std_fontsize',request.form.get("std_fontsize"), school_info['current_term'], school_inf0['current_session'] )

        if  request.form.get("watermark") != setting["watermark"]:
            if request.form.get("watermark") =='on':
                update_term_settings(tables['settings'], 'watermark','on', school_info['current_term'], school_inf0['current_session'] )
            else :
                update_term_settings(tables['settings'], 'watermark','off', school_info['current_term'], school_inf0['current_session'] )
        
        if  request.form.get("email_notification") != setting["email_notification"]:
            if request.form.get("email_notification") =='on':
                update_term_settings(tables['settings'], 'email_notification','on', school_info['current_term'], school_inf0['current_session'] )
            else :
                update_term_settings(tables['settings'], 'email_notification','off', school_info['current_term'], school_inf0['current_session'] )

        if request.form.get("std_position") and request.form.get("std_position") != setting["std_position"]:
            update_term_settings(tables['settings'], 'std_position',request.form.get("std_position"), school_info['current_term'], school_inf0['current_session'] )
    # if new term is selected or new session is selected 
    if (request.form.get("term") or request.form.get("session")):
        session_data = select_all_from_table(tables['terms'])
        session["selected_session"] = request.form.get("session")
        session["selected_term"] = request.form.get("term")
        if not session["selected_session"]:
            session["selected_session"] = school_info[0]["current_session"]
        if not session["selected_term"]:
            session["selected_term"] = "1"

        # if term and session combination is not in existence  
        if not session_term_check(session["selected_session"], session["selected_term"]):
            # if the selected session is the current session
            if session["selected_session"] == school_info[0]["current_session"]:
                new_term(session["selected_session"], session["selected_term"])
            else:
                return render_template("session_update.html", selected_session = session["selected_session"], selected_term =  session["selected_term"], schoolInfo = school_info, session_data = session_data)
        else:
            update_table('school',['current_term', 'current_session'], [session['selected_term'], session['selected_session']], 'id', session['user_id'] )
    session["school_setting"] = False
    flash("Settings updated successfully!")
    return render_portfolio()


@app.route("/session_update", methods=["POST"])
@login_required
@check_confirmed
def session_update():
    all_classes = []
    tables = database(0)
    classes = select_all_from_table(tables['classes'])
    school_info =  select_school_by_id(session['user_id'])
    for klass in classes:
        name = "name"+str(klass["id"])
        # check for new name
        if request.form.get(name) == "":
            error = klass["classname"].upper() +" do not have a new name for the new session"
            flash(error)
            return render_template("session_update.html", selected_session = session["selected_session"], selected_term =  session["selected_term"], schoolInfo = school_info, session_data = classes)

        # check if new name is equal to old name
        if request.form.get(name).lower() == klass["classname"]:
            error = klass["classname"].upper()+ " cannot have the same name for different sessions"
            flash(error)
            return render_template("session_update.html", selected_session = session["selected_session"], selected_term =  session["selected_term"], schoolInfo = school_info, session_data = classes)
        # add new name to array
        all_classes.append(request.form.get(name).lower())
	
    if has_duplicate(all_classes):
        error = "Two or more classes have the same name"
        flash(error)
        return render_template("session_update.html", selected_session = session["selected_session"], selected_term =  session["selected_term"], schoolInfo = school_info, session_data = classes)

    new_term( request.form.get("selected_session"),request.form.get("selected_term"))
    update_table('school', 'current_session',request.form.get("selected_session"),'id',session['user_id'] )
    tables = database(0)
    classes = select_all_from_table(tables['classes'])
    for  clas in classes:
        id = str(clas["id"])
        name = "name"+id
        section = "section"+id
        update_table(table['classes'], ['classname', 'section'],[request.form.get(name),request.form.get(section)],'id', id )
    error = "session changed successfully"
    return render_portfolio(error)
         


@app.route("/check_results", methods=["POST","GET"])
def check_results():
    if request.method == "POST":
        if session:
            session.clear()
        #if reg number is empty
        if not request.form.get("regnumber"):
            error = "provide students regnumber"
            flash(error)
            return render_template("login.html")
        #if reg number is empty
        if  not request.form.get("pin"):
            error = "provide students pin"
            flash(error)
            return render_template("login.html")

        # get user digit
        reg_number = request.form.get("regnumber")
        pin = request.form.get("pin")
        #if len of user string is less than 10 render invalid regnumber
        if len(reg_number) < 7:
            session.clear()
            error = "reg number invalid"
            flash(error)
            return render_template("login.html")

        #collect student id class id and school id
        student_id = reg_number[0]+reg_number[1]+reg_number[2]
        while student_id[0] == "0":
            student_id = student_id.strip("0")

        class_id = reg_number[3]+reg_number[4]+reg_number[5]
        if class_id[0] == "0":
            class_id = class_id.strip("0")
        if class_id[0] == "0":
            class_id = class_id.strip("0")
        school_length = len(reg_number) - 6
        school_id = reg_number[-school_length:]
        #check if school exist else
        schoolInfo = select_school_by_id(school_id)
        if len(schoolInfo) != 1:
            error ="reg number invalid"
            flash(error)
            return render_template("login.html")
            
        session["user_id"] = schoolInfo[0]["id"]
        tables = database(0)
        #check if class exist else "reg doesnt exist"
        classInfo = select_all_from_row(tables['classes'], 'id', class_id)
        if len(classInfo) != 1:
            error = "reg number invalid"
            session.clear()
            flash(error)
            return render_template("login.html")
        
        tables = database(str(classInfo[0]["id"]))
        #check if student exist in class else "reg doesnt exist"
        studentInfo = select_all_from_row(tables['classlist'], 'id', student_id)
        if len(studentInfo) != 1:
            error = "regnumber invalid"
            session.clear()
            flash(error)
            return render_template("login.html")
        
        #check if pin is same with given pin is students pin else pin is incorrect
        if pin != str(studentInfo[0]["pin"]):
            error = "pin invalid"
            session.clear()
            flash(error)
            return render_template("login.html")
        tables= database(class_id)
        classrow = select_all_from(tables['classes'], 'id', class_id)
        schoolrow = select_school_by_id(session['user_id'])
        carow = select_all_from_row(tables['ca'],'id', student_id)
        testrow = select_all_from_row(tables['test'],'id', student_id)
        examrow = select_all_from_row(tables['exam'],'id', student_id)
        classlistrow = select_all_from_row(tables['classlist'],'id', student_id)
        mastersheet_rows = select_all_from_row(tables['mastersheet'],'id', student_id)
        grades = select_all_from_row(tables['grade'],'id', student_id)
        subject_position_row = select_all_from_row(tables['subject_position'],'id', student_id)
        subjectrow = select_all_from_row(tables['subjects'],'id', student_id)
        results = select_all_from_row(tables['classes'],'id', class_id)
        session.clear()

        return render_template("result_sheet.html",gradeRows = grades,result = results[0], schoolInfo = schoolrow, classData = classrow, caData = carow, testData = testrow, examData = examrow, subjectData = subjectrow,class_list = classlistrow, mastersheet = mastersheet_rows, subject_position = subject_position_row)
    else:
        return render_template("check_result.html")
            

@app.route("/result_check", methods=["POST"])
def result_check():
    # get user digit
    reg_number = request.form.get("regnumber")
    pin = request.form.get("pin")

    if len(reg_number) < 7:
        session.clear()
        return jsonify(value="fail")

    #collect student id class id and school id
    student_id = reg_number[0]+reg_number[1]+reg_number[2]
    while student_id[0] == "0":
        student_id = student_id.strip("0")

    class_id = reg_number[3]+reg_number[4]+reg_number[5]
    if class_id[0] == "0":
        class_id = class_id.strip("0")

    if class_id[0] == "0":
        class_id = class_id.strip("0")

    school_length = len(reg_number) - 6
    school_id = reg_number[-school_length:]
    
    #check if school exist else
    studentInfo = select_all_from_row(tables['classlist'], 'id', student_id)
    if len(schoolInfo) != 1:
        return jsonify(value="fail")
        
    session["user_id"] = schoolInfo[0]["id"]
    tables = database(0)
    #check if class exist else "reg doesnt exist"
    classInfo = select_all_from_row(tables['classes'], 'id', class_id)
    if len(classInfo) != 1:
        session.clear()
        return jsonify(value="fail")
    
    tables = database(str(classInfo[0]["id"]))
    #check if student exist in class else "reg doesnt exist"
    studentInfo = select_all_from_row(tables['classlist'], 'id', student_id)
    if len(studentInfo) != 1:
        session.clear()
        return jsonify(value="fail")
    
    #check if pin is same with given pin is students pin else pin is incorrect
    if pin != str(studentInfo[0]["pin"]):
        session.clear()
        return jsonify(value="pin invalid")
    
    else:
        return jsonify(value="pass")


@app.route("/admin_check", methods=["POST"])
@login_required
@check_confirmed
def admin_check():
    password = request.form.get("password")
    school =  select_school_by_id(session['user_id'])
    if check_password_hash(school[0]["admin_password"],password):
        return "correct"
    else:
        return "incorrect password"



@app.route("/terms", methods=["GET"])
def terms():
    return render_template("terms.html")

@app.route("/privacy", methods=["GET"])
def privacy():
    return render_template("privacy.html")


@app.route("/print_pins", methods=["GET"])
@login_required
@check_confirmed
def print_pins():        
    tables= database(0)
    classrow = select_all_from_table(tables['classes'])
    schoolrow =  select_school_by_id(session['user_id'])
    return render_template("pin_verification.html", schoolInfo = schoolrow, classData=classrow)


@app.route("/admin_verified", methods=["POST"])
@login_required
@check_confirmed
def admin_verified():        
    password = request.form.get("password")
    tables= database(0)
    classrow = select_all_from_table(tables['classes'])
    schoolrow =  select_school_by_id(session['user_id'])
    settings = select_all_from_table(tables['term'])
    classlist = []
    if check_password_hash(schoolrow[0]["admin_password"], password ):
        for klass in classrow:
            tables=database(klass["id"])
            classlis = select_all_from_table(tables['classlist'])
            classlist.append(classlis)
        return render_template("pins.html", schoolInfo = schoolrow, classData=classrow, result = settings[0], classlists= classlist)

    else:
        error = "admin password incorrect"
        flash(error)
        
        return render_template("pin_verification.html",schoolInfo = schoolrow, error=error)

@app.route("/manage_password", methods=["GET"])
@login_required
@check_confirmed
def manage_password():        
    tables= database(0)
    schoolrow =  select_school_by_id(session['user_id'])
    return render_template("password_verification.html", schoolInfo = schoolrow)


@app.route("/password_verified", methods=["POST"])
@login_required
@check_confirmed
def password_verified():        
    password = request.form.get("password")
    tables= database(0)
    classrow = select_all_from_table(tables['classes'])
    schoolrow =  select_school_by_id(session['user_id'])
    if check_password_hash(schoolrow[0]["admin_password"], password ):
        return render_template("change_passwords.html", schoolInfo = schoolrow, classData=classrow)
    else:
        error = "admin password incorrect"
        flash(error)
        return render_template("password_verification.html",schoolInfo = schoolrow, error=error)


@app.route("/password_changer", methods=["POST"])
@check_confirmed
@login_required
def password_changer():        
    tables= database(0)
    classrow = select_all_from_table(tables['classes'])
    user_input = request.form.get("general")
    if user_input:
        update_school('school', 'password',generate_password_hash(request.form.get("general")), 'id', session['user_id'] )
    for klass in classrow:
        if request.form.get(klass["id"]):
            update_school(tables['terms'], 'password',generate_password_hash(request.form.get(klass['id'])))

    error="password changed successfully"
    return render_portfolio(error)

@app.route("/contact", methods=["GET"])
def contact():
    return render_template('contact.html')      

