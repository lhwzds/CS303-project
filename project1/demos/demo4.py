import numpy as np
import random
import time
COLOR_BLACK=-1
COLOR_WHITE=1
COLOR_NONE=0
random.seed(0)

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
        #     [[-500,25,-10,-5,-5,-10,25,-500],
        #     [25,45,-1,-1,-1,-1,45,25],
        #     [-10,-1,-3,-2,-2,-3,-1,-10],
        #     [-5,-1,-2,-1,-1,-2,-1,-5],
        #     [-5,-1,-2,-1,-1,-2,-1,-5],
        #     [-10,-1,-3,-2,-2,-3,-1,-10],
        #     [25,45,-1,-1,-1,-1,45,25],
        #     [-500,25,-10,-5,-5,-10,25,-500]])
        self.wmatrix= np.array([
            [-990, 200, -300, -200, -200, -300, 200, -990],
            [200, 400, -4, -2, -2, -4, 400, 200],
            [-300, -4, -5, -1, -1, -5, -4, -300],
            [-200, -2, -1, 0, 0, -1, -2, -200],
            [-200, -2, -1, 0, 0, -1, -2, -200],
            [-300, -4, -5, -1, -1, -5, -4, -300],
            [200, 400, -4, -2, -2, -4, 400, 200],
            [-990, 200, -300, -200, -200, -300, 200, -990],
        ])

    def evaluate1(self,chessboard):
        return sum(sum(self.wmatrix*chessboard))*self.color

    def evaluate(self,chessboard):
        idx = np.where(chessboard == COLOR_NONE)
        idx = list(zip(idx[0], idx[1]))
        mobility=0
        
        for p in idx:
            result=self.test(chessboard,p,-1,self.color)
            if self.color in result:
                mobility+=1

        potentialmobility=0
        
        opidx=np.where(chessboard == -self.color)
        opidx=list(zip(opidx[0],opidx[1]))

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

        value=mobility-potentialmobility

        return value      

    # def minimax(self,board,player,depth=0):

    #     for action in board.get_legal_actions():
    #         board._move(action,self.take)
    #         val,_ = player.minimax(board,self,depth+1) # 切换到假想敌
    #         board._unmove(action) # 撤销走法，回溯

    #         if self.take == "O":
    #             if val > bestVal: # Max
    #                 bestVal,bestAction = val,action
    #         else: # Min
    #             if val < bestVal:
    #                 bestVal,bestAction = val,action
    #     return bestVal,bestAction    

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


    def getscore1(self,idx,chessboard,color,depth,max_depth):
    
        if depth==0:
            return self.evaluate1(chessboard)
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
                            

    # def minimax(self,chessboard,color,idx):
            resultlist=[]
            otherlist=[]
            tempscore=-100000
            for p in idx:
                result=self.test(chessboard, p, -1, color)
                
                if color in result:
                    idx1 = np.where(result == COLOR_NONE)
                    idx1 = list(zip(idx1[0], idx1[1]))

                    minscore=1000000
                    for p1 in idx1:
                        result1=self.test(result,p1,-1,-color)
                   
                        if -color in result1:
                            idx2 = np.where(result1 == COLOR_NONE)
                            idx2 = list(zip(idx2[0], idx2[1]))

                            maxscore=-1000000 
                            for p2 in idx2:
                                result2=self.test(result1,p2,-1,color) 
                                     
                                if color in result2:
                                    idx3 = np.where(result2 == COLOR_NONE)
                                    idx3 = list(zip(idx3[0], idx3[1]))
                                    
                                    minscore2=1000000
                                    for p3 in idx3:
                                        result3=self.test(result2, p3, -1, -color)
                                        if -color in result3:
                                            evalscore=self.evaluate(result3, color)
                                            # print(evalscore)
                                            minscore2=min(minscore2,evalscore)
                               
                                    maxscore=max(maxscore,minscore2)
                              
                            minscore=min(minscore,maxscore)

                    if minscore>tempscore:
                        # print(minscore)
                        resultlist.append(p)
                        tempscore=minscore
                   
                    else: 
                        otherlist.append(p)
            for i in resultlist:
                otherlist.append(i)
         
            return otherlist
                        


    def go(self, chessboard):
        idx = np.where(chessboard == COLOR_NONE)
        idx = list(zip(idx[0], idx[1]))
        self.candidate_list.clear()
        start = time.time()
        self.candidate_list=self.getscore1(idx, chessboard, self.color, 2,2)
        run_time = (time.time() - start)
        print(run_time)
        self.candidate_list=self.getscore(idx, chessboard, self.color, 3,3)
        run_time = (time.time() - start)
        print(run_time)
        # self.candidate_list=self.getscore(idx, chessboard, self.color, self.max_depth2,4)
        # self.candidate_list=self.getscore(idx, chessboard, self.color, self.max_depth3,5)
        # self.candidate_list=self.getscore(idx, chessboard, self.color, self.max_depth3,6)
        # self.candidate_list=self.getscore(idx, chessboard, self.color, self.max_depth3,7)


# time measurement
# start = time.time()
# run_time = (time.time() - start)

def takefirst(elem):
    return elem[0]

if __name__ == '__main__':

    chessboard=[
    [ 0, 0, 0, 0, 0, 0, 0, 0],
    [ 0, 0, 0, 0, 0, 0, 0, 0],
    [ 0, 0, 0, 0, 0, 0, 0, 0],
    [ 0, 0, 0,-1, 1, 0, 0, 0],
    [ 0, 0, 0, 1,-1, 1, 0, 0],
    [ 0, 0, 0, 0, 0, 0, 0, 0],
    [ 0, 0, 0, 0, 0, 0, 0, 0],
    [ 0, 0, 0, 0, 0, 0, 0, 0]
    ] 

    # chessboard=[
    #     [0,0,0,0,],
    #     [0,-1,1,0,],
    #     [0,1,-1,0,],
    #     [0,0,0,0,],
    # ]
    AI=AI(8,-1,5)
    # AI.max_depth=3
    chessboard=np.array(chessboard)
    
    AI.go(chessboard)

    # AI.candidate_list.sort(key=takefirst)
    print(AI.candidate_list)
    