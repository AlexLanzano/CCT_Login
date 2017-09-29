import MySQLdb
import time

def table_exists():
	try:
		cursor = db.cursor()
		cursor.execute("SHOW TABLES LIKE 'TIMESHEET'")
		result = cursor.fetchone()
		if result:
			return True
		else:
			return False
	except:
		init()

def store_timestamp(student_id, first_name, last_name, timestamp, project, in_or_out):
	try:
		cursor = db.cursor()
		timestamp = time.ctime()
		command = """INSERT INTO TIMESHEET (
                     STUDENT_ID,
                     FIRST_NAME,
                     LAST_NAME,
                     TIMESTAMP,
                     PROJECT,
                     IN_OR_OUT)
                     VALUES ("%s", "%s", "%s", "%s", "%s", "%s")""" % (student_id, first_name, last_name, timestamp, project, in_or_out)

		print(command)
		try:
			cursor.execute(command)
			db.commit()
		except:
			print("DATABASE ERROR: Failed to store data in database.")
			db.rollback()

	except:
		init()
		store_timestamp(student_id, first_name, last_name, timestamp, project, in_or_out)

def is_checkedin(student_id):
	try:
		cursor = db.cursor()
		command = "SELECT * FROM TIMESHEET WHERE STUDENT_ID = '%s'" % (student_id)
		cursor.execute(command)
		length = len(cursor.fetchall())
		if (length % 2 == 0):
			return False
		else:
			return True
	except:
		init()
		return -1

def init():
	global db
	sql_config = open("sql.conf", "r")
	host = sql_config.readline().rstrip()
	user = sql_config.readline().rstrip()
	password = sql_config.readline().rstrip()
	name = sql_config.readline().rstrip()
	sql_config.close()
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
