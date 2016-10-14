//Josh Mack 10/12/`6

#include "roomNav.h"
int startX;    //Randomized Start x,y points
int startY;    // of robot

int posX;      //Current x,y Position
int posY;		// of robot

int **testArray;   //2-D array of room to simulate sensor inputs
int testArrayW;
int testArrayH;
int mostRecentNode = 0;

int **printArray;   //Print Array is so we can show node values in the grid
					//without impacting the sensor array

char direction;    //Direction robot is facing

sensorNode* head;
sensorNode** tail;

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
	
	linkedList(direction);		
	printArray[posY][posX] = mostRecentNode-1;

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
	head = (struct sensorNode *)malloc(sizeof(sensorNode));
	tail = (struct sensorNode **)malloc(sizeof(sensorNode*));
	
	head->number = mostRecentNode++;
	head->top = NULL;
	head->bottom = NULL;
	head->left = NULL;
	head->right = NULL;
	
	(*tail) = head;
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
	printArray = (int**)malloc(testArrayH*sizeof(sizeof(int)*testArrayW));
	
	rewind(fp);   //Rewind file
	for(int y = 0; y < testArrayH; y++){
		getline(&buffer, &lineLen, fp);

		testArray[y] = (int*)malloc(sizeof(int)*testArrayW);
		printArray[y] = (int*)malloc(sizeof(int)*testArrayW);
		for(int x = 0; x < testArrayW; x++){
			testArray[y][x] = (buffer[x] == '0')?0:1;
			printArray[y][x] = testArray[y][x];
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
	printf("\nPosition: (%i,%i)\n", posX, posY);
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
				printf("%i ",printArray[y][x]);
		}
		printf("\n");
	}
}

int linkedList(char direction){
	sensorNode *current = (*tail);
	
	if(direction == 'n'){
		current->top = malloc(sizeof(sensorNode));
		(current->top)->number = mostRecentNode++;
		(current->top)->top = NULL;
		(current->top)->bottom = current;
		(current->top)->left = NULL;
		(current->top)->right = NULL;
		(*tail) = (current->top);
	}
	else if(direction == 'e'){
		current->right = malloc(sizeof(sensorNode));
		(current->right)->number = mostRecentNode++;
		(current->right)->top = NULL;
		(current->right)->bottom = NULL;
		(current->right)->left = current;
		(current->right)->right = NULL;
		(*tail) = (current->right);
	}
	else if(direction == 's'){
		current->bottom = malloc(sizeof(sensorNode));
		(current->bottom)->number = mostRecentNode++;
		(current->bottom)->top = current;
		(current->bottom)->bottom = NULL;
		(current->bottom)->left = NULL;
		(current->bottom)->right = NULL;
		(*tail) = (current->bottom);
	}
	else if(direction == 'w'){
		current->left = malloc(sizeof(sensorNode));
		(current->left)->number = mostRecentNode++;
		(current->left)->top = NULL;
		(current->left)->bottom = NULL;
		(current->left)->left = NULL;
		(current->left)->right = current;
		(*tail) = (current->left);
	}
	

	
	
	
	
}
int printLinkedList(int dir){
	sensorNode *current = (*tail);
	switch(dir){
		case 0: //Top-Bottom
			printf("TOP Node Number: %i", current->number);	
			while(current->bottom !=NULL){
				current = current->bottom;
				printf(" %i", current->number);	
			}
			break; 
		case 1: //Bottom-Top
			printf("BOT Node Number: %i", current->number);	
			while(current->top !=NULL){
				current = current->top;
				printf(" %i", current->number);	
			}
			break; 
		case 2: //Left-Right
			printf("LEFT Node Number: %i", current->number);	
			while(current->right !=NULL){
				current = current->right;
				printf(" %i", current->number);	
			}
			break; 
		case 3: //Right-Left
			printf("RIGHT Node Number: %i", current->number);	
			while(current->left !=NULL){
				current = current->left;
				printf(" %i", current->number);	
			}
			break; 
	}
	printf("\n");
	
}
int printNode(){
	
	if((((*tail)->top)) != NULL)
		printf("\n\n       %i       \n", ((*tail)->top)->number);
	else
		printf("\n\n       x       \n");
	
	if((((*tail)->left)) != NULL)
		printf("%i      ", ((*tail)->left)->number);
	else
		printf("x      ");
	
	printf("%i",(*tail)->number);
	
	if((((*tail)->right)) != NULL)
		printf("      %i\n", ((*tail)->right)->number);
	else
		printf("      x\n");
	
	if((((*tail)->bottom)) != NULL)
		printf("       %i       \n\n", ((*tail)->bottom)->number);
	else
		printf("       x       \n\n");
}

int main(int argc, char **argv){
	direction = 'n';     //Start off with robot facing "Up"
	Initi();
	sensorInput(argv[1]);  //Initialize array to simulate sensor input
	posX = startX;     //
	posY = startY;	
	printArray[startY][startX] = -1;


#ifdef PRINTROOM
	int userIn = (argv[2])?atoi(argv[2]):0;   //Let user specifiy how many
											  //time steps to run simulation for	
											  //If no value specify, loop infinitely
	if(userIn > 0){
		for(int i = 0; i < userIn; i++){ 
			printf("Move: %i\n", i);
			printGrid();
			#ifdef PRINTLL	
				printNode();
				printLinkedList(0); //Print Left-to-Right
				printLinkedList(1); //Print Left-to-Right
				printLinkedList(2); //Print Left-to-Right
				printLinkedList(3); //Print Left-to-Right
			#endif
			if(!sensor()){
				move();
			}
			else{
				rotate();
				printNode();
			}
		sleep(1);
		}
	}
	else{
		while(1){
			printGrid();
			#ifdef PRINTLL
				printNode();
				printLinkedList(0); //Print Left-to-Right
				printLinkedList(1); //Print Left-to-Right
				printLinkedList(2); //Print Left-to-Right
				printLinkedList(3); //Print Left-to-Right
			#endif
			if(!sensor()){
				move();
			}
		else{
			rotate();
			printNode();
		}
		sleep(1);
		}
	}
#endif
}


