from grid import *
from playerCollection import *
from gamePlay import *

def main():
    #creates the splash screen
    win=GraphWin("Diagonal Dominoes",1000,600)
    win.setCoords(0,600,1000,0)
    win.setBackground("gray")
    text=Text(Point(500,120),"Diagonal Dominoes")
    text.draw(win)
    text.setSize(36)
    gameB=Button(win,Point(350,300),200,150,'black',"Play Game")
    gameB.setTextColor('white')
    gameB.setTextSize(24)
    instB=Button(win,Point(650,300),200,150,'black',"Instructions")
    instB.setTextColor('white')
    instB.setTextSize(24)
    x=100
    y=500
    for i in range(6):
        c1=color_rgb(randrange(255),randrange(255),randrange(255))
        c2=color_rgb(randrange(255),randrange(255),randrange(255))
        tile = Tile(c1,c2,win)
        tile.drawTile(Point(x,y),Point(x+50,y))
        x+=150
    pt=win.getMouse()
    #until the playgame button is clicked, gets new clicks and/or displays
    #instructions
    while not gameB.isClicked(pt):
        if instB.isClicked(pt):
            instRect=Rectangle(Point(245,100),Point(755,375))
            instRect.setFill('white')
            instRect.draw(win)
            instMess=Text(Point(530,230),
            "In this two-person game, each player gets five tiles, each with\
            \ntwo colors (as below). The first tile chosen is placed \
            \nhorizontally on the bottom-left corner of the board.\
            \nThe next player must place a tile one slot above it and one\
            \nto the right, matching the left-most color of their new tile to\
            \nthe right-most color of the last tile placed on the board. The\
            \ngame ends when either a player has run out of tiles (they win),\
            \nor has no more valid moves to make (they lose). Give it a try\
            \nand it will start to make sense. Have fun!\n\n(click to return)")
            instMess.draw(win)
            instMess.setSize(18)
            win.getMouse()
            instRect.undraw()
            instMess.undraw()
        pt=win.getMouse()

    #creates the game grid
    gameB.die()
    instB.die()
    grid = Grid(win)
    win.setBackground("gray")
    grid.drawGrid()
    quitB=grid.getQuitB()

    #sets up each player collection
    player1=PlayerCollection(win,Point(120,50),1)
    player2 = PlayerCollection(win,Point(880,50),2)
    player1.displayTiles()
    player1.humanSetup()
    player2.displayTiles()

    #starts the game 
    game=GamePlay(win,grid,player1,player2,quitB)
    game.playGame()

       

main()




