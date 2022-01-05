#ifndef O_AKOM
#define O_AKOM

#include "sboard.h"
#include "game.h"


#define NACHRICHT_MAX	500
#define DATEINAME_MAX	100


#define SIGNAL_ANZ	6


#define	SIG_EXIT	0
#define	SIG_BREAK	1
#define SIG_BOARD	2	/* ' ' Partei ' ' Sekunden ' ' LetzterZug ' ' */
				/* SF(64) */
#define SIG_MOVE	3	/* ' ' Zug */

#define SIG_GAME	4	/* [ ('+'|'-') Pos ]+ Steindifferenz */

#define SIG_CLEAR	5	/* clear hashtab */

void	Send		(char *kanal, char *s);
BOOL	SyncSend	(char *kanal, char *s);

BOOL	SyncSendEXIT	(char *kanal);
BOOL	SyncSendCLEAR	(char *kanal);
BOOL	SyncSendBREAK	(char *kanal);
BOOL	SyncSendBOARD	(char *kanal, 
			 PARTEI Partei, int Sek, SFPOS LetzterZug, SPFELD *psf);
BOOL	SyncSendGAME	(char *channel, int player, int time, GAME *pGame, BOOL to_move);
void	SendMOVE  	(char *kanal, SFPOS zug, int MoveTime);

BOOL	Empf		(char *kanal, char *s);
BOOL	SyncEmpf	(char *kanal, char *s, int MaxZeit);

void	Sync		(char *kanal);

void	KillChannel	(char *Kanal);

extern	int	KommAus;

#endif
