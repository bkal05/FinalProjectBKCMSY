import pygame
import sys
import math
import random


# Car class used for car objects
class Car:
    def __init__(self, name, orient, long, rowPos, colPos):
        self.name = name
        self.orient = str(orient)
        self.long = int(long)
        self.rowPos = int(rowPos)
        self.colPos = int(colPos)
        self.front = int(self.frontOfCar())
        self.rear = int(self.backOfCar())

    # method to determine the back of the cars
    def backOfCar(self):
        if self.orient == "v": # if there is a car vertical, make sure it goes by rows
            return self.rowPos
        else: # if the car is not vertical (horizontal), make sure it goes by columns
            return self.colPos

    # method to determine the front of the car
    def frontOfCar(self):
        if self.orient == "v": # if the car is vertical, make it go down by rows by the car's length
            return (self.rowPos + (int(self.long)))
        else: # if the car is horizontal, make it go across by columns by the cars length
            return (self.colPos + (int(self.long)))


# Game class that will check legal placement, import puzzle from pygame, and allow cars to move
class Game:
    def __init__(self):
        self.listOfCars = self.loadGame()
        self.allCars = []
        self.board = [
            [" ~ ", " ~ ", " ~ ", " ~ ", " ~ ", " ~ "],
            [" ~ ", " ~ ", " ~ ", " ~ ", " ~ ", " ~ "],
            [" ~ ", " ~ ", " ~ ", " ~ ", " ~ ", " ~ "],
            [" ~ ", " ~ ", " ~ ", " ~ ", " ~ ", " ~ "],
            [" ~ ", " ~ ", " ~ ", " ~ ", " ~ ", " ~ "],
            [" ~ ", " ~ ", " ~ ", " ~ ", " ~ ", " ~ "]
        ]
        # make sure colors appear in RGB format
        self.red = 255, 0, 0
        self.green = 0, 255, 0
        self.blue = 0, 0, 255
        self.black = 0, 0, 0
        self.yellow = 255, 255, 0
        self.size = int(100)
        self.boardSide = self.size * 6
        self.screen = pygame.display.set_mode((self.boardSide, self.boardSide))
        self.listOfSprites = []

    # method that loads the game file and put the contents in it into a list
    def loadGame(self):
        gameFile = open(sys.argv[1], "r")
        content = gameFile.readlines()
        gameFile.close()
        for x in range(len(content)):
            content[x].replace("\n", "")
        return content

    # method sets up the GUI
    def setup(self):
        pygame.init()
        screen = self.screen
        screen.fill((255, 255, 255))
        count = 0
        # for loop that traverses until i = 6
        for i in range(6):
            # for loop that traverses until x = 6
            for x in range(6):
                if count % 2 == 0: # if current loop value is even
                    pygame.draw.rect(screen, (255, 255, 255), [self.size * x, self.size * i, self.size, self.size])
                else: # if current loop value is odd
                    pygame.draw.rect(screen, self.black, [self.size * x, self.size * i, self.size, self.size])
                count += 1
            count -= 1
        pygame.draw.rect(screen, self.green, [500, 200, 100, 100])
        # for loop to traverse when "car" is one of the cars listed
        for car in self.allCars:
            long_side = int(((self.size * (car.long)) - 10))
            short_side = int(90)
            x = ((car.colPos) * self.size + (5))
            y = ((car.rowPos) * self.size + (5))
            # if it is the red (main) car
            if car.name == 0:
                image = pygame.Surface((long_side, short_side))
                sprite = pygame.draw.rect(image, self.red, (0, 0, ((self.size * (car.long)) - 10), (self.size - 10)))
            # if the car is longer than 2 (yellow car)
            elif car.long > 2:
                # if it is faced horizontally
                if car.orient == "h":
                    image = pygame.Surface((long_side, short_side))
                    sprite = pygame.draw.rect(image, self.yellow,
                                              (0, 0, ((self.size * car.long) - 10), (self.size - 10)))
                # if it is faced vertically
                else:
                    image = pygame.Surface((short_side, long_side))
                    sprite = pygame.draw.rect(image, self.yellow,
                                              (0, 0, (self.size - 10), ((self.size * car.long) - 10)))
            # if it is a car of length 2 (blue car)
            else:
                # if it is faced horizontally
                if car.orient == "h":
                    image = pygame.Surface((long_side, short_side))
                    sprite = pygame.draw.rect(image, self.blue, (0, 0, ((self.size * car.long) - 10), (self.size - 10)))
                # if it is faced vertically
                else:
                    image = pygame.Surface((short_side, long_side))
                    sprite = pygame.draw.rect(image, self.blue, (0, 0, (self.size - 10), ((self.size * car.long) - 10)))
            screen.blit(image, (x, y))
        pygame.display.update()

    # this function determines where the user is clicking and to locate the new coordinate placement of the car
    # these new coords are then returned and legal placement is checked
    def movement(self):
        complete = False
        marker = 0
        target = None
        # while loop that runs until movement is finished
        while complete == False:
            ev = pygame.event.get()
            # for loop that runs for event
            for event in ev:
                # if user wants to quit
                if event.type == pygame.QUIT:
                    pygame.quit
                # if user clicks on the mouse
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    # if the marker is 0 (initial)
                    if marker == 0:
                        marker = 1
                        origin = pygame.mouse.get_pos()
                        originX = origin[0] // 100
                        originY = origin[1] // 100
                        # if the board is not empty at the coordinate (user clicks a car)
                        if self.board[originY][originX] != " ~ ":
                            target = int(self.board[originY][originX])
                            car = self.allCars[target]
                            num = int(car.name)
                        # if the user clicks on a blank space (not a car)
                        else:
                            marker = 0
                            print("please click on a car")
                    # if the marker is 1 (after first click)
                    elif marker == 1:
                        newPos = pygame.mouse.get_pos()
                        nCol = newPos[0] // 100
                        nRow = newPos[1] // 100
                        return car, nCol, nRow

    # method to create car objects to add a new car
    def addCar(self, name, orient, long, rowPos, colPos):
        return Car(name, orient, long, rowPos, colPos)

    # method that will conglomerate all of the cars to one list
    def carGen(self):
        # for loop that traverses through all of the cars
        for x in range(len(self.listOfCars)):
            self.listOfCars[x].replace("\n", "")
            spec = self.listOfCars[x].split(",")
            orient = spec[0]
            long = spec[1]
            rowPos = spec[2]
            colPos = spec[3]

            newCar = self.addCar(x, orient, long, rowPos, colPos)

            self.allCars.append(newCar)

    # method that updates the board with the new cars and their coordinates
    def updateBoard(self):
        # for loops to traverse through each car
        for car in self.allCars:
            # if the car is horizontal
            if car.orient == "h":
                # for loop that traverses through car length
                for x in range(int(car.long)):
                    # if the car is less than 10
                    if car.name < 10:
                        self.board[int(car.rowPos)][int(car.colPos) + x] = " " + str(car.name) + " "
                    # if the car is greater than 10
                    elif car.name >= 10:
                        self.board[int(car.rowPos)][int(car.colPos) + x] = str(car.name) + " "
            # if the car is vertical
            elif car.orient == "v":
                # for loop that traverses through car length
                for x in range(int(car.long)):
                    # if the car is less than 10
                    if car.name < 10:
                        self.board[int(car.rowPos) + x][int(car.colPos)] = " " + str(car.name) + " "
                    # if the car is greater than 10
                    elif car.name >= 10:
                        self.board[int(car.rowPos) + x][int(car.colPos)] = str(car.name) + " "

    # function to check the legal placement of the move
    # checks to verify that there is no car between the move and it is not out of bounds
    def isLegal(self, carNum, newRow, newCol):
        nRow = int(newRow)
        nCol = int(newCol)
        car = self.allCars[carNum]
        deltaR = int(nRow - car.rowPos)
        deltaC = int(nCol - car.colPos)
        # if the car is horizontal (horizontal movement)
        if car.orient == "h":
            # if the new row inputted is not the same as the cars row position
            if nRow != car.rowPos:
                return 0
            # if the distance between the colomns is greater than 0
            elif deltaC > 0:
                # for loop that traverses through the spaces between the moves
                for i in range(int(deltaC)):
                    # if the coordinate between the car's rear and the spaces horizontal it has to move is occupied
                    if self.board[car.rowPos][(car.rear + (1 + i))] != " ~ ":
                        # if it is a car
                        if int(self.board[car.rowPos][(car.rear + (1 + i))]) == int(car.name):
                            pass
                        else:
                            return 0
                   # if the column position + change in columns is greater than 6 (impossible)
                    elif (car.colPos + (deltaC)) > 6:
                        return 0
                    else:
                        return 1
            # if the change in columns is less than 0
            elif deltaC < 0:
                # for loop that traverses between distance between columns (fabs is abs but always returns a float)
                for i in range(int(math.fabs(deltaC))):
                    # # if the coordinate between the car's column position and spaces traversed is occupied
                    if self.board[car.rowPos][(car.colPos - (1 + i))] != " ~ ":
                        # if it is a car
                        if int(self.board[car.rowPos][(car.colPos - (1 + i))]) == int(car.name):
                            pass
                        else:
                            return 0
                    # if the column position plus the change in columns is less than 0
                    elif (car.colPos + (deltaC)) < 0:
                        return 0
                    else:
                        return 1
        # if the car is vertical
        elif car.orient == "v":
            # if the user's column is not the same as the column position of the car
            if nCol != car.colPos:
                return 0
            # if the change in rows is greater than 0
            elif deltaR > 0:
                # for loop that traverses the spaces between the rows
                for i in range(int(deltaR)):
                    # if the space between the car and the traversed rows is occupied
                    if self.board[(car.rowPos + (car.long - 1) + (1 + i))][(car.colPos)] != " ~ ":
                        # if the occupied space is a car
                        if int(self.board[(car.rowPos + (car.long - 1) + (1 + i))][(car.colPos)]) == int(car.name):
                            pass
                        else:
                            return 0
                    # if the car's row position plus the change in rows is greater than 6 (impossible)
                    elif (car.rowPos + (deltaR)) > 6:
                        return 0
                    else:
                        return 1
            # if the change is less than 0
            elif deltaR < 0:
                # for loop that traverses the absolute value of the distance between rows
                for i in range(int(math.fabs(deltaR))):
                    # if the space between the car's row and spaces traversed to the left is occupied
                    if self.board[car.rowPos - (1 + i)][(car.colPos)] != " ~ ":
                        # if the occupied space is a car
                        if int(self.board[car.rowPos - (1 + i)][(car.colPos)]) == int(car.name):
                            pass
                        else:
                            return 0
                    # if the cars row position + the distance between rows is less than 0
                    elif (car.rowPos + (deltaR)) < 0:
                        return 0
                    else:
                        return 1

    # method to remove a car from the list so it's coordinates can change
    def removeCar(self, carNum):
        car = self.allCars[carNum]
        # if the car is facing horizontally
        if car.orient == "h":
            # for loop to traverse car length
            for x in range(int(car.long)):
                self.board[int(car.rowPos)][int(car.colPos) + x] = " ~ "
        # if the car is facing vertically
        elif car.orient == "v":
            # for loop to traverse car length
            for x in range(int(car.long)):
                self.board[int(car.rowPos) + x][int(car.colPos)] = " ~ "

    # method to check if the game is over
    def endGame(self):
        car = self.allCars[0]
        # if the front of the red car's column is 5 (last column, row doesn't matter since car can only move horizontally
        if (car.colPos + ((car.long) - 1)) == 5:
            return 1
        else:
            return 0

    # method to move the car provided legal placement
    def moveCar(self):
        car, newCol, newRow = self.movement()
        num = int(car.name)
        # if the user's move is legal
        if self.isLegal(num, newRow, newCol) == 1:
            deltaR = newRow - car.rowPos
            deltaC = newCol - car.colPos
            deltaRfront = newRow - (car.rowPos + (car.long - 1))
            deltaCfront = newCol - (car.colPos + (car.long - 1))
            # if the car is facing horizontally
            if car.orient == "h":
                # if the change in columns is greater than 0 (moving to the right)
                if deltaC > 0:
                    self.removeCar(num)
                    car.colPos += (deltaCfront)
                    self.updateBoard()
                # if the change in columns is less than 0 (moving to the left)
                elif deltaC < 0:
                    self.removeCar(num)
                    car.colPos += (deltaC)
                    self.updateBoard()
            # if the car is vertically faced
            elif car.orient == "v":
                # if the change in rows is greater than 0 (moving up)
                if deltaR > 0:
                    self.removeCar(num)
                    car.rowPos += (deltaRfront)
                    self.updateBoard()
                # if the change in rows is less than 0 (moving down)
                elif deltaR < 0:
                    self.removeCar(num)
                    car.rowPos += (deltaR)
                    self.updateBoard()
        # if the move is illegal
        else:
            print("INVALID MOVE")

    # the method that runs rush hour
    def play(self):
        self.carGen()
        self.updateBoard()
        self.setup()
        # while loop that runs until end of game
        while self.endGame() != 1:
            ev = pygame.event.get()
            for event in ev:
                # if the user wants to quit
                if event.type == pygame.QUIT:
                    pygame.quit
            self.moveCar()
            self.setup()


# the main play method
if __name__ == "__main__":

    if len(sys.argv) != 2:
        sys.stderr.write("usage: () game_file.txt\n")
        sys.exit()
    RushHour = Game()
    RushHour.play()