import numpy as np
import random
import time

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
        
        # self.wmatrix=np.array([[500,-25,10,5,5,10,-25,500],
        #             [-25,-45,1,1,1,1,-45,-25],
        #             [10,1,3,2,2,3,1,10],
        #             [5,1,2,1,1,2,1,5],
        #             [5,1,2,1,1,2,1,5],
        #             [10,1,3,2,2,3,1,10],
        #             [-25,-45,1,1,1,1,-45,-25],
        #             [500,-25,10,5,5,10,-25,500]])

        # self.wmatrix=np.array(
        #     [[-10000,25,-20,-10,-10,-20,25,-10000],
        #     [25,-45,10,10,10,10,-45,25],
        #     [-20,10,100,200,200,100,10,-20],
        #     [-10,10,200,0,0,100,10,-10],
        #     [-10,10,200,0,0,200,10,-10],
        #     [-20,10,100,200,200,100,10,-20],
        #     [25,-45,10,10,10,10,-45,25],
        #     [-10000,25,-20,-5,-5,-20,25,-10000]])

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
        # self.wline=np.array([41, 10, -14, 5])
        # self.wline=np.array([14, 5, -4, 1])
        # self.wline=np.array([-5, 7, -14, 9])
        # self.wline=np.array([29, 21, -12, 9])
        # self.wline=np.array([40,21,-1,3])
        # self.patterns=[]
        # self.row1=np.array([(0,0),(0,1),(0,2),(0,3),(0,4),(0,5),(0,6),(0,7)])
        # self.row2=np.array([(1,0),(1,1),(1,2),(1,3),(1,4),(1,5),(1,6),(1,7)])
        # self.row3=np.array([(2,0),(2,1),(2,2),(2,3),(2,4),(2,5),(2,6),(2,7)])
        # self.row4=np.array([(3,0),(3,1),(3,2),(3,3),(3,4),(3,5),(3,6),(3,7)])
        # self.row5=np.array([(4,0),(4,1),(4,2),(4,3),(4,4),(4,5),(4,6),(4,7)])
        # self.row6=np.array([(5,0),(5,1),(5,2),(5,3),(5,4),(5,5),(5,6),(5,7)])
        # self.row7=np.array([(6,0),(6,1),(6,2),(6,3),(6,4),(6,5),(6,6),(6,7)])
        # self.row8=np.array([(7,0),(7,1),(7,2),(7,3),(7,4),(7,5),(7,6),(7,7)])
        # self.patterns.append(self.row1)
        # self.patterns.append(self.row2)
        # self.patterns.append(self.row3)
        # self.patterns.append(self.row4)
        # self.patterns.append(self.row5)
        # self.patterns.append(self.row6)
        # self.patterns.append(self.row7)
        # self.patterns.append(self.row8)
        # self.col1=np.array([(0,0),(1,0),(2,0),(3,0),(4,0),(5,0),(6,0),(7,0)])
        # self.col2=np.array([(0,1),(1,1),(2,1),(3,1),(4,1),(5,1),(6,1),(7,1)])
        # self.col3=np.array([(0,2),(1,2),(2,2),(3,2),(4,2),(5,2),(6,2),(7,2)])
        # self.col4=np.array([(0,3),(1,3),(2,3),(3,3),(4,3),(5,3),(6,3),(7,3)])
        # self.col5=np.array([(0,4),(1,4),(2,4),(3,4),(4,4),(5,4),(6,4),(7,4)])
        # self.col6=np.array([(0,5),(1,5),(2,5),(3,5),(4,5),(5,5),(6,5),(7,5)])
        # self.col7=np.array([(0,6),(1,6),(2,6),(3,6),(4,6),(5,6),(6,6),(7,6)])
        # self.col8=np.array([(0,7),(1,7),(2,7),(3,7),(4,7),(5,7),(6,7),(7,7)])
        # self.patterns.append(self.col1)
        # self.patterns.append(self.col2)
        # self.patterns.append(self.col3)
        # self.patterns.append(self.col4)
        # self.patterns.append(self.col5)
        # self.patterns.append(self.col6)
        # self.patterns.append(self.col7)
        # self.patterns.append(self.col8)
        # self.cor331=np.array([(0,0),(0,1),(0,2),(1,0),(1,1),(1,2),(2,0),(2,1),(2,2)])
        # self.cor332=np.array([(5,0),(5,1),(5,2),(6,0),(6,1),(6,2),(7,0),(7,1),(7,2)])
        # self.cor333=np.array([(0,5),(0,6),(0,7),(1,5),(1,6),(1,7),(2,5),(2,6),(2,7)])
        # self.cor334=np.array([(5,5),(5,6),(5,7),(6,5),(6,6),(6,7),(7,5),(7,6),(7,7)])
        # self.patterns.append(self.cor331)
        # self.patterns.append(self.cor332)
        # self.patterns.append(self.cor333)
        # self.patterns.append(self.cor334)
        # self.cor251=np.array([(0,0),(0,1),(0,2),(0,3),(0,4),(1,0),(1,1),(1,2),(1,3),(1,4)])
        # self.cor252=np.array([(0,0),(1,0),(2,0),(3,0),(4,0),(0,1),(1,1),(2,1),(3,1),(4,1)])
        # self.cor253=np.array([(6,0),(6,1),(6,2),(6,3),(6,4),(7,0),(7,1),(7,2),(7,3),(7,4)])
        # self.cor254=np.array([(0,6),(1,6),(2,6),(3,6),(4,6),(0,7),(1,7),(2,7),(3,7),(4,7)])
        # self.cor255=np.array([(7,7),(6,7),(5,7),(4,7),(3,7),(7,6),(6,6),(5,6),(4,6),(3,6)])
        # self.cor256=np.array([(7,7),(7,6),(7,5),(7,4),(7,3),(6,7),(6,6),(6,5),(6,4),(6,3)])
        # self.cor257=np.array([(7,0),(6,0),(5,0),(4,0),(3,0),(7,1),(6,1),(5,1),(4,1),(3,1)])
        # self.cor258=np.array([(0,7),(0,6),(0,5),(0,4),(0,3),(1,7),(1,6),(1,5),(1,4),(1,3)])
        # self.patterns.append(self.cor251)
        # self.patterns.append(self.cor252)
        # self.patterns.append(self.cor253)
        # self.patterns.append(self.cor254)
        # self.patterns.append(self.cor255)
        # self.patterns.append(self.cor256)
        # self.patterns.append(self.cor257)
        # self.patterns.append(self.cor258)

        # self.dia1=np.array([(0,3),(1,2),(2,1),(3,0)])
        # self.dia2=np.array([(7,3),(6,2),(5,1),(4,0)])
        # self.dia3=np.array([(0,4),(1,5),(2,6),(3,7)])
        # self.dia4=np.array([(7,4),(6,5),(5,6),(4,7)])
        # self.dia5=np.array([(0,4),(1,3),(2,2),(3,1),(2,0)])
        # self.dia6=np.array([(7,4),(6,3),(5,2),(4,1),(3,0)])
        # self.dia7=np.array([(0,3),(1,4),(2,5),(3,6),(4,7)])
        # self.dia8=np.array([(7,3),(6,4),(5,5),(4,6),(3,7)])
        # self.dia9=np.array([(0,5),(1,4),(2,3),(3,2),(4,1),(5,0)])
        # self.dia10=np.array([(7,5),(6,4),(5,3),(4,2),(3,1),(2,0)])
        # self.dia11=np.array([(0,2),(1,3),(2,4),(3,5),(4,6),(5,7)])
        # self.dia12=np.array([(7,2),(6,3),(5,4),(4,5),(3,6),(2,7)])
        # self.dia13=np.array([(0,6),(1,5),(2,4),(3,3),(4,2),(5,1),(6,0)])
        # self.dia14=np.array([(7,6),(6,5),(5,4),(4,3),(3,2),(2,1),(1,0)])
        # self.dia15=np.array([(0,1),(1,2),(2,3),(3,4),(4,5),(5,6),(6,7)])
        # self.dia16=np.array([(7,1),(6,2),(5,3),(4,4),(3,5),(2,6),(1,7)])

        # self.patterns.append(self.dia1)
        # self.patterns.append(self.dia2)
        # self.patterns.append(self.dia3)
        # self.patterns.append(self.dia4)
        # self.patterns.append(self.dia7)
        # self.patterns.append(self.dia8)
        # self.patterns.append(self.dia9)
        # self.patterns.append(self.dia10)
        # self.patterns.append(self.dia11)
        # self.patterns.append(self.dia12)
        # self.patterns.append(self.dia13)
        # self.patterns.append(self.dia14)
        # self.patterns.append(self.dia15)
        # self.patterns.append(self.dia16)

        # self.maindia1=np.array([(0,0),(1,1),(2,2),(3,3),(4,4),(5,5),(6,6),(7,7)])
        # self.maindia2=np.array([(0,7),(1,6),(2,5),(3,4),(4,3),(5,2),(6,1),(7,0)])

        # self.patterns.append(self.maindia1)
        # self.patterns.append(self.maindia2)

        # self.edgex1=np.array([(0,0),(0,1),(0,2),(0,3),(0,4),(0,5),(0,6),(0,7),(1,1),(1,6)])
        # self.edgex2=np.array([(7,0),(7,1),(7,2),(7,3),(7,4),(7,5),(7,6),(7,7),(6,1),(6,6)])
        # self.edgex3=np.array([(0,0),(1,0),(2,0),(3,0),(4,0),(5,0),(6,0),(7,0),(1,1),(6,1)])
        # self.edgex4=np.array([(0,7),(1,7),(2,7),(3,7),(4,7),(5,7),(6,7),(7,7),(1,6),(6,6)])

        # self.patterns.append(self.edgex1)
        # self.patterns.append(self.edgex2)
        # self.patterns.append(self.edgex3)
        # self.patterns.append(self.edgex4)

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



    def getscore(self,idx,chessboard,color,depth,max_depth):

        if depth==0:
            return self.evaluate(chessboard)
        else:
            if depth==max_depth:
                resultlist=[]
                otherlist=[]               
                maxscore=-1000000 
                for p in idx:
                    result=self.test(chessboard,p,-1,color)
                    if color in result:
                        idx1 = np.where(result == COLOR_NONE)
                        idx1 = list(zip(idx1[0], idx1[1]))   
                        score=self.getscore(idx1, result, -color, depth-1,max_depth) 
                            
                        if score>maxscore:
                            resultlist.append(p)
                            maxscore=score
                    
                        else: 
                            otherlist.append(p)
                for i in resultlist:
                    otherlist.append(i)      
                return otherlist             
            else:
                if (max_depth-depth+1) %2 ==1:
                    maxscore=-1000000 
                    for p in idx:
                        result=self.test(chessboard,p,-1,color)
                        if color in result:
                            idx1 = np.where(result == COLOR_NONE)
                            idx1 = list(zip(idx1[0], idx1[1]))   
                            score=self.getscore(idx1, result, -color, depth-1,max_depth) 
                            maxscore=max(score,maxscore)
                    return maxscore
                else:
                    minscore=1000000 
                    for p in idx:
                        result=self.test(chessboard,p,-1,color)
                        if color in result:
                            idx1 = np.where(result == COLOR_NONE)
                            idx1 = list(zip(idx1[0], idx1[1]))    
                            score=self.getscore(idx1, result, -color, depth-1,max_depth)
                            minscore=min(score,minscore)
                    return minscore


    def go(self, chessboard):
        idx = np.where(chessboard == COLOR_NONE)
        idx = list(zip(idx[0], idx[1]))
        self.candidate_list.clear()
        self.candidate_list=self.getscore(idx, chessboard, self.color, 1,1)
        if len(self.candidate_list) >9:
            self.candidate_list=self.getscore(idx, chessboard, self.color, 2,2)
        elif len(self.candidate_list) >3:
            self.candidate_list=self.getscore(idx, chessboard, self.color, 3,3)
        else :
            self.candidate_list=self.getscore(idx, chessboard, self.color, 4,4)
        
    

# time measurement
# start = time.time()
# run_time = (time.time() - start)

def takefirst(elem):
    return elem[0]

if __name__ == '__main__':

    chessboard=np.array([
            [ 0, 0, 0, 0, 0, 0, 0, 0],
            [ 0, 0, 0, 0, 0, 0, 0, 0],
            [ 0, 0, 0, 0, 0, 0, 0, 0],
            [ 0, 0, 0, 0, 0, 0, 0, 0],
            [ 0, 0, 0, 0, 0, 0, 0, 0],
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
    AI=AI(8,-1,5)
    AI.max_depth=3
    chessboard=np.array(chessboard)
    
    AI.go(chessboard)

    AI.candidate_list.sort(key=takefirst)
    print(AI.candidate_list)
  