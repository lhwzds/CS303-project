/* Allerlei für Spielfelder */


#ifndef PRECOMP
#include "main.h"
#endif

#include "sboard.h"
#include "attr.h"
#include "crt.h"
#include "trans.h"
#include "game.h"


BOOL TabZug[100] = {

  0,0,0,0,0,0,0,0,0,0,
  0,1,1,1,1,1,1,1,1,0,
  0,1,1,1,1,1,1,1,1,0,
  0,1,1,1,1,1,1,1,1,0,
  0,1,1,1,1,1,1,1,1,0,
  0,1,1,1,1,1,1,1,1,0,
  0,1,1,1,1,1,1,1,1,0,
  0,1,1,1,1,1,1,1,1,0,
  0,1,1,1,1,1,1,1,1,0,
  0,0,0,0,0,0,0,0,0,0
};


BOOL Ecke[100] = {

  0,0,0,0,0,0,0,0,0,0,
  0,1,0,0,0,0,0,0,1,0,
  0,0,0,0,0,0,0,0,0,0,
  0,0,0,0,0,0,0,0,0,0,
  0,0,0,0,0,0,0,0,0,0,
  0,0,0,0,0,0,0,0,0,0,
  0,0,0,0,0,0,0,0,0,0,
  0,0,0,0,0,0,0,0,0,0,
  0,1,0,0,0,0,0,0,1,0,
  0,0,0,0,0,0,0,0,0,0
};


int SqType[100] = {

  0,0,0,0,0,0,0,0,0,0,
  0,1,2,3,4,4,3,2,1,0,
  0,2,5,6,7,7,6,5,2,0,
  0,3,6,8,9,9,8,6,3,0,
 0,4,7,9,10,10,9,7,4,0,
 0,4,7,9,10,10,9,7,4,0,
  0,3,6,8,9,9,8,6,3,0,
  0,2,5,6,7,7,6,5,2,0,
  0,1,2,3,4,4,3,2,1,0,
  0,0,0,0,0,0,0,0,0,0
};


int Innen[INNENANZ] = { 
  G2, F2, E2, D2, C2, B2, 
  G3, F3, E3, D3, C3, B3, 
  G4, F4, E4, D4, C4, B4,
  G5, F5, E5, D5, C5, B5,
  G6, F6, E6, D6, C6, B6,
  G7, F7, E7, D7, C7, B7,
};



SPFELD SfNull = {
  {
  RAND,RAND,RAND,RAND,RAND,RAND,RAND,RAND,RAND,RAND,
  RAND,LEER,LEER,LEER,LEER,LEER,LEER,LEER,LEER,RAND,
  RAND,LEER,LEER,LEER,LEER,LEER,LEER,LEER,LEER,RAND,
  RAND,LEER,LEER,LEER,LEER,LEER,LEER,LEER,LEER,RAND,
  RAND,LEER,LEER,LEER,LEER,LEER,LEER,LEER,LEER,RAND,
  RAND,LEER,LEER,LEER,LEER,LEER,LEER,LEER,LEER,RAND,
  RAND,LEER,LEER,LEER,LEER,LEER,LEER,LEER,LEER,RAND,
  RAND,LEER,LEER,LEER,LEER,LEER,LEER,LEER,LEER,RAND,
  RAND,LEER,LEER,LEER,LEER,LEER,LEER,LEER,LEER,RAND,
  RAND,RAND,RAND,RAND,RAND,RAND,RAND,RAND,RAND,RAND
  },
  0

};


int Tab8to10[64] = {		/* y*8+x -> (y+1)*10+x+1 */

  11, 12, 13, 14, 15, 16, 17, 18,
  21, 22, 23, 24, 25, 26, 27, 28,
  31, 32, 33, 34, 35, 36, 37, 38,
  41, 42, 43, 44, 45, 46, 47, 48,
  51, 52, 53, 54, 55, 56, 57, 58,
  61, 62, 63, 64, 65, 66, 67, 68,
  71, 72, 73, 74, 75, 76, 77, 78,
  81, 82, 83, 84, 85, 86, 87, 88

};

