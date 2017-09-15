import database_interface
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk

def GUI_handle_checkin_button(button):
	# todo:
	# Check if input box is empty (they didn't swipe their card); print error if empty
	# Get name from input box
	# Check if name is already checked in ; print error if checked in
	# Send checkin timestamp to database
	print("Checked in!")


def GUI_handle_checkout_button(button):
	# todo:
	# Check if input box is empty ; print error if empty
	# Get name from input box
	# Check if name is checked in ; print error if not checked in
	# Store checkout time in db
	print("Checked out!")

def init():
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
