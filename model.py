import psycopg2.extras
from psycopg2 import sql
from config import config
import logging
import enum
logging.basicConfig(level= logging.DEBUG)
logger = logging.getLogger()

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
        logger.error(error)


def create_schools():
    try:
        conn = connect()
        db = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        query = sql.SQL("CREATE TABLE IF NOT EXISTS school \
                            (id SERIAL PRIMARY KEY  NOT NULL, username VARCHAR(255) UNIQUE NOT NULL, email VARCHAR(255) \
                            UNIQUE NOT NULL, school_name VARCHAR(255), address VARCHAR(255), city VARCHAR(255), state \
                                VARCHAR(255), current_term VARCHAR(255), current_session VARCHAR(255), password VARCHAR(255), admin_password VARCHAR(255), token_id VARCHAR(255), token VARCHAR(255),\
                                confirmed BOOLEAN DEFAULT false, registered_on date, confirmed_on date, logo boolean DEFAULT false, logo_address VARCHAR(255))")
        db.execute(query)
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        logger.error(error)
        val = False
    else:
        logger.info(query.as_string(db))
        val = True
    finally:
        db.close()
        if conn is not None:
            conn.close()
        return val


def create_terms_table(name):
    try:
        conn = connect()
        db = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        query = sql.SQL("CREATE TABLE IF NOT EXISTS {terms} (id SERIAL NOT NULL, session VARCHAR(255) NOT NULL, term VARCHAR(255)  NOT NULL, school_head VARCHAR(255), school_head_position VARCHAR(255),background_color VARCHAR(255) DEFAULT '#ffffff',text_color VARCHAR(255) DEFAULT 'black',line_color VARCHAR(255) DEFAULT 'black',background_font VARCHAR(255) DEFAULT 'Ariel',ld_position VARCHAR(255) DEFAULT 'center',l_font VARCHAR(255) DEFAULT 'Ariel',l_weight VARCHAR(255) DEFAULT '900',l_color VARCHAR(255) DEFAULT '#537fbe',l_fontsize VARCHAR(255) DEFAULT '30px',sd_font VARCHAR(255) DEFAULT 'Ariel',sd_color VARCHAR(255) DEFAULT '#808000',sd_fontsize VARCHAR(255) DEFAULT '20px',sd_position VARCHAR(255) DEFAULT 'center',sd_email VARCHAR(255) DEFAULT 'None',admin_email BOOLEAN DEFAULT false, address VARCHAR(255) DEFAULT 'None',po_box VARCHAR(255) DEFAULT 'None',phone VARCHAR(255) DEFAULT 'None',next_term VARCHAR(255) DEFAULT 'None',sd_other VARCHAR(255) DEFAULT 'None',std_color VARCHAR(255) DEFAULT 'black',std_font VARCHAR(255) DEFAULT 'Arial Narrow',std_fontsize VARCHAR(255) DEFAULT '18px',std_position VARCHAR(255) DEFAULT 'left', logo BOOLEAN DEFAULT false,watermark BOOLEAN DEFAULT false,email_notification BOOLEAN DEFAULT false,  PRIMARY KEY(session, term))").format(terms = sql.Identifier(name))
        db.execute(query)
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        logger.error(error)
        val = False
    else:
        logger.info(query.as_string(db))
        val = True
    finally:
        db.close()
        if conn is not None:
            conn.close()
        return val


def create_classes_table(name):
    try:
        conn = connect()
        db = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        query = sql.SQL("CREATE TABLE IF NOT EXISTS {classes} (id  SERIAL PRIMARY KEY  NOT NULL, classname VARCHAR(255) UNIQUE NOT NULL, section VARCHAR(255),class_teacher_surname VARCHAR(255),class_teacher_firstname VARCHAR(255),position VARCHAR(255),subscription VARCHAR(255),date_of_subscription VARCHAR(255),amount_paid VARCHAR(255),payment_order VARCHAR(255),superscription_expires VARCHAR(255),no_of_passes VARCHAR(255),no_of_failure VARCHAR(255),grading_type VARCHAR(255) DEFAULT 'WAEC',ca VARCHAR(255),test VARCHAR(255),exam VARCHAR(255))").format(classes = sql.Identifier(name))
        db.execute(query)
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        logger.error(error)
        val = False
    else:
        logger.info(query.as_string(db))
        val = True
    finally:
        db.close()
        if conn is not None:
            conn.close()  
        return val