int dx[8] = { 1,  1,  0, -1, -1, -1, 0, 1 };
int dy[8] = { 0, -1, -1, -1,  0,  1, 1, 1 };

int ds[8] = { 1, -9, -10, -11, -1, 9, 10, 11 };


int ZM_Word[100] = {

 0,  0,  0,  0,  0,  0,  0,  0,  0,  0, 
 0,  0,  0,  0,  0,  0,  0,  0,  0,  0, 
 0,  0,  0,  0,  0,  0,  0,  0,  0,  0, 
 0,  0,  1,  1,  1,  1,  1,  1,  1,  1, 
 1,  1,  1,  1,  1,  1,  1,  1,  1,  1, 
 1,  1,  1,  1,  1,  1,  1,  1,  1,  1, 
 1,  1,  1,  1,  2,  2,  2,  2,  2,  2, 
 2,  2,  2,  2,  2,  2,  2,  2,  2,  2, 
 2,  2,  2,  2,  2,  2,  2,  2,  2,  2, 
 2,  2,  2,  2,  2,  2,  3,  3,  3,  3, 

};


int ZM_Bit[100] = {

0x00000001, 0x00000002, 0x00000004, 0x00000008, 0x00000010, 0x00000020, 0x00000040, 0x00000080, 0x00000100, 0x00000200, 
0x00000400, 0x00000800, 0x00001000, 0x00002000, 0x00004000, 0x00008000, 0x00010000, 0x00020000, 0x00040000, 0x00080000, 
0x00100000, 0x00200000, 0x00400000, 0x00800000, 0x01000000, 0x02000000, 0x04000000, 0x08000000, 0x10000000, 0x20000000, 
0x40000000, 0x80000000, 0x00000001, 0x00000002, 0x00000004, 0x00000008, 0x00000010, 0x00000020, 0x00000040, 0x00000080, 
0x00000100, 0x00000200, 0x00000400, 0x00000800, 0x00001000, 0x00002000, 0x00004000, 0x00008000, 0x00010000, 0x00020000, 
0x00040000, 0x00080000, 0x00100000, 0x00200000, 0x00400000, 0x00800000, 0x01000000, 0x02000000, 0x04000000, 0x08000000, 
0x10000000, 0x20000000, 0x40000000, 0x80000000, 0x00000001, 0x00000002, 0x00000004, 0x00000008, 0x00000010, 0x00000020, 
0x00000040, 0x00000080, 0x00000100, 0x00000200, 0x00000400, 0x00000800, 0x00001000, 0x00002000, 0x00004000, 0x00008000, 
0x00010000, 0x00020000, 0x00040000, 0x00080000, 0x00100000, 0x00200000, 0x00400000, 0x00800000, 0x01000000, 0x02000000, 
0x04000000, 0x08000000, 0x10000000, 0x20000000, 0x40000000, 0x80000000, 0x00000001, 0x00000002, 0x00000004, 0x00000008, 

};

/* Spielfeld besetzen */

void SfSet(SPFELD *psf, PARTEI Partei)
{
  int i;

  *psf = SfNull;

  FOR_SFPOS10(i) psf->p[i] = Partei;
}


/* Grundstellung im Spielfeld erzeugen */

void SfGrund(SPFELD *psf)
{
  *psf = SfNull;

  psf->p[E4] = psf->p[D5] = BLACK;
  psf->p[D4] = psf->p[E5] = WHITE;
}



/* Steine invertieren */

void SfInvert(SPFELD *psf)
{
  int i;

  FOR_SFPOS10(i) {
    if	    (psf->p[i] == BLACK) psf->p[i] = WHITE;
    else if (psf->p[i] == WHITE) psf->p[i] = BLACK;
  }
}



static int SpiegelPaare[] = { 
11, 18, 12, 17, 13, 16, 14, 15, 21, 28, 22, 27, 23, 26, 24, 25, 31, 38, 32, 37,
33, 36, 34, 35, 41, 48, 42, 47, 43, 46, 44, 45, 51, 58, 52, 57, 53, 56, 54, 55,
61, 68, 62, 67, 63, 66, 64, 65, 71, 78, 72, 77, 73, 76, 74, 75, 81, 88, 82, 87,
83, 86, 84, 85, 0
};


