import create


def main():
	r = create.Create('/dev/ttyUSB0')
	r.toSafeMode()
	r.seekDock()
	
	
	
main()