from typing_extensions import runtime

import numpy as np

import random

import time

import math


COLOR_BLACK=-1

COLOR_WHITE=1

COLOR_NONE=0

infinity=math.inf

class AI(object):


    def __init__(self, chessboard_size, color, time_out):

        self.chessboard_size = chessboard_size

        self.color = color

        self.time_out = time_out

        self.candidate_list = []

        self.start=0

        self.no_time=False

        self.wmatrix= np.array([
            [-800, 40, -300, -200, -200, -300, 40, -800],
            [40, 80, -4, -2, -2, -4, 80, 40],
            [-300, -4, -5, -1, -1, -5, -4, -300],
            [-200, -2, -1, 0, 0, -1, -2, -200],
            [-200, -2, -1, 0, 0, -1, -2, -200],
            [-300, -4, -5, -1, -1, -5, -4, -300],
            [40, 80, -4, -2, -2, -4, 80, 40],
            [-800, 40, -300, -200, -200, -300, 40, -800],
        ])

        self.wline=np.array([19, 9, -8, 4])

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
    
    def isterminate(self,chessboard):
        selflist=self.get_candidate_list(chessboard, self.color)

        oppolist=self.get_candidate_list(chessboard, -self.color)

        return  len(selflist)+len(oppolist)==0

    def coin_diff(self,chessboard):
        selfcoin=0
        oppocoin=0

        for i in range(8):
            for  j in range(8):
                if chessboard[i][j]==self.color:
                    selfcoin+=1
                elif chessboard[i][j]== -self.color:
                    oppocoin+=1

        return oppocoin-selfcoin
 

    def alphabeta(self,chessboard,depth):
        v,move=self.maxlayer(chessboard, self.color, -10000000000000000, 10000000000000000,depth,depth)
        if move is not None:
            self.takechoice(move)   
        
    def maxlayer(self,chessboard,color,alpha,beta,depth,maxdepth):
        if self.isterminate(chessboard) or depth==0:
            return self.evaluate(chessboard),None

        v,move=-infinity,None
        clist=self.get_candidate_list(chessboard, color)
     
        if len(clist)==0:
            ans,_=self.minlayer(chessboard,-color,alpha,beta,depth-1,maxdepth)
            if ans>v:
                v,move =ans,None
             
                alpha=max(alpha,v)       
            if v>=beta:
                return v,move
           
        for i in clist:
            next_chessboard=chessboard.copy()
            appendlist=self.flip(next_chessboard,i,color)
            next_chessboard[i[0]][i[1]]=color
            for j in appendlist:
                next_chessboard[j[0]][j[1]]=color
            self.flip(next_chessboard, i, color)
            ans,_=self.minlayer(next_chessboard,-color,alpha,beta,depth-1,maxdepth)
            if ans>v:
                v,move =ans,i
                alpha=max(alpha,v)      
            if v>=beta:
                return v,move
    
        return  v,move

    def minlayer(self,chessboard,color,alpha,beta,depth,maxdepth):
        if self.isterminate(chessboard) or depth==0:
            return self.evaluate(chessboard),None
        
        v,move=infinity,None
        clist=self.get_candidate_list(chessboard, color)
        if len(clist)==0:
            ans,_=self.maxlayer(chessboard,-color,alpha,beta,depth-1,maxdepth)
            if ans<v:
                v,move=ans,None
                beta=min(beta,v)
            if v<=alpha:
                return v,move
            
        for i in clist:
            next_chessboard=chessboard.copy()
            appendlist=self.flip(next_chessboard,i,color)
            next_chessboard[i[0]][i[1]]=color
            for j in appendlist:
                next_chessboard[j[0]][j[1]]=color
            ans,_=self.maxlayer(next_chessboard,-color,alpha,beta,depth-1,maxdepth)
            if ans<v:
                v,move=ans,i
            
                beta=min(beta,v)
            if v<=alpha:
                return v,move
 
        return v,move

    def takechoice(self,p):
        self.candidate_list.remove(p)

        self.candidate_list.append(p)

    def get_candidate_list(self,chessboard,color):

        idx = np.where(chessboard == COLOR_NONE)

        idx = list(zip(idx[0], idx[1]))

        returnlist=[]

        for p in idx:

            result=self.test(chessboard,p,-1,color)

            if color in result:

                returnlist.append(p)
        random.shuffle(returnlist)
        return returnlist

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
        
        if self.isterminate(chessboard):
            coin_diff=self.coin_diff(chessboard)
            if coin_diff>0:
                return infinity
            elif coin_diff<0:
                return -infinity
            else:
                return 0

        for p in idx:
            result=self.test(chessboard,p,-1,self.color)
            if self.color in result:
                mobility+=1

        for p in idx:
            result=self.test(chessboard,p,-1,-self.color)
            if -self.color in result:
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


    def alphabeta2(self,chessboard,depth,inputlist):
        v,move=self.maxlayer2(chessboard, self.color, -10000000000000000, 10000000000000000,depth,depth,inputlist)
        if move is not None:
            self.takechoice(move)   
        if time.time()>self.time_out+self.start:
            self.no_time=True
        
    def maxlayer2(self,chessboard,color,alpha,beta,depth,maxdepth,inputlist):
        if time.time()>self.time_out+self.start:
            return None,None
        if self.isterminate(chessboard) or depth==0:
            return self.evaluate(chessboard),None

        v,move=-infinity,None
        clist=self.get_candidate_list(chessboard, color)
        if depth==maxdepth:
            clist=inputlist

        if len(clist)==0:
            ans,_=self.minlayer2(chessboard,-color,alpha,beta,depth-1,maxdepth,inputlist)
            if time.time()>self.time_out+self.start:
                return None,None
            if ans>v:
                v,move =ans,None
             
                alpha=max(alpha,v)       
            if v>=beta:
                return v,move
           
        for i in clist:
            next_chessboard=chessboard.copy()
            appendlist=self.flip(next_chessboard,i,color)
            next_chessboard[i[0]][i[1]]=color
            for j in appendlist:
                next_chessboard[j[0]][j[1]]=color
            self.flip(next_chessboard, i, color)
            ans,_=self.minlayer2(next_chessboard,-color,alpha,beta,depth-1,maxdepth,inputlist)
            if time.time()>self.time_out+self.start:
                return None,None
            if ans>v:
                v,move =ans,i
                alpha=max(alpha,v)      
                if depth==maxdepth:
                    self.takechoice(move)
            if v>=beta:
                return v,move
    
        return  v,move

    def minlayer2(self,chessboard,color,alpha,beta,depth,maxdepth,inputlist):
        if time.time()>self.time_out+self.start:
            return None,None
        if self.isterminate(chessboard) or depth==0:
            return self.evaluate(chessboard),None
        
        v,move=infinity,None
        clist=self.get_candidate_list(chessboard, color)
        if len(clist)==0:
            ans,_=self.maxlayer2(chessboard,-color,alpha,beta,depth-1,maxdepth,inputlist)
            if time.time()>self.time_out+self.start:
                return None,None            
            if ans<v:
                v,move=ans,None
                beta=min(beta,v)
            if v<=alpha:
                return v,move
            
        for i in clist:
            next_chessboard=chessboard.copy()
            appendlist=self.flip(next_chessboard,i,color)
            next_chessboard[i[0]][i[1]]=color
            for j in appendlist:
                next_chessboard[j[0]][j[1]]=color
            ans,_=self.maxlayer2(next_chessboard,-color,alpha,beta,depth-1,maxdepth,inputlist)
            if time.time()>self.time_out+self.start:
                return None,None        
            if ans<v:
                v,move=ans,i
                beta=min(beta,v)
            if v<=alpha:
                return v,move
 
        return v,move




    def go(self, chessboard):
        self.start=time.time()
        idx = np.where(chessboard == COLOR_NONE)
        idx = list(zip(idx[0], idx[1]))
        self.candidate_list.clear()
        self.candidate_list=self.get_candidate_list(chessboard, self.color)
        self.time_out=self.time_out-0.5

        if len(idx)<10:
            depth=9
            self.alphabeta2(chessboard,  depth ,self.candidate_list.copy()[::-1])   
        # elif len(idx)<15:
        #     depth=4
        #     self.alphabeta2(chessboard,  depth ,self.candidate_list.copy()[::-1])   
        #     while not self.no_time:
        #         depth+=1
        #         self.alphabeta2(chessboard, depth,self.candidate_list.copy()[::-1])  
        else: 
            depth=3
            self.alphabeta2(chessboard,  depth ,self.candidate_list.copy()[::-1])      
            while not self.no_time:
                depth+=1
                self.alphabeta2(chessboard, depth,self.candidate_list.copy()[::-1])   
        self.no_time=False
        self.time_out+=0.5

if __name__ == '__main__':


    chessboard=np.array([[  0 ,0  ,0  ,0  ,0  ,0  ,0  ,0],
 [ 0  ,0  ,0  ,0  ,0  ,0  ,0  ,0],
[ 0  ,0  ,0  ,0  ,0  ,0  ,0  ,0],
 [ 0  ,0  ,0  ,0  ,0  ,0  ,0  ,0],
 [ 0  ,0  ,1  ,1  ,1  ,1  ,0  ,0],
 [ 0  ,0  ,0  ,-1  ,1  ,0  ,0  ,0],
[ 0  ,0  ,0  ,0  ,0  ,0  ,0  ,0],
 [ 0  ,0  ,0  ,0  ,0  ,0  ,0  ,0]] )

    AI=AI(8,-1,5)

    chessboard=np.array(chessboard)

    AI.go(chessboard)

    print(AI.candidate_list)
  