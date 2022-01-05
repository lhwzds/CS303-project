from typing_extensions import runtime
import numpy as np
import random
import time
import math

COLOR_BLACK=-1
COLOR_WHITE=1
COLOR_NONE=0

class AI(object):

    def __init__(self, chessboard_size, color, time_out):
        self.chessboard_size = chessboard_size
        self.color = color
        self.time_out = time_out
        self.candidate_list = []
        self.max_depth1=3
        self.max_depth2=4
        self.max_depth3=5
        self.steps=0
        
        self.wmatrix= np.array([
            [-500, 20, -300, -200, -200, -300, 20, -500],
            [20, 40, -4, -2, -2, -4, 40, 20],
            [-300, -4, -5, -1, -1, -5, -4, -300],
            [-200, -2, -1, 0, 0, -1, -2, -200],
            [-200, -2, -1, 0, 0, -1, -2, -200],
            [-300, -4, -5, -1, -1, -5, -4, -300],
            [20, 40, -4, -2, -2, -4, 40, 20],
            [-500, 20, -300, -200, -200, -300, 20, -500],
        ])
        # self.wline=np.array([31,10,-16,2])
        # self.wline=np.array([19,5,-1,4])
        self.wline=np.array([19, 9, -8, 4])


    def evaluate1(self,chessboard):
        weight=self.wmatrix.copy()
        if chessboard[0,0]!=0:
            weight[1,1]=-400
            weight[1,0]=-300
            weight[0,1]=-300
        if chessboard[7,0]!=0:
            weight[6,1]=-400
            weight[7,1]=-300
            weight[6,0]=-300
        if chessboard[0,7]!=0:
            weight[1,6]=-400
            weight[1,7]=-300
            weight[0,6]=-300
        if chessboard[7,7]!=0:
            weight[6,6]=-400
            weight[7,6]=-300
            weight[6,7]=-300        
        return sum(sum(weight*chessboard))*self.color

    def evaluate(self,chessboard):
        idx = np.where(chessboard == COLOR_NONE)
        idx = list(zip(idx[0], idx[1]))
        mobility=0
        opmobility=0
        
        if self.color in chessboard and -self.color not in chessboard:
            return -100000
        elif self.color not in chessboard and -self.color in chessboard:
            return 100000

        for p in idx:
            result=self.test(chessboard,p,-1,self.color)
            if self.color in result:
                mobility+=1

        for p in idx:
            result=self.test(chessboard,p,-1,-self.color)
            if self.color in result:
                opmobility+=1

       
        potentialmobility=0
        oppotentialmobility=0
        
        opidx=np.where(chessboard == -self.color)
        opidx=list(zip(opidx[0],opidx[1]))
        selfidx=np.where(chessboard == self.color)
        selfidx=list(zip(selfidx[0],selfidx[1]))

        for p in idx:
            x=p[0]
            y=p[1]
            minx=max(p[0]-1,0)
            maxx=min(p[0]+1,self.chessboard_size-1)
            miny=max(p[1]-1,0)
            maxy=min(p[1]+1,self.chessboard_size-1)

            p0=(minx,miny)
            p1=(minx,y)
            p2=(minx,maxy)
            p3=(x,miny)
            p4=(x,maxy)
            p5=(maxx,miny)
            p6=(maxx,y)
            p7=(maxx,maxy)
            if p0 in opidx or p1 in opidx or p2 in opidx or p3 in opidx or p4 in opidx or p5 in opidx or p6 in opidx or p7 in opidx:
                potentialmobility+=1 

        for p in idx:
            x=p[0]
            y=p[1]
            minx=max(p[0]-1,0)
            maxx=min(p[0]+1,self.chessboard_size-1)
            miny=max(p[1]-1,0)
            maxy=min(p[1]+1,self.chessboard_size-1)

            p0=(minx,miny)
            p1=(minx,y)
            p2=(minx,maxy)
            p3=(x,miny)
            p4=(x,maxy)
            p5=(maxx,miny)
            p6=(maxx,y)
            p7=(maxx,maxy)
            if p0 in selfidx or p1 in selfidx or p2 in selfidx or p3 in selfidx or p4 in selfidx or p5 in selfidx or p6 in selfidx or p7 in selfidx:
                oppotentialmobility+=1   

        selfcount=len(selfidx)
        opcount=len(opidx)

        mobdif=mobility-opmobility
        pomobidif=potentialmobility-oppotentialmobility
        countdif=selfcount-opcount
        eval=self.evaluate1(chessboard)
        vals=[mobdif,pomobidif,countdif,eval]
        value=0
        for i in range(len(vals)):
            value+=vals[i]*self.wline[i]
        return value      

    
    def flip(self,chessboard,p,color):
        
        x0=p[0]
        y0=p[1]
        templist=[]
        appendlist=[]
        x=x0
        y=y0
        while x>0 :
            x=x-1
            if chessboard[x,y]==0 :
                break
            elif chessboard[x,y]==-color:
                templist.append((x,y)) 
            else :
                for i in templist:
                    appendlist.append(i)
                break

        x=x0
        y=y0
        templist.clear()
        while x<7 :
            x=x+1
            if chessboard[x,y]==0 :
                break
            elif chessboard[x,y]==-color:
                templist.append((x,y)) 
            else :
                for i in templist:
                    appendlist.append(i)
                break

        x=x0
        y=y0
        templist.clear()
        while y>0 :
            y=y-1
            if chessboard[x,y]==0 :
                templist.clear()
                break
            elif chessboard[x,y]==-color:
                templist.append((x,y)) 
            else :
                for i in templist:
                    appendlist.append(i)
                break

        x=x0
        y=y0
        templist.clear()
        while y<7 :
            y=y+1
            if chessboard[x,y]==0 :
                templist.clear()
                break
            elif chessboard[x,y]==-color:
                templist.append((x,y)) 
            else :
                for i in templist:
                    appendlist.append(i)
                break

        x=x0
        y=y0
        templist.clear()
        while x>0 and y>0 :
            y=y-1
            x=x-1
            if chessboard[x,y]==0 :
                templist.clear()
                break
            elif chessboard[x,y]==-color:
                templist.append((x,y)) 
            else :
                for i in templist:
                    appendlist.append(i)
                break

        x=x0
        y=y0
        templist.clear()
        while x>0 and y<7 :
            y=y+1
            x=x-1
            if chessboard[x,y]==0 :
                templist.clear()
                break
            elif chessboard[x,y]==-color:
                templist.append((x,y)) 
            else :
                for i in templist:
                    appendlist.append(i)
                break

        x=x0
        y=y0
        templist.clear()
        while x<7 and y<7 :
            y=y+1
            x=x+1
            if chessboard[x,y]==0 :
                templist.clear()
                break
            elif chessboard[x,y]==-color:
                templist.append((x,y)) 
            else :
                for i in templist:
                    appendlist.append(i)
                break

        x=x0
        y=y0
        templist.clear()
        while x<7 and y>0 :
            y=y-1
            x=x+1
            if chessboard[x,y]==0 :
                templist.clear()
                break
            elif chessboard[x,y]==-color:
                templist.append((x,y)) 
            else :
                for i in templist:
                    appendlist.append(i)
                break

        return appendlist
    #test判断某一下子位置是否可以下子
    def test(self,chessboard,p,direction,color):
        plist=[]
        x=p[0]
        y=p[1]
        minx=max(p[0]-1,0)
        maxx=min(p[0]+1,self.chessboard_size-1)
        miny=max(p[1]-1,0)
        maxy=min(p[1]+1,self.chessboard_size-1)

        p0=(minx,miny)
        p1=(minx,y)
        p2=(minx,maxy)
        p3=(x,miny)
        p4=(x,maxy)
        p5=(maxx,miny)
        p6=(maxx,y)
        p7=(maxx,maxy)

        plist.append(p0) 
        plist.append(p1)
        plist.append(p2)
        plist.append(p3)
        plist.append(p4)            
        plist.append(p5)
        plist.append(p6)
        plist.append(p7)

        corner=[0,2,5,7]
        xedge=[3,4]
        yedge=[1,6]
        if direction!=-1 :
           if direction in corner:

               if p[0] == plist[direction][0] or p[1] == plist[direction][1]:
                   return 0
               else:

                   if chessboard[plist[direction]]+chessboard[p]==0:
                        return chessboard[plist[direction]]
                   elif chessboard[plist[direction]]==0:
                        return 0
                   else:
                        return self.test(chessboard, plist[direction], direction,color)

           elif direction in xedge:

                if p[1] == plist[direction][1]:
                        return 0
                else:

                   if chessboard[plist[direction]]+chessboard[p]==0:
                        return chessboard[plist[direction]]
                   elif chessboard[plist[direction]]==0:
                        return 0
                   else:
                        return self.test(chessboard, plist[direction], direction,color)

           elif direction in yedge:

                if p[0] == plist[direction][0]:
                        return 0
                else:

                   if chessboard[plist[direction]]+chessboard[p]==0:
                        return chessboard[plist[direction]]
                   elif chessboard[plist[direction]]==0:
                        return 0
                   else:
                        return self.test(chessboard, plist[direction], direction,color)

        else: 
            result=[]
            output=chessboard.copy()
            for d in range(len(plist)):
                if chessboard[plist[d]] !=0:
                    result.append(self.test(chessboard, plist[d], d,color))
                else: 
                    result.append(0)
            if color in result:
                now=p
                for i in range(len(plist)):
                    if result[i] == color:
                        while output[now]!=color:
                            output[now]=color
                            x=now[0]
                            y=now[1]
                            nplist=[(x-1,y-1),(x-1,y),(x-1,y+1),(x,y-1),(x,y+1),(x+1,y-1),(x+1,y),(x+1,y+1)]                            
                            now=nplist[i]

                return output
            else:
                return [0]



    def getscore(self,idx,chessboard,color,depth,max_depth,alpha,beta):

        if depth==0:
            return self.evaluate(chessboard)
        else:
            if depth==max_depth:   
                maxscore=-1000000 
                for p in idx:
                    result=self.test(chessboard,p,-1,color)
                    if color in result:
                        idx1 = np.where(result == COLOR_NONE)
                        idx1 = list(zip(idx1[0], idx1[1]))   
                        self.candidate_list.append(p)
                        # print(self.candidate_list)
                for p in self.candidate_list:

                    result=self.test(chessboard,p,-1,color)
                    score=self.getscore(idx, result, -color, depth-1,max_depth,alpha,beta) 
        
                    if score>maxscore:
                        maxscore=score
                        self.takechoice(p)
    
                    if maxscore>=beta:
                        break
                    if maxscore>alpha:
                        alpha=maxscore 

            else:
                if (max_depth-depth+1) %2 ==1:
                    maxscore=-1000000 
                    for p in idx:
                        result=self.test(chessboard,p,-1,color)
                        if color in result:
                            idx1 = np.where(result == COLOR_NONE)
                            idx1 = list(zip(idx1[0], idx1[1]))   
                            score=self.getscore(idx1, result, -color, depth-1,max_depth,alpha,beta) 
                            maxscore=max(score,maxscore)
                            if maxscore>=beta:
                                break
                            if maxscore>alpha:
                                alpha=maxscore
                        
                    return maxscore
                else:
                    minscore=1000000 
                    for p in idx:
                        result=self.test(chessboard,p,-1,color)
                        if color in result:
                            idx1 = np.where(result == COLOR_NONE)
                            idx1 = list(zip(idx1[0], idx1[1]))    
                            score=self.getscore(idx1, result, -color, depth-1,max_depth,alpha,beta)
                            minscore=min(score,minscore)
                            if minscore<=alpha:
                                break
                            if minscore<beta:
                                beta=minscore

                    return minscore

    def takechoice(self,p):
        self.candidate_list.remove(p)
        print(self.candidate_list)
        self.candidate_list.append(p)


    def go(self, chessboard):
        idx = np.where(chessboard == COLOR_NONE)
        idx = list(zip(idx[0], idx[1]))
        self.candidate_list.clear()
        start = time.time()
        self.getscore(idx, chessboard, self.color, 1,1,-1000000,1000000)  
        depth=5
        le=0
        if self.candidate_list!=None:
            le=len(self.candidate_list)
   
        if self.steps<8:
            if le>4:
                depth=4
            else:
                depth=5
        elif self.steps>24:
            if le>4:
                depth=6
            else:
                depth=7
        else:
            if le>10:
                depth=1
            elif le>7:
                depth=2
            elif le>4:
                depth=3
            else:
                depth=4
        if depth !=1:
            self.candidate_list.clear()
            self.getscore(idx, chessboard, self.color, depth,depth,-1000000,1000000)

        run_time = (time.time() - start)
        print('depth '+str(depth)+ ' takes '+str(run_time)+' seconds')
        self.steps+=1
        

def takefirst(elem):
    return elem[0]

if __name__ == '__main__':

    chessboard=np.array([
            [ 0, 0, 0, 0, 0, 0, 0, 0],
            [ 0, 0, 0, 0, 0, 0, 0, 0],
            [ 0, 0, 0, 0, 0, 0, 0, 0],
            [ 0, 0, 0, 1, -1, 0, 0, 0],
            [ 0, 0, 0, -1, 1, 1, 0, 0],
            [ 0, 0, 0, 0, 0, 0, 0, 0],
            [ 0, 0, 0, 0, 0, 0, 0, 0],
            [ 0, 0, 0, 0, 0, 0, 0, 0]
        ] )
    AI=AI(8,-1,5)
    AI.max_depth=3
    chessboard=np.array(chessboard)
    
    AI.go(chessboard)

    AI.candidate_list.sort(key=takefirst)
    print(AI.candidate_list)
  