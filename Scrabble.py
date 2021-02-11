# -*- coding: utf-8 -*-
import turtle
import random
import requests as rq


########
#METODY#
########

def wordCheck(word = 'dom'): 
    r = rq.get('https://sjp.pl/' + word)
    # if r.text.rfind('nie występuje w słowniku') > 0 or r.text.rfind('niedopuszczalne w grach') > 0: return False
    # else: return True
    # print(r.text)
    if r.text.rfind('>występuje w słowniku <') > 0 or r.text.rfind('>dopuszczalne w grach <') > 0: return True
    else: return False

def cell(leng):
    for i in range(4):
        turtle.forward(leng)
        turtle.left(90)  
        
def showBoard(board):
    for line in board:
        print(line , end = "\n")
        
def close():
    screen.bye()
    

def writeInHiddenBoard(hiddenBoard, textOutput, textPos, textOrient, x, y):
    
    move = 0
    
    try:
        for i in textOutput:    
            if textOrient.lower() == 'x':
                if i != ' ':
                    hiddenBoard[x][y+move] = i
                    move += 1
                else: move += 1
            if textOrient.lower() == 'y':
                if i != ' ':
                    hiddenBoard[x+move][y] = i
                    move += 1
                else: move += 1
        return True
    
    except IndexError:
        print("Wyszło poza zakres tablicy")
        return False
        
    print(hiddenBoard)
    

def fillWord(textOutput, hiddenBoard,tuple1):
    
    wordToCheck = textOutput

    if ' ' in textOutput:
        if tuple1[2] == 'x':           
            j = str(hiddenBoard[tuple1[3]][tuple1[4] + textOutput.index(' ')])
            wordToCheck = wordToCheck.replace(' ',j)
                
        if tuple1[2] == 'y':   
            j = str(hiddenBoard[tuple1[3] + textOutput.index(' ')][tuple1[4]])
            wordToCheck = textOutput.replace(' ',j)
    
    return wordToCheck

   
def checkAnalys(check, tuple1, checkedPlayer, updatedSet):
    
    updatingSet = updatedSet   
    word = fillWord(tuple1[0], hiddenBoard,tuple1)
    
    if check.lower() == 't': 
            
            thinking = wordCheck(word)
            if thinking == True:
                writeInHiddenBoard(hiddenBoard, tuple1[0], tuple1[1], tuple1[2], tuple1[3], tuple1[4])
                writeLetTurtle(tuple1[4], tuple1[3], cellSize,tuple1[2],tuple1[0])

                print("Sprawdzone słowo znajduje się w słowniku.")
                
                checkedPlayer.delLetFromHand(tuple1[0])
                updatingSet = checkedPlayer.playerAlphaSet(len(tuple1[0]), updatedSet)
                
                points = addPoints(word)
                checkedPlayer.points += points
                
                if checkedPlayer == player1: drawPlayerSit(-3.5 * 50, (-225) - 80, checkedPlayer)  
                if checkedPlayer == player2: drawPlayerSit(-3.5 * 50, (225) + 20, checkedPlayer) 
                return False, updatingSet
            else:
                print("Sprawdzone słowo nie znajduje się w słowniku.")
                return True, updatingSet       
    
    if check.lower() == 'n':
        writeInHiddenBoard(hiddenBoard, tuple1[0], tuple1[1], tuple1[2], tuple1[3], tuple1[4])
        writeLetTurtle(tuple1[4], tuple1[3], cellSize,tuple1[2],tuple1[0])    
        
        checkedPlayer.delLetFromHand(tuple1[0])
        updatingSet = checkedPlayer.playerAlphaSet(len(tuple1[0]), updatedSet)  
        
        points = addPoints(word)
        checkedPlayer.points += points
                
        if checkedPlayer == player1: drawPlayerSit(-3.5 * 50, (-225) - 80, checkedPlayer)  
        if checkedPlayer == player2: drawPlayerSit(-3.5 * 50, (225) + 20, checkedPlayer) 
        return True, updatingSet
    
    


