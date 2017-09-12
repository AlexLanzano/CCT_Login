import database_interface
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

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
	win = Gtk.Window() # Establish window
	widget_grid = Gtk.Grid()
	input_box = Gtk.Entry()
	project_list = Gtk.ListStore(str)
	project_box = Gtk.ComboBox.new_with_model(project_list)
	checkin_button = Gtk.Button.new_with_label("Check In") # Creates checkin button
	checkout_button = Gtk.Button.new_with_label("Check Out") # Creates checkout button

	# Setup project list
	# todo: grab project names from text file or database
	project_list.append(["project 1"])
	project_list.append(["project 2"])
	project_list.append(["project 3"])
	project_list.append(["project 4"])

	renderer_text = Gtk.CellRendererText()
	project_box.pack_start(renderer_text, True)
	project_box.add_attribute(renderer_text, "text", 0)
	
	# Setup where buttons and input boxes on screen
	win.add(widget_grid)
	widget_grid.attach(input_box, 0, 0, 15, 1)
	widget_grid.attach(project_box, 0, 1, 15, 2)
	widget_grid.attach(checkin_button, 0, 3, 5, 4)
	widget_grid.attach(checkout_button, 5, 3, 10, 4)
	
	win.connect("delete-event", Gtk.main_quit) # Closes window when the X is pressed
	checkin_button.connect("clicked", GUI_handle_checkin_button) # handles button press event
	checkout_button.connect("clicked", GUI_handle_checkout_button) # handles button press event
	
	win.show_all()
	Gtk.main() # This is the main loop that handles all the events above
