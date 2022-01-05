/* allgemeine Routinen */

#ifndef PRECOMP
#include "main.h"
#endif

#include "goodies.h"
#include "crt.h"


#include <sys/time.h>
/* #include <sys/timeb.h> */
#include <sys/resource.h>



/* Multiplikativer Kongruenzgenerator mit Periodenlänge MOD/2 */

/* >> 3 für mod-Operation */

#define MOD (1UL<<30)
#define A   8893UL	/* = 5 (8)! */

/* Startwert relativ prim zu MOD, reicht: 3,5(8) */

static ULONG RandRectSeed = 5; 



/* Startwert laden */

void sMyRand(ULONG x)
{
  RandRectSeed = (x & ~7UL) + 5;
}


/* Zufallswert bestimmen */

ULONG MyRand(void)
{
  RandRectSeed = (RandRectSeed * A) & (MOD-1);   

  return RandRectSeed >> 3;
}


BOOL UseCpuTime=FALSE;

void Zeit(ZEIT *pZ)
{
  if (UseCpuTime) CPUZeit(pZ); else RealeZeit(pZ);
}



/* Wanduhr: Sekunden... seit ... zurueck */

void RealeZeit(ZEIT *pZ)
{
#ifdef UNIX

#if 0
   struct timeb TimeB;
   int	  ftime(struct timeb *);


   if (ftime(&TimeB) == -1) Error("ftime");

   pZ->sek      = TimeB.time;
   pZ->millisek = TimeB.millitm;

#else

   struct timeval tv;
   struct timezone tz;

   gettimeofday(&tv, &tz);

   pZ->sek = tv.tv_sec;
   pZ->millisek = tv.tv_usec/1000;

#endif

#else

   clock_t z;


   z = clock();

   pZ->sek      = z / CLOCKS_PER_SEC;
   pZ->millisek = ((z % CLOCKS_PER_SEC) * 1000) / CLOCKS_PER_SEC;
#endif
} 




void CPUZeit(ZEIT *pZ)
{
#ifdef UNIX


   struct rusage ru; 

   if (getrusage(RUSAGE_SELF, &ru) == -1 ) Error("getrusage");
   pZ->sek = ru.ru_utime.tv_sec;
   pZ->millisek = ru.ru_utime.tv_usec / 1000;


/*
   struct tms buffer;

   times(&buffer);

   pZ->sek      =  buffer.tms_utime / 60;
   pZ->millisek = ((buffer.tms_utime % 60) * 1000) / 60;
*/

#else

   clock_t z;


   z = clock();

   pZ->sek      = z / CLOCKS_PER_SEC;
   pZ->millisek = ((z % CLOCKS_PER_SEC) * 1000) / CLOCKS_PER_SEC;
#endif
} 




/* Zeitdifferenz in Sekunden zurück */

REAL ZeitDiff(ZEIT *pZ1, ZEIT *pZ2)
{
  return (REAL) ((long)pZ1->sek - (long)pZ2->sek) + 
	 (REAL) ((long)pZ1->millisek - (long)pZ2->millisek) / 1000.0;
}



void ZeitAdd(ZEIT *pZ, REAL Sekunden)
{
  ULONG r, s;


  if (Sekunden < 0.0) Error("negative Dauer");
  
  r = (int) Sekunden;
  s = (int) (Sekunden*1000 - r*1000);

  pZ->sek += r;
  pZ->millisek += s;

  if (pZ->millisek >= 1000) { pZ->millisek -= 1000; pZ->sek++; }
}



/* n * 0.1 Sekunden "beschäftigt warten" */

void BusyWait(int n)
{
  int  i;
  ZEIT Start, Ende;

  
  if (n <= 0) return;


  Zeit(&Start);

  FOREVER {

    FOR (i, 100);

    Zeit(&Ende);

    if (ZeitDiff(&Ende, &Start) >= n * 0.1) return;
  }
}







/* Integer von s einlesen, snew zeigt dahinter, TRUE <=> Zahl da */

BOOL ParseNumber(char *s, int *pn, char **psnew)
{
  int r;


  *psnew = s;

  r = sscanf(s, "%d", pn);

  if (r != 1) return FALSE;

  while (*s == ' ' || *s == '\t') s++;
  while (*s == '-' || (*s >= '0' && *s <= '9')) s++;

  *psnew = s;

  return TRUE;
}



void TabToSf(SPFELD *psf1, SPFELD *psf2)
{
  int    i;
  

  *psf2 = *psf1;

  FOR_SFPOS10 (i) 
    if (psf2->p[i] != BLACK && psf2->p[i] != WHITE) psf2->p[i] = LEER;

}



