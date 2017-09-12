#!/usr/bin/python3

import database_interface
import graphical_interface


def main():
	if (database_connect() == 0):
		print("DATABASE_ERROR: unable to connect to database\n")
		return -1

	GUI_init()
	

main()
