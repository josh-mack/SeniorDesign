'''Project: Envirobot for Senior Design at University of Delaware
Navigation Code
by Josh Mack 3/8/2017'''
import random
import time
import create
import math
import takeSample as ts
import signal
import sys





global battery, dockPercent
global robot, turnAngle, moveDist
global TRIG, TRIG_L, TRIG_R
global ECHO, ECHO_L, ECHO_R
global threshold_Front, threshold_R, threshold_L
global roomFile  #Text file containing layout of test room
global direction  #Current Direction Robot is Facing
global globalX, globalY  #Global coordinate of robot in roomFile
global posX, posY  #Current coordinates of robot in generated array
global roomList #2D array representing the room
global currentNode #current node representing the robot
global numNodes #Number of nodes currently in roomList
global maxX, maxY #max coordinates of 2D array stored in roomList
global turnCount
global stop
global hallwayWidth, seperationWidth


arrowDir = {'North': "^", 'South': "v", 'East': ">", 'West': "<"}

def signal_handler(signal, frame):
	global robot
	robot.stop()
	robot.toSafeMode()
	print("Exiting...")
	
	sys.exit(0)


class Node(object):   #Nodes represent grid blocks in the 2D array roomList
  
	def __init__(self, nodeNum, top, bottom, left, right, col, row):
		self.nodeNum = nodeNum
		self.bottom = bottom
		self.top = top
		self.left = left
		self.right = right
		self.row = row
		self.col = col
			

def test():   #load textfile as test room
	global roomFile
	with open("./room.txt") as textFile:
		roomFile = [line.split() for line in textFile]
		
	for row in range(len(roomFile)):
		for col in range(len(roomFile[row])):
			roomFile[row][col] = int(roomFile[row][col])	
'''	
def sensor():  #Artificial Sensor for testing 1= obstacle detected, 0 = none
	if direction is "North":
		return roomFile[globalY-1][globalX]
	elif direction is "South":
		return roomFile[globalY+1][globalX]
	elif direction is "East":
		return roomFile[globalY][globalX+1]
	elif direction is "West":
		return roomFile[globalY][globalX-1]
'''


 


def sensor():
	global TRIG, ECHO, threshold_Front
	distance = ts.takeSamples(TRIG,ECHO)
	print("Front Distance:",distance,"cm")
	return 1 if(distance < threshold_Front) else 0

def turn():
	global direction, robot
	robot.go(0, -75)
	robot.waitAngle(turnAngle)
	robot.stop()
	
	
	if direction is "North":
		direction = "East"
	elif direction is "East":
		direction = "South"
	elif direction is "South":
		direction = "West"
	elif direction is "West":
		direction = "North"

		
def bumpMaxX():
	global maxX, roomList
	maxX+=1
	for row in range(len(roomList)):
		roomList[row].append(Node(-1, None, None, None, None, maxX, row))

		
def bumpMaxY():
	global maxY, roomList
	maxY+=1
	roomList.append([])
	for col in range(len(roomList[0])):
		roomList[maxY].append(Node(-1, None, None, None, None, col, maxY))


def bumpMinX():
	global maxX, roomList, posX
	maxX+=1
	posX+=1
	for row in range(len(roomList)):
		roomList[row].insert(0, Node(-1, None, None, None, None, -1, row))
		for col in range(len(roomList[0])):
			roomList[row][col].col += 1


def bumpMinY():
	global maxY, roomList, posY
	maxY+=1
	posY+=1
	roomList.insert(0, [])
	for col in range(len(roomList[1])):
		roomList[1][col].row = 1
		roomList[0].append(Node(-1, None, None, None, None, col, 0))


def checkSides():
	global TRIG_R, ECHO_R, TRIG_L, ECHO_L, maxX, maxY, posX, posY, direction, roomList, \
	threshold_L, threshold_R, hallwayWidth, seperationWidth, rightDist, leftDist
	
	
	rightDist =  ts.takeSamples(TRIG_R,ECHO_R)

	leftDist = ts.takeSamples(TRIG_L,ECHO_L)
	time.sleep(0.5)
	hallwayWidth = leftDist+rightDist+seperationWidth
	

	
	print("Right Distance: ", rightDist, "cm")
	print("Left Distance: ", leftDist, "cm")
	if (direction is "North") or (direction is "South"):
		if(posX+1 > maxX):
			bumpMaxX()
				
		if(posX == 0):
			bumpMinX()
			
		if (leftDist<threshold_L):
			if direction is "North":
				markObstacle("West")
			else:
				markObstacle("East")

		if (rightDist<threshold_R):
			if direction is "North":
				markObstacle("East")
			else:
				markObstacle("West")
			
			
	if (direction is "East") or (direction is "West"):
		if(posY+1 > maxY):
			bumpMaxY()
				
		if(posY == 0):
			bumpMinY()
			
		if (leftDist<threshold_L):
			if direction is "East":
				markObstacle("North")
			else:
				markObstacle("South")

		if (rightDist<threshold_R):
			if direction is "East":
				markObstacle("South")
			else:
				markObstacle("north")
	

		