def create_settings_table(table_name, referenced_table):
    try:
        conn = connect()
        db = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        query = sql.SQL("CREATE TABLE IF NOT EXISTS {setting} (id INT  REFERENCES  {referenced_table} (id),background_color VARCHAR(255) DEFAULT '#ffffff',text_color VARCHAR(255) DEFAULT 'black',line_color VARCHAR(255) DEFAULT 'black',background_font VARCHAR(255) DEFAULT 'Ariel',ld_position VARCHAR(255) DEFAULT 'center',l_font VARCHAR(255) DEFAULT 'Ariel',l_weight VARCHAR(255) DEFAULT '900',l_color VARCHAR(255) DEFAULT '#537fbe',l_fontsize VARCHAR(255) DEFAULT '30px',sd_font VARCHAR(255) DEFAULT 'Ariel',sd_color VARCHAR(255) DEFAULT '#808000',sd_fontsize VARCHAR(255) DEFAULT '20px',sd_position VARCHAR(255) DEFAULT 'center',sd_email VARCHAR(255) DEFAULT 'None',admin_email BOOLEAN DEFAULT false, address VARCHAR(255) DEFAULT 'None',po_box VARCHAR(255) DEFAULT 'None',phone VARCHAR(255) DEFAULT 'None',next_term VARCHAR(255) DEFAULT 'None',sd_other VARCHAR(255) DEFAULT 'None',std_color VARCHAR(255) DEFAULT 'black',std_font VARCHAR(255) DEFAULT 'Arial Narrow',std_fontsize VARCHAR(255) DEFAULT '18px',std_position VARCHAR(255) DEFAULT 'left', table_type VARCHAR(255) DEFAULT 'striped',ca BOOLEAN DEFAULT true,test BOOLEAN DEFAULT true,exam BOOLEAN DEFAULT true,combined BOOLEAN DEFAULT true,subject_total BOOLEAN DEFAULT true,class_average BOOLEAN DEFAULT true,subject_position BOOLEAN DEFAULT true,grade BOOLEAN DEFAULT true,subject_comment BOOLEAN DEFAULT false,teachers_initials BOOLEAN DEFAULT false,total_score BOOLEAN DEFAULT true,average BOOLEAN DEFAULT true,position BOOLEAN DEFAULT true,teachers_line INTEGER DEFAULT 0,shadow BOOLEAN DEFAULT true,principal_line INTEGER DEFAULT 0,teachers_signature BOOLEAN DEFAULT false,principal_signature BOOLEAN DEFAULT false,pandf BOOLEAN DEFAULT true,grade_summary BOOLEAN DEFAULT true,watermark BOOLEAN DEFAULT false,email_notification BOOLEAN DEFAULT true)").format(setting = sql.Identifier(table_name), referenced_table = sql.Identifier(referenced_table))
        db.execute(query)
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        logger.error(error)
        val = False
    else:
        logger.info(query.as_string(db))
        val = True
    finally:
        db.close()
        if conn is not None:
            conn.close()  
        return val

def create_classlist_table(name):
    try:
        conn = connect()
        db = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        query = sql.SQL("CREATE TABLE IF NOT EXISTS {classlist}(id  SERIAL PRIMARY KEY  NOT NULL, surname VARCHAR(255)  NOT NULL, firstname VARCHAR(255) NOT NULL,othername VARCHAR(255),gender VARCHAR(255),pin VARCHAR(255),regnumber VARCHAR(255))").format(classlist = sql.Identifier(name))
        db.execute(query)
        conn.commit()    
    except (Exception, psycopg2.DatabaseError) as error:
        logger.error(error)
        val = False
    else:
        logger.info(query.as_string(db))
        val = True
    finally:
        db.close()
        if conn is not None:
            conn.close()  
        return val

