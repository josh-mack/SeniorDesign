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
	
	print("len(roomList)", len(roomList))
	print("len(roomList[0])", len(roomList[0]))
	print("maxY", maxY)
	print("maxX", maxX)
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
				roomList[row].insert(0, Node(-1, None, None, None, None, 0, row))
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

		if(posY >= maxY):
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
		
		if(posX >= maxX):
			maxX+=1
			for row in range(len(roomList)):
				roomList[row].append(Node(-1, None, None, None, None, maxX, row))
						
		roomList[posY][posX].nodeNum = numNodes+1
		roomList[posY][posX].left = currentNode
		currentNode.right = roomList[posY][posX]
		currentNode = roomList[posY][posX]
		numNodes+=1
		
	
def checkMove():
	global turnCount
	
	if(sensor()) is 0:
		turnCount = 0
		move()
	else:
		turn()
		turnCount+=1
		checkMove()
		
	if(turnCount > 3):
		exit()

	
	
	
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
	print("Current Node", currentNode.nodeNum,":", currentNode.col, ",", currentNode.row,)
	
	for i in range(len(roomList)):
		for j in range(len(roomList[i])):
			if (i is globalY) and (j is globalX):
				print(arrowDir[direction], end=' ')
			elif(roomList[i][j].nodeNum is -1):
				print('*', end=' ')
			else:
				print(roomList[i][j].nodeNum, end=' ')
		print()
	print('~'*20)
	
	
	
	
def init():    #Initialize variables and create staring node. Default direction is "North"
	global globalX, globalY, direction, roomList, currentNode, posX, posY, numNodes, maxX, maxY, turnCount
	globalX = globalY = 4
	turnCount = 0
	posX = posY = 0
	maxX = maxY = 0
	direction = "North"
	roomList = [[]]
	currentNode = Node(0, None, None, None, None, posX, posY)
	roomList[0].append(currentNode)
	numNodes = 0
	
	
	
def main():
	global direction
	init()
	test()
	printRoom()
	printList()
	
	while(1):
		checkMove()
		printRoom()
		printList()
		time.sleep(1)
main()