def move():	    #Move depending on the current direction the robot is facing
				#This will also adjust the roomList array's boundries as needed
	
	global globalX, globalY, posX, posY, currentNode, roomList, direction, numNodes, maxX, maxY, robot, moveDist
	
	
	robot.go(18,0)
	robot.waitDistance(moveDist/16)
	robot.go(25,0)
	robot.waitDistance(moveDist/16)
	robot.go(50, 0)
	robot.waitDistance(moveDist/4)
	robot.go(25,0)
	robot.waitDistance(moveDist/16)
	robot.go(10,0)
	robot.waitDistance(moveDist/16)
	robot.stop()
	
	if direction is "North":
		globalY-=1
		posY-=1
		if(posY == -1):
			bumpMinY()
		
		roomList[posY][posX].nodeNum = numNodes+1
		roomList[posY][posX].bottom = currentNode
		currentNode.top = roomList[posY][posX]
		currentNode = roomList[posY][posX]
		numNodes+=1
		
	
	elif direction is "West":
		globalX-=1
		posX-=1
		if(posX == -1):
			bumpMinX()
				
		
		roomList[posY][posX].nodeNum = numNodes+1
		roomList[posY][posX].right = currentNode
		currentNode.left = roomList[posY][posX]
		currentNode = roomList[posY][posX]
		numNodes+=1
	
	
	elif direction is "South":
		globalY+=1
		posY+=1

		if(posY > maxY):
			bumpMaxY()
		
		roomList[posY][posX].nodeNum = numNodes+1
		roomList[posY][posX].top = currentNode
		currentNode.bottom = roomList[posY][posX]
		currentNode = roomList[posY][posX]
		numNodes+=1
	
	elif direction is "East":
		globalX+=1
		posX+=1
		
		if(posX > maxX):
			bumpMaxX()
						
		roomList[posY][posX].nodeNum = numNodes+1
		roomList[posY][posX].left = currentNode
		currentNode.right = roomList[posY][posX]
		currentNode = roomList[posY][posX]
		numNodes+=1


def checkVisited():

	if direction is "North":
		try:
			if(posY is 0):
				return True
				
			elif (roomList[posY-1][posX].nodeNum == -1):
				return True
		except IndexError:
			print("ERROR")
			return True
		
	elif direction is "East":
		try:
			if (roomList[posY][posX+1].nodeNum == -1):
				return True 
		except IndexError:
			return True
	
	elif direction is "South":
		try:
			if (roomList[posY+1][posX].nodeNum == -1):
				return True 
		except IndexError:
			return True	
	
	elif direction is "West":
		try:
			if(posX is 0):
				return True
				
			elif (roomList[posY][posX-1].nodeNum == -1):
				return True 
		except IndexError:
			return True
		
	return False
	
	
	
def findNext():
	global roomList
	try:
		for i in range(len(roomList)):
			for j in range(len(roomList[i])):
				if(roomList[i][j].nodeNum >= 0):
					if(roomList[i-1][j].nodeNum == -1 and i != 0):
						return roomList[i][j].nodeNum, j, i, "North"
					elif(roomList[i][j+1].nodeNum == -1):
						return roomList[i][j].nodeNum, j, i, "East"
					elif(roomList[i+1][j].nodeNum == -1): 
						return roomList[i][j].nodeNum, j, i, "South"
					elif(roomList[i][j-1].nodeNum == -1 and j!= 0):
						return roomList[i][j].nodeNum, j, i, "West"
	except IndexError:
		print("ERRR")
	return -1, -1, -1, -1

def moveTo(targetNode, targetX, targetY):
	global posX, posY, currentNode, roomList, globalX, globalY, stop
	if(targetNode is -1):
		print("All possible nodes visited")
		stop = 1
	else:
		#NOT SURE HOW YET
		diffX = posX-targetX
		diffY = posY-targetY
		
		globalX = globalX - diffX
		globalY = globalY - diffY
		posX = targetX
		posY = targetY
		currentNode = roomList[targetY][targetX]
		
