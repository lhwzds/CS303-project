

OFLAGS	= $(WARN) $(OPT) $(MACHINE_OPT)
DFLAGS	= $(WARN) -g
PFLAGS	= $(WARN) $(MACHINE_OPT) -pg -lc


ifeq ("$(MODE)", "normal")
  FLAGS   = $(OFLAGS) -DNDEBUG
  STRIP   = strip
endif

ifeq ("$(MODE)", "prof")
  FLAGS   = $(PFLAGS) -DNDEBUG
  STRIP   = echo
  OBJ = $(OBJ_PROF)
endif

ifeq ("$(MODE)", "debug")
  FLAGS   = $(DFLAGS)
  STRIP   = echo
  OBJ = $(OBJ_DEBUG)
endif


SRC	= 


CCOPTS	= -c -DUNIX $(CC_OPTS) -DSELF_PROTOS=$(SELF_PROTOS) \
             -DUSLEEP=$(USLEEP) -DSMALL_HASH=$(SMALL_HASH)  \
             $(FLAGS) 

LNOPTS  = $(FLAGS) 
LIBS	= -lm -lc

LN	= $(CC)


#
# rule for c-files
#
$(OBJ)/%.o: %.c 
	$(CC) $(CCOPTS) -o $@ $<



#$(OBJ)/lclient.o: client.c
#	$(CC) $(CCOPTS) -o $(OBJ)/lclient.o client.c


# automatically generated dependencies:






######## ox story ... #########

# Compiler flags.

CPPFLAGS += -traditional -I~/c/o/src -I$(SRC) -I/usr/local/X11/include
#-I$(GUIDEHOME)/include -I$(OPENWINHOME)/include
LDFLAGS  +=
#-L$(GUIDEHOME)/lib -L$(OPENWINHOME)/lib
LDLIBS   +=  -lX11 -lxview -lolgx 
#-lguidexv 
#-lguide  

ox_OBJ	 = 	$(OBJ)/xm.o	\
	  	$(OBJ)/playgm.o	\
		$(OBJ)/int.o	\
		$(OBJ)/o_stubs.o\
		$(OBJ)/o_ui.o   \
		$(OBJ)/filecom.o\
		$(OBJ)/pipecom.o\
		$(OBJ)/sboard.o \
		$(OBJ)/trans.o  \
		$(OBJ)/crt.o    \
		$(OBJ)/goodies.o\
		$(OBJ)/game.o


       

o_stubs.c o_ui.c: o.G
	$(GUIDEHOME)/bin/gxv o.G

../ox:	$(ox_OBJ)
	$(LN) -o $(OBJ)/temp  -L/usr/X11/lib -L/usr/openwin/lib $(LNOPTS) $(LDLIBS) $^ 
	$(STRIP) $(OBJ)/temp
	mv $(OBJ)/temp $@
	
$(OBJ)/o_stubs.o:	o_stubs.c o.G
	gcc -c $(CCOPTS) -DUNIX -pipe -I/usr/local/X11/include -o $(OBJ)/o_stubs.o o_stubs.c 

$(OBJ)/o_ui.o:	o_ui.c o.G
	gcc -c $(CCOPTS) -DUNIX -pipe -I/usr/local/X11/include -o $(OBJ)/o_ui.o o_ui.c 