int TabToInfo(SPFELD *psf, SPIELINFO *Spiel)
{
  int	 i, nr, SteinAnz;
  PARTEI Partei;
  SPFELD sf0, sf;
  SFPOS	 Zuege[60], *p;


  nr = 1;

  Spiel[nr].AmZug = Partei = psf->Marke;

  if (Partei != BLACK && Partei != WHITE) Error("Partei? TabToInfo");

  TabToSf(psf, &sf);
  Spiel[nr].Sf = sf;

  Spiel[0].Zug = ZUG_UNBEKANNT;

  FOR (i, 60) Zuege[i] = ZUG_UNBEKANNT;

  p = psf->p;

  FOR (i, 100) 
    if (p[i] >= NUM_DISP) Zuege[p[i] - NUM_DISP -1] = i;

  SteinAnz = SfAnz(&sf);

  for (i=0;;) {

    if (SteinAnz == 64) return nr;	/* Spielfeld voll */

    if (Zuege[i] == ZUG_UNBEKANNT) return nr;

    if (!SfSetzen(&sf, Partei, Zuege[i])) {

      sf0 = sf;

      if (!SfSetzen(&sf, GEGNER(Partei), Zuege[i])) {
	printf("*** Tabelle korrupt\n");
KoorAus(Zuege[i]); printf(" %d %d\n", i, Partei);
SfAus(&sf, BLACK, 0);
fTabAus(stdout, psf);

        return TAB_KORRUPT;
      }

      sf = sf0;

      Spiel[nr].Zug = ZUG_PASSEN;


    } else {

      Spiel[nr].Zug = Zuege[i];
      SteinAnz++;
      i++;
    }

    Partei = GEGNER(Partei);

    nr++;

    Spiel[nr].AmZug = Partei;
    Spiel[nr].Sf    = sf;

    if (Spiel[nr-1].Zug == ZUG_PASSEN && Spiel[nr-2].Zug == ZUG_PASSEN) {
      return nr;
    }
  }
}



void InfoToTab(SPIELINFO *Spiel, int MaxNr, SPFELD *psf)
{
  int nr = 1, i;


  *psf = Spiel[nr].Sf;

  for (i=1; i < MaxNr; i++) {

    if (ZUG(Spiel[i].Zug)) psf->p[Spiel[i].Zug] = (nr++) + NUM_DISP;
    if (nr > 60) break;

  }

  psf->Marke = Spiel[1].AmZug;
}


    

#define LOADERR(x)	{ printf("*** %s\n", x); goto Ende; }

BOOL SaveGame(char *name, SPIELINFO *Spiel, int MaxNr)
{
  int	    i, Zeilen;
  FILE      *fp;
  SPFELD    sf;


  if (!(fp=fopen(name, "w"))) return FALSE;

  fSfAus(fp, &Spiel[1].Sf, BLACK, 0);

  InfoToTab(Spiel, MaxNr, &sf);

  fTabAus(fp, &sf);

  Zeilen = MaxNr/2;

  for (i=1; i < MaxNr; i += 2) {

    fprintf(fp, "%2d:   ", i); fKoorAus(fp, Spiel[i].Zug); 

    if (i + 1 < MaxNr) {
      fprintf(fp, "        %2d:   ", i+1); 
      fKoorAus(fp, Spiel[i+1].Zug);
    } 
    fprintf(fp, "\n");
  }

  fprintf(fp, "\n\n");

  fSfAus(fp, &Spiel[MaxNr].Sf, BLACK, 0);

  fprintf(fp, BLACKMAN":%d - "WHITEMAN":%d\n", 
    SfAnzBLACK(&Spiel[MaxNr].Sf), SfAnzWHITE(&Spiel[MaxNr].Sf));

  if (ferror(fp)) return FALSE;

  return !fclose(fp);
}



#define STRLEN	100

int LoadGame(char *name, SPIELINFO *Spiel)
{
  int    MaxNr = LADE_FEHLER;
  FILE   *fp;
  SPFELD sf;


 
  if (!(fp=fopen(name, "r"))) LOADERR("Datei?")

  if (fTabEin(fp, &sf)) LOADERR("Tabelle?");

  MaxNr = TabToInfo(&sf, Spiel);

/*printf("%d \n", MaxNr);*/
Ende:

  fclose(fp);

  return MaxNr;
}



int LoadNextGame(FILE *fp, SPIELINFO *Spiel)
{
  int    MaxNr = LADE_FEHLER;
  SPFELD sf;


  if (fTabEin(fp, &sf)) goto Ende;

  MaxNr = TabToInfo(&sf, Spiel);

Ende:

  return MaxNr;
}



int round(REAL w) 
{ 
  int r;

  r = (int)w;

  if      (w-r >=  0.5) r++;
  else if (w-r <= -0.5) r--;

  return r;
}

int sgn(int a) 
{
  if      (a > 0) return  1;
  else if (a < 0) return -1;
  else            return  0;
}
