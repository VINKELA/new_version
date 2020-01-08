import psycopg2.extras
from psycopg2 import sql
from config import config

def connect():
    """ Connect to the PostgreSQL database server """
    conn = None
    try:
        # read connection parameters
        params = config()
        # connect to the PostgreSQL server
        conn = psycopg2.connect(**params)
       # return cursor
        return conn
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)


def create_schools():
    conn = connect()
    db = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    query = sql.SQL("CREATE TABLE IF NOT EXISTS schools (id SERIAL PRIMARY KEY  NOT NULL, username VARCHAR(255), email VARCHAR(255), school_name VARCHAR(255), address VARCHAR(255), city VARCHAR(255), state VARCHAR(255), current_term VARCHAR(255), current_session VARCHAR(255), password VARCHAR(255), admin_password VARCHAR(255), token_id VARCHAR(255), token VARCHAR(255),confirmed BOOLEAN DEFAULT false, registered_on date, confirmed_on date, logo boolean DEFAULT false, logo_address VARCHAR(255))")
    db.execute(query)
    print(query.as_string(db))
    conn.commit()
    db.close()
    print('school table created successfully')
    if conn is not None:
        conn.close()


def create_terms_table(name):
    conn = connect()
    db = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    query = sql.SQL("CREATE TABLE IF NOT EXISTS {terms} (id SERIAL NOT NULL, session VARCHAR(255) NOT NULL, term VARCHAR(255)  NOT NULL, school_head VARCHAR(255), school_head_position VARCHAR(255),background_color VARCHAR(255) DEFAULT '#ffffff',text_color VARCHAR(255) DEFAULT 'black',line_color VARCHAR(255) DEFAULT 'black',background_font VARCHAR(255) DEFAULT 'Ariel',ld_position VARCHAR(255) DEFAULT 'center',l_font VARCHAR(255) DEFAULT 'Ariel',l_weight VARCHAR(255) DEFAULT '900',l_color VARCHAR(255) DEFAULT '#537fbe',l_fontsize VARCHAR(255) DEFAULT '30px',sd_font VARCHAR(255) DEFAULT 'Ariel',sd_color VARCHAR(255) DEFAULT '#808000',sd_fontsize VARCHAR(255) DEFAULT '20px',sd_position VARCHAR(255) DEFAULT 'center',sd_email VARCHAR(255) DEFAULT 'None',admin_email BOOLEAN DEFAULT false, address VARCHAR(255) DEFAULT 'None',po_box VARCHAR(255) DEFAULT 'None',phone VARCHAR(255) DEFAULT 'None',next_term VARCHAR(255) DEFAULT 'None',sd_other VARCHAR(255) DEFAULT 'None',std_color VARCHAR(255) DEFAULT 'black',std_font VARCHAR(255) DEFAULT 'Arial Narrow',std_fontsize VARCHAR(255) DEFAULT '18px',std_position VARCHAR(255) DEFAULT 'left', logo BOOLEAN DEFAULT false,watermark BOOLEAN DEFAULT false,email_notification BOOLEAN DEFAULT false,  PRIMARY KEY(session, term))").format(terms = sql.Identifier(name))
    db.execute(query)
    print(query.as_string(db))
    conn.commit()
    db.close()
    if conn is not None:
        conn.close()


def create_classes_table(name):
    conn = connect()
    db = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    query = sql.SQL("CREATE TABLE IF NOT EXISTS {classes}(id  SERIAL PRIMARY KEY  NOT NULL, classname VARCHAR(255) UNIQUE NOT NULL, section VARCHAR(255),class_teacher_surname VARCHAR(255),class_teacher_firstname VARCHAR(255),position VARCHAR(255),subscription VARCHAR(255),date_of_subscription VARCHAR(255),amount_paid VARCHAR(255),payment_order VARCHAR(255),superscription_expires VARCHAR(255),no_of_passes VARCHAR(255),no_of_failure VARCHAR(255)),grading_type VARCHAR(255) DEFAULT 'WAEC',").format(classes = sql.Identifier(name))
    db.execute(query)
    print(query.as_string(db))
    conn.commit()
    db.close()
    if conn is not None:
        conn.close()  