void SfxSpiegeln(SPFELD *psf)
{
  int   t, p1, p2;
  SBYTE *p=psf->p;
  int   *pp = SpiegelPaare;

  while ((p1=*pp++)) {

    p2 = *pp++;

    t = p[p1]; p[p1] = p[p2]; p[p2] = t;
  }
}



/*  alt
void SfxSpiegeln(SPFELD *psf)
{
  int a, x, y, p1, p2;
  SBYTE *p=psf->p;


  FOR (y, 10)
    FOR (x, 5) 

      if (x > 0 && x < 9 && y > 0 && y < 9) {
      a = p[p1 = y * 10 + x];
      p[p1] = p[p2 = y * 10 + 9 - x];
      p[p2] = a;

printf("%d, %d, ", p1, p2);

    }
printf("\n");

}
*/


int TransPaare[] = {
21, 12, 31, 13, 32, 23, 41, 14, 42, 24, 43, 34, 51, 15, 52, 25, 53, 35, 54, 45,
61, 16, 62, 26, 63, 36, 64, 46, 65, 56, 71, 17, 72, 27, 73, 37, 74, 47, 75, 57,
76, 67, 81, 18, 82, 28, 83, 38, 84, 48, 85, 58, 86, 68, 87, 78, 0
}; 



void SfTransponieren(SPFELD *psf)
{
  int   t, p1, p2;
  SBYTE *p=psf->p;
  int   *pp = TransPaare;

  while ((p1=*pp++)) {

    p2 = *pp++;

    t = p[p1]; p[p1] = p[p2]; p[p2] = t;
  }
}



/*   alt 
void SfTransponieren(SPFELD *psf)
{
  int a, x, y, p1, p2;
  SBYTE *p=psf->p;


  FOR (y, 10)
    FOR (x, y) if (x>0 && x<9 && y>0 && y<9) {
      a = p[p1 = y * 10 + x];
      p[p1] = p[p2 = x * 10 + y];
      p[p2] = a;
printf("%d, %d, ", p1, p2);
    }
printf("\n");
}
*/


void SfDrehen(SPFELD *psf)
{
  SfxSpiegeln(psf);
  SfTransponieren(psf);
}



#ifdef xxx

/* Spielfeld zufällig mit Anz Steinen besetzen */


void SfZuf2(SPFELD *psf, int Anz)
{
  int  i, Pos;


  if (Anz >= 64) Error("Anz zu groß");

  FOR (i, 64) psf->p[i] = LEER;

  FOR (i, Anz) {

    do { Pos = (IRAN >> 3) & 63; } while (psf->p[Pos]);

    if (IRAN & 0x80) psf->p[Pos] = BLACK; else psf->p[Pos] = WHITE;

  }
  psf->Marke = MA_WEISS_NICHT;
}


#endif



/* Steinanzahl von BLACK bestimmen */

int SfAnzBLACK(SPFELD *psf)
{
  int i, anz;

  
  anz = 0;

  FOR_SFPOS8(i) if (psf->p[Tab8to10[i]] == BLACK) anz++;

  return anz;  
}


/* Steinanzahl von WHITE bestimmen */

int SfAnzWHITE(SPFELD *psf)
{
  int i, anz;

  
  anz = 0;

  FOR_SFPOS8(i) if (psf->p[Tab8to10[i]] == WHITE) anz++;

  return anz;  
}




/* Steinanzahl bestimmen */

int SfAnz(SPFELD *psf)
{
  return SfAnzBLACK(psf) + SfAnzWHITE(psf);
}



/* Spielfeld packen */

void SfPack(SPFELD *psf, SFCODE *pc)
{
  int j;


  j = pc->Marke = psf->Marke;

  if (j != MA_VERLOREN && j != MA_GEWONNEN && 
      j != MA_REMIS    && j != MA_WEISS_NICHT &&
      (j < MA_WKEIT || j > MA_WKEIT+100) &&
      (j < MA_DIFF  || j > MA_DIFF+128) && 
      !ZUG(j-MA_ZUG)) {
printf("%d: ", j); Error("Fehler beim Packen: Marke?");
  }

  FOR (j, 8) pc->MapB[j] = pc->MapW[j] = 0;

  FOR_SFPOS8(j) {

    switch (psf->p[Tab8to10[j]]) {

      case BLACK: pc->MapB[j >> 3] |= 1 << (j & 7); break;
      case WHITE: pc->MapW[j >> 3] |= 1 << (j & 7); break;
    }
  }
}


