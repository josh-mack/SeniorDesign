#include "roomNav.h"
int startX;    //Randomized Start x,y points
int startY;    // of robot

int posX;      //Current x,y Position
int posY;		// of robot

int **testArray;   //2-D array of room to simulate sensor inputs
int testArrayW;
int testArrayH;

char direction;    //Direction robot is facing


void rotate(){
	if(direction == 'n')
		direction = 'e';
	else if(direction == 'e')
		direction = 's';
	else if(direction == 's')
		direction = 'w';
	else if(direction == 'w')
		direction = 'n';


}
void move(){
	if(direction == 'n')
		posY--;
	else if(direction == 'e')
		posX++;
	else if(direction == 's')
		posY++;
	else if(direction == 'w')
		posX--;
}

int sensor(){
	if(direction == 'n')
		return testArray[posY-1][posX];
	else if(direction == 'e')
		return testArray[posY][posX+1];
	else if(direction == 's')
		return testArray[posY+1][posX];
	else if(direction == 'w')
		return testArray[posY][posX-1];
	
}

void Initi(){   //Initialize Linked List
	headNode = (struct sensorNode *)malloc(sizeof(struct sensorNode));
	tailNode = (struct sensorNode *)malloc(sizeof(struct sensorNode));
	struct sensorNode *tempNode;  
	headNode = NULL;
	tailNode = NULL;
	currNode = NULL;


}

int sensorInput(char* filename){   //Simulate sensor input based on room array values
	testArrayH = 1;

	FILE *fp;
	char* buffer;
	buffer = malloc(200*sizeof(char));	
	fp = fopen(filename, "r");

	size_t lineLen = 1;
	getline(&buffer, &lineLen, fp); 
	testArrayW = lineLen-3;

	if(lineLen == -1){
		printf("ERROR COULD NOT READ MAP\n");
		return -1;
		}
	else{
	printf("\n");
	while(getline(&buffer, &lineLen, fp) > 0){
		testArrayH++;
		}
	}
  	

//Fill array with int values 1 represents an obstacle
	printf("Room Dimensions = w: %i x h: %i\n", testArrayW, testArrayH);
	
	testArray = (int**)realloc(testArray, testArrayH*sizeof(sizeof(int)*testArrayW));

	rewind(fp);   //Rewind file
	for(int y = 0; y < testArrayH; y++){
		getline(&buffer, &lineLen, fp);

		testArray[y] = (int*)malloc(sizeof(int)*testArrayW);

		for(int x = 0; x < testArrayW; x++){
			testArray[y][x] = (buffer[x] == '0')?0:1;
		}
	}
	srand ( time(NULL) );
	startX = rand()%(testArrayW-1)+1;
	startY = rand()%(testArrayH-1)+1;

//REASSIGN if starting position is on an obstacle
	while(testArray[startY][startX] == 1){	
		startX = rand()%(testArrayW-1)+1;
		startY = rand()%(testArrayH-1)+1;
	}

	
}

void printGrid(){
	printf("Position: (%i,%i)\n", posX, posY);
	for(int y = 0; y < testArrayH; y++){
		for(int x = 0; x < testArrayW; x++){
			if(x == posX && y == posY){
				if(direction == 'n')
					printf(" ^");
				else if(direction == 'e')
					printf(" >");
				else if(direction == 's')
					printf(" v");
				else if(direction == 'w')
					printf(" <");
			}	
			else
				printf("%i ",testArray[y][x]);
		}
		printf("\n");
	}
}

int main(int argc, char **argv){
	direction = 'n';     //Start off with robot facing "Up"
	Initi();
	sensorInput(argv[1]);  //Initizlise array to simulate sensor input
	posX = startX;     //
	posY = startY;
	
	int userIn = (argv[2])?atoi(argv[2]):0;   //Let user specifiy how many
											  //time steps to run simulation for	
											  //If no value specify, loop infinitely
	
	if(userIn > 0){
		for(int i = 0; i < userIn; i++){ 
			printf("Move: %i\n", userIn);
			printGrid();
			if(!sensor())
				move();
			else
				rotate();

			sleep(1);
		}
	}
	else{
		while(1){
			printGrid();
			if(!sensor())
				move();
			else
				rotate();

			sleep(1);
		}
	}
}