def writeLetTurtle(x,y,cellSize,textOrient,text):
    turtle.color('black','black')
    turtle.penup()
    turtle.goto(-207 + x * cellSize,194 - y * cellSize)
    turtle.pendown()
    
    if textOrient == 'y': turtle.right(90)
   
    for i in text.upper():
        turtle.write(i, font = style, align = 'center')
        turtle.penup()
        turtle.forward(cellSize)    
        turtle.pendown()
    turtle.setheading(0)


def addPoints(word):
    alphaPoints = {'A': 1,'Ą': 5,'B': 3, 'C': 2,'Ć': 6, 'D': 2, 'E': 1,'Ę': 5, 'F': 5, 'G': 3, 'H': 3, 'I': 1, 'J': 3, 'K': 2, 'L': 2,'Ł': 3,'M': 2, 'N': 1,'Ń': 7, 'O': 1, 'Ó': 5, 'P': 2, 'R': 1, 'S': 1, 'Ś': 5,'T': 2, 'U': 3, 'W': 1, 'Y': 2, 'Z': 1, 'Ź': 9, 'Ż': 5,'?': 0}    
    points = 0
    
    for i in word.upper():
        if i.isalpha(): points += alphaPoints[i]
        else: pass
    return points

#######
#KLASY#
#######
        
class Player:
    
    def __init__(self, ID=0, name = " ", points = 0, letters=[]):
        self.ID = ID
        self.name = name
        self.points = points
        self.letters = []
    
        
    def playerAlphaSet(self,quantity, gameAplhaSet):
        updatedSet = gameAplhaSet 
        for i in range(0,quantity):
            self.letters.append(gameAplhaSet.pop(0))
                  
        return updatedSet
    
    
    def delLetFromHand(self, word):
        for letter in word.upper():
            if letter != ' ':
                self.letters.remove(letter)
            else: pass
    
    
    def showLetters(self):
        print("Twoje iterki to: ", self.letters)
    
        
    
class Letter: 
    
    def __init__(self, letterPoints = 0):
     
        self.letterPoints = letterPoints
    
    
    def gameAlphaSet(self):
        alphaQuantity = {'A': 9,'Ą': 1,'B': 2, 'C': 3,'Ć': 1, 'D': 3, 'E': 7,'Ę': 1, 'F': 1, 'G': 2, 'H': 2, 'I': 8, 'J': 2, 'K': 3, 'L': 3,'Ł': 2,'M': 3, 'N': 5,'Ń': 1, 'O': 6, 'Ó': 1, 'P': 3, 'R': 4, 'S': 4, 'Ś': 1,'T': 3, 'U': 2, 'W': 4, 'Y': 4, 'Z': 5, 'Ź': 1, 'Ż': 1}
        gameAlhaSet = []

        for i in alphaQuantity:
            for j in range(alphaQuantity[i]):
                gameAlhaSet.append(i)

        gameAlphaSet = random.shuffle(gameAlhaSet)
        return gameAlhaSet

#####################
#Tworzenie rozgrywki#
#####################

# name1 = screen.textinput("Ustawienia", "Wpisz imię 1 gracza:")
# name2 = screen.textinput("Ustawienia", "Wpisz imię 2 gracza:")


game = Letter()
gameSet = game.gameAlphaSet()

# player1 = Player(0,str(name1),0)
player1 = Player(0,"Kinga",0)
updatedSet = player1.playerAlphaSet(7,gameSet)

# player2 = Player(1,str(name2),0)
player2 = Player(1,"Mati",0)
updatedSet = player2.playerAlphaSet(7,gameSet)

#########
# TURTLE#
#########
#Ogólne ustawienia turtle
turtle.tracer(False)
turtle.speed('fastest')
# turtle.hideturtle()
turtle.bgcolor('dimgray')
screen = turtle.Screen()
screen.setup(1200,700)
style = ('Arial', 18)
style2 = ('Arial', 7)

