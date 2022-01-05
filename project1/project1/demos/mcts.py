from typing_extensions import runtime
import numpy as np
import random
import time
import math

COLOR_BLACK=-1
COLOR_WHITE=1
COLOR_NONE=0
class Node(object):
    def __INIT__(self):
        self.parent = None
        self.children= []
        self.visit_times=0
        self.quality_value=0.0
        self.state=None
class State(object):
    def __init__(self):
        
    def is_terminal(self):

    def evaluate(self):

    def 


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



 
    def takechoice(self,p):
        self.candidate_list.remove(p)
        self.candidate_list.append(p)


    def go(self, chessboard):
        idx = np.where(chessboard == COLOR_NONE)
        idx = list(zip(idx[0], idx[1]))
        self.candidate_list.clear()
        self.getscore(idx, chessboard, self.color, 1,1)
        if len(self.candidate_list) >9:
            self.candidate_list.clear()
            self.getscore(idx, chessboard, self.color, 2,2)
        else  :
            self.candidate_list.clear()
            self.getscore(idx, chessboard, self.color, 3,3)
        

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
  