/* Spielfeld entpacken */

void SfEntpack(SFCODE *pc, SPFELD *psf)
{
  int j;


  *psf = SfNull;

  j = psf->Marke = pc->Marke;

  if (j != MA_VERLOREN && j != MA_GEWONNEN && 
      j != MA_REMIS    && j != MA_WEISS_NICHT &&
      (j < MA_DIFF  || j > MA_DIFF+128) && 
      (j < MA_WKEIT || j > MA_WKEIT+100) &&
      !ZUG(j-MA_ZUG)) {
printf("SfEntpack: Marke=%d: ", j);
psf->Marke = MA_WEISS_NICHT;

 /* Error("Fehler beim Entpacken: Marke?"); */
  }


  FOR_SFPOS8(j) {

    if      (pc->MapB[j >> 3] & (1 << (j & 7))) psf->p[Tab8to10[j]] = BLACK;
    else if (pc->MapW[j >> 3] & (1 << (j & 7))) psf->p[Tab8to10[j]] = WHITE;
    else					psf->p[Tab8to10[j]] = LEER;
  }
}



/* Spielfelder ablegen		*/
/* return TRUE <=> Fehler	*/

BOOL fSfWrite(FILE *fp, SPFELD *sf, int anz)
{
  int    i;
  SFCODE sfpack;

  
  FOR (i, anz) {

    SfPack(&sf[i], &sfpack);
 
    if (fwrite((char*)&sfpack, sizeof(sfpack), (size_t)1, fp) < 1) return TRUE; 
  }

  return FALSE;
}



/* Spielfelder in Datei ablegen	*/
/* return TRUE <=> Fehler		*/

BOOL SfWrite(SPFELD *sf, int anz, char *name)
{
  int    r;
  FILE   *fp;

  
  fp = fopen(name, "wb");

  if (!fp) return TRUE;

  r = fSfWrite(fp, sf, anz);

  fclose(fp);
  return r;	
}



/* Spielfelder aus Datei holen	*/
/*   Anzahl der Felder zurück, 0 <=> Fehler	*/

int fSfRead(FILE *fp, SPFELD *sf, int anz)
{
  int    i;
  SFCODE sfpack;

  
  FOR (i, anz) {

    if (fread((char*)&sfpack, sizeof(sfpack), (size_t)1, fp) < 1) break; 

    SfEntpack(&sfpack, &sf[i]);
  }

  return i;
}



/* Spielfelder aud Datei holen			*/
/*   Anzahl der Felder zurück, 0 <=> Fehler	*/

int SfRead(SPFELD *sf, int anzmax, char *name)
{
  int    anz;
  FILE   *fp;

 
  fp = fopen(name, "rb");

  if (!fp) return 0;

  anz = fSfRead(fp, sf, anzmax);

  fclose(fp);

  return anz;	
}









#define OK(x)  (((x) >= 0) && ((x) < 8))


/* Stein setzen			 */
/*   return == 0  <=> geht nicht */

#define SETZ(d) \
  Pos1 = Pos + d;\
  if (p[Pos1] == f_gegn) {\
    while (p[Pos1] == f_gegn) Pos1 += d;\
    if (p[Pos1] == f_eigen) {\
      SetzOK = TRUE;\
      while (Pos1 != Pos) { p[Pos1] = f_eigen; Pos1 -= d; }\
    }\
  }