def create_settings_table(table_name, referenced_table):
    conn = connect()
    db = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    query = sql.SQL("CREATE TABLE IF NOT EXISTS {setting} (id INT  REFERENCES  {referenced_table} (id),background_color VARCHAR(255) DEFAULT '#ffffff',VARCHAR(255)_color VARCHAR(255) DEFAULT 'black',line_color VARCHAR(255) DEFAULT 'black',background_font VARCHAR(255) DEFAULT 'Ariel',ld_position VARCHAR(255) DEFAULT 'center',l_font VARCHAR(255) DEFAULT 'Ariel',l_weight VARCHAR(255) DEFAULT '900',l_color VARCHAR(255) DEFAULT '#537fbe',l_fontsize VARCHAR(255) DEFAULT '30px',sd_font VARCHAR(255) DEFAULT 'Ariel',sd_color VARCHAR(255) DEFAULT '#808000',sd_fontsize VARCHAR(255) DEFAULT '20px',sd_position VARCHAR(255) DEFAULT 'center',sd_email VARCHAR(255) DEFAULT 'None',admin_email BOOLEAN DEFAULT false, address VARCHAR(255) DEFAULT 'None',po_box VARCHAR(255) DEFAULT 'None',phone VARCHAR(255) DEFAULT 'None',next_term VARCHAR(255) DEFAULT 'None',sd_other VARCHAR(255) DEFAULT 'None',std_color VARCHAR(255) DEFAULT 'black',std_font VARCHAR(255) DEFAULT 'Arial Narrow',std_fontsize VARCHAR(255) DEFAULT '18px',std_position VARCHAR(255) DEFAULT 'left', table_type VARCHAR(255) DEFAULT 'striped',ca BOOLEAN DEFAULT true,test BOOLEAN DEFAULT true,exam BOOLEAN DEFAULT true,combined BOOLEAN DEFAULT true,subject_total BOOLEAN DEFAULT true,class_average BOOLEAN DEFAULT true,subject_position BOOLEAN DEFAULT true,grade BOOLEAN DEFAULT true,subject_comment BOOLEAN DEFAULT false,teachers_initials BOOLEAN DEFAULT false,total_score BOOLEAN DEFAULT true,average BOOLEAN DEFAULT true,position BOOLEAN DEFAULT true,teachers_line INTEGER DEFAULT 0,shadow BOOLEAN DEFAULT true,principal_line INTEGER DEFAULT 0,teachers_signature BOOLEAN DEFAULT false,principal_signature BOOLEAN DEFAULT false,pandf BOOLEAN DEFAULT true,grade_summary BOOLEAN DEFAULT true,watermark BOOLEAN DEFAULT false,email_notification BOOLEAN DEFAULT true)").format(setting = sql.Identifier(table_name), referenced_table = sql.Identifier(referenced_table))
    db.execute(query)
    print(query.as_string(db))
    conn.commit()
    db.close()
    if conn is not None:
        conn.close()  

def create_classlist_table(name):
    conn = connect()
    db = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    query = sql.SQL("CREATE TABLE IF NOT EXISTS {classlist}(id  SERIAL PRIMARY KEY  NOT NULL, surname VARCHAR(255)  NOT NULL, firstname VARCHAR(255) NOT NULL,othername VARCHAR(255),gender VARCHAR(255),pin VARCHAR(255),regnumber VARCHAR(255))").format(classlist = sql.Identifier(name))
    db.execute(query)
    print(query.as_string(db))
    conn.commit()
    db.close()
    if conn is not None:
        conn.close()  

def create_subjects_table(name):
    conn = connect()
    db = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    query = sql.SQL("CREATE TABLE IF NOT EXISTS {classlist}(id  SERIAL PRIMARY KEY  NOT NULL, name VARCHAR(255)  NOT NULL, firstname VARCHAR(255) NOT NULL,surname VARCHAR(255) NOT NULL,subject_total INT DEFAULT 0,subject_average INT DEFAULT 0, no_of_a  INT DEFAULT 0,no_of_b  INT DEFAULT 0,no_of_c  INT DEFAULT 0,no_of_d  INT DEFAULT 0,no_of_e  INT DEFAULT 0,no_of_f  INT DEFAULT 0)").format(classlist = sql.Identifier(name))
    db.execute(query)
    print(query.as_string(db))
    conn.commit()
    db.close()
    if conn is not None:
        conn.close()  


def create_mastersheet_table(table_name, referenced_table):
    conn = connect()
    db = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    query = sql.SQL("CREATE TABLE IF NOT EXISTS {mastersheet}(id INT REFERENCES {classlist} (id), total INT DEFAULT 0, average VARCHAR(255),position INT)").format(mastersheet = sql.Identifier(table_name),  classlist =  sql.Identifier(referenced_table))
    db.execute(query)
    print(query.as_string(db))
    conn.commit()
    db.close()
    if conn is not None:
        conn.close()  



