#!/usr/bin/python3

import database_interface
import graphical_interface


def main():	
	if (database_interface.init() == False):
		print("DATABASE_ERROR: unable to connect to database\n")
		return -1

	graphical_interface.init()
	return 0
	
main()