#Ustawienia do rysowania planszy
turtle.color('azure2','DarkOliveGreen4')
turtle.pensize(3)
cellSize = 30
cellQuantity = 15 
boardSize = (cellQuantity/2) * cellSize
x,y = -1 * boardSize,-1 * boardSize
i = 0
j = cellQuantity -1

#Rysowanie planszy
turtle.penup()
turtle.goto(x,y)
turtle.begin_fill()

while y < boardSize:
    turtle.penup()
    turtle.goto(x,y)
    turtle.pendown()
    x += cellSize
    cell(cellSize)
    turtle.penup()
    turtle.goto(x,y)
    turtle.pendown()
    turtle.write(str(j)+','+str(i), font = style2, align = "right")
    i += 1
    
    if i >= cellQuantity: i = 0   
    if x >= boardSize:
        x = -1 * boardSize
        y += cellSize
        j -= 1

turtle.penup()
turtle.goto(x,y)
turtle.end_fill()

#Ustawienia dla stanowiska gracza           
cellSizeB = 50 

#Rysowanie stanowiska gracza + wpisanie liter
def drawPlayerSit(x,y,player):
    
    i = 0
    cellSizeB = 50
    turtle.color('azure2','DarkSlateGray')
    turtle.pensize(4)
    turtle.penup()
    turtle.goto(x,y)
    turtle.begin_fill()

    while x < 3.5 * cellSizeB:
        turtle.penup()
        turtle.goto(x,y)
        turtle.pendown()
        x += cellSizeB
        cell(cellSizeB)
        turtle.penup()
        turtle.forward(cellSizeB/2)
        turtle.write(player.letters[i], font = style, align = 'center')  
        turtle.pendown()
        i += 1
        
    turtle.end_fill()
    
drawPlayerSit(-3.5 * cellSizeB, (-1* boardSize) - 80, player1)
drawPlayerSit(-3.5 * cellSizeB, boardSize + 20, player2)

turtle.penup()
turtle.goto(-3.5 * cellSizeB - 50, (-1* boardSize) - 80)
turtle.pendown()
turtle.write(player1.name, font = style, align = 'center')

turtle.penup()
turtle.goto(-3.5 * cellSizeB - 50, boardSize + 20)
turtle.pendown()
turtle.write(player2.name, font = style, align = 'center') 

def playerRound(player, firstRound):
         
    
    goNext = False  
    quantitySecure = []
    
    while goNext == False:
        
        if firstRound == False:
            textOutput = screen.textinput("Gracz: " + player.name,"Wpisz słowo: ") 
            quantitySecure = player.letters.copy()
            quantitySecure.append(' ')
            j = len(str(textOutput))
            
            if ' ' in textOutput:
                for i in textOutput.upper():
                    if i not in quantitySecure: break        
                    if i in quantitySecure: 
                        quantitySecure.remove(i) 
                        j -= 1                
                if j < 1 : goNext = True 
            else: textOutput = screen.textinput("Błąd" , "Słowo musi zawierać spację.")
    
        if firstRound == True:
            textOutput = screen.textinput("Gracz: " + player.name,"Wpisz słowo: ") 
            quantitySecure = player.letters.copy()
            
            j = len(str(textOutput))
            
            
            for i in textOutput.upper():
                if i not in quantitySecure: break        
                if i in quantitySecure: 
                    quantitySecure.remove(i) 
                    j -= 1                
            if j < 1 : goNext = True
            
    
    textOrient = screen.textinput("Gracz: " + player.name,"Wpisz x(poziomo)/y(pionowo): ")   
    while textOrient.lower() != 'x' and textOrient.lower() != 'y': textOrient = screen.textinput("Gracz: " + player.name,"Błąd, wpisz x/y: ")
    
    if firstRound == True or firstRound == False:
       
        textPos = screen.textinput("Gracz: " + player.name,"Wpisz pozycję początkową (np. 1,4): ")
        goNext = False
        while goNext == False:    
            while ',' not in textPos:textPos = screen.textinput("Gracz: " + player.name,"Błąd, podaj pozycję początkową (np. 1,4): ")         
            if ',' in textPos:    
                try:
                    index = textPos.index(',')
                    x = int(textPos[:index])
                    y = int(textPos[index + 1:])  
                except: textPos = screen.textinput("Gracz: " + player.name,"Błąd, podana pozycja musi być liczbą po przecinku: ")     
            if x <= 14 and x>= 0:
                if y <= 14 and y >=0:                                
                    if textOrient.lower() == 'x':
                        if y + len(textOutput) > 15: textPos = screen.textinput("Gracz: " + player.name,"Błąd, wyraz wyjdzie poza tablicę: ")
                        else: goNext = True
                    if textOrient.lower() == 'y':
                        if x + len(textOutput) > 15: textPos = screen.textinput("Gracz: " + player.name,"Błąd, wyraz wyjdzie poza tablicę: ")
                        else: goNext = True                            
                else: textPos = screen.textinput("Gracz: " + player.name,"Błąd, podaj pozycję początkową (np. 1,4): ")
            else: textPos = screen.textinput("Gracz: " + player.name,"Błąd, podaj pozycję początkową (np. 1,4): ")   
    return textOutput, textPos, textOrient, x, y


