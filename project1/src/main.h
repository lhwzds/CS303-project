#ifndef MAIN_H
#define MAIN_H

#include <ctype.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stddef.h>
#include <math.h>
#include <limits.h>
#include <float.h>
#include <time.h>
#include <setjmp.h>
#include <assert.h>
#include <fcntl.h>
#include <signal.h>

#define FOR(i,n)	for (i=0; i < (n); i++)
#define FOREVER 	for (;;)

#define min(a,b)	((a) < (b) ? (a) : (b))
#define max(a,b)	((a) > (b) ? (a) : (b))

#undef PI


#ifndef SMALL_HASH
#error SMALL_HASH not defined
#endif

#if SMALL_HASH
#define HASHBITS     17
#define HASHMAXDEPTH 8
#else
#define HASHBITS     20
#define HASHMAXDEPTH 10
#endif


#ifdef AMIGA
#define TO_PRAEFIX	"T:.To."
#define FROM_PRAEFIX	"T:.From."
#else
#define TO_PRAEFIX	".To."
#define FROM_PRAEFIX	".From."
#endif

#define QUOTE(x) 	#x
#define STRING(x)	QUOTE(x)

#define REAL_IS_DOUBLE

#ifdef REAL_IS_FLOAT

#define REAL		float
#define R_F		"f"
#define R_E		"e"
#define REAL_MAX  	FLT_MAX

#else

#define REAL		double
#define R_F		"lf"
#define R_E		"le"
#define REAL_MAX  	DBL_MAX

#endif


#if INTSIZE == 4
#define L_F		"d"
#else
#define L_F		"ld"
#endif

#define P_REAL(x)	printf("%" R_F "\n", x)

#define EPS 		(1e-5)	/* fabs(x-y) < EPS <=> x = y */

#define RGLEICH(r,s) 	(fabs((r)-(s)) < EPS)








/* Systemabhängig: */


#ifndef GCC
#define inline
#endif

#ifdef AMIGA

#define IRAN		rand()
#define SRAN		srand
#define SLEEP(x)	Delay((x) * 5L)		/* x * 0.1 sek warten */
#define WARTEN(x)	SLEEP(x)
#define SETJMP(env)	setjmp(env)
#define LONGJMP(env)	longjmp(env, 1)

#define	CHECK_COUNT	100	/* #Knoten -> Filecheck */

#define FUELL 		51	/* fehlende Bytes in Struktur KNOTEN */

#define LIBRARIES_MATHFFP_H

#include <stat.h>

extern	void	Delay(long);
#endif




#ifdef ATARI

#define IRAN		rand()
#define SRAN		srand
#define SLEEP(x)	delay((x) * 100)	/* x * 0.1 sek warten */
#define SETJMP(env)	setjmp(env)
#define LONGJMP(env)	longjmp(env, 1)

#define CLOCKS_PER_SEC	200
#define FUELL		37		/* fehlende Bytes in Struktur KNOTEN */

typedef unsigned char	UBYTE;
typedef unsigned short	USHORT;
typedef unsigned long	ULONG;
typedef unsigned int	BOOL;

#define TRUE		1
#define FALSE		0

extern void Chk_Abort(void);

#endif




#ifdef UNIX

#ifdef GPP
#include <std.h>
#endif


#include <sys/types.h>
/*#include <sys/timeb.h>*/
#include <sys/times.h>
#include <sys/stat.h>
#include <memory.h>
#include <unistd.h>


#define IRAN		rand()
#define SRAN		srand

#ifndef USLEEP
#error USLEEP undef.
#endif


#if USLEEP
#define SLEEP(x)	usleep((x) * 100000L)	/* wait x * 0.1 sec */
#else
#define SLEEP(x)        sleep((x) <= 10 ? 1 : round(((x)/10.0)))
#endif

#define WARTEN(x)	BusyWait(x)
#define SETJMP(env) 	setjmp(env)
#define LONGJMP(env)	longjmp(env, 1)

#define	CHECK_COUNT	15000	/* #Knoten -> Filecheck */


#define X		/* für BusyWait */



typedef unsigned char	UBYTE;
typedef unsigned short	USHORT;
typedef unsigned long	ULONG;
typedef unsigned int	BOOL;
typedef signed   char	SBYTE;

#define TRUE		1
#define FALSE		0

extern void Chk_Abort	(void);


#if SELF_PROTOS

#define RAND_MAX	((1<<31)-1)
#define CLOCKS_PER_SEC	60

extern void usleep      (unsigned);
extern int puts      	(const char*);
extern int fputs     	(const char*, FILE*);
extern int printf 	(const char*, ...);
extern int fprintf	(FILE*, const char*, ...);
extern int scanf  	(const char*, ...);
extern int fscanf	(FILE*, const char*, ...);
extern int sscanf 	(const char*, const char*, ...);
extern int fread  	(char*, unsigned int, int, FILE*);
extern int fwrite 	(const char*, unsigned int, int, FILE*);
extern int fclose 	(FILE*);
extern int fflush 	(FILE*);
extern int fseek  	(FILE*, long, int);
extern void rewind	(FILE*);
extern int getw   	(FILE*);
extern int fgetc  	(FILE*);

extern int pclose 	(FILE*);
extern int putw   	(int, FILE*);
extern int fputc  	(char, FILE*);
extern void setbuf	(FILE*, char*);
extern void setbuffer 	(FILE*, char*, int);
extern void setlinebuf 	(FILE*);
extern int ungetc 	(int, FILE*);

extern long strtol	(const char *, char **, int);
extern double strtod	(const char *, char **);
extern int atoi   	(const char*);
extern double atof	(const char*);
extern long atol  	(const char*);
extern void perror	(const char*);

extern char   *ctermid    (char *);
extern char   *cuserid    (char *);
extern char   *tempnam    (const char *, const char *);
extern char   *tmpnam     (char *);
extern void    psignal    (unsigned, char*);
extern int     putenv     (const char*);
extern void    setusershell(void);
extern char   *setstate   (char*);
extern void    srandom    (unsigned);
extern long    random     (void);
extern void    swab       (const char*, char*, int);
extern char   *getpass    (const char*);

extern int	unlink	(const char *);


#endif
#endif


#define FRAN 		((REAL)IRAN/RAND_MAX)


extern char TO_1[], FROM_1[], TO_2[], FROM_2[];
extern BOOL f_pipes;
extern void _abort(void);

#endif
