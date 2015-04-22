from graphics import *
from ButtonClass import *
class Grid:
    def __init__(self,win):
        '''Constructs the game grid'''
        self.width=win.getWidth()
        self.height=win.getHeight()
        self.win= win
        self.win.setCoords(0,600,1000,0)
        self.grid = []
        self.squareWidth = 50
        self.squareHeight = 50
        

    def drawGrid(self):
        '''Draws the grid'''
        rect=Rectangle(Point(0,0),Point(1000,600))
        rect.draw(self.win)
        rect.setOutline('gray')
        rect.setFill('gray')
        for x in range(1,11):
            row =[]
            for y in range(1,10):
                square= Rectangle(Point((x*self.squareWidth-self.squareWidth*.5)+.22*self.width,
                                        (y*self.squareHeight-self.squareHeight*.5)+self.height*.05),
                                  Point((x*self.squareWidth+self.squareWidth*.5)+.22*self.width,
                                        (y*self.squareHeight+self.squareHeight*.5)+self.height*.05))
                square.draw(self.win)
                square.setFill("black")
                square.setOutline("white")
                row.append(square)
            self.grid.append(row)

        self.quitB=Button(self.win,Point(self.width/2,self.height-30),50,40,'black','Quit')
        self.quitB.setTextColor('white')

    def getWin(self):
        '''returns the graphical window'''
        return self.win

    def getQuitB(self):
        '''returns the quit button'''
        return self.quitB
    
    def gridPoint(self, x, y):
        '''returns the centerpoint of a given grid square'''
        return self.grid[x][y].getCenter()
        

    def moveGrid(self):
        '''moves the grid so a different portion of the board is shown'''
        for row in self.grid:
            for square in row:
                for i in range(20):
                    square.move(-5,5)
            

    def closeGrid(self):
        '''closes the grid'''
        self.win.close()
        

