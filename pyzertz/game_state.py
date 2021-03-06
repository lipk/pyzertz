import table
import os
import copy

class Player:
    def __init__(self, name):
        self.marbles = [0,0,0] #white, gray, black
        self.name = name
        
    def __str__(self):
        return self.name + ": white(1):"+str(self.marbles[0])+"  gray(2):"+str(self.marbles[1])+"  black(3):"+str(self.marbles[2])+'\n'
        
    def copy(self):
        p=Player(self.name)
        p.marbles=copy.deepcopy(self.marbles)
        return p
	
class State:
    def __init__(self):
        self.pl1 = Player("Odon")
        self.pl2 = Player("Bela")
        self.t=table.Table(3)
    
        self.winner = None
        self.act=self.pl1
        
        #self.t.get(0,0).type=1
        #self.t.get(-3,0).type=1
        #self.t.get(-2,-1).type=2
        
    def copy(self):
        s = State()
        s.pl1 = self.pl1.copy()
        s.pl2 = self.pl2.copy()
        s.t=self.t.copy()
        if self.act==self.pl1:
            s.act = s.pl1
        else:
            s.act = s.pl2
        
        if self.winner:
            s.winner = self.winner.copy()
        else:
            s.winner = None
        
        return s
        
    def __str__(self):
        s = ''
        s += str(self.t) + str(self.pl1) + str(self.pl2) + '\n'
        return s

    def next_player(self):
        if self.act is self.pl1:
            self.act = self.pl2
        else:
            self.act = self.pl1

def isValidPlace(move, t):
    x = move[0]
    y = move[1]
    color = move[2]
    
    if not (-3<=x<=3 and -3<=y<=3 and -3<=x+y<=3):
        return False
    
    if t.marbles[color]<=0:
        return False
    
    if t.get(x,y).type != 0:
        return False    
    
    return True

def place(move, state):
    s = state.copy()
    s.t.marbles[move[2]] -= 1
    s.t.get(move[0],move[1]).type = move[2]+1
    return s
    
def isValidRemove(move,t):
    x = move[0]
    y = move[1]
    if not (-3<=x<=3 and -3<=y<=3 and -3<=x+y<=3):
        return False

    if t.get(x,y).type != 0:
        return False  
        
    directions = [[1,0],[1,-1],[0,-1],[-1,0],[-1,1],[0,1]] #TODO: expand with [1,0] again. Easier to check all 2-sides.
    i = 0
    isFirstFree = False
    k = -5
    for d in directions:
        xx = x + d[0]
        yy = y + d[1]
        if not (-3<=xx<=3 and -3<=yy<=3 and -3<=xx+yy<=3) or t.get(xx,yy).type==-1:
            if k==i-1:
                break
            else: 
                k=i
                if i == 0:
                    isFirstFree = True       
        #print("direction",i,d,xx,yy)
        i += 1
    
    if k==5 and isFirstFree:
        pass
    elif i==6:
        return False
            
    return True
        
        
def remove(move,state):
    s=state.copy()
    s.t.get(move[0],move[1]).type=-1
    return s
    

def isValidJump(move,t):
    [x1,y1,x2,y2] = move
    if not (isValidTile([x1,y1],t) and isValidTile([x2,y2],t)):
        return False
    z1=-x1-y1
    z2=-x2-y2
    if ((x1-x2)**2+(y1-y2)**2+(z1-z2)**2) !=8:
        return False
    if not (1 <= t.get(x1,y1).type <= 3):
        return False
    if not (1 <= t.get(int((x1+x2)/2),int((y1+y2)/2)).type <= 3):
        return False
    
    return True
    
def isValidTile(tile,t):
    if not(-3<=tile[0]<=3 and -3<=tile[1]<=3 and -3<=tile[0]+tile[1]<=3):
        return False
    if t.get(tile[0],tile[1]).type == -1:
        return False
    return True
    
def isThereAValidCaptureFromOneTile(tile,t):
    if not isValidTile(tile,t):
        return False
    directions = [[1,0],[1,-1],[0,-1],[-1,0],[-1,1],[0,1]]
    
    for d in directions:
        xx=tile[0]+2*d[0]
        yy=tile[1]+2*d[1]
        if isValidTile([xx,yy],t) and isValidJump([tile[0],tile[1],xx,yy],t):
            return True
    
    return False

def isThereAValidCaptureFromAnyTile(t):
    for i in range(-3,4):
        for j in range(-3,4):
            if isValidTile([i,j],t):
                if isThereAValidCaptureFromOneTile([i,j],t):
                    return True
    return False

def jump(move, state):
    s=state.copy()
    [x1,y1,x2,y2] = move
    xx=int((x1+x2)/2)
    yy=int((y1+y2)/2)
    
    s.t.get(x2,y2).type=s.t.get(x1,y1).type
    s.t.get(x1,y1).type=0
    s.act.marbles[s.t.get(xx,yy).type-1] += 1
    s.t.get(xx,yy).type=0
    
    return s
    
##############==============-------- MAIN --------==============##############
'''
s=State()     
while (not s.winner):
    os.system('cls')
    print(s)
    print(s.act.name + " moves")
    
    if not isThereAValidCaptureFromAnyTile(s.t):
        print('Where and which marble do you want to place? (4 3 2 means put marble type 2 to (4,3))')
        print('white - 0 , gray - 1, black - 2')
        move = input('').strip().split(' ')
        if (len(move)>2):
            move = list(map(int, move))
            if isValidPlace(move,s.t):
                s=place(move,s)
            else:
                print('You can not cheat with place!')
                break
        else:
            print("You will not cheat with place!")
            break
        
        #TODO: Check, whether there is a removable ring, or not.
        print('Which ring do you want to remove? (4 3 means remove ring (4,3))')
        move = input('').strip().split(' ')
        if (len(move)>1):
            move = list(map(int, move))
            if isValidRemove(move,s.t):
                s=remove(move,s)
                #TODO: Check, whether there is an island, or not. (if the removed ring had only two neighbours, then there has been vreated an islad. The question is, that which side is the island, and which is the continent. (which is the larger side))
            else:
                print('You can not cheat with remove!')    
                break
        else:
            print("You will not cheat with remove!")
            break
            
            
    else:
        print('From where and where to do you want to jump? (1 2 3 0 means jump from ring(1,2) to ring(3,0))')
        move = input('').strip().split(' ')
        move = list(map(int, move))        
        while(isThereAValidCaptureFromOneTile([move[0],move[1]],s.t)):
            if (len(move)>3):
                if isValidJump(move,s.t):
                    s=jump(move,s)
                    
                else:
                    print('You can not cheat with jump!')
                    break
            else:
                print("You will not cheat with jump!")
                break
            if isThereAValidCaptureFromOneTile([move[2],move[3]],s.t):
                print('Where do you want to jump now? (3 0 means jump from)',move[2],move[3])
                move2=input('').strip().split(' ')
                move=[move[2],move[3],move2[0],move2[1]]
                move = list(map(int, move))
            else:
                break
    
    if (sum(s.t.marbles) == 0):
        s.winner = "draw"
        
    if (s.act.marbles[0]==4 or s.act.marbles[1]==5 or s.act.marbles[2]==6):
        s.winner = s.act

    if (s.act.marbles[0]>2 and s.act.marbles[1]>2 and s.act.marbles[2]>2):
        s.winner = s.act
        
    if (s.act == s.pl1):
        s.act = s.pl2
    else:
        s.act = s.pl1
    
        
print("The winner is: " + str(s.winner.name))
'''
