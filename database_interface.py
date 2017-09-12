import MySQLdb
import time

def database_store_checkin_time(name):
	# todo:
	# get current time
	# store current time for name in checkin time
	print("store checkin time")

def database_store_checkout_time(name):
	# todo:
	# get current time
	# store current time for name in checkout time
	print("store checkout time")
	
def database_is_checkedin(name):
	# todo:
	# find name in db
	# check table if checked in
	# return true if checked in, else return false
	print("is checked in?")

def database_connect():
	global db = MySQLdb.connect("", "", "", "") # todo: Fill values in
	# todo: if db didn't connect, return 1
	return 0
	
	
