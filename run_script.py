import importlib.util, sys, time

if __name__ == "__main__":
	startTime = time.time()

	if len(sys.argv) < 2:
		print("First arg must be the script name")
	else:
		scriptPath = sys.argv[1]

		spec = importlib.util.spec_from_file_location("__main__", scriptPath)
		module = importlib.util.module_from_spec(spec)
		spec.loader.exec_module(module)

	endTime = time.time()
	print("\nScript duration:", endTime - startTime, "seconds")