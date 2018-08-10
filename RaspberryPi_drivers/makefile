PROG = exe
CC = g++
CPPFLAGS = -g -Wall -I/.
LDFLAGS = -lwiringPi 
OBJS = main.o socket_server.o drv_acc.o

# sciezka do bibliotek c++-L/usr/include/c++/6.3.0 

$(PROG) : $(OBJS)
		$(CC) $(LDFLAGS) -o $(PROG) $(OBJS)
main.o :
		$(CC) $(CPPFLAGS) -c main.cpp

socket_server.o: socket_server.h	
		$(CC) $(CPPFLAGS) -c socket_server.cpp

drv_acc.o: drv_acc.h
		$(CC) $(CPPFLAGS) -c drv_acc.cpp	

clean:
		rm -f core $(PROG) $(OBJS)
