import table
import os
import copy

class Player:
    def __init__(self, name):
        self.marbles = [0,0,0] #white, gray, black
        self.name = name
        
    def __str__(self):
        return self.name
        
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
        
        self.t.get(0,0).type=1
        self.t.get(-3,0).type=1
        self.t.get(-2,-1).type=2
        
    def copy(self):
        s = State()
        s.pl1 = self.pl1.copy()
        s.pl2 = self.pl2.copy()
        s.t=self.t.copy()
        s.act = self.act.copy()
        
        if self.winner:
            s.winner = self.winner.copy()
        else:
            s.winner = None
        
        return s

s=State() 

#print(t)

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
    print("kukiiiiiiiiiiiii",move)
    s.t.get(move[0],move[1]).type = move[2]+1
    return s
    
def isValidRemove(move,t):
    x = move[0]
    y = move[1]
    if not (-3<=x<=3 and -3<=y<=3 and -3<=x+y<=3):
        return False

    if t.get(x,y).type != 0:
        return False  
        
    directions = [[1,0],[1,-1],[0,-1],[-1,0],[-1,1],[0,1]]
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
    if ((x1-x2)**2+(y1-y2)**2)**0.5 !=2:
        return False
    if not (1 <= t.get((x1+x2)/2,(y1+y2)/2).type <= 3):
        return False
    
    return True

def isThereAValidCaptureFromOneTile(tile,t):
    directions = [[1,0],[1,-1],[0,-1],[-1,0],[-1,1],[0,1]]
    
    for d in directions:
        if isValidJump(tile[0],tile[1],t.get(tile[0]+2*d[0],tile[1]+2*d[1])):
            pass
    

     
while (not s.winner):
    os.system('cls')
    print(s.t,'kuki')
    print(s.act.name + " moves")
    print("What do you want? Place a marble, and remove a ring (p), or capture some marbles(c)?")
    
    if input('') == 'p':
        print('Where and which marble do you want to place? (4 3 2 means put marble type 2 to (4,3))')
        move = input('').split(' ')
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
        
        print('Which ring do you want to remove? (4 3 means remove ring (4,3))')
        move = input('').split(' ')
        if (len(move)>1):
            move = list(map(int, move))
            if isValidRemove(move,s.t):
                s=remove(move,s)
            else:
                print('You can not cheat with remove!')    
                break
        else:
            print("You will not cheat with remove!")
            break
            
            
    else:
        print('From where and where to do you want to jump? (1 2 3 0 means jump from ring(1,2) to ring(3,0))')
        move = input('').split(' ')
        if (len(move)>3):
            move = list(map(int, move))
            if isValidJump(move,s.t):
                pass
                #jump(move,s.t)
        else:
            print("You will not cheat with jump!")
    
    
    
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
    
        
print("The winner is: " + s.winner)