def calibrate():
	global ECHO_L, ECHO_R, TRIG_L, TRIG_R, hallwayWidth, seperationWidth, robot, rightDist, leftDist, moveDist
	
	print("Left", leftDist, "Right:", rightDist)

  
	if((leftDist > 1500) or (rightDist > 1000)):   #   Greater than 1500 being considered
		print("RETURNING LEFT OR RIGHT DIST > 1000 cm")
		return									 #      infinite for these purposes
	
	rightDist2 =  ts.takeSamples(TRIG_R,ECHO_R)
	leftDist2 = ts.takeSamples(TRIG_L,ECHO_L)
	print("LEFT2 is ", leftDist2, "RIGHT2 is ", rightDist2)
	
	if((leftDist2 > 1500) or (rightDist2 > 1000)):
		print("RETURNING LEFT2 OR RIGHT2 DIST > 1000 cm")
		return
	
	
	if((rightDist2 < rightDist) and (rightDist2 < (rightDist+leftDist)/2)):
		theta = math.degrees(math.asin((rightDist - rightDist2)/(moveDist/2)))
		print("Right Angle is ", theta)
		if(theta > 90):
			print("RETURNING, RIGHT ANGLE OVER 90")
			return
		robot.go(0, 25)
		robot.waitAngle(2*theta)
		robot.stop()
		
		robot.go(18,0)
		robot.waitDistance(moveDist/16)
		robot.go(25,0)
		robot.waitDistance(moveDist/16)
		robot.go(50, 0)
		robot.waitDistance(moveDist/4)
		robot.go(25,0)
		robot.waitDistance(moveDist/16)
		robot.go(10,0)
		robot.waitDistance(moveDist/16)
		robot.stop()
		
		robot.go(0, -25)
		robot.waitAngle(-theta)
		robot.stop()
	
	elif((leftDist2 < leftDist) and (leftDist2 < (rightDist+leftDist)/2)):
		theta = math.degrees(math.asin((leftDist - leftDist2)/(moveDist/2)))
		if(theta > 90):
			print("RETURNING LEFT ANGLE OVER 90")
			return
		print("Left Angle is ", theta)
		robot.go(0, -25)
		robot.waitAngle(-2*theta)
		robot.stop()
		
		robot.go(18,0)
		robot.waitDistance(moveDist/16)
		robot.go(25,0)
		robot.waitDistance(moveDist/16)
		robot.go(50, 0)
		robot.waitDistance(moveDist/4)
		robot.go(25,0)
		robot.waitDistance(moveDist/16)
		robot.go(10,0)
		robot.waitDistance(moveDist/16)
		robot.stop()
		
		robot.go(0, 25)
		robot.waitAngle(theta)
		robot.stop()
	
	
	
	
	
	
	

	
def markObstacle(direction):
	global roomList, posX, posY, maxX, maxY
	
	if(posX+1 > maxX):
		bumpMaxX()
				
	if(posX == 0):
		bumpMinX()
	
	if(posY+1 > maxY):
		bumpMaxY()
				
	if(posY == 0):
		bumpMinY()
			
			
	if direction is "North" and roomList[posY-1][posX].nodeNum == -1:
		roomList[posY-1][posX].nodeNum = -2
	elif direction is "East" and roomList[posY][posX+1].nodeNum == -1:
		roomList[posY][posX+1].nodeNum = -2
	elif direction is "South" and roomList[posY+1][posX].nodeNum == -1:
		roomList[posY+1][posX].nodeNum = -2
	elif direction is "West" and roomList[posY][posX-1].nodeNum == -1:
		roomList[posY][posX-1].nodeNum = -2

		
		
def checkMove():
	global turnCount, direction
	
	if(sensor() is 0 and checkVisited()):
		turnCount = 0
		move()
		
	elif(turnCount > 3):
		newNode, x, y, direction = findNext()
		print("MOVING TO NODE", newNode, "at X:", x, "Y:", y, " Direction: ", direction)
		print("roomList:", roomList[y-1][x].nodeNum)
		moveTo(newNode, x, y)
		turnCount = 0
		
	else:
		markObstacle(direction)
		turn()
		checkSides()
		turnCount+=1
		checkMove()
		
	

	
	
	
def printRoom():
	global direction, globalX, globalY
	print("Position: (", globalX, ",", globalY, ")\n")
	for i in range(len(roomFile)):
		for j in range(len(roomFile[i])):
			if (i is globalY) and (j is globalX):
				print(arrowDir[direction], end=' ')
			else:
				print(roomFile[i][j], end=' ')
		print()	
		