int SfSetzen(
  SPFELD *psf,		/* Zeiger auf Feld, auf dem gesetzt wird  */
  PARTEI Partei,	/* Partei am Zug			  */
  SFPOS	 Pos		/* zu setzende Position			  */
)
{
  int  f_eigen, f_gegn, Pos1;
  BOOL SetzOK;
  SFPOS *p = psf->p;

if (Partei != BLACK && Partei != WHITE) Error("SfSetzen Partei");
if (!ZUG(Pos)) Error("SfSetzen1");

  if (p[Pos] != LEER) return FALSE;

  f_eigen = Partei; 
  f_gegn  = GEGNER(Partei);

  SetzOK = FALSE; 

  SETZ(1); SETZ(-1); SETZ(10); SETZ(-10);
  SETZ(9); SETZ(-9); SETZ(11); SETZ(-11);
 
  if (SetzOK) p[Pos] = f_eigen;

  return SetzOK;
}



/* Stein versuchen zu setzen	 */
/*   return == 0  <=> geht nicht */

#define CHECK(d) \
  Pos1 = Pos + d;\
  if (p[Pos1] == f_gegn) {\
    while (p[Pos1] == f_gegn) Pos1 += d;\
    if (p[Pos1] == f_eigen) return TRUE;\
  }

int SfSetzCheck(
  SPFELD *psf,		/* Zeiger auf Feld, auf dem gesetzt wird  */
  PARTEI Partei,	/* Partei am Zug			  */
  SFPOS	 Pos		/* zu setzende Position			  */
)
{
  int   Pos1, f_eigen, f_gegn;
  SFPOS *p=psf->p;


  if (p[Pos] != LEER) return FALSE;

  f_eigen = Partei; 
  f_gegn  = GEGNER(Partei);

  
  CHECK(1); CHECK(-1); CHECK(10); CHECK(-10);
  CHECK(9); CHECK(-9); CHECK(11); CHECK(-11);

  return FALSE;
}



/* mögliche Züge ab Zuege ablegen und Anzahl zurück */

int SfMoeglZuege(SPFELD *psf, PARTEI Partei, SFPOS *Zuege)
{
  SFPOS i;
  int anz = 0;


  FOR_SFPOS10 (i)

    if (psf->p[i] == LEER) if (SfSetzCheck(psf, Partei, i)) {
      *Zuege++ = i; anz++;
    }

  return anz;
}



#define BUCHSTABEN "   A  B  C  D  E  F  G  H\n"



/* Spielfeld auf Datei */

void fSfAus(FILE *fp, SPFELD *psf, PARTEI Partei, int Moegl)
{
  int x, y, Pos;
  

  fprintf(fp, "\n"BUCHSTABEN);

  FOR (y, 8) {

    fprintf(fp, "%1d ", y+1);    

    FOR (x, 8) {

      Pos = (y << 3) + x;

      fprintf(fp, "|");

      if	(psf->p[Tab8to10[Pos]] == WHITE) fprintf(fp, WHITEMAN);
      else if	(psf->p[Tab8to10[Pos]] == BLACK) fprintf(fp, BLACKMAN);
      else if	(psf->p[Tab8to10[Pos]] == LEER && 
		 Moegl && SfSetzCheck(psf, Partei, (SFPOS)(Tab8to10[Pos]))) 
	fKoorAus(fp, (SFPOS)(Tab8to10[Pos]));
      else if   (psf->p[Tab8to10[Pos]] == LEER) fprintf(fp, "  ");
      else fprintf(fp, "??");

    }

    fprintf(fp, "| %1d\n", y+1);
  }
  fprintf(fp, BUCHSTABEN"\n");
}



/* Spielfeld ausgeben */

void SfAus(SPFELD *psf, PARTEI Partei, int Moegl)
{ fSfAus(stdout, psf, Partei, Moegl); }





/* Tabelle ausgeben */

