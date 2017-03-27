class Tile:
    type = 0
    row = 0
    col = 0
    
    def __init__(self , type : int, col : int, row : int):
        self.type=type
        self.col=col
        self.row=row

    def __str__(self):
        return str(self.type)
        
    def coord(self):
        return("col: " + str(self.col) + " row: " + str(self.row))
    
    
    
class Table:
    size = 0
    tiles = []
    
    def __init__(self, size : int):
        self.size=size
        
        for i in range(self.size+1):
            row1 = []
            row2 = []
            for j in range(i+self.size+1):
                row1.append(Tile(0,j-i,i-self.size))
                if i != self.size:
                    row2.append(Tile(0,j-self.size,self.size-i))
            if i != self.size:
                self.tiles.insert(i,row2)    
            self.tiles.insert(i,row1)    
                
        
        
    def __str__(self):
        s=""
        for row in self.tiles:
            for t in row:
                s+=str(t)
                s+=' '
            s+="\n"
        return s 
            
    def get(self , col : int , row : int):
        if col+row > -self.size-1 and col+row < self.size+1:
            return self.tiles[row+self.size][col+self.size+min(0,row)]
        else:
            pass
            
t=Table(3)

t.get(0,0).type=1
t.get(-3,0).type=1
t.get(-2,-1).type=2

print(t)

print("------------")
for i in range(6):
    for j in range(6):
        print(i,j)
#print("-3:" , t.get(-3,-3).coord())