def create_grades_table(table_name, referenced_table):
    conn = connect()
    db = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    query = sql.SQL("CREATE TABLE IF NOT EXISTS {grades}(id INT REFERENCES {classlist} (id), no_of_a  INT DEFAULT 0,no_of_b  INT DEFAULT 0,no_of_c  INT DEFAULT 0,no_of_d  INT DEFAULT 0,no_of_e  INT DEFAULT 0,no_of_f  INT DEFAULT 0)").format(grades = sql.Identifier(table_name), classlist = sql.Identifier(referenced_table))
    db.execute(query)
    print(query.as_string(db))
    conn.commit()
    db.close()
    if conn is not None:
        conn.close() 

def create_ca_table(table_name, referenced_table):
    conn = connect()
    db = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    query = sql.SQL("CREATE TABLE IF NOT EXISTS {ca}(id INT REFERENCES {classlist} (id))").format(ca = sql.Identifier(table_name), classlist = sql.Identifier(referenced_table))
    db.execute(query)
    print(query.as_string(db))
    conn.commit()
    db.close()
    if conn is not None:
        conn.close() 

def create_test_table(table_name, referenced_table):
    conn = connect()
    db = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    query = sql.SQL("CREATE TABLE IF NOT EXISTS {test}(id INT REFERENCES {classlist} (id))").format(test = sql.Identifier(table_name), classlist = sql.Identifier(referenced_table))
    db.execute(query)
    print(query.as_string(db))
    conn.commit()
    db.close()
    if conn is not None:
        conn.close() 

def create_exam_table(table_name, referenced_table):
    conn = connect()
    db = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    query = sql.SQL("CREATE TABLE IF NOT EXISTS {exam}(id INT REFERENCES {classlist} (id))").format(exam = sql.Identifier(table_name), classlist = sql.Identifier(referenced_table))
    db.execute(query)
    print(query.as_string(db))
    conn.commit()
    db.close()
    if conn is not None:
        conn.close() 

def create_subject_position_table(table_name, referenced_table):
    conn = connect()
    db = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    query = sql.SQL("CREATE TABLE IF NOT EXISTS {sub_p}(id INT REFERENCES {classlist} (id))").format(sub_p = sql.Identifier(table_name), classlist = sql.Identifier(referenced_table))
    db.execute(query)
    print(query.as_string(db))
    conn.commit()
    db.close()
    if conn is not None:
        conn.close() 


# function for selecting rows from table
def select_all_from_table(table_name):
    conn = connect()
    db = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    query = sql.SQL("SELECT * FROM {tablename}").format(tablename = sql.Identifier(table_name))
    db.execute(query)
    print(query.as_string(db))
    rows = db.fetchall()
    if conn is not None:
        conn.close()  
    return rows

def select_all_from_id(table_name,id):
    conn = connect()
    db = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    query  = sql.SQL("SELECT * FROM {tablename} WHERE id = {id}").format(tablename = sql.Identifier(table_name), id = sql.Identifier(id))
    db.execute(query)
    print(query.as_string(db))
    rows = db.fetchall()
    if conn is not None:
        conn.close()  
    return rows

def select_column_from_id(table_name,columns,id):
    conn = connect()
    db = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    query = sql.SQL("SELECT {column} FROM {tablename} WHERE id = {id}").format(column = sql.SQL(',').join(sql.Identifier(n) for n  in columns), tablename = sql.Identifier(table_name), id = sql.Literal(id))
    db.execute(query)
    print(query.as_string(db))
    rows = db.fetchall()
    if conn is not None:
        conn.close()  
    return rows

def drop_table(name):
    conn = connect()
    db = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    query = sql.SQL("DROP TABLE IF EXISTS {table}").format(table = sql.Identifier(name))
    db.execute(query)
    conn.commit()
    db.close()
    print(query.as_string(db))
    if conn is not None:
        conn.close()

def delete_from_id(table_name, id):
    conn = connect()
    db = conn.cursor()
    query = sql.SQL("DELETE FROM TABLE {table} WHERE id={id}").format(table=sql.Identifier(table_name), id=sql.Literal(id))
    db.execute(query)
    conn.commit()
    db.close()
    print(query.as_string(db))
    if conn is not None:
        conn.close()

