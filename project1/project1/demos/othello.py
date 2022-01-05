from alphabeta import AI
import numpy as np
import time
import random
from tqdm import tqdm

origin=np.array([
        [ 0, 0, 0, 0, 0, 0, 0, 0],
        [ 0, 0, 0, 0, 0, 0, 0, 0],
        [ 0, 0, 0, 0, 0, 0, 0, 0],
        [ 0, 0, 0, 1,-1, 0, 0, 0],
        [ 0, 0, 0, -1, 1, 0, 0, 0],
        [ 0, 0, 0, 0, 0, 0, 0, 0],
        [ 0, 0, 0, 0, 0, 0, 0, 0],
        [ 0, 0, 0, 0, 0, 0, 0, 0]
    ] )
# chessboard=[
#     [0,0,0,0,],
#     [0,-1,1,0,],
#     [0,1,-1,0,],
#     [0,0,0,0,],
# ]
black=AI(8,-1,5)
white=AI(8,1,5)
step=0
new=[random.randint(-50, 50),random.randint(-30, 30),random.randint(-20, -1),random.randint(1, 5)]
old=[30,10,-10,1]

newwin=0
oldwin=0
for iter in tqdm(range(2)):
    chessboard=origin.copy()
    white.wline=new
    black.wline=old
    # print('--------The first iteration-------')
    while True:
        start = time.time()
        black.go(chessboard)
        blacklist=black.candidate_list
        if blacklist !=[]:
            choice=blacklist[-1:]    
            appendlist=black.flip(chessboard,choice[0],-1)
            chessboard[choice[0][0],choice[0][1]]=-1
            for i in appendlist:
                chessboard[i]=-1

        white.go(chessboard)
        whitelist=white.candidate_list
        if whitelist !=[]:
            choice=whitelist[-1:]
            appendlist=white.flip(chessboard,choice[0],1)
            chessboard[choice[0][0],choice[0][1]]=1
            for i in appendlist:
                chessboard[i]=1

        run_time = (time.time() - start)
        print('the '+str(step)+' step takes '+str(run_time)+' seconds')
        print(len(blacklist)+len(whitelist))
        step+=1
        if blacklist == [] and whitelist==[]:
            break

    black_cnt=0
    white_cnt=0

    for i in chessboard:
        for j in i:
            if j==-1:
                black_cnt+=1
            elif j==1:
                white_cnt+=1

    if black_cnt>white_cnt:
        newwin+=1
    elif white_cnt>black_cnt:
        oldwin+=1


    chessboard=origin.copy()
    white.wline=old
    black.wline=new

    while True:
        start = time.time()
        black.go(chessboard)
        blacklist=black.candidate_list
        if blacklist !=[]:
            choice=blacklist[-1:]    
            appendlist=black.flip(chessboard,choice[0],-1)
            chessboard[choice[0][0],choice[0][1]]=-1
            for i in appendlist:
                chessboard[i]=-1

        white.go(chessboard)
        whitelist=white.candidate_list
        if whitelist !=[]:
            choice=whitelist[-1:]
            appendlist=white.flip(chessboard,choice[0],1)
            chessboard[choice[0][0],choice[0][1]]=1
            for i in appendlist:
                chessboard[i]=1

        run_time = (time.time() - start)
        print('the '+str(step)+' step takes '+str(run_time)+' seconds')
        print(len(blacklist)+len(whitelist))
        step+=1
        if blacklist == [] and whitelist==[]:
            break

    black_cnt=0
    white_cnt=0

    for i in chessboard:
        for j in i:
            if j==-1:
                black_cnt+=1
            elif j==1:
                white_cnt+=1

    if black_cnt>white_cnt:
        newwin+=1
    elif white_cnt>black_cnt:
        oldwin+=1

if oldwin<newwin:
    print(new)