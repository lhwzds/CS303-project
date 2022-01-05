#define BEGINNER     BLACK

#include "main.h"
#include "sys.h"
#include "sboard.h"
#include "playgm.h"
#include "int.h"
#include "filecom.h"


int	VERB = 1;		/* Ausgabe bei Zugermittlung */

extern	int Enable_Abort;


char	TO_1[100],   TO_2[100];
char	FROM_1[100], FROM_2[100];

BOOL f_old=FALSE;
BOOL f_pipes=FALSE;

PROPINFO defpropinfo = {
  2, 10,			/* Zeiten		*/
  SP_COMP1, SP_MENSCH,		/* SpielerB, SpielerW	*/

  BLACK_AM_ZUG,			/* Am Zug bei Eingabe	*/
  SETZE_BLACK,
  TRUE,				/* MoeglAnzeig		*/
  FALSE				/* Beep			*/
};


PROPINFO propinfo;

#ifdef xxx

SPFELD st = {

1, 1, 1, 1, 1, 1, 1, 1,
1, 1, 2, 1, 2, 1, 0, 0,
1, 2, 1, 2, 1, 2, 0, 0,
1, 1, 2, 1, 0, 0, 0, 0,
1, 0, 0, 0, 0, 0, 0, 0,
0, 0, 0, 0, 0, 0, 0, 0,
0, 0, 0, 0, 0, 0, 0, 0,
0, 0, 0, 0, 0, 0, 0, 0

};

SPFELD st1 = {

0,0,0,0,0,0,0,0,
0,0,0,2,0,0,0,0,
0,2,2,2,2,2,2,0,
0,0,0,2,1,2,0,0,
0,0,0,2,1,1,2,0,
0,0,0,0,1,1,0,0,
0,0,0,0,0,0,0,0,
0,0,0,0,0,0,0,0
};

#define B BLACK
#define W WHITE

SPFELD Sf2 = {

B,0,B,0,B,W,0,W,
0,B,B,B,B,B,0,W,
W,W,B,B,B,W,B,W,
W,W,W,B,B,B,W,W,
W,B,W,W,B,B,W,W,
W,B,W,B,B,W,B,W,
W,B,B,W,B,B,W,W,
W,B,W,W,W,W,W,W
};


SPFELD Sf3 = {
B,B,W,B,B,B,B,W,
B,B,W,B,B,B,W,W,
B,W,B,B,W,B,W,W,
W,W,W,B,B,0,0,W,
W,B,W,0,B,W,0,W,
W,W,W,B,B,B,B,B,
0,0,0,B,B,0,W,W,
B,0,B,B,0,B,B,W
};


#endif



void _abort(void)
{
#ifdef AMIGA
  Enable_Abort = 0;
#endif

  FreeInter();

  if (!f_pipes) {

    // kill player

    if (!SyncSendEXIT(TO_1)) { SLEEP(10); SyncSendEXIT(TO_1); }
    if (!SyncSendEXIT(TO_2)) { SLEEP(10); SyncSendEXIT(TO_2); }

    SLEEP(10);

    KillChannel(TO_1);   KillChannel(TO_2);
    KillChannel(FROM_1); KillChannel(FROM_2);
  }

  exit(1);
}



int main(int argc, char **argv)
{
  int argi; 

  propinfo = defpropinfo;

  XDefProps(&propinfo);

  InitInter(&argc, argv, &propinfo);

  if (argc < 3 || argc > 5) {

error:
    Error("call: ox com1 com2 [-old] [-pipes]\n");
  }

  if (strlen(argv[1]) + strlen(TO_PRAEFIX)   > 90 ||
      strlen(argv[2]) + strlen(TO_PRAEFIX)   > 90 ||
      strlen(argv[1]) + strlen(FROM_PRAEFIX) > 90 ||
      strlen(argv[2]) + strlen(FROM_PRAEFIX) > 90)
    Error("Id too long");

  for (argi=3; argi < argc; argi++) {

    if (!strcmp(argv[argi], "-old")) { f_old = TRUE; }
    else if (!strcmp(argv[argi], "-pipes")) { f_pipes = TRUE; }
    else goto error;
  }

  sprintf(TO_1, "%s"TO_PRAEFIX, argv[1]);
  sprintf(FROM_1, "%s"FROM_PRAEFIX, argv[1]);

  sprintf(TO_2, "%s"TO_PRAEFIX, argv[2]);
  sprintf(FROM_2, "%s"FROM_PRAEFIX, argv[2]);

  Loop();

  _abort();
  return 0;
}