void fTabAus(FILE *fp, SPFELD *psf)
{
  int x, y, Pos;
  

  if	  (psf->Marke == BLACK) fprintf(fp, "\n"BLACK_TO_MOVE);
  else if (psf->Marke == WHITE) fprintf(fp, "\n"WHITE_TO_MOVE);
  else 	  Error("Unbekannte Partei am Zug in fTabAus");


  fprintf(fp, "\n"BUCHSTABEN);

  FOR (y, 8) {

    fprintf(fp, "%1d ", y+1);    

    FOR (x, 8) {

      Pos = (y << 3) + x;

      fprintf(fp, "|");

      if (psf->p[Tab8to10[Pos]] >= NUM_DISP) 

	fprintf(fp, "%2d", psf->p[Tab8to10[Pos]] - NUM_DISP);

      else fSteinAus(fp, psf->p[Tab8to10[Pos]]);

    }

    fprintf(fp, "| %1d\n", y+1);

  }

  fprintf(fp, BUCHSTABEN"\n");

  { GAME game;
    SPFELD sf;

    if (Tab2Game(psf, &game)) PlayGame(game.MoveNum, &game, &sf);
    else                      sf = *psf;
  
    fprintf(fp, "##:() - %d:%d\n\n", SfAnzBLACK(&sf), SfAnzWHITE(&sf));
  }
}


#define READERR(x)	{ printf("*** %s\n", x); ok = FALSE; goto Ende; }
#define STRLEN		100

/* return TRUE <=> Fehler */

BOOL fTabEin(FILE *fp, SPFELD *psf)
{
  char s[STRLEN+1], t[STRLEN+1];
  BOOL ok = FALSE;
  int  i0, i, Pos, y, num;


  *psf = SfNull;


  while (!feof(fp)) {

    if (!fgets(s, STRLEN, fp)) break;

    if (!strcmp(s, BLACK_TO_MOVE)) { 
      psf->Marke = BLACK; ok = TRUE; break; 
    }
    if (!strcmp(s, WHITE_TO_MOVE)) { 
      psf->Marke = WHITE; ok = TRUE; break; 
    }
  }

  if (!ok) return TRUE;

  while (!feof(fp)) {

    if (fgets(s, STRLEN, fp) && !strcmp(s, BUCHSTABEN)) { ok = TRUE; break; }

  }


  if (!ok) READERR("Tabelle?");



  FOR (y, 8) {

    if (!fgets(s, STRLEN, fp)) READERR("Tabelle?");

    if (strlen(s) < 3*8+2) READERR("Zeile zu kurz");

    i0 = 2;

    FOR (i, 8) {

      Pos = y * 8 + i;

      if (s[i0+3*i] != '|') READERR("| fehlt");

      t[0] = s[i0+3*i+1]; t[1] = s[i0+3*i+2]; t[2] = 0;

/*printf("|%2s|   ", t);*/

      if	(!strcmp(t, "  "))	psf->p[Tab8to10[Pos]] = LEER;
      else if	(!strcmp(t, BLACKMAN))	psf->p[Tab8to10[Pos]] = BLACK;
      else if	(!strcmp(t, WHITEMAN))	psf->p[Tab8to10[Pos]] = WHITE;
      else if	(sscanf(t, "%2d", &num) == 1) 
					psf->p[Tab8to10[Pos]] = num + NUM_DISP; 
      else	READERR("unbekannter Eintrag");
    }  
/*printf("\n");*/
  }

  if (!fgets(s, STRLEN, fp) || strcmp(s, BUCHSTABEN)) READERR("Beschriftung?");

  ok = TRUE;

Ende:

  return !ok;
}



void TabAus(SPFELD *psf) { fTabAus(stdout, psf); }


void fSteinAus(FILE *fp, PARTEI Partei)
{
  switch (Partei) {

    case LEER:  fprintf(fp, "  "); break;
    case BLACK: fprintf(fp, BLACKMAN); break;
    case WHITE: fprintf(fp, WHITEMAN); break;
    
    default: printf("%d\n", Partei); Error("unbekannte Partei");
  }
}




#if 0

