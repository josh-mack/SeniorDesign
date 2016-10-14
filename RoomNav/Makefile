#Josh Mack
#10/12/16


#Default make will show both linked list print and room array
all: roomNav

roomNav: roomNavBuild
	./roomNav ./testRoom1.txt
	
roomNavBuild: roomNav.c Makefile
	gcc -std=c99 -o roomNav roomNav.c -DPRINTLL=1 -DPRINTROOM=1
	
	
#RoomNavList will only show linkedList output
roomNavList: roomNavListBuild
	./roomNav ./testRoom1.txt

roomNavListBuild: roomNav.c Makefile
	gcc -std=c99 -o roomNav roomNav.c -DPRINTLL=1

#RoomNavRoom will only show room array output
roomNavRoom: roomNavRoomBuild
	./roomNav ./testRoom1.txt

roomNavRoomBuild: roomNav.c Makefile
	gcc -std=c99 -o roomNav roomNav.c -DPRINTROOM=1
	
clean:
	rm -f roomNav
