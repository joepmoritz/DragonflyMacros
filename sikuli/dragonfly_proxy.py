from subprocess import Popen
import xmlrpclib

from dragonfly.timer import timer
from dragonfly import Function, Key, DictList

JAVA_EXE_PATH = "C:/Program Files (x86)/Java/jre1.8.0_161/bin/java.exe"
SIKULI_IDE_JAR_PATH = "C:/SikuliX/sikulix.jar"
SIKULI_API_JAR_PATH = "C:/SikuliX/sikulixapi.jar"
SIKULI_SERVER_PATH = "C:/Users/Joep/Google Drive/ScriptsAndSettings/DragonflyMacros/sikuli/dragonfly_server"
LOCALHOST = "127.0.0.1"
SERVER_PORT = "8001"


server_proxy = None
mappings = {}


def get_mapping(name):
	if name not in mappings:
		mappings[name] = DictList(name)
	return mappings[name]


def clear_mappings():
	for name, mapping in mappings.iteritems():
		mapping.clear()


def add_command(mapping_name, spec, fname):
	mapping = get_mapping(mapping_name)
	mapping[spec] = Function(execute, fname=fname)
	print "Sikuli command: %s  fname: %s" % (spec, fname)


def generate_commands(list_of_functions):
	clear_mappings()

	for fname in list_of_functions:
		(mapping_name, rest) = fname.split(".", 1)
		spec = rest.split(".")[-1].replace("_", " ")

		add_command(mapping_name, spec, fname)


def launch_IDE():
	Popen([JAVA_EXE_PATH, "-jar", SIKULI_IDE_JAR_PATH])


def launch_server():
	command = ''.join(['"', JAVA_EXE_PATH, '"', " -jar ", SIKULI_API_JAR_PATH, ' -r "', SIKULI_SERVER_PATH, '"'])
	Popen(["runas.exe", "/trustlevel:0x20000", command])


def execute(fname):
	fn = getattr(server_proxy, fname)
	print "Executing sikuli %s" % fname
	fn()


def reload_scripts():
	functions = server_proxy.list_scripts()
	if functions:
		generate_commands(functions)




def start_server_proxy():
	global server_proxy

	server_proxy = xmlrpclib.ServerProxy("http://"+LOCALHOST+":" + SERVER_PORT)
	reload_scripts()
	
	print("Sikuli server started successfully.")


def start_server_proxy_timer_fn():
	print("Attempting to connect to Sikuli ...")

	try:
		start_server_proxy()
		timer.remove_callback(start_server_proxy_timer_fn)
	except Exception:
		pass


def setup_connection():
	try:
		# if the server is already running, this should go off without a hitch
		start_server_proxy()
	except Exception:
		launch_server()
		timer.add_callback(start_server_proxy_timer_fn, 6)


def unload_proxy():
	timer.remove_callback(start_server_proxy_timer_fn)





#setup_connection()