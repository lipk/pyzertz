import copy

class Tile:
    #type = 0
    #row = 0
    #col = 0
    
    def __init__(self , type : int, col : int, row : int):
        self.type=type  #-1 - not exists, 0 - empty, 1 - white, 2 - gray, 3 - black 
        self.col=col
        self.row=row

    def __str__(self):
        return str(self.type)
        
    def coord(self):
        return("col: " + str(self.col) + " row: " + str(self.row))
        
    def copy(self):
        t=Tile(self.type,self.col,self.row)
        t.type=self.type
        t.col=self.col
        t.row=self.row
    
    
    
class Table:
    size = 0
    tiles = []
    marbles = [6,8,10] #white, gray, black
    
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

    def copy(self):
        t = Table(3)
        t.size=self.size
        for i in range(-3,4):
            for j in range(-3,4):
                if -3 <= i+j <=3:
                    print("Kakaaiiiiiiiiii ",self.tiles[i][j])
                    t.tiles[i][j]=self.tiles[i][j].copy()
        t.marbles = copy.deepcopy(self.marbles)
            
            
        
        
    def __str__(self):
        #return '\n'.join([' '.join(map(str,row) for row in self.tiles])
		#return '\n'.join(map(lambda row:map(str,row),self.tiles))
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
           

