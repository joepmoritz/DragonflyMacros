from ctypes import *
from dragonfly import Mouse

DLL_DIRECTORY = "C:\\Program Files (x86)\\Tobii\\Tobii EyeX\\"

eyex_dll = CDLL(DLL_DIRECTORY + "Tobii.EyeX.Client.dll")
tracker_dll = CDLL(DLL_DIRECTORY + "Tracker.dll")


def eye_tracker_connect():
	result = tracker_dll.connect()
	print "connect: %d" % result

def eye_tracker_disconnect():
	result = tracker_dll.disconnect()
	print "disconnect: %d" % result

def eye_tracker_get_position():
	x = c_double()
	y = c_double()
	tracker_dll.last_position(byref(x), byref(y))
	return (x.value, y.value)

def eye_tracker_print_position():
	print "(%f, %f)" % eye_tracker_get_position()

def eye_tracker_move_to_position():
	position = eye_tracker_get_position()
	Mouse("[%d, %d]" % (max(0, int(position[0])), max(0, int(position[1])))).execute()

def eye_tracker_activate_position():
	tracker_dll.activate()

def eye_tracker_phantom_mouse(action, **data):
	# print(data)
	eye_tracker_move_to_position()
	action.execute(data)
	# Mouse('wheeldown:%(nn)d/30') * 3
	# Mouse('wheelup:%(nn)d/30') * 3


eye_tracker_connect()