def passCheck(player, i):
    passMove = screen.textinput(player.name, "Czy pasujesz ruch? t(tak)/n(nie)")
    enemyMove = False
    
    while passMove.lower() != 't' and passMove.lower() != 'n':
        passMove = screen.textinput(player.name, "Czy pasujesz ruch? t(tak)/n(nie)")
    if passMove.lower() == 't': 
        i+=1
        enemyMove = True
    else: 
        i = 0
    return i, enemyMove
           
turtle.tracer(True)
turtle.listen()

###########
#Rozgrywka#
###########     

hiddenBoard = [[0 for x in range(15)] for x in range(15)]
showBoard(hiddenBoard)
passedMove = (0, False)

# Ustawienia pierwszej rundy
firstRound = True
checkMove1 = (True, updatedSet)
checkMove2 = (True, updatedSet)

while passedMove[0] <= 2:
    
    
    if checkMove1[0] == True or passedMove[1] == True:
        passedMove = passCheck(player1, passedMove[0])
        if passedMove[0] == 0: 
            tuple1 = playerRound(player1, firstRound)
            firstRound = False
            
            word = fillWord(tuple1[0], hiddenBoard,tuple1)
            check = screen.textinput(player2.name, "Czy sprawdzasz słowo"+ word.upper() + " t(tak)/n(nie)?") 
            checkMove2 = checkAnalys(check, tuple1, player1, updatedSet)
            updatedSet = checkMove2[1]
            print("Gracz ", player1.name, " ma: ", player1.points, " punktów.")
            
    if checkMove2[0] == True or passedMove[1] == True:
        passedMove = passCheck(player2, passedMove[0])
        if passedMove[0] == 0:
            tuple2 = playerRound(player2, firstRound)
            firstRound = False
            
            word = fillWord(tuple2[0], hiddenBoard,tuple2)
            check2 = screen.textinput(player1.name, "Czy sprawdzasz słowo "+ word.upper() + " t(tak)/n(nie)?")
            chceckMove1 = checkAnalys(check2, tuple2, player2, updatedSet)
            updatedSet = checkMove1[1]
            print("Gracz ", player2.name, " ma: ", player2.points, " punktów.")

print("PODSUMOWANIE------------------------")
print(player1.name, " - ", player1.points)
print(player2.name, " - ", player2.points)
if player1.points > player2.points: print("Wygrywa gracz: " + player1.name)
if player1.points == player2.points: print("Remis!")
if player2.points > player1.points: print("Wygrywa gracz: " + player2.name)


turtle.mainloop()




