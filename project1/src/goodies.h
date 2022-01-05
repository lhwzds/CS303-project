#ifndef O_ALLG
#define O_ALLG

#include "sboard.h"
#include "attr.h"


/* Ausgabe von LoadGame etc. */

#define LADE_FEHLER	(-1)
#define TAB_KORRUPT	(-2)


typedef struct { ULONG sek; USHORT millisek; } ZEIT;

extern	BOOL UseCpuTime;	/* Flag für Zeit() */


/* Multiplikativer Kongruenzgenerator langer */

extern  void	sMyRand	(ULONG x);
extern  ULONG	MyRand	(void);

extern int round(REAL w);
extern int sgn(int a);

extern  void	Zeit		(ZEIT *);
extern  void	RealeZeit	(ZEIT *);
extern  void	CPUZeit		(ZEIT *);
extern  REAL	ZeitDiff	(ZEIT *nach, ZEIT *vor);
extern  void	ZeitAdd		(ZEIT *, REAL Sekunden);
extern  void	BusyWait	(int n);
extern  BOOL	ParseNumber	(char *s, int *pn, char **psnew);
extern  void	InfoToTab	(SPIELINFO *Spiel, int MaxNr, SPFELD *psf);
extern  int	TabToInfo	(SPFELD *psf, SPIELINFO *Spiel);
extern  void	TabToSf		(SPFELD *psf1, SPFELD *psf2);
extern  BOOL	SaveGame	(char *name, SPIELINFO *Spiel, int MaxNr);
extern  int	LoadGame	(char *name, SPIELINFO *Spiel);
extern  int	LoadNextGame	(FILE *fp,   SPIELINFO *Spiel);

#endif