def create_subjects_table(name):
    try:
        conn = connect()
        db = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        query = sql.SQL("CREATE TABLE IF NOT EXISTS {classlist}(id  SERIAL PRIMARY KEY  NOT NULL, name VARCHAR(255)  NOT NULL, firstname VARCHAR(255) NOT NULL,surname VARCHAR(255) NOT NULL,subject_total INT DEFAULT 0,subject_average INT DEFAULT 0, no_of_a  INT DEFAULT 0,no_of_b  INT DEFAULT 0,no_of_c  INT DEFAULT 0,no_of_d  INT DEFAULT 0,no_of_e  INT DEFAULT 0,no_of_f  INT DEFAULT 0)").format(classlist = sql.Identifier(name))
        db.execute(query)
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        logger.error(error)
        val = False
    else:
        logger.info(query.as_string(db))
        val = True
    finally:
        db.close()
        if conn is not None:
            conn.close()  
        return val


def create_mastersheet_table(table_name, referenced_table):
    try:
        conn = connect()
        db = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        query = sql.SQL("CREATE TABLE IF NOT EXISTS {mastersheet}(id INT REFERENCES {classlist} (id), total INT DEFAULT 0, average VARCHAR(255),position INT)").format(mastersheet = sql.Identifier(table_name),  classlist =  sql.Identifier(referenced_table))
        db.execute(query)
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        logger.error(error)
        val = False
    else:
        logger.info(query.as_string(db))
        val = True
    finally:
        db.close()
        if conn is not None:
            conn.close()  
        return val



def create_grades_table(table_name, referenced_table):
    try:
        conn = connect()
        db = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        query = sql.SQL("CREATE TABLE IF NOT EXISTS {grades}(id INT REFERENCES {classlist} (id), no_of_a  INT DEFAULT 0,no_of_b  INT DEFAULT 0,no_of_c  INT DEFAULT 0,no_of_d  INT DEFAULT 0,no_of_e  INT DEFAULT 0,no_of_f  INT DEFAULT 0)").format(grades = sql.Identifier(table_name), classlist = sql.Identifier(referenced_table))
        db.execute(query)
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        logger.error(error)
        val = False
    else:
        logger.info(query.as_string(db))
        val = True
    finally:
        db.close()
        if conn is not None:
            conn.close()  
        return val

def create_ca_table(table_name, referenced_table):
    try:
        conn = connect()
        db = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        query = sql.SQL("CREATE TABLE IF NOT EXISTS {ca}(id INT REFERENCES {classlist} (id))").format(ca = sql.Identifier(table_name), classlist = sql.Identifier(referenced_table))
        db.execute(query)
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        logger.error(error)
        val = False
    else:
        logger.info(query.as_string(db))
        val = True
    finally:
        db.close()
        if conn is not None:
            conn.close()  
        return val

def create_test_table(table_name, referenced_table):
    try:
        conn = connect()
        db = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        query = sql.SQL("CREATE TABLE IF NOT EXISTS {test}(id INT REFERENCES {classlist} (id))").format(test = sql.Identifier(table_name), classlist = sql.Identifier(referenced_table))
        db.execute(query)
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        logger.error(error)
        val = False
    else:
        logger.info(query.as_string(db))
        val = True
    finally:
        db.close()
        if conn is not None:
            conn.close()  
        return val

def create_exam_table(table_name, referenced_table):
    try:
        conn = connect()
        db = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        query = sql.SQL("CREATE TABLE IF NOT EXISTS {exam}(id INT REFERENCES {classlist} (id))").format(exam = sql.Identifier(table_name), classlist = sql.Identifier(referenced_table))
        db.execute(query)
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        logger.error(error)
        val = False
    else:
        logger.info(query.as_string(db))
        val = True
    finally:
        db.close()
        if conn is not None:
            conn.close()  
        return val

def create_subject_position_table(table_name, referenced_table):
    try:
        conn = connect()
        db = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        query = sql.SQL("CREATE TABLE IF NOT EXISTS {sub_p}(id INT REFERENCES {classlist} (id))").format(sub_p = sql.Identifier(table_name), classlist = sql.Identifier(referenced_table))
        db.execute(query)
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        logger.error(error)
        val = False
    else:
        logger.info(query.as_string(db))
        val = True
    finally:
        db.close()
        if conn is not None:
            conn.close()  
        return val

