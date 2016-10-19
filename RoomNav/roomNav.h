#define _GNU_SOURCE
#include <string.h>
#include <stdlib.h>
#include <stdio.h>
#include <math.h>
#include <time.h>
#include <unistd.h>


int sensor();
void Initi();
void move();
void rotate();
int sensorInput(char*);
void printGrid();
int linkedList(char);
int printNode();
int checkNode();
int findNode();



typedef struct sensorNode
{
	int number;
	struct sensorNode *top;
	struct sensorNode *bottom;
	struct sensorNode *left;
	struct sensorNode *right;
	int row;
	int col;

} sensorNode;
