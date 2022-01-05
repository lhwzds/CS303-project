/* normales Spielfeld */

#ifndef SBOARD_H
#define SBOARD_H 

typedef int	PARTEI;
typedef SBYTE	SFPOS;		/* hier auch negative Werte moegl. */

#define RAND		(-2)
#define FOR_SFPOS10(p)	for (p=11; p < 89; p++) if (TabZug[p])
#define FOR_SFPOS8(p)	FOR (p, 64)

#define X100(Pos)	((Pos % 10) - 1)
#define Y100(Pos)	((Pos / 10) - 1)

#define INNENANZ	36

/* normales Spielfeld */

typedef struct { SBYTE p[100]; short Marke; } SPFELD;


/* gepacktes Spielfeld */

typedef struct { UBYTE MapB[8], MapW[8]; short Marke; } SFCODE;


typedef struct { 

  SPFELD  Sf;
  PARTEI  AmZug;
  SFPOS	  Zug;

} SPIELSTAND;



/* Koordinaten im 10x10 Feld */

enum KOOR10 {

  RA00, RA01, RA02, RA03, RA04, RA05, RA06, RA07, RA08, RA09, 
  RA10, A1,   B1,   C1,   D1,   E1,   F1,   G1,   H1,   RA19,
  RA20, A2,   B2,   C2,   D2,   E2,   F2,   G2,   H2,   RA29,
  RA30, A3,   B3,   C3,   D3,   E3,   F3,   G3,   H3,   RA39,
  RA40, A4,   B4,   C4,   D4,   E4,   F4,   G4,   H4,   RA49,
  RA50, A5,   B5,   C5,   D5,   E5,   F5,   G5,   H5,   RA59,
  RA60, A6,   B6,   C6,   D6,   E6,   F6,   G6,   H6,   RA69,
  RA70, A7,   B7,   C7,   D7,   E7,   F7,   G7,   H7,   RA79,
  RA80, A8,   B8,   C8,   D8,   E8,   F8,   G8,   H8,   RA89,
  RA90, RA91, RA92, RA93, RA94, RA95, RA96, RA97, RA98, RA99

};



/* set of moves */

typedef ULONG ZUGMENGE[3];

#define ZM_LOESCHEN	memset(zm, 0, sizeof(zm))

#if 0

#define ZM_SETZEN(zug) \
  if      (zug < 32) zm[0] |= 1<<zug;\
  else if (zug < 64) zm[1] |= 1<<(zug-32);\
  else 		     zm[2] |= 1<<(zug-64);

#define ZM_GESETZT(zug) \
  ((zug < 32 ? zm[0] & (1<<zug) : \
   (zug < 64 ? zm[1] & (1<<(zug-32)) :\
	       zm[2] & (1<<(zug-64)))))

#else

#define ZM_SETZEN(zug)  zm[ZM_Word[zug]] |= ZM_Bit[zug]   
#define ZM_GESETZT(zug) (zm[ZM_Word[zug]] & ZM_Bit[zug])

#endif



#define ZUG_PASSEN	(-1)
#define ZUG_UNBEKANNT	(-2)

#define ZUG(z)		((z) >= 11 && (z) <= 88 && TabZug[z])


/* Eintragungen im SPFELD */

#define LEER		0
#define BLACK		1
#define WHITE		(-BLACK)

#define UMG		10	/* >= UMG:  Pos+UMG */
#define NUM_DISP	10	/* >= NUM_DISP: Zugnummer */

#define GEGNER(p)	(-(p))


/* Marken-Werte */

#define MA_GEWONNEN 		1
#define MA_VERLOREN		(-1)
#define MA_REMIS		0
#define MA_WEISS_NICHT		2

#define MA_WKEIT		100	/* hier bis +100 W'keit*100 */
#define MA_DIFF			500	/* hier bis +128 Differenz  */
#define MA_ZUG			1000	/* +11 bis +88 Zug */

#define BLACK_TO_MOVE	"-> "BLACKMAN"\n"
#define WHITE_TO_MOVE	"-> "WHITEMAN"\n"


typedef enum { BLACK_AM_ZUG, WHITE_AM_ZUG } 	AM_ZUG;
typedef enum { SP_COMP1, SP_COMP2, SP_MENSCH }  SP_TYP;


typedef struct {

  SPFELD  Sf;
  PARTEI  AmZug;
  REAL	  RestBLACK, RestWHITE;
  SP_TYP  SpielerBLACK, SpielerWHITE;
  SFPOS	  Zug;

} SPIELINFO;



/* Funktionen */

void	SfGrund		(SPFELD *psf);
void	SfxSpiegeln	(SPFELD *psf);
void	SfDrehen	(SPFELD *psf);
void	SfTransponieren	(SPFELD *psf);
void	SfZuf2		(SPFELD *psf,	int Anz);
void	SfInvert	(SPFELD *psf);
int	SfAnz		(SPFELD *psf);
int	SfAnzBLACK	(SPFELD *psf);
int	SfAnzWHITE	(SPFELD *psf);
void	SfAus		(SPFELD *psf,	PARTEI Partei,	int Moegl);
void	fSfAus		(FILE   *fp,	SPFELD *psf,	PARTEI Partei, int Moegl);
BOOL	TabEindeutig	(SPFELD *psf);
void	TabAus		(SPFELD *psf);
void	fTabAus		(FILE   *fp,	SPFELD *psf);
BOOL	fTabEin		(FILE   *fp,	SPFELD *psf);
BOOL	fSfWrite	(FILE	*fp,	SPFELD *sfgen,	int anz);
BOOL	SfWrite		(SPFELD *sfgen, int anz,	char *name);
int	fSfRead		(FILE	*fp,	SPFELD *sfgen,	int anzmax);
int	SfRead		(SPFELD *sfgen, int anzmax,	char *name);
int	SfSetzen	(SPFELD *psf,	PARTEI Partei,	SFPOS SfPos);
int	SfSetzCheck	(SPFELD *psf,	PARTEI Partei,	SFPOS SfPos);
int	SfMoeglZuege	(SPFELD *psf,	PARTEI Partei,	SFPOS *Zuege);
int	SfMoeglZuegeE	(SPFELD *psf, PARTEI Partei, SFPOS *Zuege);
void	SteinAus	(PARTEI Partei);
void	fSteinAus	(FILE	*fp,	PARTEI Partei);
void	SfPack		(SPFELD *psf,	SFCODE *pc);
void	SfEntpack	(SFCODE *pc,	SPFELD *psf);
void	SfSet		(SPFELD *psf,	PARTEI Partei);
BOOL	SfGleich	(SPFELD *psf1, SPFELD *psf2);
int	SfMax		(SPFELD *psf);



/* Daten */

extern BOOL TabZug[100], Ecke[100];
extern int  Tab8to10[64];
extern SPFELD SfNull;
extern int  Innen[INNENANZ];

extern int dx[8]; 
extern int dy[8]; 
extern int ds[8];
extern int ZM_Word[100], ZM_Bit[100], SqType[100];

#endif