def copy_table(table_name, referenced_table):
    try:
        conn = connect()
        db = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        query = sql.SQL("CREATE TABLE {result} AS  TABLE {class_settings}")\
        .format(result = sql.Identifier(table_name), class_settings= sql.Identifier(referenced_table))
        print(query.as_string(db))
        db.execute(query)
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        logger.error(error)
        val = False
    else:
        logger.info(query.as_string(db))
        val = True
    finally:
        db.close()
        if conn is not None:
            conn.close()  
        return val

# function for selecting rows from table
def select_all_from_table(table_name):
    try:
        conn = connect()
        db = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        query = sql.SQL("SELECT * FROM {tablename}").format(tablename = sql.Identifier(table_name))
        db.execute(query)
        rows = db.fetchall()
    except (Exception, psycopg2.DatabaseError) as error:
        logger.error(error)
    else:
        logger.info(query.as_string(db))
    finally:
        if conn is not None:
            conn.close()  
        if not rows:
            return [] 
        return rows

def select_all_from_row(table_name,attr=None, value=None):
    try:
        conn = connect()
        db = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        query  = sql.SQL("SELECT * FROM {tablename} WHERE {att} = {val}").format(tablename = sql.Identifier(table_name), att = sql.Identifier(attr), val = sql.Literal(value))
        db.execute(query)
        rows = db.fetchall()
    except (Exception, psycopg2.DatabaseError) as error:
        logger.error(error)
    else:
        logger.info(query.as_string(db))
    finally:
        if conn is not None:
            conn.close()
        if not rows:
            return [] 
        return rows

def select_all_from_row_with_and(table_name,attr1, value1, attr2, value2 ):
    try:
        conn = connect()
        db = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        query  = sql.SQL("SELECT * FROM {tablename} WHERE {att1} = {val1} AND {att2} = {val2} ").\
            format(tablename = sql.Identifier(table_name), att1 = sql.Identifier(attr1), val1 = sql.Literal(value1), att2=sql.Identifier(attr2), val2 = sql.Literal(value2))
        db.execute(query)
        rows = db.fetchall()
    except (Exception, psycopg2.DatabaseError) as error:
        logger.error(error)
    else:
        logger.info(query.as_string(db))
    finally:
        if conn is not None:
            conn.close()
        if not rows:
            return [] 
        return rows

def select_columns_by_attr(table_name,columns,attr = None, value=None):
    try:
        conn = connect()
        db = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        if attr and value:
            query = sql.SQL("SELECT {column} FROM {tablename} WHERE {att} = {val}").format(column = sql.SQL(',').join(sql.Identifier(n) for n  in columns), tablename = sql.Identifier(table_name),att = sql.Identifier(attr), val = sql.Literal(value))
        else:
            query = sql.SQL("SELECT {column} FROM {tablename}").format(column = sql.SQL(',').join(sql.Identifier(n) for n  in columns), tablename = sql.Identifier(table_name))
        db.execute(query)
        rows = db.fetchall()
    except (Exception, psycopg2.DatabaseError) as error:
        logger.error(error)
    else:
        logger.info(query.as_string(db))
    finally:
        if conn is not None:
            conn.close()  
        if not rows:
            return [] 
        return rows

def select_school_by_username(username):
    try:
        conn = connect()
        db = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        query = sql.SQL("SELECT * FROM school WHERE username = {user}").format(user = sql.Literal(username.lower()))
        db.execute(query)
        rows = db.fetchall()
    except (Exception, psycopg2.DatabaseError) as error:
        logger.error(error)
    else:
        logger.info(query.as_string(db))
    finally:
        if conn is not None:
            conn.close()  
        if not rows:
            return [] 
        return rows

def select_school_by_email(email):
    try:
        conn = connect()
        db = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        query = sql.SQL("SELECT * FROM school WHERE email = {em}").format(em = sql.Literal(email.lower()))
        db.execute(query)
        rows = db.fetchall()
    except (Exception, psycopg2.DatabaseError) as error:
        logger.error(error)
    else:
        logger.info(query.as_string(db))
    finally:
        if conn is not None:
            conn.close()  
        if not rows:
            return [] 
        return rows

    
