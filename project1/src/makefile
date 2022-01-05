# LINUX makefile

CC	= gcc
CC_OPTS	= -DGCC -pipe -I/usr/openwin/include -Dbool=int


# normal, debug, prof

MODE = normal


# gcc/g++ settings

WARN	= -Wall 

ifeq ("$(OSTYPE)", "Linux")

  OPT0	= -O6 \
          -fforce-addr \
          -fforce-mem \
 	  -fstrength-reduce \
  	  -fthread-jumps \
          -frerun-cse-after-loop \
	  -fexpensive-optimizations \
          -funroll-loops \
	  -finline-functions

  OBJ       = ../obj.LINUX
  OBJ_DEBUG = ../obj.LINUX.debug
  OBJ_PROF  = ../obj.LINUX.prof

  EVAL_EXCEPTION = -fno-force-addr

  MACHINE_OPT = $(OPT0)
  OPT         = -fomit-frame-pointer

  SELF_PROTOS = 0
  USLEEP      = 1
  SMALL_HASH  = 1

else 

ifeq ("$(OSTYPE)", "IRIX")

  OPT0    = -O6 \
          -fforce-addr \
          -fforce-mem \
          -fstrength-reduce \
          -fthread-jumps \
          -frerun-cse-after-loop \
          -fexpensive-optimizations \
          -funroll-loops \
          -fschedule-insns -fschedule-insns2 -fdelayed-branch \
          -finline-functions
  OBJ       = ../obj.IRIX
  OBJ_DEBUG = ../obj.IRIX.debug
  OBJ_PROF  = ../obj.IRIX.prof

  MACHINE_OPT = $(OPT0)
  OPT         = -fomit-frame-pointer

  SELF_PROTOS = 0
  USLEEP      = 0
  SMALL_HASH  = 0

else

ifeq ("$(OSTYPE)", "solaris")

  OPT0    = -O6 \
          -fforce-addr \
          -fforce-mem \
          -fstrength-reduce \
          -fthread-jumps \
          -frerun-cse-after-loop \
          -fexpensive-optimizations \
          -funroll-loops \
          -fschedule-insns -fschedule-insns2 -fdelayed-branch \
          -finline-functions
  OBJ       = ../obj.SUNOS
  OBJ_DEBUG = ../obj.SUNOS.debug
  OBJ_PROF  = ../obj.SUNOS.prof

  MACHINE_OPT = $(OPT0)
  OPT         = -fomit-frame-pointer

  SELF_PROTOS = 0
  USLEEP      = 1
  SMALL_HASH  = 0

else
  
  xxx

endif
endif
endif


include make.i
