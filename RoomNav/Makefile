

all: roomNavTest

roomNavTest: roomNav
	./roomNav ./testRoom1.txt

roomNav: roomNav.c Makefile
	gcc -std=c99 -o roomNav roomNav.c
	
clean:
	rm -f roomNav