def select_school_by_attr(attr, value):
    try:
        conn = connect()
        db = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        query = sql.SQL("SELECT * FROM school WHERE {att} = {val}").format(val = sql.Literal(value), att = sql.Identifier(attr))
        db.execute(query)
        rows = db.fetchall()
    except (Exception, psycopg2.DatabaseError) as error:
        logger.error(error)
    else:
        logger.info(query.as_string(db))
    finally:
        if conn is not None:
            conn.close()  
        if not rows:
            return [] 
        return rows


def select_school_by_id(id):
    try:
        conn = connect()
        db = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        query = sql.SQL("SELECT * FROM school WHERE id = {user_id}").format(user_id = sql.Literal(id))
        db.execute(query)
        rows = db.fetchall()
    except (Exception, psycopg2.DatabaseError) as error:
        logger.error(error)
    else:
        logger.info(query.as_string(db))
    finally:
        if conn is not None:
            conn.close()  
        if not rows:
            return [] 
        return rows

def select_current_term(tbl, current_term, current_session):
    try:
        conn = connect()
        db = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        query = sql.SQL("SELECT * FROM {tble} WHERE term = {cur_t} AND session = {cur_s}").format(tble = sql.Identifier(tbl), cur_t = sql.Literal(current_term), cur_s = sql.Literal(current_session))
        db.execute(query)
        rows = db.fetchall()
    except (Exception, psycopg2.DatabaseError) as error:
        logger.error(error)
    else:
        logger.info(query.as_string(db))
    finally:
        if conn is not None:
            conn.close()  
        if not rows:
            return [] 
        return rows


def drop_table(name):
    try:
        conn = connect()
        db = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        query = sql.SQL("DROP TABLE IF EXISTS {table}").format(table = sql.Identifier(name))
        db.execute(query)
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        logger.error(error)
        val = False
    else:
        logger.info(query.as_string(db))
        val = True
    finally:
        db.close()
        if conn is not None:
            conn.close()
        return val

def delete_from_id(table_name, id):
    try:
        conn = connect()
        db = conn.cursor()
        query = sql.SQL("DELETE FROM TABLE {table} WHERE id={id}").format(table=sql.Identifier(table_name), id=sql.Literal(id))
        db.execute(query)
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        logger.error(error)
        val = False
    else:
        logger.info(query.as_string(db))
        val = True
    finally:
        db.close()
        if conn is not None:
            conn.close()
        return val

#insert into columns or columns 
def insert_into_table(table_name,columns,col_values):
    try:
        conn = connect()
        db = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        if type(columns) is  list and  type(col_values) is  list:
            if len(columns) != len(col_values):
                raise ValueError('columns list and value list must be equal in size')
            query = sql.SQL("INSERT INTO  {tbl}  ({cols}) VALUES ({vals})  WHERE {att} = {val} RETURNING id ").format(cols = sql.SQL(',').join(sql.Identifier(n) for n  in columns), vals = sql.SQL(',').join(sql.Literal(n) for n  in col_values), tbl = sql.Identifier(table_name),att = sql.Identifier(columns), val = sql.Literal(col_values))
        elif type(columns) is  str and  type(col_values) is  str:
            query = sql.SQL("INSERT INTO  {tbl}  ({cols}) VALUES ({vals})  WHERE {att} = {val} RETURNING id ").format(cols = sql.Identifier(columns), vals = sql.Literal(col_values), tbl = sql.Identifier(table_name),att = sql.Identifier(columns), val = sql.Literal(col_values))
        else:
            raise TypeError('columns and values must  be  of type list or str and of same type ')
        db.execute(query)
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        logger.error(error)
        val = False
    else:
        logger.error(query.as_string(db))
        val = True
    finally:
        db.close()
        if conn is not None:
            conn.close()  
        return val


