import create


def checkCharge():
	r = create.Create("/dev/ttyUSB0")
	charge = r.getSensor('BATTERY_CHARGE')
	capacity = r.getSensor('BATTERY_CAPACITY')
	print("BATTERY:", charge/capacity*100//1, "%")
	
	if((charge/capacity*100//1) <= 20 ):
		print("FINDING DOCK")
		#r.toSafeMode()
		#r.seekDock()
	
def main():
	checkCharge()

main()
