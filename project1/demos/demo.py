import numpy as np
import random
import time
COLOR_BLACK=-1
COLOR_WHITE=1
COLOR_NONE=0
random.seed(0)
#don't change the class name
class AI(object):
#chessboard_size, color, time_out passed from agent
    def __init__(self, chessboard_size, color, time_out):
        self.chessboard_size = chessboard_size
    #You are white or black
        self.color = color
    #the max time you should use, your algorithm's run time must not exceed the time limit.
        self.time_out = time_out
    # You need add your decision into your candidate_list. System will get the end of 
    # your candidate_list as your decision .
        self.candidate_list = []

    # The input is current chessboard.
    def go(self, chessboard):
    # Clear candidate_list, must do this step
        self.candidate_list.clear()
    #==================================================================
    #Write your algorithm here
    #Here is the simplest sample:Random decision
        # idx = np.where(chessboard == COLOR_NONE)
        # idx = list(zip(idx[0], idx[1]))

        blacklist=[]
        whitelist=[]
        
        for i in range(self.chessboard_size):
            row=chessboard[i,:]
            reverse=row[::-1]
            if 1 in row and -1 in row and 0 in row:
                for j in range(len(row)):
                    if row[j]!=0:
                        left=j
                        break
                for j in range(len(reverse)):
                    if reverse[j]!=0:
                        right=len(reverse)-j-1
                        break

                if row[left] == 1:
                    if left!=0:
                        blacklist.append((i,left-1))
                else:
                    if left!=0:
                        whitelist.append((i,left-1))

                if row[right] == 1:
                    if right!=len(row)-1:
                        blacklist.append((i,right+1))
                else:
                    if right!=len(row)-1:
                        whitelist.append((i,right+1))
        
        for i in range(self.chessboard_size):
            row=chessboard[:,i]
            reverse=row[::-1]
            if 1 in row and -1 in row and 0 in row:
                for j in range(len(row)):
                    if row[j]!=0:
                        left=j
                        break
                for j in range(len(reverse)):
                    if reverse[j]!=0:
                        right=len(reverse)-j-1
                        break
                    
                if row[left] == 1:
                    if left!=0:
                        blacklist.append((left-1,i))
                else:
                    if left!=0:
                        whitelist.append((left-1,i))

                if row[right] == 1:
                    if right!=len(row)-1:
                        blacklist.append((right+1,i))
                else:
                    if right!=len(row)-1:
                        whitelist.append((right+1,i))

        for i in range(2,self.chessboard_size):
            row=[]
            for j in range(i+1):
                row.append(chessboard[j,i-j])
                # print((j,i-j))
                # print(chessboard[j,i-j])
            reverse=row[::-1]
            # print(row)
            if 1 in row and -1 in row and 0 in row:
                # print('True')
                for j in range(len(row)):
                    if row[j]!=0:
                        left=j
                        break

                for j in range(len(reverse)):
                    if reverse[j]!=0:
                        right=len(reverse)-j-1
                        break
                        
                if row[left] == 1:
                    if left!=0 and (left-1,i-(left-1)) not in blacklist:
                        blacklist.append((left-1,i-(left-1)))
                else:
                    if left!=0 and (left-1,i-(left-1)) not in whitelist:
                        whitelist.append((left-1,i-(left-1)))

            
                if row[right] == 1:
                    if right!=len(row)-1 and (right+1,i-(right+1)) not in blacklist:
                        blacklist.append((right+1,i-(right+1)))
                else:
                    if right!=len(row)-1 and (right+1,i-(right+1)) not in whitelist:
                        whitelist.append((right+1,i-(right+1)))
            
        for i in range(2,self.chessboard_size):
            row=[]
            for j in range(i+1):
                row.append(chessboard[j,self.chessboard_size-1-(i-j)])
                # print((j,self.chessboard_size-1-(i-j)))
            reverse=row[::-1]

            if 1 in row and -1 in row and 0 in row:
                for j in range(len(row)):
                    if row[j]!=0:
                        left=j
                        break

                for j in range(len(reverse)):
                    if reverse[j]!=0:
                        right=len(reverse)-j-1
                        break
                        
                if row[left] == 1:
                    if left!=0 and (left-1,self.chessboard_size-1-(i-(left-1))) not in blacklist:
                        blacklist.append((left-1,self.chessboard_size-1-(i-(left-1))))
                else:
                    if left!=0 and (left-1,self.chessboard_size-1-(i-(left-1)))not in whitelist:
                        whitelist.append((left-1,self.chessboard_size-1-(i-(left-1))))

            
                if row[right] == 1:
                    if right!=len(row)-1 and (right+1,self.chessboard_size-1-(i-(right+1))) not in blacklist:
                        blacklist.append((right+1,self.chessboard_size-1-(i-(right+1))))
                else:
                    if right!=len(row)-1 and (right+1,self.chessboard_size-1-(i-(right+1))) not in whitelist:
                        whitelist.append((right+1,self.chessboard_size-1-(i-(right+1))))
                
        for i in range(2,self.chessboard_size-1):
            row=[]
            for j in range(i+1):
                row.append(chessboard[self.chessboard_size-1-j,(i-j)])
                # print((self.chessboard_size-1-j,(i-j)))
            reverse=row[::-1]

            if 1 in row and -1 in row and 0 in row:
                for j in range(len(row)):
                    if row[j]!=0:
                        left=j
                        break

                for j in range(len(reverse)):
                    if reverse[j]!=0:
                        right=len(reverse)-j-1
                        break
                        
                if row[left] == 1:
                    if left!=0 and (self.chessboard_size-1-(left-1),i-(left-1)) not in blacklist:
                        blacklist.append((self.chessboard_size-1-(left-1),i-(left-1)))
                else:
                    if left!=0 and (self.chessboard_size-1-(left-1),i-(left-1))not in whitelist:
                        whitelist.append((self.chessboard_size-1-(left-1),i-(left-1)))

            
                if row[right] == 1:
                    if right!=len(row)-1 and (self.chessboard_size-1-(right+1),i-(right+1)) not in blacklist:
                        blacklist.append((self.chessboard_size-1-(right+1),i-(right+1)))
                else:
                    if right!=len(row)-1 and (self.chessboard_size-1-(right+1),i-(right+1)) not in whitelist:
                        whitelist.append((self.chessboard_size-1-(right+1),i-(right+1)))

        for i in range(2,self.chessboard_size-1):
            row=[]
            for j in range(i+1):
                row.append(chessboard[self.chessboard_size-1-j,self.chessboard_size-1-(i-j)])
                # print((self.chessboard_size-1-j,self.chessboard_size-1-(i-j)))
            reverse=row[::-1]

            if 1 in row and -1 in row and 0 in row:
                for j in range(len(row)):
                    if row[j]!=0:
                        left=j
                        break

                for j in range(len(reverse)):
                    if reverse[j]!=0:
                        right=len(reverse)-j-1
                        break
                        
                if row[left] == 1:
                    if left!=0 and (self.chessboard_size-1-(left-1),self.chessboard_size-1-(i-(left-1))) not in blacklist:
                        blacklist.append((self.chessboard_size-1-(left-1),self.chessboard_size-1-(i-(left-1))))
                else:
                    if left!=0 and (self.chessboard_size-1-(left-1),self.chessboard_size-1-(i-(left-1)))not in whitelist:
                        whitelist.append((self.chessboard_size-1-(left-1),self.chessboard_size-1-(i-(left-1))))

            
                if row[right] == 1:
                    if right!=len(row)-1 and (self.chessboard_size-1-(right+1),self.chessboard_size-1-(i-(right+1))) not in blacklist:
                        blacklist.append((self.chessboard_size-1-(right+1),self.chessboard_size-1-(i-(right+1))))
                else:
                    if right!=len(row)-1 and (self.chessboard_size-1-(right+1),self.chessboard_size-1-(i-(right+1))) not in whitelist:
                        whitelist.append((self.chessboard_size-1-(right+1),self.chessboard_size-1-(i-(right+1))))

        if self.color==COLOR_BLACK:
            self.candidate_list=blacklist
        else:
            self.candidate_list=whitelist


    #==============Find new pos========================================
    # Make sure that the position of your decision in chess board is empty. 
    # If not, the system will return error.
    # Add your decision into candidate_list, Records the chess board
    # You need add all the positions which is valid
    # candiidate_list example: [(3,3),(4,4)]
    # You need append your decision at the end of the candiidate_list, 
    # we will choice the last element of the candidate_list as the position you choose
    # If there is no valid position, you must return an empty list.

# time measurement
# start = time.time()
# run_time = (time.time() - start)

def takefirst(elem):
    return elem[0]

if __name__ == '__main__':
    AI=AI(5,-1,5)
    # chessboard=[
    # [ 0, 0, 0, 0, 0, 0, 0, 0],
    # [ 0, 0, 0, 0, 0, 0, 0, 0],
    # [ 0, 0, 0, 0, 0, 1, 0, 0],
    # [ 0, 0, 0, 1, 1, 0, 0, 0],
    # [ 0, 0, 0, 1,-1, 0, 0, 0],
    # [ 0, 0,-1,-1,-1, 0, 0, 0],
    # [ 0, 0,-1, 1, 0, 0, 0, 0],
    # [ 0, 0, 0, 0, 0, 0, 0, 0]
    # ] 
    chessboard=[
        [0,0,0,0,0,],
        [0,0,0,0,0,],
        [0,0,0,0,0,],
        [0,0,0,0,0,],
        [0,0,0,0,0,],
    ]
    chessboard=np.array(chessboard)
    AI.go(chessboard)
    AI.candidate_list.sort(key=takefirst)
    print(AI.candidate_list)
    