BOOL TabEindeutigAlt(SPFELD *psf)
{
  int    i, j, k, trans, sym[8], symanz, min;
  SPFELD sf, sftrans[8];
  SFPOS  Zuege[60], Zug, *p, *pt;
  PARTEI Partei;


  sf = *psf;

  FOR (i, 60) Zuege[i] = ZUG_UNBEKANNT;
  
  FOR_SFPOS10(i) {

    if (psf->p[i] >= NUM_DISP) { 
      Zuege[psf->p[i] - NUM_DISP - 1] = i;
      sf.p[i] = LEER;
    }
  }

  *psf = sf;

  trans = 0;

  Partei = psf->Marke;


  FOR (i, 60) {

    if ((Zug=Zuege[i]) == ZUG_UNBEKANNT) break;

    Zug = Trans[trans](Zug);

    Transform(&sf, sftrans);

    sym[0] = 0; symanz = 1;

/* alle Symmetrien feststellen */

    p = sf.p;

    for (j=1; j < 8; j++) {

      pt = sftrans[j].p;

      FOR_SFPOS10(k) if (p[k] != pt[k]) break;

      if (k >= 89) sym[symanz++] = j;
    }

    if (symanz > 1) {

/* minimalen Zug ermitteln */

      min = 1000;

      FOR (k, symanz) {

/*printf("->"); KoorAus(Trans[sym[k]](Zug)); */

        if (Trans[sym[k]](Zug) < min) {
	  min = Trans[sym[k]](Zug);
	  j = k;
	}  
      }



/* und Transformation anpassen: zuerst alte, dann neue Permutation */

      trans = TransMat[trans][sym[j]];
      Zug = min;
    } 

    psf->p[Zug] = i + NUM_DISP + 1;

/* KoorAus(Zug); printf(" %d \n", trans); */


    if (!SfSetzen(&sf, Partei, Zug)) {

      Partei = GEGNER(Partei);

      if (!SfSetzen(&sf, Partei, Zug)) {
printf("TabEindeutig: setzen???\n"); return FALSE;
      }
    }

    Partei = GEGNER(Partei);

  }

  return TRUE;      
}



/* ähnlicher Code in lernsub */

int SfMoeglZuegeEAlt(SPFELD *psf, PARTEI Partei, SFPOS *Zuege)
{
  int    i, j, k, sym[8], symanz, ZugAnz;
  SPFELD sftrans[8];
  SFPOS  *p, *pt;


  ZugAnz = SfMoeglZuege(psf, Partei, Zuege);

  if (ZugAnz <= 1) return ZugAnz;

  Transform(psf, sftrans);


/* alle Symmetrien feststellen */

  sym[0] = 0; symanz = 1;

  p = psf->p;

  for (j=1; j < 8; j++) {

    pt = sftrans[j].p;

    FOR_SFPOS10(k) if (p[k] != pt[k]) break;

    if (k >= 89) sym[symanz++] = j;
  }

  if (symanz < 2) return ZugAnz;	/* keine Symmetrie */

  FOR (i, ZugAnz) {

    for (j=i+1; j < ZugAnz; j++) {

      for (k=1; k < symanz; k++)
	if (Zuege[j] == Trans[sym[k]](Zuege[i])) break;
     
      if (k < symanz) {			/* symmetrischen Zug gefunden */

	for (k=j; k < ZugAnz-1; k++) Zuege[k] = Zuege[k+1];
	ZugAnz--;
	j--;		/* j nochmal */
      }
    }
  }

  return ZugAnz;
}



#endif 




