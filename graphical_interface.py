import database_interface
import gi
import time
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk
import datetime
import threading

def reset_message_label():
	message_label.set_text("")

def set_message_label(message):
	reset_message_label_thread = threading.Timer(5.0, reset_message_label)
	message_label.set_text(message)
	reset_message_label_thread.start()

def append_projects(project_list):
	projects_file = open("projects.txt", "r")
	for line in projects_file:
		project_list.append([line])

def get_project_text():
	index = project_box.get_active()
	model = project_box.get_model()
	if (index == -1):
		return ""
	item = model[index]
	project = item[0]
	return project


def split_scan_input(scan_input):
	scan_input = scan_input[2:]
	student_id, full_name, tmp = scan_input.split('^')
	last_name, first_name = full_name.split('/')
	return student_id, first_name, last_name

def GUI_handle_check_in_out_buttons(button, in_or_out):
	scan_input = input_box.get_text()
	project = get_project_text()

	if (scan_input == ""):
		set_message_label("INPUT ERROR: Please swipe your card and try again.")
		return -1

	if (project == ""):
		set_message_label("INPUT ERROR: Please select a project and try again.")
		return -1

	try:
		student_id, first_name, last_name = split_scan_input(scan_input)
	except:
		set_message_label("INPUT ERROR: Invalid input from card reader. Reswipe your card and try again")
		input_box.set_text("")
		return -1

	response = database_interface.is_checkedin(student_id)
	if (response == -1):
		GUI_handle_checkout_button(button);
	if (response == False):
		set_message_label("DATABASE ERROR: You are already checked out.")
		return -1

	database_interface.store_timestamp(student_id, first_name, last_name, 0, project, in_or_out)

	input_box.set_text("")

	if (in_or_out == "IN"):
		set_message_label("Checked in!")
	if (in_or_out == "OUT"):
		set_message_label("Checked out!")
	return 0

def GUI_handle_manual_entry_button(button):
	scan_input = input_box.get_text()
	project = get_project_text()
	timein_input = manual_timein.get_text()
	timeout_input = manual_timeout.get_text()
	date = manual_date.get_text()

	if (scan_input == ""):
		set_message_label("INPUT ERROR: Please swipe your card and try again")
		return -1
	if (project == ""):
		set_message_label("INPUT ERROR: Please select a project and try again")
		return -1
	if (timein_input == ""):
		set_message_label("INPUT ERROR: Please set the time you checked in and try again")
		return -1
	if (timeout_input == ""):
		set_message_label("INPUT ERROR: Please set the time you checked out and try again")
		return -1
	if (date == ""):
		set_message_label("INPUT ERROR: Please set the date and try again")
		return -1

	student_id, first_name, last_name = split_scan_input(scan_input)
	if (student_id == "" or first_name == "" or last_name == ""):
		set_message_label("INPUT ERROR: Input read from card swipe is invalid, please clear the input field and try again")
		input_box.set_text("")
		return -1

	time_in = datetime.datetime.strptime(timein_input, "%I:%M%p").strftime("%H:%M:00")
	time_out = datetime.datetime.strptime(timeout_input, "%I:%M%p").strftime("%H:%M:00")
	day, month, year = date.split("/")
	timestamp_in = "%s-%s-%s %s" % (year, month, day, time_in)
	timestamp_out = "%s-%s-%s %s" % (year, month, day, time_out)

	database_interface.store_timestamp(student_id, first_name, last_name, timestamp_in, project, "IN")
	database_interface.store_timestamp(student_id, first_name, last_name, timestamp_out, project, "OUT")

def gtk_style():
	css=b"""
GtkWindow{
	background-color: #870911;
}

GtkComboBox{
	background-color: #ffffff;
}
GtkButton{
	background-color: #ffffff;
}
	"""
	style_provider = Gtk.CssProvider()
	style_provider.load_from_data(css)

	Gtk.StyleContext.add_provider_for_screen(Gdk.Screen.get_default(),style_provider,Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)

def init():
	global input_box
	global project_box
	global project_list
	global manual_timein
	global manual_timeout
	global manual_date
	global message_label

	gtk_style()
	# Define widgets
	win = Gtk.Window()
	s = Gdk.Screen.get_default()
	s_width = s.get_width()
	s_height = s.get_height()
	widget_grid = Gtk.Grid(column_homogeneous = False, row_homogeneous = False, row_spacing = 25, column_spacing = 50)
	widget_fixed = Gtk.Fixed() # Testing out fixed container rather than grid

	input_box = Gtk.Entry()
	input_box.set_visibility(False)
	#input_box.set_margin_bottom(20)
	#input_box.set_margin_right(s_width/24)
	input_box.set_placeholder_text("Swipe your ID")

	project_list = Gtk.ListStore(str)
	project_box = Gtk.ComboBox.new_with_model(project_list)
	#project_box.set_margin_top(s_height/64)
	#project_box.set_margin_right(s_width/24)

	checkin_button = Gtk.Button.new_with_label("Check In")
	#checkin_button.set_margin_top(s_height/24)
	#checkin_button.set_margin_left(s_width/16)

	checkout_button = Gtk.Button.new_with_label("Check Out")
	#checkout_button.set_margin_top(s_height/24)
	#checkout_button.set_margin_left(s_width/16)


	manual_timein = Gtk.Entry()
	manual_timein.set_placeholder_text("Time In: 00:00am/pm")

	manual_timeout = Gtk.Entry()
	manual_timeout.set_placeholder_text("Time Out: 00:00am/pm")

	manual_date = Gtk.Entry()
	manual_date.set_placeholder_text("Date: dd/mm/yyyy")
	#manual_date.set_alignment(1)

	manual_entry_button = Gtk.Button.new_with_label("Manual Entry")
	#manual_entry_button.set_margin_right(s_width/11)

	message_label = Gtk.Label()

	# Setup project list
	append_projects(project_list)

	# This puts the text on the combo box
	renderer_text = Gtk.CellRendererText()
	project_box.pack_start(renderer_text, True)
	project_box.add_attribute(renderer_text, "text", 0)

	# Setup where buttons and input boxes on screen
	win.add(widget_fixed)
	widget_fixed.put(widget_grid, (s_width/6) + s_width/18, s_height/3)
	widget_grid.attach(input_box, 1, 1, 10, 1)
	widget_grid.attach(project_box, 1, 2, 10, 1)
	widget_grid.attach(checkin_button, 2, 3, 4, 1)
	widget_grid.attach(checkout_button, 6, 3, 4, 1)
	widget_grid.attach(manual_timein, 3, 5, 2, 1)
	widget_grid.attach(manual_timeout, 5, 5, 2, 1)
	widget_grid.attach(manual_date, 7, 5, 2, 1)
	widget_grid.attach(manual_entry_button, 2, 6, 8, 1)
	widget_grid.attach(message_label, 1, 0, 8, 1)

	# Tell gtk how to handle events
	win.connect("delete-event", Gtk.main_quit) # Closes window when the X is pressed
	checkin_button.connect("clicked", GUI_handle_check_in_out_buttons, "IN") # handles button press event
	checkout_button.connect("clicked", GUI_handle_check_in_out_buttons, "OUT") # handles button press event
	manual_entry_button.connect("clicked", GUI_handle_manual_entry_button) # handles button press event

	win.show_all()
	checkin_button.grab_focus()
	win.fullscreen()

	Gtk.main() # This is the main loop that handles all the events above
