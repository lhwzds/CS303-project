#ifndef GAME_H
#define GAME_H

typedef SBYTE SMOVE;

/* packed representation:  P F M 
 *                        Player: 0=BLACK
 *                          Flag: 1=TRUE
 *                            Move: 1..60	(without center squares)
 */


#define SMOVE_BIT_PLAYER	0x80
#define SMOVE_BIT_FLAG 		0x40

#define SMOVE_PLAYER(b)	(((b) & SMOVE_BIT_PLAYER) ? WHITE : BLACK)
#define SMOVE_MOVE(b)	\
	Code2Move[((b) & 0xff & ~(SMOVE_BIT_PLAYER | SMOVE_BIT_FLAG))]
#define SMOVE_FLAG(b)   (((b) & SMOVE_BIT_FLAG) != 0)


#define SMOVE_GEN(m,p)	(Move2Code[m] | (p == WHITE ? SMOVE_BIT_PLAYER : 0))


/* flags */

#define GAME_BLACK	1
#define GAME_WHITE	2
#define GAME_ALT	4


typedef struct {

  UBYTE MoveNum;
  SBYTE DiscDiffBW;
  SMOVE	Moves[61];	/* endmarker 0    */
  UBYTE Flags;		

} GAME;



extern int 	Code2Move[], Move2Code[];


extern void	sReadGame(char *s, GAME *pGame);
extern BOOL	fReadGame(FILE *fp, GAME *pGame);
extern void	sWriteGame(char *s, GAME *pGame);
extern BOOL	fWriteGame(FILE *fp, GAME *pGame);
extern BOOL	fReadPackedGame(FILE *fp, GAME *pGame);
extern BOOL	fReadPackedGameOld(FILE *fp, GAME *pGame);
extern BOOL	fWritePackedGame(FILE *fp, GAME *pGame);
extern int	PlayGame(int MoveNum, GAME *pGame, SPFELD *pBoard);
extern void 	UniqueGame(GAME *pGame);
extern void	Game2Tab(GAME *pGame, SPFELD *pTab);
extern BOOL	Tab2Game(SPFELD *pTab, GAME *pGame);

extern void	UpdateGame(GAME *pGame, SPFELD *pNewBoard, PARTEI ToMove);


#endif

