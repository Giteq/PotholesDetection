# Directory to serach source files.
VPATH = src
#Source files.
SRC = 	main.cpp \
		drv_acc.cpp \
		socket_server.cpp
		
DEPS = $(patsubst %.cpp, deps.$(CFG)/%.d, ${SRC})
OBJS = $(patsubst %.cpp, objs$(CFG)/%.o, ${SRC})		

PROG = exe
CC = g++
CCDEP = g++
CPPFLAGS = -g -Wall -I/.
LDFLAGS = -lwiringPi 
INCLUDEFLAGS = -I src

all:		bin$(CFG)/${PROG}

bin$(CFG)/${PROG}: ${OBJS}
		@mkdir -p $(dir $@)
		$(CC) -g -o $@ $^ ${LDFLAGS}
		
objs$(CFG)/%.o: %.cpp
		@mkdir -p $(dir $@)
		$(CC) -c $(CPPFLAGS) -o $@ $<
		
deps.$(CFG)/%.d: %.cpp
		@mkdir -p $(dir $@)
		@set -e ; $(CCDEP) -MM -MP $(INCLUDEFLAGS) $< > $@.$$$$; \
		rm -f $@.$$$$
		
clean:
		@rm -rf \
		deps.debug objs.debug bin.debug \
		deps.release objs.release bin.release