def update_table(table_name,columns,col_values, attr = None, value=None):
    try:
        conn = connect()
        db = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        if type(columns) is list and  type(col_values) is list:
            if len(columns) != len(col_values):
                raise ValueError('columns list and value list must be equal in size')
            if value and attr:
                for i in range(len(columns)):
                    query = sql.SQL("UPDATE  {tbl} SET {colval} = {vals} WHERE {att} = {val} ").format(colval = sql.Identifier(columns[i]), vals = sql.Literal(col_values[i]), tbl = sql.Identifier(table_name),att = sql.Identifier(attr), val = sql.Literal(value))
            else:
                for i in range(len(columns)):
                    query = sql.SQL("UPDATE  {tbl} SET {colval} = {vals} ").format(colval = sql.Identifier(columns[i]), vals = sql.Literal(col_values[i]), tbl = sql.Identifier(table_name))
        elif type(columns) is str and  type(col_values) in [str, int, bool]:
            if value and attr:
                query = sql.SQL("UPDATE  {tbl} SET {colval} = {vals} WHERE {att} = {val} ").format(colval = sql.Identifier(columns), vals = sql.Literal(col_values), tbl = sql.Identifier(table_name),att = sql.Identifier(attr), val = sql.Literal(value))
            else:
                query = sql.SQL("UPDATE  {tbl} SET {colval} = {vals} ").format(colval = sql.Identifier(columns), vals = sql.Literal(col_values), tbl = sql.Identifier(table_name))
            print()
        else:
            raise TypeError('columns and values must  be  of type list or str and of same type ')
        db.execute(query)
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        logger.error(error)
        val = False
    else:
        logger.info(query.as_string(db))
        val = True
    finally:
        db.close()
        if conn is not None:
            conn.close() 
        return val


def alter_table(table_name, column):
    try:
        conn = connect()
        db = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        query = sql.SQL('ALTER TABLE {tbl} ADD COLUMN {col}').format(tbl = sql.Identifier(table_name), col = sql.Identifier(column))
        db.execute(query)
    except (Exception, psycopg2.DatabaseError) as error:
        logger.error(error)
        val = False
    else:
        logger.info(query.as_string(db))
        val = True
    finally:
        db.close()
        conn.commit()
        if conn is not None:
            conn.close()
        return val

        
def drop_column(table_name, column):
    try:
        conn = connect()
        db = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        query = sql.SQL('ALTER TABLE {tbl} DROP COLUMN {col}').format(tbl = sql.Identifier(table_name), col = sql.Identifier(column))
        db.execute(query)
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        logger.error(error)
        val = False
    else:
        logger.info(query.as_string(db))
        val = True
    finally:
        db.close()
        if conn is not None:
            conn.close()
        return val

def update_term_settings(table_name,columns,col_values, term, session):
    try:
        conn = connect()
        db = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        if type(columns) is list and  type(col_values) is list:
            if len(columns) != len(col_values):
                raise ValueError('columns list and value list must be equal in size')
            for i in range(len(columns)):
                query = sql.SQL("UPDATE  {tbl} SET {colval} = {vals} WHERE term = {cur_t} AND session = {cur_s} ").format(colval = sql.Identifier(columns[i]), vals = sql.Literal(col_values[i]), tbl = sql.Identifier(table_name),cur_t = sql.Literal(term), cur_s = sql.Literal(session))
        elif type(columns) is str and  type(col_values) in [str, int, bool]:
            query = sql.SQL("UPDATE  {tbl} SET {colval} = {vals} WHERE term = {cur_t} AND session = {cur_s} ").format(colval = sql.Identifier(columns), vals = sql.Literal(col_values), tbl = sql.Identifier(table_name),cur_t = sql.Literal(term), cur_s = sql.Literal(session))
        else:
            raise TypeError('columns and values must  be  of type list or str and of same type ')
        db.execute(query)
        conn.commit()    
    except (Exception, psycopg2.DatabaseError) as error:
        logger.error(error)
        val = False
    else:
        logger.info(query.as_string(db))
        val = True
    finally:
        db.close()
        if conn is not None:
            conn.close() 
        return val
    

class UserRoles(enum.Enum):
    SuperAdmin = 1
    SchoolAdmin = 2
    ClassAdmin = 3
    Teacher = 4
