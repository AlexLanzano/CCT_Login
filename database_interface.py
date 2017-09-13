import MySQLdb
import time

def table_exists():
	cursor = db.cursor()
	cursor.execute("SHOW TABLES LIKE 'TIMESHEET'")
	result = cursor.fetchone()
	if result:
		return True
	else:
		return False

def store_timestamp(student_id, first_name, last_name, timestamp, project, in_or_out):
	# todo:
	if (is_checkedin(student_id)):
		return
	timestamp = time.ctime()
	command = "INSERT INTO TIMESHEET ( \
               STUDENT_ID, \
               FIRST_NAME, \
               LAST_NAME, \
               TIMESTAMP, \
               PROJECT, \
               IN_OR_OUT) \
               VALUES ('%s', '%s', '%s', '%s', '%s' '%s')" % \
	(student_id, first_name, last_name, timestamp, project, in_or_out)

	try:
		db.cursor().execute(command)
		db.commit()
	except:
		# display error
		db.rollback()

def is_checkedin(student_id):
	command = "SELECT * FROM TIMESHEET WHERE STUDENT_ID = '%s'" % (student_id)
	db.cursor.execute(command)
	length = len(db.cursor.fetchall())
	if (length % 2 == 0):
		return False
	else:
		return True

def init():
	global db
	sql_config = open("sql.conf", "r")
	host = sql_config.readline().rstrip()
	user = sql_config.readline().rstrip()
	password = sql_config.readline().rstrip()
	name = sql_config.readline().rstrip()
	print(host)
	print(user)
	print(password)
	print(name)
	try:
		db = MySQLdb.connect(host, user, password, name)
	except MySQLdb.Error:
		return False
	cursor = db.cursor()
	if (table_exists() == False):
		command = """CREATE TABLE TIMESHEET (
                     STUDENT_ID CHAR(20) NOT NULL,
                     FIRST_NAME CHAR(20) NOT NULL,
                     LAST_NAME CHAR(20) NOT NULL,
                     TIMESTAMP CHAR(50) NOT NULL,
                     PROJECT CHAR(50) NOT NULL,
                     IN_OR_OUT CHAR(4) NOT NULL
                     )"""

		cursor.execute(command)

	return True
