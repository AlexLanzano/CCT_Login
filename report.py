import database_interface
import MySQLdb
from datetime import datetime
import sys

def calc(first,last,project):
	total = 0
	if (project == "all"):
		cursor = db.cursor()
		cursor.execute("SELECT COUNT(*) FROM TIMESHEET WHERE FIRST_NAME = '%s' AND LAST_NAME = '%s'" % (first,last))
		rows = cursor.fetchone()[0]
		for i in range(1, int(rows/2)):
			cursor.execute("SELECT TIMESTAMP FROM TIMESHEET WHERE FIRST_NAME = '%s' AND LAST_NAME = '%s' LIMIT %s,%s" % (first,last,(i*2)-2,(i*2)-1))
			cin = datetime.strptime(cursor.fetchone()[0], '%Y-%m-%d %H:%M:%S')
			cursor.execute("SELECT TIMESTAMP FROM TIMESHEET WHERE FIRST_NAME = '%s' AND LAST_NAME = '%s' LIMIT %s, %s" % (first, last,(i*2)-1,i*2))
			cout = datetime.strptime(cursor.fetchone()[0], '%Y-%m-%d %H:%M:%S')

			total = total + (cout-cin).seconds

	else:
		cursor = db.cursor()
		cursor.execute("SELECT COUNT(*) FROM TIMESHEET WHERE PROJECT = '%s' AND FIRST_NAME = '%s' AND LAST_NAME = '%s'" % (project,first,last))
		rows = cursor.fetchone()[0]
		for i in range(1, int(rows/2)):
			cursor.execute("SELECT TIMESTAMP FROM TIMESHEET WHERE PROJECT = '%s' AND FIRST_NAME = '%s' AND LAST_NAME = '%s' LIMIT %s,%s" % (project, first,last,(i*2)-2,(i*2)-1))
			cin = datetime.strptime(cursor.fetchone()[0], '%Y-%m-%d %H:%M:%S')
			cursor.execute("SELECT TIMESTAMP FROM TIMESHEET WHERE PROJECT = '%s' AND FIRST_NAME = '%s' AND LAST_NAME = '%s' LIMIT %s, %s" % (project, first, last,(i*2)-1,i*2))
			cout = datetime.strptime(cursor.fetchone()[0], '%Y-%m-%d %H:%M:%S')

			total = total + (cout-cin).seconds
	return int(total)

def main(first, last, project):
	first.upper()
	last.upper()
	project.lower()
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
		print("Can't connect to database")
		return 0
	if(database_interface.init() == False):
		print("DATABASE_ERROR: unavle to connect to database\n")
		return -1

	min_worked, sec_worked  =  divmod(calc(first,last,project), 60)
	hours_worked, min_worked = divmod(min_worked, 60)

	print(first + " " + last + " has worked a total of " + str(hours_worked) + " hours " + str(min_worked) + " minutes and " + str(sec_worked) + " seconds on " + project)

for i in range(3, len(sys.argv)):
	if i == 3:
		project_name = sys.argv[i]
	else:
		project_name = project_name + " " + sys.argv[i]
main(sys.argv[1],sys.argv[2],project_name)
