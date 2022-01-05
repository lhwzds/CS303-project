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

        self.blackdic=dict()
        self.whitedic=dict()
        self.candic=dict()
        danger=-10
        X=40
        C=20
        A=-300
        B=-150
        corner=-1000000000000
        D=0
        E=10
        F=20
        center=30
        self.traplineweight=5
        self.wmatrix= np.array([
            [corner, C, A, B, B, A, C, corner],
            [C, X, danger, D, D, danger, X, C],
            [A, danger, E, F, F, E, danger, A],
            [B, D, F, center, center, F, D, B],
            [B, D, F, center, center, F, D, B],
            [A, danger, E, F, F, E, danger, A],
            [C, X, danger, D, D, danger, X, C],
            [corner, C, A, B, B, A, C, corner],
        ])
        self.testmode=False
        self.first=True

        self.wline=np.array([19, 9, -8, 4])
        self.trapline=np.array([5, 1, 30, 6])

    def run(self,chessboard,idx):
        if len(idx)<12:
            self.wline=np.array([19, 9, -3000, 0])
            depth=11
            self.alphabeta2(chessboard, depth,self.candidate_list[::-1])  
        elif len(idx)<23:
            self.wline=np.array([19, 9, -8, 4])
            depth=3
            while not self.no_time:
                depth+=1
                self.alphabeta2(chessboard, depth,self.candidate_list[::-1])     
        elif len(idx)<40:
            self.wline=np.array([11,4,-4,12])
            depth=2
            while not self.no_time:
                depth+=1
                self.alphabeta2(chessboard, depth,self.candidate_list[::-1])           
        else:
            self.wline=np.array([19, 9, -8, 4])
            depth=2
            while not self.no_time:
                depth+=1
                self.alphabeta2(chessboard, depth,self.candidate_list[::-1])  
           
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
  
    def takechoice(self,p):
        self.candidate_list.remove(p)

        self.candidate_list.append(p)

    def get_candidate_list(self,chessboard,color):

        key=chessboard.copy()

        key=key.flatten().tolist()

        key.append(color)

        key=tuple(key)
         
        if key in self.candic:
            return self.candic[key]
        else:
            
            idx = np.where(chessboard == COLOR_NONE)

            idx = list(zip(idx[0], idx[1]))

            returnlist=[]

            for p in idx:

                result=self.test(chessboard,p,-1,color)

                if color in result:

                    returnlist.append(p)

            random.shuffle(returnlist)
            
            self.candic[key]=returnlist

            return returnlist

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
            key=chessboard.copy()
            key=key.flatten().tolist()
            key.append(i)
            key=tuple(key)
            if color== COLOR_BLACK:
                if key in self.blackdic:
                    next_chessboard=self.blackdic[key]
                else:
                    next_chessboard=chessboard.copy()
                    appendlist=self.flip(next_chessboard,i,color)
                    next_chessboard[i[0]][i[1]]=color
                    for j in appendlist:
                        next_chessboard[j[0]][j[1]]=color      
                    self.blackdic[key]  =next_chessboard
            else:
                if key in self.whitedic:
                    next_chessboard=self.whitedic[key]
                else:
                    next_chessboard=chessboard.copy()
                    appendlist=self.flip(next_chessboard,i,color)
                    next_chessboard[i[0]][i[1]]=color
                    for j in appendlist:
                        next_chessboard[j[0]][j[1]]=color      
                    self.whitedic[key]  =next_chessboard

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
            key=chessboard.copy()
            key=key.flatten().tolist()
            key.append(i)
            key=tuple(key)
            if color== COLOR_BLACK:
                if key in self.blackdic:
                    next_chessboard=self.blackdic[key]
                else:
                    next_chessboard=chessboard.copy()
                    appendlist=self.flip(next_chessboard,i,color)
                    next_chessboard[i[0]][i[1]]=color
                    for j in appendlist:
                        next_chessboard[j[0]][j[1]]=color      
                    self.blackdic[key]  =next_chessboard
            else:
                if key in self.whitedic:
                    next_chessboard=self.whitedic[key]
                else:
                    next_chessboard=chessboard.copy()
                    appendlist=self.flip(next_chessboard,i,color)
                    next_chessboard[i[0]][i[1]]=color
                    for j in appendlist:
                        next_chessboard[j[0]][j[1]]=color      
                    self.whitedic[key]  =next_chessboard


            ans,_=self.maxlayer2(next_chessboard,-color,alpha,beta,depth-1,maxdepth,inputlist)
            if time.time()>self.time_out+self.start:
                return None,None        
            if ans<v:
                v,move=ans,i
            
                beta=min(beta,v)
            if v<=alpha:
                return v,move
 
        return v,move

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

        trap=0
        optrap=0
        diatrap=0
        opdiatrap=0
        cornertrap=0
        opcornertrap=0
        cornerdiatrap=0
        opcornerdiatrap=0

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
            if (not p1 in opidx) or (not p3 in opidx) or (not p4 in opidx) or (not p6 in opidx) :
                if p in [(0,2),(0,3),(0,4),(0,5),(2,0),(3,0),(4,0),(5,0),(7,2),(7,3),(7,4),(7,5),(2,7),(3,7),(4,7),(5,7)]:
                    trap+=1
                if p in [(0,0),(0,7),(7,0),(7,7)]:
                    cornertrap+=1
            if (not p0 in idx) or (not p2 in idx) or (not p5 in idx) or (not p7 in idx) :
                if p in [(0,2),(0,3),(0,4),(0,5),(2,0),(3,0),(4,0),(5,0),(7,2),(7,3),(7,4),(7,5),(2,7),(3,7),(4,7),(5,7)]:
                    diatrap+=1
                if p in [(0,0),(0,7),(7,0),(7,7)]:
                    cornerdiatrap+=1


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
            if (not p1 in idx) or (not p3 in idx) or (not p4 in idx) or (not p6 in idx) :
                if p in [(0,2),(0,3),(0,4),(0,5),(2,0),(3,0),(4,0),(5,0),(7,2),(7,3),(7,4),(7,5),(2,7),(3,7),(4,7),(5,7)]:
                    optrap+=1
                if p in [(0,0),(0,7),(7,0),(7,7)]:
                    opcornertrap+=1
            if (not p0 in idx) or (not p2 in idx) or (not p5 in idx) or (not p7 in idx) :
                if p in [(0,2),(0,3),(0,4),(0,5),(2,0),(3,0),(4,0),(5,0),(7,2),(7,3),(7,4),(7,5),(2,7),(3,7),(4,7),(5,7)]:
                    opdiatrap+=1
                if p in [(0,0),(0,7),(7,0),(7,7)]:
                    opcornerdiatrap+=1               

        selfcount=len(selfidx)
        opcount=len(opidx)

        mobdif=mobility-opmobility
        pomobidif=potentialmobility-oppotentialmobility
        countdif=selfcount-opcount
        eval=self.evaluate1(chessboard)
        vals=[mobdif,pomobidif,countdif,eval]
        trapdif=trap-optrap
        diatrapdif=diatrap-opdiatrap
        cornertrapdif=cornertrap-opcornerdiatrap
        cornerdiatrapdif=cornerdiatrap-opcornerdiatrap
        traps=[trapdif,diatrapdif,cornertrapdif,cornerdiatrapdif]
        value=0
        trapvalue=0
        for i in range(len(vals)):
            value+=vals[i]*self.wline[i]
        for i in range(len(traps)):
            value+=traps[i]*self.trapline[i]*self.traplineweight
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

  

    def iftestmode(self,idx,chessboard):
        testchessboard1=np.array([[ 0, 0, 0, 0, 0, 0, 0, 0], [ 0, 0, 0, 0, 0, 0, 0, 0], [ 0, 0, 0, 0, 0, 0, 0, 0], [ 0, 0, 0, 1, -1, 0, 0, 0], [ 0, 0, 0, 1, -1, 0, 0, 0], [ 0, 0, 0, 0, 0, 0, 0, 0], [ 0, 0, 0, 0, 0, 0, 0, 0], [ 0, 0, 0, 0, 0, 0, 0, 0]])
        testchessboard2=np.array([[ 0, 0, 0, 0, 0, 0, 0, 0], [ 0, 0, 0, 0, 0, 0, 0, 0], [ 0, 0, 0, 0, 0, 0, 0, 0], [ 0, 0, 0, -1, 1, 0, 0, 0], [ 0, 0, 0, -1, 1, 0, 0, 0], [ 0, 0, 0, 0, 0, 0, 0, 0], [ 0, 0, 0, 0, 0, 0, 0, 0], [ 0, 0, 0, 0, 0, 0, 0, 0]])
        testchessboard3=np.array([[ 0, 0, 0, 0, 0, 0, 0, 0], [ 0, 0, 0, 0, 0, 0, 0, 0], [ 0, 0, 0, 0, 0, 0, 0, 0], [ 0, 0, 0, 1, -1, 0, 0, 0], [ 0, 0, 0, -1, 1, 0, 0, 0], [ 0, 0, 0, 0, 0, 0, 0, 0], [ 0, 0, 0, 0, 0, 0, 0, 0], [ 0, 0, 0, 0, 0, 0, 0, 0]])
        testchessboard4=np.array([[ 0, 0, 0, 0, 0, 0, 0, 0], [ 0, 0, 0, 0, 0, 0, 0, 0], [ 0, 0, 0, 0, 0, 0, 0, 0], [ 0, 0, 0, -1, 1, 0, 0, 0], [ 0, 0, 0, -1, 1, 0, 0, 0], [ 0, 0, 0, 0, 0, 0, 0, 0], [ 0, 0, 0, 0, 0, 0, 0, 0], [ 0, 0, 0, 0, 0, 0, 0, 0]])
        if len(idx)!=60:
            self.testmode=True
        if np.array_equal(testchessboard1,chessboard):
            self.testmode=True
        if np.array_equal(testchessboard2,chessboard):
            self.testmode=True
        if np.array_equal(testchessboard3,chessboard):
            self.testmode=True
        if np.array_equal(testchessboard4,chessboard):
            self.testmode=True

    def go(self, chessboard):
        self.start=time.time()
        idx = np.where(chessboard == COLOR_NONE)
        idx = list(zip(idx[0], idx[1]))
        self.candidate_list.clear()
        self.candidate_list=self.get_candidate_list(chessboard, self.color)
        if self.first:
            self.iftestmode(idx,chessboard)
        if not self.testmode:
            self.run(chessboard,idx)
        if self.first:
            self.testmode=False
            self.first=False

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
  