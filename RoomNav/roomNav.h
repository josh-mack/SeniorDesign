#include <string.h>
#include <stdlib.h>
#include <stdio.h>
#include <math.h>
#include <time.h>



int sensor();
void Initi();
void move();
void rotate();
int sensorInput(char*);
void printGrid();



struct sensorNode
{
	int number;
	struct sensorNode *top;
	struct sensorNode *bottom;
	struct sensorNode *left;
	struct sensorNode *right;

} *headNode, *tailNode, *currNode, *tempNode;