BOOL TabEindeutig(SPFELD *psf)
{
  int    i, j, k, trans, trmax, sym[8], symanz, min;
  SPFELD sf, sftrans[8];
  SFPOS  Zuege[60], Zug, *p, *pt;
  PARTEI Partei;


  sf = *psf;

  FOR (i, 60) Zuege[i] = ZUG_UNBEKANNT;
  
  FOR_SFPOS10(i) {

    if (psf->p[i] >= NUM_DISP) { 
      Zuege[psf->p[i] - NUM_DISP - 1] = i;
      sf.p[i] = LEER;
    }
  }

  *psf = sf;

  trans = 0;

  Partei = psf->Marke;


  FOR (i, 60) {

    if ((Zug=Zuege[i]) == ZUG_UNBEKANNT) break;

    Zug = Trans[trans](Zug);

    Transform(&sf, sftrans);


    sym[0] = 0; symanz = 1;

/* alle Symmetrien feststellen */

    p = sf.p;

    for (j=1; j < 8; j++) {

      pt = sftrans[j].p;

      FOR_SFPOS10(k) if (p[k] != pt[k]) break;

      if (k >= 89) sym[symanz++] = j;
    }

    if (symanz > 1) {

/* find minimal move in maximum board => move unique */

      trmax = SfMax(&sf);

#define X123 0

#if X123

if (SfAnz(&sf) == 12) {

  SfAus(&sf, 0, 0);

  printf("SfMax:\n");

  SfAus(&sftrans[trmax], 0, 0);

  { int l; FOR (l, 60) { KoorAus(Zuege[l]); printf(" "); }
  printf("\n"); }

}
#endif

 
      min = 1000;

      FOR (k, symanz) {

/*printf("->"); KoorAus(Trans[sym[k]](Zug)); */

        if (Trans[TransMat[sym[k]][trmax]](Zug) < min) {
	  min = Trans[TransMat[sym[k]][trmax]](Zug);
	  j = k;
	}  
      }



/* und Transformation anpassen: zuerst alte, dann neue Permutation */

      trans = TransMat[trans][sym[j]];
      Zug = Trans[sym[j]](Zug);

#if X123
if (SfAnz(&sf) == 8) { KoorAus(Zuege[i]); KoorAus(Zug); printf("\n"); }
#endif



    } 


    psf->p[Zug] = i + NUM_DISP + 1;

/* KoorAus(Zug); printf(" %d \n", trans); */


    if (!SfSetzen(&sf, Partei, Zug)) {

      Partei = GEGNER(Partei);

      if (!SfSetzen(&sf, Partei, Zug)) {
printf("TabEindeutig: setzen???\n"); return FALSE;
      }
    }

    Partei = GEGNER(Partei);

  }

  return TRUE;    
}




/* ähnlicher Code in lernsub */

int SfMoeglZuegeE(SPFELD *psf, PARTEI Partei, SFPOS *Zuege)
{
  int    i, j, k, sym[8], symanz, ZugAnz, trmax;
  SPFELD sftrans[8];
  SFPOS  *p, *pt;


  ZugAnz = SfMoeglZuege(psf, Partei, Zuege);

  if (ZugAnz <= 1) return ZugAnz;

  Transform(psf, sftrans);


/* alle Symmetrien feststellen */

  sym[0] = 0; symanz = 1;

  p = psf->p;

  for (j=1; j < 8; j++) {

    pt = sftrans[j].p;

    FOR_SFPOS10(k) if (p[k] != pt[k]) break;

    if (k >= 89) sym[symanz++] = j;
  }

  if (symanz < 2) return ZugAnz;	/* keine Symmetrie */


/* find unique moves */

  trmax = SfMax(psf);

  FOR (i, ZugAnz) {

    for (j=i+1; j < ZugAnz; j++) {

      for (k=1; k < symanz; k++)
	if (Zuege[j] == Trans[sym[k]](Zuege[i])) break;
     
      if (k < symanz) {			/* symmetrischen Zug gefunden */

/* choose minimal move in maximal position */

        if (Trans[trmax](Zuege[j]) < Trans[trmax](Zuege[i])) 
          Zuege[i] = Zuege[j];

	for (k=j; k < ZugAnz-1; k++) Zuege[k] = Zuege[k+1];
	ZugAnz--;
	j--;		/* j again */
      }
    }
  }

  return ZugAnz;
}
	  



void SteinAus(PARTEI Partei) { fSteinAus(stdout, Partei); }


BOOL SfGleich(SPFELD *psf1, SPFELD *psf2)
{
  int i;

  FOR (i, 100) 
    if (psf1->p[i] != psf2->p[i]) return FALSE;

  return TRUE;
}







/* maximales Spielfeld finden, Transformationsnummer zurück */

int SfMax(SPFELD *psf)
{
  int   max=0, j, i, a;
  int   *trj, *trmax, *sch;
  SBYTE *p=psf->p;


  trmax = TransTab[max];

  for (j=1; j < 8; j++) {

    trj   = TransTab[j];
    sch   = Schichten;

    FOR (i, 64) {
      a = *sch++;
      a = p[trj[a]] - p[trmax[a]];
      if (a > 0) { max = j; trmax = TransTab[max]; break; }
      if (a < 0) break;
    }
/*
    printf("%d ", i); fflush(stdout);
*/
  }

  return TransInv[max];		/* Achtung!!! */
}