def printList():  #Print contents of roomList

	global roomList, currentNode
	print('~'*20)
	print("Current Node", currentNode.nodeNum,":(", currentNode.col, ",", currentNode.row,")")
	
	for i in range(len(roomList)):
		for j in range(len(roomList[i])):
			if (i is posY) and (j is posX):
				print(arrowDir[direction], end=' ')
			elif(roomList[i][j].nodeNum is -1):
				print('-', end=' ')
			elif(roomList[i][j].nodeNum is -2):
				print('#', end=' ')
			else:
				print(roomList[i][j].nodeNum, end=' ')
		print()
	print('~'*20)
	
	
	
	

	
	
def angleTest():
	global TRIG_L, TRIG_R, ECHO_L, ECHO_R, robot, moveDist
	rightDist =  ts.takeSamples(TRIG_R,ECHO_R)
	leftDist = ts.takeSamples(TRIG_L,ECHO_L)
	print("LEFT is ", leftDist, "RIGHT is ", rightDist)
		
	if((leftDist > 1500) or (rightDist > 1500)):   #   Greater than 1500 being considered
		print("RETURNING LEFT OR RIGHT DIST > 1500 cm")
		return									 #      infinite for these purposes
	
	robot.go(18,0)
	robot.waitDistance(moveDist/8)
	robot.go(25,0)
	robot.waitDistance(moveDist/8)
	robot.go(50, 0)
	robot.waitDistance(moveDist/2)
	robot.go(25,0)
	robot.waitDistance(moveDist/8)
	robot.go(10,0)
	robot.waitDistance(moveDist/8)
	robot.stop()
	
	rightDist2 =  ts.takeSamples(TRIG_R,ECHO_R)
	leftDist2 = ts.takeSamples(TRIG_L,ECHO_L)
	print("LEFT2 is ", leftDist2, "RIGHT2 is ", rightDist2)
	
	if((leftDist2 > 1500) or (rightDist2 > 1500)):
		print("RETURNING LEFT2 OR RIGHT2 DIST > 1500 cm")
		return
	
	
	if((rightDist2 < rightDist) and (rightDist2 < (rightDist+leftDist)/2)):
		theta = math.degrees(math.asin((rightDist - rightDist2)/moveDist))
		print("Right Angle is ", theta)
		if(theta > 90):
			print("RETURNING, RIGHT ANGLE OVER 90")
			return
		robot.go(0, 25)
		robot.waitAngle(2*theta)
		robot.stop()
		
		robot.go(18,0)
		robot.waitDistance(moveDist/8)
		robot.go(25,0)
		robot.waitDistance(moveDist/8)
		robot.go(50, 0)
		robot.waitDistance(moveDist/2)
		robot.go(25,0)
		robot.waitDistance(moveDist/8)
		robot.go(10,0)
		robot.waitDistance(moveDist/8)
		robot.stop()
		
		robot.go(0, -25)
		robot.waitAngle(-theta)
		robot.stop()
	
	elif((leftDist2 < leftDist) and (leftDist2 < (rightDist+leftDist)/2)):
		theta = math.degrees(math.asin((leftDist - leftDist2)/moveDist))
		if(theta > 90):
			print("RETURNING LEFT ANGLE OVER 90")
			return
		print("Left Angle is ", theta)
		robot.go(0, -25)
		robot.waitAngle(-2*theta)
		robot.stop()
		
		robot.go(18,0)
		robot.waitDistance(moveDist/8)
		robot.go(25,0)
		robot.waitDistance(moveDist/8)
		robot.go(50, 0)
		robot.waitDistance(moveDist/2)
		robot.go(25,0)
		robot.waitDistance(moveDist/8)
		robot.go(10,0)
		robot.waitDistance(moveDist/8)
		robot.stop()
		
		robot.go(0, 25)
		robot.waitAngle(theta)
		robot.stop()

def checkCharge():
	global robot, battery, dockPercent
	charge = robot.getSensor('BATTERY_CHARGE')
	if(charge > 2800):
		return
	capacity = robot.getSensor('BATTERY_CAPACITY')
	battery = charge/capacity*100//1
	print("BATTERY:", battery, "%")
	
	if((battery) <= dockPercent ):
		print("Battery Below", dockPercent, "% \nFINDING DOCK")
		robot.toSafeMode()
		robot.seekDock()
		
		while(battery < 50):
			charge = robot.getSensor('BATTERY_CHARGE')
			capacity = robot.getSensor('BATTERY_CAPACITY')
			battery = charge/capacity*100//1
			time.sleep(60)
			print("BATTERY:", battery, "%")
		
		
	return 0
		
