import database_interface.py
import gi
from gi.repository import gtk

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
	
def GUI_init():
	win = gtk.Window() # Establish window
	checkin_button = Gtk.Button.new_with_label("Check In") # Creates checkin button
	checkout_button = Gtk.Button.new_with_label("Check Out") # Creates checkout button
	# todo: create input box
	
	win.connect("delete-event", Gtk.main_quit) # Closes window when the X is pressed
	checkin_button.connect("clicked", GUI_handle_checkin_button) # handles button press event
	checkout_button.connect("clicked", GUI_handle_checkout_button) # handles button press event
	# todo: handle card swipe input event into input box
	Gtk.main() # This is the main loop that handles all the events above
