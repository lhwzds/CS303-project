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

        self.choice=None

        
        self.quarter=np.array([
            [1000, -50, 300, 200],

            [-50, -500, 5, 2],

            [300, 5, 8, 1],

            [200, 2, 1, 0]
        ])    
        self.values = np.array([

            [10000000, -30, 300, 200, 200, 300, -3, 10000000],

            [-30, -7, -4, 1, 1, -4, -70, -30],

            [300, -4, 2, 2, 2, 2, -4, 300],

            [200, 1, 2, -3, -3, 2, 1, 200],

            [200, 1, 2, -3, -3, 2, 1, 200],

            [300, -4, 2, 2, 2, 2, -4, 300],

            [-30, -70, -4, 1, 1, -4, -70, -30],

            [10000000, -30, 300, 200, 200, 300, -30, 10000000],
        ])
  
        self._edge= np.array([(0,0),(0,1),(0,2),(0,3),(0,4),(0,5),(0,6),(0,7),
        (7,0),(7,1),(7,2),(7,3),(7,4),(7,5),(7,6),(7,7),
        (1,0),(2,0),(3,0),(4,0),(5,0),(6,0),
        (1,7),(2,7),(3,7),(4,7),(5,7),(6,7)])
        self._corner=np.array([
        (0,0),(0,7),(7,0),(7,7)
        ])
        self.corner_coe=100
        self.edge_coe=100
        self.mobi_coe=10
        self.diff_coe=3
        self.front_coe=1
        self.near_coe=50
        self.chessboard_coe=100

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
                 
    def alphabeta(self,chessboard,depth):
        v,move=self.maxlayer(chessboard, self.color, -10000000000000000, 10000000000000000,depth)
        if move is not None:
            self.takechoice(move)   
        
    def maxlayer(self,chessboard,color,alpha,beta,depth):
        if self.isterminate(chessboard) or depth==0:
            return self.evaluate(chessboard),None

        v,move=-infinity,None
        clist=self.get_candidate_list(chessboard, color)
     
        if len(clist)==0:
            ans,_=self.minlayer(chessboard,-color,alpha,beta,depth-1)
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
            ans,_=self.minlayer(next_chessboard,-color,alpha,beta,depth-1)
            if ans>v:
                v,move =ans,i
            
                alpha=max(alpha,v)       
            if v>=beta:
                return v,move
    
        return  v,move

    def minlayer(self,chessboard,color,alpha,beta,depth):
        if self.isterminate(chessboard) or depth==0:
            return self.evaluate(chessboard),None
        
        v,move=infinity,None
        clist=self.get_candidate_list(chessboard, color)
        if len(clist)==0:
            ans,_=self.maxlayer(chessboard,-color,alpha,beta,depth-1)
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
            ans,_=self.maxlayer(next_chessboard,-color,alpha,beta,depth-1)
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
        
    def chessboard_value(self,chessboard):
        
        if chessboard[0][0]==0:
            self.values[0][1]=300
            self.values[1][0]=300
        else:
            self.values[0][1]=-30
            self.values[1][0]=-30

        if chessboard[7][0]==0:
            self.values[7][1]=300
            self.values[6][0]=300
        else:
            self.values[7][1]=-30
            self.values[6][0]=-30

        if chessboard[0][7]==0:
            self.values[0][6]=300
            self.values[1][7]=300
        else:
            self.values[0][6]=-30
            self.values[1][7]=-30

        if chessboard[7][7]==0:
            self.values[6][7]=300
            self.values[7][6]=300      
        else:
            self.values[6][7]=-30
            self.values[7][6]=-30      
   
        sum=0
        for i in range(8):
            for j in range(8):
                if chessboard[i][j]!=0:
                    sum+=self.values[i][j]*chessboard[i][j]*self.color
        return -sum

    def mobility(self,chessboard):       

        selflist=self.get_candidate_list(chessboard, self.color)

        oppolist=self.get_candidate_list(chessboard, -self.color)
 
        if len(selflist)+len(oppolist)>0:
          
            return len(selflist)-len(oppolist)
        else:
            return 0

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
     
    def front_diff(self,chessboard):
        x=[-1,-1,0,1,1,1,0,-1]
        y=[0,1,1,1,0,-1,-1,-1]
        selffront=0
        oppofront=0
        frontdiff=0
        for i in range(8):
            for  j in range(8):
                if chessboard[i][j]!=0:
                    for k in range(8):
                        X = i + x[k]
                        Y= j + y[k]
                        if X >= 0 and X < 8 and Y >= 0 and Y < 8 and chessboard[X][Y] == 0 :
                            if chessboard[i][j] == 0  :
                                selffront+=1
                            else :
                                oppofront+=1
                            break

        if selffront+oppofront >0:
            return 100*(oppofront-selffront)/(selffront+oppofront)
        else:
            return 0
                  
    def corner(self,chessboard):
        selfcorner=0
        oppocorner=0

        for i in self._corner:
            if chessboard[i[0]][i[1]]==self.color:
                selfcorner+=1
            elif chessboard[i[0]][i[1]]==-self.color:
                oppocorner+=1
        
        return oppocorner-selfcorner
      
    def edge(self,chessboard):
        selfedge=0
        oppoedge=0

        for i in self._edge:
            if chessboard[i[0]][i[1]]==self.color:
                selfedge+=1
            elif chessboard[i[0]][i[1]]==-self.color:
                oppoedge+=1
    
        return oppoedge-selfedge
    
    def corner_near(self,chessboard):
        selfcornernear=0
        oppocornernear=0
        if chessboard[0][0]==0:
            if chessboard[1][0]==self.color:
                selfcornernear+=1
            if chessboard[0][1]==self.color:
                selfcornernear+=1
            if chessboard[1][0]==-self.color:
                oppocornernear+=1
            if chessboard[0][1]==-self.color:
                oppocornernear+=1
        if chessboard[7][0]==0:
            if chessboard[7][1]==self.color:
                selfcornernear+=1
            if chessboard[6][0]==self.color:
                selfcornernear+=1
            if chessboard[7][1]==-self.color:
                oppocornernear+=1
            if chessboard[6][0]==-self.color:
                oppocornernear+=1   
        if chessboard[0][7]==0:
            if chessboard[1][7]==self.color:
                selfcornernear+=1
            if chessboard[0][6]==self.color:
                selfcornernear+=1
            if chessboard[1][7]==-self.color:
                oppocornernear+=1
            if chessboard[0][6]==-self.color:
                oppocornernear+=1      
        if chessboard[7][7]==0:
            if chessboard[6][7]==self.color:
                selfcornernear+=1
            if chessboard[7][6]==self.color:
                selfcornernear+=1
            if chessboard[6][7]==-self.color:
                oppocornernear+=1
            if chessboard[7][6]==-self.color:
                oppocornernear+=1     
        return selfcornernear-oppocornernear

    def evaluate(self,chessboard):
        idx = np.where(chessboard == COLOR_NONE)
        idx = list(zip(idx[0], idx[1]))

        if self.isterminate(chessboard):
            print('Game end')
            # print(chessboard)
            return infinity*self.coin_diff(chessboard)

        score=self.mobi_coe*self.mobility(chessboard)+self.diff_coe*self.coin_diff(chessboard)
        +self.chessboard_coe*self.chessboard_value(chessboard)

        print('Game continue')
        print(str(self.mobi_coe*self.mobility(chessboard))+' '+str(self.diff_coe*self.coin_diff(chessboard))+' '+str(self.chessboard_coe*self.chessboard_value(chessboard)))
        print(chessboard)
        return score

    def go(self, chessboard):
        
        idx = np.where(chessboard == COLOR_NONE)
        idx = list(zip(idx[0], idx[1]))
        self.candidate_list.clear()
        self.candidate_list=self.get_candidate_list(chessboard, self.color)
        
        self.values[0]=np.hstack((self.quarter[0],self.quarter[0][::-1]))
        self.values[1]=np.hstack((self.quarter[1],self.quarter[1][::-1]))
        self.values[2]=np.hstack((self.quarter[2],self.quarter[2][::-1]))
        self.values[3]=np.hstack((self.quarter[3],self.quarter[3][::-1]))
        self.values[4]=np.hstack((self.quarter[3],self.quarter[3][::-1]))
        self.values[5]=np.hstack((self.quarter[2],self.quarter[2][::-1]))
        self.values[6]=np.hstack((self.quarter[1],self.quarter[1][::-1]))
        self.values[7]=np.hstack((self.quarter[0],self.quarter[0][::-1]))
        
        if len(idx)<9:
            self.mobi_coe=200
            self.diff_coe=200
            self.chessboard_coe=3
            self.alphabeta(chessboard,  3)
        elif len(idx)<20:
            self.mobi_coe=250
            self.diff_coe=100
            self.chessboard_coe=4
            self.alphabeta(chessboard,  3)         
        else: 
            self.mobi_coe=300
            self.diff_coe=40
            self.chessboard_coe=5
            self.alphabeta(chessboard,  3)

        # if len(idx)>=12:
        #     for i in self._corner:
        #         if (i[0],i[1]) in self.candidate_list:
        #             self.candidate_list.remove((i[0],i[1]))
        #             self.candidate_list.insert(0,(i[0],i[1]))

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

    AI.max_depth=3

    chessboard=np.array(chessboard)

    AI.go(chessboard)

    print(AI.candidate_list)
  