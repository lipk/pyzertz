import table
import os

class Player:
    def __init__(self, name):
        self.marbles = [0,0,0] #white, gray, black
        self.name = name
        
    def __str__(self):
        return self.name
	

pl1 = Player("Odon")
pl2 = Player("Bela")
winner = None  
act = pl1
t=table.Table(3)

t.get(0,0).type=1
t.get(-3,0).type=1
t.get(-2,-1).type=2
print(t)

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

def place(move, t):
    t.marbles[move[2]] -= 1
    t.get(move[0],move[1]).type = move[2]+1
    
def isValidRemove(move,t):
    x = move[0]
    y = move[1]
    if not (-3<=x<=3 and -3<=y<=3 and -3<=x+y<=3):
        return False

    if t.get(x,y).type != 0:
        return False  

    return True
        
        
def remove(move,t):
    t.get(move[0],move[1]).type=-1
    
     
while (not winner):
    os.system('cls')
    print(t)
    print(act.name + " moves")
    print("What do you want? Place a marble, and remove a ring (p), or capture some marbles(c)?")
    
    if input('') == 'p':
        print('Where and which marble do you want to place? (4 3 2 means put marble type 2 to (4,3))')
        move = input('').split(' ')
        if (len(move)>2):
            move = list(map(int, move))
            if isValidPlace(move,t):
                place(move,t)
            else:
                print('You can not cheat!')
                break
        else:
            print("You will not cheat!")
            break
        
        print('Which ring do you want to remove? (4 3 means remove ring (4,3))')
        move = input('').split(' ')
        if (len(move)>1):
            move = list(map(int, move))
            if isValidRemove(move,t):
                remove(move,t)
            else:
                print('You can not cheat!')    
                break
        else:
            print("You will not cheat!")
            break
            
            
    else:
        print('capture')
     

    
    
    
    if (sum(t.marbles) == 0):
        winner = "draw"
        
    if (act.marbles[0]==4 or act.marbles[1]==5 or act.marbles[2]==6):
        winner = act

    if (act.marbles[0]>2 and act.marbles[1]>2 and act.marbles[2]>2):
        winner = act
        
    if (act == pl1):
        act = pl2
    else:
        act = pl1
    
        
print("The winner is: " + winner)