def centerTest():
	global TRIG_L, TRIG_R, ECHO_L, ECHO_R, robot, moveDist
	rightDist =  ts.takeSamples(TRIG_R,ECHO_R)
	leftDist = ts.takeSamples(TRIG_L,ECHO_L)
	print("TESTING CENTERING PROCESS")
	print("LEFT is ", leftDist, "RIGHT is ", rightDist)
	if((leftDist > 1500) or (rightDist > 1500)):   #   Greater than 1500 being considered infinite
		print("RETURNING LEFT OR RIGHT DIST > 1500 cm")
		return	
	
	if(rightDist < (rightDist+leftDist)/2):
		robot.go(0, 25)
		robot.waitAngle(90)
		robot.stop()
		
		robot.go(25)
		robot.waitDistance(((rightDist+leftDist)/2)-rightDist)
		robot.stop()
		
		robot.go(0, -25)
		robot.waitAngle(-90)
		robot.stop()
	
	elif(leftDist < (rightDist+leftDist)/2):
		robot.go(0, -25)
		robot.waitAngle(-90)
		robot.stop()
		
		robot.go(25)
		robot.waitDistance(((rightDist+leftDist)/2)-leftDist)
		robot.stop()
		
		robot.go(0, 25)
		robot.waitAngle(90)
		robot.stop()
		
	
def init():    #Initialize variables and create staring node. Default direction is "North"
	global globalX, globalY, direction, roomList, currentNode, posX, posY, \
	numNodes, maxX, maxY, turnCount, stop, TRIG, ECHO, TRIG_R, ECHO_R, TRIG_L, ECHO_L, \
	threshold_Front, threshold_R, threshold_L, robot, turnAngle, moveDist, seperationWidth, hallwayWidth, \
	dockPercent, battery

	
	robot = create.Create('/dev/ttyUSB0')
	turnAngle = -90
	moveDist = 100
	
	#GPIO Mapping for Front, Left and Right sonar sensors
	TRIG = 23
	ECHO = 25
	TRIG_R = 4
	ECHO_R = 21
	ECHO_L = 12
	TRIG_L = 24
	
	#Sensitivity Threshold for Obstacle distance in cm
	threshold_Front = 120
	threshold_L = 150
	threshold_R = 150
	hallwayWidth = 250
	seperationWidth = 32
	
	globalX = globalY = 4
	turnCount = 0
	posX = posY = 0
	maxX = maxY = 0
	direction = "North"
	roomList = [[]]
	currentNode = Node(0, None, None, None, None, posX, posY)
	roomList[0].append(currentNode)
	numNodes = 0
	stop = 0

	dockPercent = 20
	
	battery = 100
	waitVal = checkCharge()
	
	
def startJingle():
	global robot
	robot.playSong([(58,8)])
	time.sleep(0.15)
	robot.playSong([(60,8)])
	time.sleep(0.15)
	robot.playSong([(62,8)])
	time.sleep(0.15)
	robot.playSong([(58,8)])
	
	
def IR():
	global robot
	IR_Signal = [255]*10
	#while(1): 
	for x in range(10):
		try:
			IR_Signal[x] = robot.getSensor('IR_BYTE')%255
			
		except TypeError:
			IR_Signal[x] = 0
			
			
		print(IR_Signal[x])
		robot.go(0,35)
		robot.waitAngle(36)
		robot.stop()
		time.sleep(2)
		
	max_IR = max(IR_Signal)
	max_index = IR_Signal.index(max_IR)
	time.sleep(5)

	print("Max Value is ", max_IR, "IR Signal ", max_index)

	if(max_IR > 0):
		robot.go(0, 50)
		angle = max_index*36
		robot.waitAngle(angle)
		robot.stop()
		
		robot.go(15, 0)
		robot.waitDistance(20)
		robot.stop()
		print("FACING CHARGER?")
		time.sleep(2)
	
def main():
	global direction, stop, roomList
	global robot
	init()
	signal.signal(signal.SIGINT, signal_handler)
	
	startJingle()
	
	printList()
	checkSides()

	while(stop != 1):
		#time.sleep(0.5)

		checkSides()
		checkMove()
		printList()
		calibrate()
		#time.sleep(0.5)  #Time Delay for Viewing
		
	direction = "North"
	printList()
	
main()
#robot = create.Create('/dev/ttyUSB0')
#for i in range(5):
#	IR()
