/* transformation of game representations, 4,7.93 */

#ifndef PRECOMP
#include "main.h"
#endif


#include "crt.h" 
#include "sboard.h"
#include "game.h"
#include "goodies.h"

void _abort(void) { exit(1); }


int main(int argc, char **argv)
{
  char	    name[200];
  SPFELD    sf;
  FILE	    *fpin, *fpout;
  GAME      Game;
  int       i, firstnum;


  if (argc < 3) {

Fehler:
Error("call: otrans option file\n\
            options are:  okoosp ospoko\n\
                          okogam gamoko\n\
                          ospsfk\n\
                          ospuniq gamuniq\n\
			  osphalb sfkmittel\n\
                          iosgames iosresign\n\
                          'cutoko num_moves'\n\
                          testoko newoko firstnum\n");
  }


  fpin = fopen(argv[argc-1], "r");
  if (!fpin) Error("file not found");


  if (sscanf(argv[1], "%d", &firstnum) == 1) {

    sprintf(name, "%s.osp", argv[2]);
    printf("%s -> %s\n\n", argv[2], name);

    fpout = fopen(name, "w");
    if (!fpout) Error("write error");

    i = 0;

    FOREVER {

      if (fTabEin(fpin, &sf)) break;

      i++;

      if (i >= firstnum) fTabAus(fpout, &sf);
 
    }  

    fclose(fpin);
    fclose(fpout);


  } else if (!strcmp(argv[1], "okogam")) {

    sprintf(name, "%s.gam", argv[2]);
    printf("%s -> %s\n\n", argv[2], name);

    fpout = fopen(name, "w");
    if (!fpout) Error("write error");


    FOREVER {

      if (!fReadPackedGame(fpin, &Game)) break;
      if (!fWriteGame(fpout, &Game)) Error("write error");
 
    }  

    fclose(fpin);
    fclose(fpout);


  } else if (!strcmp(argv[1], "gamoko")) {

    sprintf(name, "%s.oko", argv[2]);
    printf("%s -> %s\n\n", argv[2], name);

    fpout = fopen(name, "w");
    if (!fpout) Error("write error");

    FOREVER {

      if (!fReadGame(fpin, &Game)) break;
      if (!fWritePackedGame(fpout, &Game)) Error("write error");
    }

    fclose(fpin);
    fclose(fpout);


  } else if (!strcmp(argv[1], "okoosp")) {

    sprintf(name, "%s.osp", argv[2]);
    printf("%s -> %s\n\n", argv[2], name);

    fpout = fopen(name, "w");
    if (!fpout) Error("write error");


    FOREVER {

      if (!fReadPackedGame(fpin, &Game)) break;

      Game2Tab(&Game, &sf);

      fTabAus(fpout, &sf);

    }  

    fclose(fpin);
    fclose(fpout);


  } else if (!strcmp(argv[1], "iosgames")) {

    int gamenum=0;


    sprintf(name, "%s.games", argv[2]);
    printf("%s -> %s\n\n", argv[2], name);

    fpout = fopen(name, "w");
    if (!fpout) Error("write error");


    FOREVER {

      int  i, d, m, player;
      GAME game;
      char s[400];
      char time[400], playerB[400], playerW[400], numB[400], numW[400],
	   timeB[400], timeW[400], incB[400], incW[400], defB[400], defW[400],
           flag[400], moves[400], end[400], *p;

      if (!fgets(s, 399, fpin)) break;

      if ((d=sscanf(s, "%s %s %s %s ( %s %s %s %s %s ( %s %s %s %s %s", 
		 time, flag, playerB, numB, timeB, incB, defB, 
		 playerW, numW, timeW, incW, defW,
		 moves, end
		)) == 14         &&
	  !strcmp(flag, "e")    && 
	  atoi(timeB) >= 10) {


        p = moves;

	for (i=0;; i++) {

	  if      (*p == '+') player = BLACK; 
	  else if (*p == '-') player = WHITE;
	  else break;

	  p++;

	  m = (p[0] - '0')*10 + (p[1] - '0');

	  p += 2;
 
	  game.Moves[i] = SMOVE_GEN(m, player);

	}

	game.MoveNum = i;

	if (!PlayGame(i, &game, &sf)) {

	  game.DiscDiffBW = SfAnzBLACK(&sf) - SfAnzWHITE(&sf);

	  fprintf(fpout, "%s %s %s %s ", time, playerB, playerW, timeB);
	  fWriteGame(fpout, &game);
  
        }
      }

printf("%d\n", d);

    }  


    fclose(fpin);
    fclose(fpout);

 } else if (!strcmp(argv[1], "iosresign")) {

    int gamenum=0;


    sprintf(name, "%s.games", argv[2]);
    printf("%s -> %s\n\n", argv[2], name);

    fpout = fopen(name, "w");
    if (!fpout) Error("write error");


    FOREVER {

      int  i, d, m, player;
      GAME game;
      char s[400];
      char time[400], playerB[400], playerW[400], numB[400], numW[400],
	   min[400], flag[400], moves[400], end[400], *p;

      if (!fgets(s, 399, fpin)) break;

      if (sscanf(s, "%s %s %s %s %s %s %s %s %s", 
	time, playerB, playerW, numB, numW, flag, min, moves, end) == 9 &&
	!strcmp(flag, "r")) {


        p = moves;

	for (i=0;; i++) {

	  if      (*p == '+') player = BLACK; 
	  else if (*p == '-') player = WHITE;
	  else break;

	  p++;

	  m = (p[0] - '0')*10 + (p[1] - '0');

	  p += 2;
 
	  game.Moves[i] = SMOVE_GEN(m, player);

	}

	game.MoveNum = i;
	game.DiscDiffBW = 0;

	fprintf(fpout, "%s %s %s %s ", time, playerB, playerW, min);
	fWriteGame(fpout, &game);

      }
    }  

    fclose(fpin);
    fclose(fpout);


  } else if (!strcmp(argv[1], "sfkmittel")) {

    int anz=0;
    float sudiff=0;


    sprintf(name, "%s.mit", argv[2]);
    printf("%s -> %s\n\n", argv[2], name);

    fpout = fopen(name, "w");
    if (!fpout) Error("write error");


    FOREVER {

      if (!fSfRead(fpin, &sf, 1)) break;

      if (sf.Marke >= MA_DIFF && sf.Marke <= MA_DIFF+128) 

        sudiff += sf.Marke - MA_DIFF - 64;

      else

        Error("value not a difference!");

      anz++;

    }  

    fclose(fpin);

    if (!anz) Error("no board!");

printf("E=%.2f\n", sudiff/anz);

    fpin = fopen(argv[2], "r");
    if (!fpin) Error("file not found");

    FOREVER {

      if (!fSfRead(fpin, &sf, 1)) break;

/*printf("%d\n", sf.Marke-MA_DIFF-64);*/

      if      (sf.Marke-MA_DIFF-64 > sudiff/anz) sf.Marke = MA_WKEIT + 99;
      else if (sf.Marke-MA_DIFF-64 < sudiff/anz) sf.Marke = MA_WKEIT + 1;
      else 			                 sf.Marke = MA_WKEIT + 50;

      fSfWrite(fpout, &sf, 1);
    }  

    fclose(fpout);


  } else if (!strcmp(argv[1], "ospoko")) {

    int n=1;
    SFPOS moves[65];

    sprintf(name, "%s.oko", argv[2]);
    printf("%s -> %s\n\n", argv[2], name);

    fpout = fopen(name, "w");
    if (!fpout) Error("write error");

    FOREVER {

      if (fTabEin(fpin, &sf)) break;
      if (Tab2Game(&sf, &Game)) fWritePackedGame(fpout, &Game);

#if 0
      { SPFELD sf;

	if ((n % 100) == 0) { printf("%6d\r", n); fflush(stdout); }

        if (PlayGame(Game.MoveNum, &Game, &sf)) 
          printf("*** game %d corrupt\n", n);

        if (SfMoeglZuege(&sf, BLACK, moves) || SfMoeglZuege(&sf, WHITE, moves))
	  printf("*** game %d not finished\n", n);

      }

#endif

      n++;

    }
    fclose(fpin);
    fclose(fpout);


  } else if (!strcmp(argv[1], "ospsfk")) {

    int n=1, nr;
    SFPOS moves[65];
    SPIELINFO Info[65];


    sprintf(name, "%s.sfk", argv[2]);
    printf("%s -> %s\n\n", argv[2], name);

    fpout = fopen(name, "w");
    if (!fpout) Error("write error");

    FOREVER {

      if (fTabEin(fpin, &sf)) break;
      if ((nr=TabToInfo(&sf, Info)) >= 1) {

        if (Info[nr].AmZug == WHITE) SfInvert(&Info[nr].Sf);

        Info[nr].Sf.Marke = MA_GEWONNEN;
        fSfWrite(fpout, &Info[nr].Sf, 1);
      }
    }

    fclose(fpin);
    fclose(fpout);

  } else if (!strcmp(argv[1], "ospuniq")) {

    sprintf(name, "%s.uniq", argv[2]);
    printf("%s -> %s\n\n", argv[2], name);

    fpout = fopen(name, "w");
    if (!fpout) Error("write error");


    for (i=0;; i++) {

if (!(i % 100)) printf("%d\n", i);

      if (fTabEin(fpin, &sf)) break;

      if (TabEindeutig(&sf)) fTabAus(fpout, &sf);

    }  

    fclose(fpin);
    fclose(fpout);


  } else if (!strcmp(argv[1], "gamuniq")) {

    sprintf(name, "%s.uniq", argv[2]);
    printf("%s -> %s\n\n", argv[2], name);

    fpout = fopen(name, "w");
    if (!fpout) Error("write error");


    for (i=0;; i++) {

      int k;

if (!(i % 100)) { printf("%6d\r", i); fflush(stdout); }

      if (!fReadGame(fpin, &Game)) break;

      k = Game.DiscDiffBW;

      UniqueGame(&Game);

      Game.DiscDiffBW = k;

      fWriteGame(fpout, &Game);
    }  

    fclose(fpin);
    fclose(fpout);


  } else if (!strcmp(argv[1], "osphalb")) {

    int anz=0, halb;
    FILE *fpout1, *fpout2;


    FOREVER {

      if (fTabEin(fpin, &sf)) break;

      anz++;
    }  

    sprintf(name, "%s.halb1", argv[2]);
    printf("%s -> %s\n", argv[2], name);

    fpout1 = fopen(name, "w");
    if (!fpout1) Error("write error");

    sprintf(name, "%s.halb2", argv[2]);
    printf("%s -> %s\n", argv[2], name);

    fpout2 = fopen(name, "w");
    if (!fpout2) Error("write error");


    halb = anz/2;
    anz = 0;

    fclose(fpin);
    fpin = fopen(argv[2], "r");
    if (!fpin) Error("file not found");

    FOREVER {

      if (fTabEin(fpin, &sf)) break;

      if (anz <= halb) fTabAus(fpout1, &sf); else fTabAus(fpout2, &sf);

      anz++;
    }  

    fclose(fpin);
    fclose(fpout1);
    fclose(fpout2);

  } else if (!strcmp(argv[1], "cutoko")) {

    // cut games

    if (argc != 4) Error("cut?");

    int num_moves = atoi(argv[2]);

    if (num_moves < 1 || num_moves > 60) Error("num_moves?");

    sprintf(name, "%s.cut", argv[3]);
    printf("%s -> %s\n\n", argv[3], name);

    fpout = fopen(name, "w");
    if (!fpout) Error("write error");
    
    FOREVER {

      int r;

      if (!fReadPackedGame(fpin, &Game)) break;

      if (Game.MoveNum > num_moves) {

        Game.MoveNum = num_moves;
        Game.Moves[num_moves] = 0;
	Game.DiscDiffBW = 0;
      }

      fWritePackedGame(fpout, &Game);

    }

    fclose(fpin);
    fclose(fpout);

  } else if (!strcmp(argv[1], "testoko")) {

    int n=1;
    SFPOS moves[65];

    sprintf(name, "%s.ok", argv[2]);
    printf("%s -> %s\n\n", argv[2], name);

    fpout = fopen(name, "w");
    if (!fpout) Error("write error");

    FOREVER {

      int r;

      if (!fReadPackedGame(fpin, &Game)) break;

      r = Game.DiscDiffBW;

      Game2Tab(&Game, &sf);

      if (Tab2Game(&sf, &Game)) { 

#if 0

/* test for suspect eval paths (discdiff = eval) */

if (n % 1000 == 0) printf("%d\n", n);

        { int p = PlayGame(Game.MoveNum, &Game, &sf);

        Game.DiscDiffBW = r;

        if (SfAnzBLACK(&sf) - SfAnzWHITE(&sf) == r) {

#if 0
SfAus(&sf, BLACK, 0);
printf(":: %d %d\n", SfAnzBLACK(&sf) - SfAnzWHITE(&sf), r);
#endif
/*printf("-");*/

	} else {


         fWritePackedGame(fpout, &Game);


        /*printf("*")*/;
	}
      }

#else

        if (PlayGame(Game.MoveNum, &Game, &sf)) {
          printf("*** game %d corrupt\n", n); 
          fWriteGame(stdout, &Game);
          goto next;
        }

        if (SfMoeglZuege(&sf, BLACK, moves) || SfMoeglZuege(&sf, WHITE, moves)) {
	  printf("*** game %d not finished\n", n); goto next;
	}
        Game.DiscDiffBW = r;
        fWritePackedGame(fpout, &Game);
#endif



      }
next:
      n++;
    }
    fclose(fpin);
    fclose(fpout);

  } else if (!strcmp(argv[1], "newoko")) {

    int n=1;
    SFPOS moves[65];

    sprintf(name, "%s.oko", argv[2]);
    printf("%s -> %s\n\n", argv[2], name);

    fpout = fopen(name, "w");
    if (!fpout) Error("write error");

    FOREVER {

      if (!fReadPackedGameOld(fpin, &Game)) break;

      fWritePackedGame(fpout, &Game);

    }
    fclose(fpin);
    fclose(fpout);

  } else goto Fehler;

  return 0;
}

