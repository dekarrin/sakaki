import os, sys, json

if len(sys.argv) < 3:
	print("Please pass in directory to scan and name of output file")
	sys.exit()

command = raw_input("Enter command that each file is an argument to: ")
command_dir = raw_input("Enter directory to run command in: ")
prepend_dir = raw_input("Enter directory to prepend each item with (blank for none): ")
if prepend_dir is "":
	prepend_dir = None
control_scheme = raw_input("Enter name of control scheme (blank for none): ")
if control_scheme is "":
	control_scheme = None
parent = raw_input("Enter parent wheel name: ")


data = []
for f in os.listdir(sys.argv[1]):
	if not os.path.isfile(os.path.join(sys.argv[1], f)):
		continue
	arg = f
	if prepend_dir is not None:
		arg = os.path.join(prepend_dir, f)
	item = {
		'title':	f,
		'parent':	parent,
		'command':	command + " \"" + arg + "\"",
		'command_dir':	command_dir
	}
	if control_scheme is not None:
		item['control_scheme'] = control_scheme
	data.append(item)

with open(sys.argv[2], 'w') as out:
	json.dump(data, out, sort_keys = True, indent = 4, ensure_ascii = False)
