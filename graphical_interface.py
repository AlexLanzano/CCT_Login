import database_interface
import gi
import time
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk

def get_project_text():
	index = project_box.get_active()
	if (index == -1):
		return ""
	return project_list[index]


def split_scan_input(scan_input):
	scan_input = scan_input[2:]
	student_id, full_name, tmp = scan_input.split('^')
	last_name, first_name = full_name.split('/')
	return student_id, first_name, last_name

def GUI_handle_checkin_button(button):
	scan_input = input_box.get_text()
	project = get_project_text()

	if (scan_input == ""):
		print("INPUT ERROR: Please swipe your card and try again.")
		return -1

	if (project == ""):
		print("INPUT ERROR: Please select a project and try again.")
		return -1

	student_id, first_name, last_name = split_scan_input(scan_input)
	print(student_id)
	print(first_name)
	print(last_name)
	timestamp = time.ctime()
	in_or_out = "IN"

	if (database_interface.is_checkedin(student_id)):
		print("DATABASE ERROR: You are already checked in.")
		return -1

	database_interface.store_timestamp(student_id, first_name, last_name, timestamp, project, in_or_out)

	print("Checked in!")
	return 0

def GUI_handle_checkout_button(button):
	scan_input = input_box.get_text()
	project = get_project_text()

	if (scan_input == ""):
		print("INPUT ERROR: Please swipe your card and try again.")
		return -1

	if (project == ""):
		print("INPUT ERROR: Please select a project and try again.")
		return -1

	student_id, first_name, last_name = split_scan_input(scan_input)
	print(student_id)
	print(first_name)
	print(last_name)
	timestamp = time.ctime()
	in_or_out = "OUT"

	if (database_interface.is_checkedout(student_id)):
		print("DATABASE ERROR: You are already checked out.")
		return -1

	database_interface.store_timestamp(student_id, first_name, last_name, timestamp, project, in_or_out)

	print("Checked out!")
	return 0


def init():
	global input_box
	global project_box
	global project_list

	# Define widgets
	win = Gtk.Window()
	s = Gdk.Screen.get_default()
	s_width = s.get_width()
	s_height = s.get_height()
	widget_grid = Gtk.Grid(column_homogeneous = False, row_homogeneous = False, row_spacing = 25, column_spacing = 50)
	widget_fixed = Gtk.Fixed() # Testing out fixed container rather than grid

	input_box = Gtk.Entry()
	input_box.set_visibility(False)
	input_box.set_margin_bottom(20)

	project_list = Gtk.ListStore(str)
	project_box = Gtk.ComboBox.new_with_model(project_list)
	project_box.set_margin_top(s_height/64)

	checkin_button = Gtk.Button.new_with_label("Check In")
	checkin_button.set_margin_top(s_height/24)
	checkin_button.set_margin_left(s_width/16)

	checkout_button = Gtk.Button.new_with_label("Check Out")
	checkout_button.set_margin_top(s_height/24)
	checkout_button.set_margin_left(s_width/16)

	# Setup project list
	# todo: grab project names from text file or database
	project_list.append(["project 1"])
	project_list.append(["project 2"])
	project_list.append(["project 3"])
	project_list.append(["project 4"])

	# This puts the text on the combo box
	renderer_text = Gtk.CellRendererText()
	project_box.pack_start(renderer_text, True)
	project_box.add_attribute(renderer_text, "text", 0)

	# Setup where buttons and input boxes on screen

	win.add(widget_fixed)
	widget_fixed.put(widget_grid, (s_width/2) - (s_width/8), s_height/2)
	widget_grid.attach(input_box, 0, 0, (s_width/200), s_height/800)
	widget_grid.attach(project_box, 0, 1, (s_width/200), s_height/800)
	widget_grid.attach(checkin_button, 0, 2, (s_width/400), s_height/450)
	widget_grid.attach(checkout_button, 3, 2, (s_width/400), s_height/450)

	# Tell gtk how to handle events
	win.connect("delete-event", Gtk.main_quit) # Closes window when the X is pressed
	checkin_button.connect("clicked", GUI_handle_checkin_button) # handles button press event
	checkout_button.connect("clicked", GUI_handle_checkout_button) # handles button press event

	win.fullscreen() # Automatically sets the window as fullscreen
	win.show_all()
	Gtk.main() # This is the main loop that handles all the events above
