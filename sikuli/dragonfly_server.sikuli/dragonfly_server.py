import SimpleXMLRPCServer
from SimpleXMLRPCServer import *
import sys
import importlib
from inspect import getmembers, isfunction


SCRIPTS_PATH = "C:/Users/Joep/Google Drive/ScriptsAndSettings/SikuliX"

scripts = []
server = SimpleXMLRPCServer(("127.0.0.1", 8001), allow_none=True)
server.register_introspection_functions()
quit = 0


def ping():
    return 1


def list_scripts():
    reload_scripts()
    return scripts


def reload_scripts():
    del scripts[:]
    load_scripts()


def terminate():
    global quit
    quit = 1
    return 1


def load_script_functions(module, name_prefix):
    l = getmembers(module, isfunction)
    for d in l:
        if d[0].startswith("export_"):
            registered_function_name = name_prefix + "." + d[0].replace("export_", "")
            scripts.append(registered_function_name)
            server.register_function(d[1], registered_function_name)
            print registered_function_name


def load_scripts():
    print "Loading sikuli scripts..."

    for path, _, _ in os.walk(SCRIPTS_PATH):
        if path.endswith(".sikuli") and not path.endswith("xmlrpc_server.sikuli"):
            load_script(path)


def load_script(path):
    # C:/Users/Joep/Google Drive/ScriptsAndSettings/SikuliX\mendeley\show_notes.sikuli
    path_parts = path.split(".")[0].split("\\")[1:]
    sys.path[0] = os.path.join(SCRIPTS_PATH, "/".join(path_parts[:-1]))
    module_name = path_parts[-1]
    # print module_name

    try:
        if module_name in sys.modules:
            del sys.modules[module_name]
        module = importlib.import_module(module_name)
        reload(module)
        load_script_functions(module, ".".join(path_parts[:-1]))
    except Exception as e:
        print "Error: %s" % str(e)



server.register_function(list_scripts, "list_scripts")
server.register_function(load_scripts, "load_scripts")
server.register_function(terminate, "terminate")

sys.path.insert(0, SCRIPTS_PATH)

print("Sikuli Bridge\n\n")
load_scripts()

try:
    while not quit:
        server.handle_request()
except KeyboardInterrupt:
    print('Exiting')
