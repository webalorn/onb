import importlib.util

if __name__ == "__main__":
	import sys
	if len(sys.argv) < 2:
		print("First arg must be the script name")
	else:
		scriptPath = sys.argv[1]

		spec = importlib.util.spec_from_file_location("__main__", scriptPath)
		module = importlib.util.module_from_spec(spec)
		spec.loader.exec_module(module)