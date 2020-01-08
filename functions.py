#!/usr/bin/python
from flask import redirect, render_template, request, session, flash
from functools import wraps
from operator import itemgetter, attrgetter
import requests
from itsdangerous import URLSafeTimedSerializer
from flask_mail import Message, Mail
import random
import string
from model import connect, select_all_from_id, select_all_from_table, create_ca_table, create_classlist_table, create_exam_table, create_grades_table, create_test_table, create_mastersheet_table, create_settings_table, create_subjects_table, create_subject_position_table, drop_table,delete_from_id
import psycopg2.extras
from psycopg2 import sql



def login_required(f):
    """
    Decorate routes to require login.

    http://flask.pocoo.org/docs/0.12/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function


def check_confirmed(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        current_user = select_all_from_id('school',session.get('user_id'))
        if not current_user[0]["confirmed"]:
            flash('Please confirm your account!', 'warning')
            return redirect("/unconfirmed")
        return func(*args, **kwargs)
    return decorated_function


# forms the result data given the id of the class
def database(id):
    if type(id) not in [int]:
        raise TypeError('id must be an int')
    if id < 0:
        raise ValueError('id must be an Integer greater than 0')
    tables = {}
    # format class tables names
    school = select_all_from_id('school',session.get('user_id'))
    current_session = school[0]["current_session"]
    current_term = school[0]["current_term"]
    tables["class_id"] = id
    tables["school_id"] = session["user_id"]
    schoolId = session["user_id"]
    tables["terms"] = "terms"+"_"+str(schoolId)
    termsql.Identifierifier = str(current_term)+"_"+str(current_session)+"_"+str(tables["school_id"])
    classsql.Identifierifier = str(tables["class_id"])+"_"+str(current_term)+"_"+str(current_session)+"_"+str(tables["school_id"])
    tables["classes"] = "classes"+"_"+termsql.Identifierifier
    tables["settings"] = "settings"+"_"+termsql.Identifierifier
    tables["classlist"] = "classlist"+"_"+classsql.Identifierifier
    tables["ca"]  = "catable"+"_"+classsql.Identifierifier
    tables["test"] = "testtable"+"_"+classsql.Identifierifier
    tables["exam"] = "examtable"+"_"+classsql.Identifierifier
    tables["subjects"] = "subjects"+"_"+classsql.Identifierifier
    tables["mastersheet"] = "mastersheet"+"_"+classsql.Identifierifier
    tables["subject_position"] = "subject_position"+"_"+classsql.Identifierifier
    tables["grade"] = "grade"+"_"+classsql.Identifierifier
    return tables

# gives the initial of a name
def initials (name):
    if type(name) is not str:
        raise TypeError('fullname or name must be a str')
    fullname = name.split()
    initials = ''
    for name in fullname:
        initials = initials+name[0]
    return initials

# returns the grade of any given score
def grade(score,grading_type="WAEC"):
    if type(score) not in [int, float]:
        raise TypeError('score must be a number ')
    score = int(score)
    if type(grading_type) is not str:
        raise TypeError('grading type must be a str')
    grading_type = grading_type.upper()
    if grading_type not in ['WAEC', 'SUBEB']:
        raise ValueError('Grading type must be waec or subeb')
    if score < 0 or score > 100:
        raise ValueError('score must be a number between 0 and 100 or 0 0r 100')
    if grading_type == "WAEC":
        pass_mark = 40
        if score < 40:
            score_grade = "F9"
        elif score > 39 and score < 46:
            score_grade = "E8"
        elif score > 44 and score < 50:
            score_grade = "D7"
        elif score > 49 and score < 55:
            score_grade = "C6"
        elif score > 54 and score < 60:
            score_grade = "C5"
        elif score > 59 and score < 65:
            score_grade = "C4"
        elif score > 64 and score < 70:
            score_grade = "B3"
        elif score > 69 and score < 75:
            score_grade = "B2"
        else:
            score_grade = "A1"
    elif grading_type == "SUBEB":
        pass_mark = 30
        if score < 30:
            score_grade = "F"
        elif score > 29 and score < 40:
            score_grade = "E"
        elif score > 39 and score < 50:
            score_grade = "D"
        elif score > 49 and score < 60:
            score_grade = "C"
        elif score > 59 and score < 70:
            score_grade = "B"
        else:
            score_grade = "A"
    grading ={}
    grading["score_grade"] = score_grade
    grading["pass_mark"] = pass_mark
    return grading

#check array for duplicate elsments, returns true if there exist one
def has_duplicate(arr):
    if type(arr) is not list:
        raise ValueError('function has_duplicate takes array as argument')
    if len(set(arr)) != len(arr):
        return True
    else:
        return False

def render_class(class_id, error=None):
    # format class tables names
    tables = database(class_id)
    #query database
    classrow = select_all_from_id(tables['classes'],class_id)
    schoolrow = select_all_from_id('school', session['user_id'])
    subjectrow = select_all_from_table(tables['subjects'])
    classlistrow = select_all_from_table(tables['classlist'])
    # render class veiw
    if error:
    	flash(error,'failure')
    return render_template("classView.html", schoolInfo = schoolrow, classData = classrow, subjectData = subjectrow,class_list = classlistrow, error=error)

def render_portfolio(error=None):
    tables = database(0)
    rows = select_all_from_id('school', session['user_id'])
    classrows = select_all_from_table(tables['classes'])
    if error:
    	flash(error,'failure')
    return render_template("portfolio.html", schoolInfo = rows, clas = classrows, error=error)

def ith_position(num):
    if type(num) is not int:
        raise TypeError('number must be an integer')
    if num < 0 or num == 0:
        raise ValueError('number must be a number greater than 0')
    temp = str(num)
    last_digit = temp[-1]
    if last_digit == '1':
        return str(num) + "st"
    elif last_digit == '2':
        return str(num) + "nd"
    elif last_digit == '3':
        return str(num) + "rd"
    else:
        return str(num)+"th"

def assign_student_position(class_id):
    tables = database(class_id)
    student_position = select_all_from_table(tables['mastersheet'])
    for student in student_position:
        student["average"] = float(student["average"])

    student_position = sorted(student_position, key = itemgetter('average'), reverse=True)
    j = 0
    i = 0
    previous = None
    conn = connect()
    db = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    for person in student_position:
        if previous == float(person["average"]):
            db.execute(sql.SQL("UPDATE {mastersheet} SET position = {sposition}  WHERE id ={id}").format(mastersheet = sql.Identifier(tables["mastersheet"]),  sposition = sql.Literal(ith_position(j)), id = sql.Literal(person["id"])))
        else:
            j = i + 1
            db.execute(sql.SQL("UPDATE {mastersheet} SET position = {sposition}  WHERE id ={id}").format(mastersheet = sql.Identifier(tables["mastersheet"]),  sposition = sql.Literal(ith_position(j)), id = sql.Literal(person["id"])))
        i = i + 1
        previous = float(person["average"])
    conn.commit()
    db.close()
    if conn is not None:
        conn.close() 

def assign_subject_position(class_id, subject_id):
    tables = database(class_id)
    subject = str(subject_id)
    subject_position  = select_all_from_table(tables['mastersheet'])
    for student in subject_position:
        student[subject] = float(student[subject])
    subject_pos = sorted(subject_position, key = itemgetter(subject), reverse=True)
    j = 0
    i = 0
    previous = 101
    conn = connect()
    db = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    for person in subject_pos:
        if previous == float(person[subject]):
            db.execute(sql.SQL("UPDATE {positIon_table} SET {subject} = {position}    WHERE id ={id}").format(positIon_table = sql.Identifier(tables["subject_position"]),subject = sql.Identifier(subject),  position =sql.Literal(ith_position(j)), id = sql.Literal(person["id"])))
        else:
            j = i + 1
            db.execute(sql.SQL("UPDATE {positIon_table} SET {subject} = {position}    WHERE id ={id}").format(positIon_table = sql.Identifier(tables["subject_position"]),subject = sql.Identifier(subject),  position = sql.Literal(ith_position(j)), id = sql.Literal(person["id"])))
        i = i + 1
        previous = float(person[subject])
    conn.commit()
    db.close()
    if conn is not None:
        conn.close() 

def term_tables(classid):
    tables = database(classid)

    # create classlist
    create_classlist_table(tables['classlist'])

    # create classlist
    create_subjects_table(tables['subjects'])

    # create  catable
    create_ca_table(tables['ca'], tables['classlist'])

    # create  grade
    create_grades_table(tables['grades'], tables['classlist'])

    # create testtable
    create_test_table(tables['test'], tables['classlist'])

    # create examtable    
    create_exam_table(tables['exam'], tables['classlist'])

    # create mastersheet
    create_mastersheet_table(tables['mastersheet'], tables['classlist'])

    # create subject_position
    create_subject_position_table(tables['subject_position'], tables['classlist'])


def passwordGen(stringLength=8):
    """Generate a random string of fixed length """
    if type(stringLength) is not int:
        raise TypeError('function take an integer as parameter')
    if stringLength < 0 or stringLength == 0:
        raise ValueError('function only take numbers greater than 0')
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))

def drop_tables(classid):
    tables = database(classid)

    # drop  catable
    drop_table(tables['ca'])

    # drop  grade
    drop_table(tables['grade'])

    # drop testtable
    drop_table(tables['test'])

    # drop examtable
    drop_table(tables['exam'])

    # drop mastersheet
    drop_table(tables['mastersheet'])

    # drop subject_position
    drop_table(tables['subject_position'])

    # drop subject_position
    drop_table(tables['subjects'])

    # drop classlist
    drop_table(tables['classlist'])


def remove_student(student_id, class_id):
    tables= database(class_id)
    student_grade = select_all_from_id(tables['grade'], student_id)
    subjects = select_all_from_table(tables['subjects'])
    students = select_all_from_table(tables['classlist'])
    totals = select_all_from_id(tables['mastersheet'], student_id)
    class_details = select_all_from_id(tables['settings'], class_id)
    db.execute("DELETE  FROM {mastersheet} where id={id}".format(mastersheet = tables["mastersheet"], id=student_id))
    delete_from_id(tables['mastersheet'], student_id)
    #for each subject in grades
    for subject in subjects:
	    #get students grade in this subject
        the_grade = student_grade[0][str(subject["id"])]		
        #form the column string for no_of_column
        the_column = "no_of_"+str(the_grade[0].lower())
        current = int(subject[the_column])
        #subract 1 from that no_of_column in subjects
        new_total = int(subject["total_score"]) - int(totals[0][str(subject["id"])])
        conn = connect()
        db = conn.cursor()
        #subtract students total from subjects total 
        db.execute(sql.SQL("UPDATE {subjects} SET total_score = {new} WHERE id = {id}").format(subjects=sql.Identifier(tables["subjects"]), new= sql.Literal(new_total) , id =sql.Literal(subject["id"])))
        no_of_students = len(students) - 1
        if no_of_students == 0:
            new_average = 0
        else:
            new_average = new_total /  no_of_students

        if the_grade[0] == "F":
            db.execute(sql.SQL("UPDATE {subjects} SET no_failed = {new},class_average = {cnew},{no_of_grade} = {gnew} WHERE id = {id}").format(subjects=sql.Identifier(tables["subjects"]), new = sql.Literal(int(subject["no_failed"])-1), id =sql.Literal(subject["id"]), no_of_grade=sql.Identifier(the_column),gnew=sql.Literal(current -1),cnew= sql.Literal(new_average))) 
        else:
            db.execute(sql.SQL("UPDATE {subjects} SET no_passed = {new},class_average = {cnew}, {no_of_grade} = {gnew} WHERE id = {id}").format(subjects=sql.Identifier(tables["subjects"]), new = sql.Literal(int(subject["no_passed"])-1), id =sql.Literal(subject["id"]) , no_of_grade=sql.Identifier(the_column),gnew=sql.Literal(current -1),cnew= sql.Literal(new_average))) 
        assign_subject_position(class_id, subject["id"])
    student_average = totals[0]["average"]
    pass_mark = grade(0)["pass_mark"]
    delete_from_id(table['ca'], student_id)
    delete_from_id(tables['grade'], student_id)
    delete_from_id(tables['test'], student_id)
    delete_from_id(tables['exam'], student_id)
    delete_from_id(tables['subject_position'], student_id)
    delete_from_id(tables['classlist'], student_id)
    assign_student_position(class_id)
    conn.commit()
    db.close()
    if conn is not None:
        conn.close()



def add_student(student_id, class_id):
    tables= database(class_id)
    student_grade = select_all_from_id(tables['grade'], student_id)
    all_std = select_all_from_table(tables['grade'])
    subjects = select_all_from_table(tables['subjects'])
    totals = select_all_from_id(tables['mastersheet'], student_id)
    class_details = select_all_from_id(tables['classes'],class_id)
    #for each subject in grades
    student_total = 0
    passed = 0
    failed = 0
    new_total = 0
    pass_mark = grade(0)["pass_mark"]
    conn = connect()
    db = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    for subject in subjects:
        student_total = student_total + int(totals[0][str(subject["id"])])
        the_grade = student_grade[0][str(subject["id"])][0]
        #form the column string for no_of_column
        the_column = "no_of_"+str(the_grade).lower()
        current = int(subject[the_column])
        #subract 1 from that no_of_column in subjects
        new_total = int(subject["total_score"]) + int(totals[0][str(subject["id"])])
        new_average = new_total / len(all_std)
        #subtract students total from subjects total 
        previous = select_all_from_id(tables['grades'], student_id)
        new_no = int(previous[0][the_column])  + 1
        if the_grade == "F":
            db.execute(sql.SQL("UPDATE {subjects} SET no_failed = {new},total_score = {tnew}, class_average = {dnew},{no_of_grade} = {gnew} WHERE id = {id}").format(subjects=sql.Identifier(tables["subjects"]), new = sql.Literal(int(subject["no_failed"])+1), id =sql.Literal(subject["id"]),dnew= sql.Literal(new_average),gnew=sql.Literal(current + 1), tnew= sql.Literal(int(new_total)) ,no_of_grade=sql.Identifier(the_column)))
            failed = failed + 1 
        else:
            db.execute(sql.SQL("UPDATE {subjects} SET no_passed = {new},total_score = {tnew}, class_average = {dnew}, {no_of_grade} = {gnew} WHERE id = {id}").format(subjects=sql.Identifier(tables["subjects"]), new = sql.Literal(int(subject["no_passed"])+1), id =sql.Literal(subject["id"]),dnew= sql.Literal(new_average),gnew=sql.Literal(current + 1), tnew= sql.Literal(int(new_total)) ,no_of_grade=sql.Identifier(the_column)))
            passed = passed + 1
        db.execute(sql.SQL("UPDATE {grades} SET {no_of_grade} = {new}  WHERE id = {id}").format(grades=sql.Identifier(tables["grade"]), no_of_grade=sql.sql.Identifierifer(the_column),new=sql.Literal(new_no), id =sql.Literal(student_id)))
        assign_subject_position(class_id, subject["id"])
    if len(subjects) > 	0:
        student_average = student_total/len(subjects)
        db.execute(sql.SQL("UPDATE {mastersheet} SET average = {new},total_score = {tnew} WHERE id={id}").format(mastersheet=sql.Identifier(tables["mastersheet"]), new=sql.Literal(student_average), id=sql.Literal(student_id), tnew=sql.Literal(student_total)))
        if pass_mark > student_average:
            db.execute(sql.SQL("UPDATE {result} Set no_of_failures ={new_fail} WHERE id={id}").format(result = sql.Identifier(tables["classes"]), new_fail = sql.Literal(int(class_details[0]["no_of_failures"])+1), id=sql.Literal(class_id)))
        else:
            db.execute(sql.SQL("UPDATE {result} Set no_of_passes={new_pass} WHERE id={id}").format(result =sql.Identifier(tables["classes"]), new_pass = sql.Literal(int(class_details[0]["no_of_passes"])+1), id=sql.Literal(class_id)))
        assign_student_position(class_id)
    conn.commit()
    db.close()
    if conn is not None:
        conn.close()



def session_term_check(session,term):
    conn = connect()
    db = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    tables = database(0)
    db.execute(sql.SQL("SELECT * FROM {term_table}  WHERE term={term} AND session={session}").format(term_table= sql.Identifier(tables["terms"]), term = sql.Literal(term), session = sql.Literal(session) ))
    session_columns = db.fetchall()
    conn.commit()
    db.close()
    if conn is not None:
        conn.close()
    if len(session_columns) > 0:
        return True
    else:
        return False


def new_term(school_session,term):
    conn = connect()
    db = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    tables = database(0)
    selected_term = term
    selected_session = school_session
    former_term_settings = select_all_from_table(tables['settings'])
    new_session = selected_session+"_"+selected_term
    db.execute(sql.SQL("INSERT INTO {terms}(session, term)VALUES({this_session},{this_term})").format(terms = sql.Identifier(tables['terms']), this_session = sql.Literal(session), this_term = sql.Literal(term)))
    class_term_data = "settings"+"_"+str(selected_term)+"_"+str(selected_session)+"_"+str(session["user_id"])
    db.execute(sql.SQL("CREATE TABLE {result} AS  TABLE {class_settings}").format(result = sql.Identifier(class_term_data), class_settings= sql.Identifier(tables["settings"])))

    for  clas in former_term_settings:
        former = database(clas["id"])
        class_subjects = select_all_from_id(former["subjects"], clas["id"])
        # format class tables names
        classsql.Identifierifier = str(clas["id"])+"_"+str(selected_term)+"_"+str(selected_session)+"_"+str(former["school_id"])
        classlist = "classlist"+"_"+classsql.Identifierifier
        ca  = "catable"+"_"+classsql.Identifierifier
        test = "testtable"+"_"+classsql.Identifierifier
        exam = "examtable"+"_"+classsql.Identifierifier
        subjects = "subjects"+"_"+classsql.Identifierifier
        mastersheet = "mastersheet"+"_"+classsql.Identifierifier
        subject_position = "subject_position"+"_"+classsql.Identifierifier
        grade = "grade"+"_"+classsql.Identifierifier

        # create classlist
        db.execute(sql.SQL("CREATE TABLE {classlist} AS TABLE {former_classlist}").format(classlist =sql.Identifier(classlist), former_classlist=sql.Identifier(former["classlist"])))

        #create tables
        create_subjects_table(subjects)

        # create  catable
        create_ca_table(ca, classlist)

        # create  grade
        create_grades_table(grade, classlist)

        # create testtable
        create_test_table(test, classlist)


        # create examtable
        create_exam_table(exam, classlist)

        # create mastersheet
        create_mastersheet_table(exam, classlist)


        # create subject_position
        create_subject_position_table(subject_position,  classlist)

        #copy classlist
        tables = database(clas["id"])
        current_classlist = select_all_from_table(classlist)
        pins = generate_pins(10, len(previous_classlist))
        #change pins for  classlist
        i = 0
        for student in current_classlist:
            db.execute(sql.SQL("UPDATE {this_list} SET pin={new_pin} WHERE id={student_id}").format(this_list = sql.Identifier(classlist), new_pin =  sql.Literal(pins[i]), student_id = student["id"]))
            db.execute(sql.SQL("INSERT INTO {table_name} (id)VALUES({id})").format(table_name = sql.Identifier(ca), id =sql.Literal(student["id"])))
            db.execute(sql.SQL("INSERT INTO {table_name} (id)VALUES({id})").format(table_name = sql.Identifier(test), id =sql.Literal(student["id"])))
            db.execute(sql.SQL("INSERT INTO {table_name} (id)VALUES({id})").format(table_name = sql.Identifier(exam), id =sql.Literal(student["id"])))
            db.execute(sql.SQL("INSERT INTO {table_name} (id)VALUES({id})").format(table_name = sql.Identifier(grade), id =sql.Literal(student["id"])))
            db.execute(sql.SQL("INSERT INTO {table_name} (id)VALUES({id})").format(table_name = sql.Identifier(subject_position), id =sql.Literal(student["id"])))
            db.execute(sql.SQL("INSERT INTO {table_name} (id)VALUES({id})").format(table_name = sql.Identifier(mastersheet), id =sql.Literal(student["id"])))
            i = i + 1
    #update term om school
    db.execute(sql.SQL("UPDATE school SET current_term={value} WHERE id={id}").format(value= sql.Literal(selected_term), id=sql.Literal(session["user_id"])))
    conn.commit()
    db.close()
    if conn is not None:
        conn.close()

def generate_pins(length, count, alphabet=string.digits):
  alphabet = ''.join(set(alphabet))
  if count > len(alphabet)**length:
    raise ValueError("Can't generate more than %s > %s pins of length %d out of %r" %
                      count, len(alphabet)**length, length, alphabet)
  def onepin(length):
    return ''.join(random.choice(alphabet) for x in range(length))
  result = set(onepin(length) for x in range(count))
  while len(result) < count:
    result.add(onepin(length))
  return list(result)

  # send message to email
def send_email(to, subject, template, sender_email):
    msg = Message(
        subject,
        recipients=[to],
        html=template,
        sender=sender_email
    )
    mail.send(msg)
