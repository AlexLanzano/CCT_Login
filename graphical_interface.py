import database_interface
import gi
import time
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk

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
	timestamp = time.ctime()
	in_or_out = "IN"

	if (database_interface.is_checkedin(student_id)):
		print("DATABASE ERROR: You are already checked in.")
		return -1

	database_interface.store_timestamp(student_id, first_name, last_name, timestamp, project, in_or_out)

	print("Checked in!")
	input_box.set_text("")
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
	timestamp = time.ctime()
	in_or_out = "OUT"

	if (database_interface.is_checkedin(student_id) == False):
		print("DATABASE ERROR: You are already checked out.")
		return -1

	database_interface.store_timestamp(student_id, first_name, last_name, timestamp, project, in_or_out)

	input_box.set_text("")
	print("Checked out!")
	return 0

def GUI_handle_manual_entry_button(button):
	timein = manual_timein.get_text()
	timeout = manual_timeout.get_text()
	date = manual_timeout.get_text()


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
	input_box.set_margin_bottom(20)
	input_box.set_placeholder_text("Swipe your ID")

	project_list = Gtk.ListStore(str)
	project_box = Gtk.ComboBox.new_with_model(project_list)
	project_box.set_margin_top(s_height/64)

	checkin_button = Gtk.Button.new_with_label("Check In")
	checkin_button.set_margin_top(s_height/24)
	checkin_button.set_margin_left(s_width/16)

	checkout_button = Gtk.Button.new_with_label("Check Out")
	checkout_button.set_margin_top(s_height/24)
	checkout_button.set_margin_left(s_width/16)

	manual_timein = Gtk.Entry()
	manual_timein.set_placeholder_text("Time In: 00:00am/pm")

	manual_timeout = Gtk.Entry()
	manual_timeout.set_placeholder_text("Time Out: 00:00am/pm")

	manual_date = Gtk.Entry()
	manual_date.set_placeholder_text("Date: dd/mm/yyyy")

	manual_entry_button = Gtk.Button.new_with_label("Manual Entry")
	checkout_button.set_margin_top(s_height/24)
	checkout_button.set_margin_left(s_width/16)



	# Setup project list
	append_projects(project_list)

	# This puts the text on the combo box
	renderer_text = Gtk.CellRendererText()
	project_box.pack_start(renderer_text, True)
	project_box.add_attribute(renderer_text, "text", 0)

	# Setup where buttons and input boxes on screen
	win.add(widget_fixed)
	widget_fixed.put(widget_grid, (s_width/2) - (s_width/8), s_height/2)
	widget_grid.attach(input_box, 0, 0, (s_width/200), s_height/450)
	widget_grid.attach(project_box, 0, 1, (s_width/200), s_height/450)
	widget_grid.attach(checkin_button, 0, 2, (s_width/400), s_height/450)
	widget_grid.attach(checkout_button, 3, 2, (s_width/400), s_height/450)
	widget_grid.attach(manual_timein, 0, 4, s_width/400, s_height/450)
	widget_grid.attach(manual_timeout, 4, 4, s_width/400, s_height/450)
	widget_grid.attach(manual_date, 8, 4, s_width/400, s_height/450)
	widget_grid.attach(manual_entry_button, 4, 5, s_width/400, s_height/450)

	# Tell gtk how to handle events
	win.connect("delete-event", Gtk.main_quit) # Closes window when the X is pressed
	checkin_button.connect("clicked", GUI_handle_checkin_button) # handles button press event
	checkout_button.connect("clicked", GUI_handle_checkout_button) # handles button press event

	win.fullscreen() # Automatically sets the window as fullscreen
	win.show_all()
	checkin_button.grab_focus()
	Gtk.main() # This is the main loop that handles all the events above
