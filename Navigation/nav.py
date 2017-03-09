'''Project: Envirobot for Senior Design at University of Delaware
Navigation Code
by Josh Mack 3/8/2017'''

import random
import time

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
arrowDir = {'North': "^", 'South': "v", 'East': ">", 'West': "<"}

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
	
def sensor():  #Artificial Sensor for testing 1= obstacle detected, 0 = none
	if direction is "North":
		return roomFile[globalY-1][globalX]
	elif direction is "South":
		return roomFile[globalY+1][globalX]
	elif direction is "East":
		return roomFile[globalY][globalX+1]
	elif direction is "West":
		return roomFile[globalY][globalX-1]
	
def turn():
	global direction

	if direction is "North":
		direction = "East"
	elif direction is "East":
		direction = "South"
	elif direction is "South":
		direction = "West"
	elif direction is "West":
		direction = "North"

def move():	    #Move depending on the current direction the robot is facing
				#This will also adjust the roomList array's boundries as needed
	
	global globalX, globalY, posX, posY, currentNode, roomList, direction, numNodes, maxX, maxY
	if direction is "North":
		globalY-=1
		posY-=1
		if(posY == -1):
			maxY+=1
			posY+=1
			roomList.insert(0, [])
			for col in range(len(roomList[1])):
				roomList[1][col].row = 1
				roomList[0].append(Node(-1, None, None, None, None, col, 0))
		
		roomList[posY][posX].nodeNum = numNodes+1
		roomList[posY][posX].bottom = currentNode
		currentNode.top = roomList[posY][posX]
		currentNode = roomList[posY][posX]
		numNodes+=1
		
	
	elif direction is "West":
		globalX-=1
		posX-=1
		if(posX == -1):
			posX+=1
			maxX+=1
			for row in range(len(roomList)):
				roomList[row].insert(0, Node(-1, None, None, None, None, -1, row))
				for col in range(len(roomList[0])):
					roomList[row][col].col += 1
				
		
		roomList[posY][posX].nodeNum = numNodes+1
		roomList[posY][posX].right = currentNode
		currentNode.left = roomList[posY][posX]
		currentNode = roomList[posY][posX]
		numNodes+=1
	
	
	elif direction is "South":
		globalY+=1
		posY+=1

		if(posY > maxY):
			maxY+=1
			roomList.append([])
			for col in range(len(roomList[0])):
				roomList[maxY].append(Node(-1, None, None, None, None, col, maxY))
		
		roomList[posY][posX].nodeNum = numNodes+1
		roomList[posY][posX].top = currentNode
		currentNode.bottom = roomList[posY][posX]
		currentNode = roomList[posY][posX]
		numNodes+=1
	
	elif direction is "East":
		globalX+=1
		posX+=1
		
		if(posX > maxX):
			maxX+=1
			for row in range(len(roomList)):
				roomList[row].append(Node(-1, None, None, None, None, maxX, row))
						
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
		
	
def markObstacle():
	global direction, roomList, posX, posY
	try:
		if direction is "North" and roomList[posY-1][posX].nodeNum == -1:
			roomList[posY-1][posX].nodeNum = -2
		elif direction is "East" and roomList[posY][posX+1].nodeNum == -1:
			roomList[posY][posX+1].nodeNum = -2
		elif direction is "South" and roomList[posY+1][posX].nodeNum == -1:
			roomList[posY+1][posX].nodeNum = -2
		elif direction is "West" and roomList[posY][posX-1].nodeNum == -1:
			roomList[posY][posX-1].nodeNum = -2
	
	except IndexError:
		print()
		
		
		
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
		markObstacle()
		turn()
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
				print('*', end=' ')
			else:
				print(roomList[i][j].nodeNum, end=' ')
		print()
	print('~'*20)
	
	
	
	
def init():    #Initialize variables and create staring node. Default direction is "North"
	global globalX, globalY, direction, roomList, currentNode, posX, posY, numNodes, maxX, maxY, turnCount, stop
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
	
	
def main():
	global direction, stop, roomList
	init()
	test()
	printRoom()
	printList()
	while(stop != 1):
		checkMove()
		#printList()
		time.sleep(0.5)  #Time Delay for Viewing
		
	direction = "North"
	printList()
	
	
main()
