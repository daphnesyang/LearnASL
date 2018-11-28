import pygame, sys
from pygame.locals import *
import os
import Leap, sys, thread, time
from Leap import CircleGesture, KeyTapGesture, ScreenTapGesture, SwipeGesture
from Block import Block
from Letter import Letter
import math
import ast
import random


pygame.init()
displayWidth = 800
displayHeight = 600
gameDisplay = pygame.display.set_mode((displayWidth, displayHeight))
pygame.display.set_caption("Term Project")
clock = pygame.time.Clock()
pygame.key.set_repeat(100, 80)

margin1 = 10
margin2 = 20
margin3 = 40

# Loading in images
question = pygame.image.load("questionmark.png")
question = pygame.transform.scale(question, (30,30))
questionRect = question.get_rect(center=(displayWidth - margin3, margin3))

BLUE = (100, 100, 255)
LIGHTBLUE = (153, 204, 255)
LIGHTYELLOW = (255,236,139)
GRAYYELLOW = (238,220,130)
CORAL = (240, 128, 128)
PINK = (255, 192, 203)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

signData = {"Thumb position" : (0, 0, 0),
            "Thumb direction" : (0, 0, 0),
            "Index position" : (0, 0, 0),
            "Index direction" : (0, 0, 0),
            "Middle position" : (0, 0, 0),
            "Middle direction" : (0, 0, 0),
            "Ring position" : (0, 0, 0),
            "Ring direction" : (0, 0, 0),
            "Pinky position" : (0, 0, 0),
            "Pinky direction" : (0, 0, 0),}

oneHand = False
newSigns = {}

class MainListener(Leap.Listener):
    finger_names = ['Thumb', 'Index', 'Middle', 'Ring', 'Pinky']
    bone_names = ['Metacarpal', 'Proximal', 'Intermediate', 'Distal']
    state_names = ['STATE_INVALID', 'STATE_START', 'STATE_UPDATE', 'STATE_END']

    def on_init(self, controller):
        print "Initialized"

    def on_connect(self, controller):
        print "Connected"

        # Enable gestures
        controller.enable_gesture(Leap.Gesture.TYPE_CIRCLE);
        controller.enable_gesture(Leap.Gesture.TYPE_KEY_TAP);
        controller.enable_gesture(Leap.Gesture.TYPE_SCREEN_TAP);
        controller.enable_gesture(Leap.Gesture.TYPE_SWIPE);

    def on_disconnect(self, controller):
        # Note: not dispatched when running in a debugger.
        print "Disconnected"

    def on_exit(self, controller):
        print "Exited"

    def on_frame(self, controller):
        
        frame = controller.frame()
        # Code for transformed data points from Leap Motion developer guide
        for hand in frame.hands:
            hand_x_basis = hand.basis.x_basis
            hand_y_basis = hand.basis.y_basis
            hand_z_basis = hand.basis.z_basis
            hand_origin = hand.palm_position
            hand_transform = Leap.Matrix(hand_x_basis, hand_y_basis, hand_z_basis, hand_origin)
            hand_transform = hand_transform.rigid_inverse()
        
            for finger in hand.fingers:
                transformed_position = hand_transform.transform_point(finger.tip_position)
                transformed_direction = hand_transform.transform_direction(finger.direction)
                signData[self.finger_names[finger.type] + " position"] = (transformed_position.x, transformed_position.y, transformed_position.z)
                signData[self.finger_names[finger.type] + " direction"] = (transformed_direction.x, transformed_direction.y, transformed_direction.z)

def main():
    # Create a sample listener and controller
    listener = MainListener()
    controller = Leap.Controller()

    # Have the sample listener receive events from the controller
    controller.add_listener(listener)

    # Keep this process running until Enter is pressed
    print "Press Enter to quit..."
    try:
        sys.stdin.readline()
    except KeyboardInterrupt:
        pass
    finally:
        # Remove the sample listener when done
        controller.remove_listener(listener)

def onButton(buttonRect):
    mouse = pygame.mouse.get_pos()
    if (mouse[0] >= buttonRect[0] and mouse[1] >= buttonRect[1] and 
        mouse[0] <= buttonRect[0] + buttonRect[2] and 
        mouse[1] <= buttonRect[1] + buttonRect[3]):
            return True
    return False

def startScreen():
    start = True
    while start:
        gameDisplay.fill(LIGHTBLUE)
        
        border1Rect = Rect(margin1, margin1, displayWidth - margin1*2, displayHeight - margin1*2)
        pygame.draw.rect(gameDisplay, BLUE, border1Rect, 5)
        border2Rect = Rect(margin2, margin2, displayWidth - margin2*2, displayHeight - margin2*2)
        pygame.draw.rect(gameDisplay, BLUE, border2Rect, 3)
        
        # creates the title of the game
        titleFont = pygame.font.Font("NewAmsterdam.ttf",120)
        titleName = titleFont.render("Learn ASL",True,BLUE,LIGHTBLUE)
        titleRect = titleName.get_rect(center=(displayWidth/2, displayHeight/2 - 50))
        gameDisplay.blit(titleName, titleRect)
        # creates help icon
        gameDisplay.blit(question, questionRect)
        # font for buttons
        buttonFont = pygame.font.Font("TheLightFont.ttf",30)
        # creates button for dictionary mode
        buttonW, buttonH = 180, 60
        x1 = displayWidth/4 - buttonW/2
        y1 = displayHeight/2 - buttonH/2 + 50
        dictionaryButton = pygame.Rect(x1, y1, buttonW, buttonH)
        # creates button for game mode
        x2 = displayWidth/2 - buttonW/2
        y2 = displayHeight/2 - buttonH/2 + 50
        gameButton = pygame.Rect(x2, y2, buttonW, buttonH)
        # creates button for test mode
        x3 = displayWidth/4 * 3 - buttonW/2
        y3 = displayHeight/2 - buttonH/2 + 50
        testButton = pygame.Rect(x3, y3, buttonW, buttonH)
        # makes button change colors when mouse is over it
        if onButton(dictionaryButton):
            pygame.draw.rect(gameDisplay, GRAYYELLOW, dictionaryButton)
            dictName = buttonFont.render("DICTIONARY",True,BLUE,GRAYYELLOW)
        else:
            pygame.draw.rect(gameDisplay, LIGHTYELLOW, dictionaryButton)
            dictName = buttonFont.render("DICTIONARY",True,BLUE,LIGHTYELLOW)
        if onButton(gameButton):
            pygame.draw.rect(gameDisplay, GRAYYELLOW, gameButton)
            gameName = buttonFont.render("GAME",True,BLUE,GRAYYELLOW)
        else:
            pygame.draw.rect(gameDisplay, LIGHTYELLOW, gameButton)
            gameName = buttonFont.render("GAME",True,BLUE,LIGHTYELLOW)
        if onButton(testButton):
            pygame.draw.rect(gameDisplay, GRAYYELLOW, testButton)
            testName = buttonFont.render("TEST",True,BLUE,GRAYYELLOW)
        else:
            pygame.draw.rect(gameDisplay, LIGHTYELLOW, testButton)
            testName = buttonFont.render("TEST",True,BLUE,LIGHTYELLOW)
        if onButton(questionRect):
            pixels = pygame.PixelArray(question)
            pixels.replace(Color(255, 255, 255), Color(211,211,211))
            del pixels
        else:
            pixels = pygame.PixelArray(question)
            pixels.replace(Color(211, 211, 211), Color(255,255,255))
            del pixels
            
            
        # creates text on button
        dictRect = dictName.get_rect(center=(displayWidth/4, displayHeight/2 + 50))
        gameDisplay.blit(dictName, dictRect)
        gameRect = gameName.get_rect(center=(displayWidth/2, displayHeight/2 + 50))
        gameDisplay.blit(gameName, gameRect)
        testRect = testName.get_rect(center=(displayWidth/4 * 3, displayHeight/2 + 50))
        gameDisplay.blit(testName, testRect)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == MOUSEBUTTONDOWN:
                if onButton(dictionaryButton):
                    dictionaryScreen()
                if onButton(gameButton):
                    gameScreen()
                if onButton(questionRect):
                    helpScreen()
                if onButton(testRect):
                    testScreen()
        
        pygame.display.update()
    


def drawLetter(letter):
    letterFont = pygame.font.SysFont("None", 200)
    letterName = letterFont.render(letter,True,BLUE,PINK)
    letterRect = letterName.get_rect(center=(displayWidth/2, displayHeight/2 + margin2))
    gameDisplay.blit(letterName, letterRect)

    
def helpScreen():
    help = True
    
    while help:
        
        gameDisplay.fill(PINK)
        titleFont = pygame.font.Font("NewAmsterdam.ttf",120)
        helpTitle = titleFont.render("Help",True,BLUE,PINK)
        helpTitleRect = helpTitle.get_rect(center=(displayWidth/2, displayHeight/8))
        gameDisplay.blit(helpTitle, helpTitleRect)
        
        pygame.draw.line(gameDisplay, BLUE, (margin2 * 3, displayHeight/5), (displayWidth - margin2 * 3, displayHeight/5), 3)
        
        alpha = pygame.image.load("aslalpha.png")
        alpha = pygame.transform.scale(alpha, (640, 400))
        alphaRect = alpha.get_rect(center=(displayWidth/2, displayHeight/2 + margin3))
        gameDisplay.blit(alpha, alphaRect)
        
        buttonFont = pygame.font.Font("TheLightFont.ttf",20)
        
        buttonW, buttonH = 180, 40
        x1 = margin1
        y1 = displayHeight - buttonH - margin1
        backButton = pygame.Rect(x1, y1, buttonW, buttonH)
        
        x4 = displayWidth - buttonW - margin1
        y4 = displayHeight - buttonH - margin1
        inputButton = pygame.Rect(x4, y4, buttonW, buttonH)
        
        if onButton(backButton):
            pygame.draw.rect(gameDisplay, GRAYYELLOW, backButton)
            backName = buttonFont.render("BACK TO MAIN MENU",True,BLUE,GRAYYELLOW)
        else:
            pygame.draw.rect(gameDisplay, LIGHTYELLOW, backButton)
            backName = buttonFont.render("BACK TO MAIN MENU",True,BLUE,LIGHTYELLOW)
        if onButton(inputButton):
            pygame.draw.rect(gameDisplay, GRAYYELLOW, inputButton)
            inputName = buttonFont.render("INPUT SIGNS",True,BLUE,GRAYYELLOW)
        else:
            pygame.draw.rect(gameDisplay, LIGHTYELLOW, inputButton)
            inputName = buttonFont.render("INPUT SIGNS",True,BLUE,LIGHTYELLOW)
        
        # creates text on back to main menu button
        x2 = margin1 + buttonW/2
        y2 = displayHeight - buttonH/2 - margin1
        backRect = backName.get_rect(center=(x2, y2))
        gameDisplay.blit(backName, backRect)
        
        x3 = displayWidth - margin1 - buttonW/2
        y3 = displayHeight - buttonH/2 - margin1
        inputRect = inputName.get_rect(center=(x3, y3))
        gameDisplay.blit(inputName, inputRect)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == MOUSEBUTTONDOWN:
                if onButton(backButton):
                    startScreen()
                if onButton(inputButton):
                    inputScreen()

        pygame.display.update()
    
def writeFile(path, contents):
    with open(path, "wt") as f:
        f.write(contents)
        
def readFile(path):
    with open(path, "rt") as f:
        return f.read()
    

def inputScreen():
    
    inputScreen = True
    
    # Create a sample listener and controller
    listener = MainListener()
    controller = Leap.Controller()
    # Have the sample listener receive events from the controller
    controller.add_listener(listener)
    
    sign = ""
    
    while inputScreen:


        #Textbox
        gameDisplay.fill(WHITE) # draw screen fill
        boxHeight = 60
        textbox = pygame.Rect(0,displayHeight/3*2 - boxHeight/2, displayWidth,boxHeight)
        pygame.draw.rect(gameDisplay, LIGHTYELLOW, textbox)
        
        titleFont = pygame.font.Font("NewAmsterdam.ttf",120)
        inputTitle = titleFont.render("Input Signs",True,BLUE,WHITE)
        inputTitleRect = inputTitle.get_rect(center=(displayWidth/2, displayHeight/8))
        gameDisplay.blit(inputTitle, inputTitleRect)
        
        pygame.draw.line(gameDisplay, BLUE, (margin2 * 3, displayHeight/5), (displayWidth - margin2 * 3, displayHeight/5), 3)
        
        #Instructions
        instructFont = pygame.font.Font("leaguespartan.otf",30)
        instructName1 = instructFont.render("Type in the name of the sign,",True,BLUE,WHITE)
        instructName2 = instructFont.render("and press enter to input it to the system!",True,BLUE,WHITE)
        instructRect1 = instructName1.get_rect(center=(displayWidth/2, displayHeight/2 - 25 - margin3))
        instructRect2 = instructName2.get_rect(center=(displayWidth/2, displayHeight/2 + 25 - margin3))
        gameDisplay.blit(instructName1, instructRect1)
        gameDisplay.blit(instructName2, instructRect2)
        
        buttonFont = pygame.font.Font("TheLightFont.ttf",20)
        
        buttonW, buttonH = 180, 40
        x1 = margin1
        y1 = displayHeight - buttonH - margin1
        backButton = pygame.Rect(x1, y1, buttonW, buttonH)
        
        if onButton(backButton):
            pygame.draw.rect(gameDisplay, GRAYYELLOW, backButton)
            backName = buttonFont.render("BACK TO MAIN MENU",True,BLUE,GRAYYELLOW)
        else:
            pygame.draw.rect(gameDisplay, LIGHTYELLOW, backButton)
            backName = buttonFont.render("BACK TO MAIN MENU",True,BLUE,LIGHTYELLOW)
        
        # creates text on back to main menu button
        x2 = margin1 + buttonW/2
        y2 = displayHeight - buttonH/2 - margin1
        backRect = backName.get_rect(center=(x2, y2))
        gameDisplay.blit(backName, backRect)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == MOUSEBUTTONDOWN:
                if onButton(backButton):
                    startScreen()
            if event.type == pygame.KEYDOWN:
                # user typing in name of the sign or letter
                if event.key == pygame.K_BACKSPACE:
                    sign = sign[:-1]
                elif event.key == pygame.K_RETURN:
                    newSigns[sign] = signData
                    currSigns = readFile("signDictionary.txt")
                    if currSigns != "":
                        currSigns = ast.literal_eval(currSigns)
                        newSigns.update(currSigns)
                    writeFile("signDictionary.txt", str(newSigns))
                    sign = ""
                elif event.key == pygame.K_SPACE:
                    sign += " "
                else:
                    sign += event.unicode
                    
        signFont = pygame.font.Font("CODE Bold.otf", 50)
        signText = signFont.render(sign, True, BLACK, LIGHTYELLOW)
        signRect = signText.get_rect(center=(displayWidth/2,displayHeight/3*2)) # draw user input
        gameDisplay.blit(signText, signRect)

    
        pygame.display.update()
    

def dictionaryScreen():
    diction = True
    # Create a sample listener and controller
    listener = MainListener()
    controller = Leap.Controller()
    # Have the sample listener receive events from the controller
    controller.add_listener(listener)
    
    while diction:
        
        gameDisplay.fill(PINK)

        titleFont = pygame.font.Font("NewAmsterdam.ttf",120)
        dictTitle = titleFont.render("Dictionary Mode",True,BLUE,PINK)
        dictTitleRect = dictTitle.get_rect(center=(displayWidth/2, displayHeight/8))
        gameDisplay.blit(dictTitle, dictTitleRect)
        
        pygame.draw.line(gameDisplay, BLUE, (margin2 * 3, displayHeight/5), (displayWidth - margin2 * 3, displayHeight/5), 3)
        
        buttonFont = pygame.font.Font("TheLightFont.ttf",20)
        
        buttonW, buttonH = 180, 40
        x1 = margin1
        y1 = displayHeight - buttonH - margin1
        backButton = pygame.Rect(x1, y1, buttonW, buttonH)
        
        if onButton(backButton):
            pygame.draw.rect(gameDisplay, GRAYYELLOW, backButton)
            backName = buttonFont.render("BACK TO MAIN MENU",True,BLUE,GRAYYELLOW)
        else:
            pygame.draw.rect(gameDisplay, LIGHTYELLOW, backButton)
            backName = buttonFont.render("BACK TO MAIN MENU",True,BLUE,LIGHTYELLOW)
        
        # creates text on back to main menu button
        x2 = margin1 + buttonW/2
        y2 = displayHeight - buttonH/2 - margin1
        backRect = backName.get_rect(center=(x2, y2))
        gameDisplay.blit(backName, backRect)
        
        headerFont = pygame.font.SysFont("greatlakes.ttf", 40)
        headerName = headerFont.render("Place an ASL sign in front to translate to English!",True,BLUE,PINK)
        headerRect = headerName.get_rect(center=(displayWidth/2, displayHeight/4))
        gameDisplay.blit(headerName, headerRect)
 
        signDictString = readFile("signDictionary.txt")
        signDict = ast.literal_eval(signDictString)
        count = 0
        for sign in signDict:
            for point in signData:
                for i in range(0,3):
                    if abs(signData[point][i] - signDict[sign][point][i]) >= 20:
                        count = 1
                        break
            if count == 0:
                drawLetter(str(sign))
            count = 0
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == MOUSEBUTTONDOWN:
                if onButton(backButton):
                    startScreen()
                    diction = False

        pygame.display.update()
        
def distance(point1, point2):
    x1, y1 = point1[0], point1[1]
    x2, y2 = point2[0], point2[1]
    return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)        

def gameScreen():

    game = True
    # Create a sample listener and controller
    listener = MainListener()
    controller = Leap.Controller()
    # Have the sample listener receive events from the controller
    controller.add_listener(listener)
    
    randAscii = random.randint(65,90)
    randLetter = chr(randAscii)
    
    baseBlock = Block(displayWidth/2, displayHeight*2/3 + margin3, 200, 200, 8, "right", randLetter)
    
    randAscii = random.randint(65,90)
    randLetter = chr(randAscii)
    
    startBlock = Block(displayWidth/2, displayHeight*2/3 + margin3 - 20, 200, 200, 8, "right", randLetter)
    blocks = [baseBlock, startBlock]
    score = 0
    
    while game:
        
        
        gameDisplay.fill(PINK)
        
        pygame.draw.line(gameDisplay, BLUE, (margin2 * 3, displayHeight/5), (displayWidth - margin2 * 3, displayHeight/5), 3)
        
        buttonFont = pygame.font.Font("TheLightFont.ttf",20)
        
        buttonW, buttonH = 180, 40
        x1 = margin1
        y1 = displayHeight - buttonH - margin1
        backButton = pygame.Rect(x1, y1, buttonW, buttonH)
        
        if onButton(backButton):
            pygame.draw.rect(gameDisplay, GRAYYELLOW, backButton)
            backName = buttonFont.render("BACK TO MAIN MENU",True,BLUE,GRAYYELLOW)
        else:
            pygame.draw.rect(gameDisplay, LIGHTYELLOW, backButton)
            backName = buttonFont.render("BACK TO MAIN MENU",True,BLUE,LIGHTYELLOW)
        
        # creates text on back to main menu button
        x2 = margin1 + buttonW/2
        y2 = displayHeight - buttonH/2 - margin1
        backRect = backName.get_rect(center=(x2, y2))
        gameDisplay.blit(backName, backRect)

        
        clock.tick(30)
        
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == MOUSEBUTTONDOWN:
                if onButton(backButton):
                    startScreen()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    # chops off part of block that is not over previous block
                    
                    if blocks[-1].direction == "right":
                        
                        #if block does not overlap at all, end game
                        if blocks[-1].getLeftCorner()[0] > blocks[-2].getBottomCorner()[0] or\
                            blocks[-1].getBottomCorner()[0] < blocks[-2].getLeftCorner()[0]:
                            endGame(score)
                        score += 1
                        if blocks[-1].getLeftCorner()[0] < blocks[-2].getLeftCorner()[0]:
                            newLeft = [blocks[-2].getLeftCorner()[0], blocks[-2].getLeftCorner()[-1] - blocks[-1].height]
                            choppedDist = distance(blocks[-1].getLeftCorner(), newLeft)
                            blocks[-1].width -= choppedDist
                        if blocks[-1].getBottomCorner()[0] > blocks[-2].getBottomCorner()[0]:
                            newBottom = [blocks[-2].getBottomCorner()[0], blocks[-2].getBottomCorner()[-1] - blocks[-1].height]
                            choppedDist = distance(blocks[-1].getBottomCorner(), newBottom)
                            blocks[-1].x, blocks[-1].y = newBottom[0], newBottom[1]
                            blocks[-1].width -= choppedDist   
                    else:
                        
                        #if block does not overlap at all, end game
                        if blocks[-1].getBottomCorner()[0] > blocks[-2].getRightCorner()[0] or\
                            blocks[-1].getRightCorner()[0] < blocks[-2].getBottomCorner()[0]:
                            endGame(score)
                        score += 1
                        if blocks[-1].getRightCorner()[0] > blocks[-2].getRightCorner()[0]:
                            newRight = [blocks[-2].getRightCorner()[0], blocks[-2].getRightCorner()[-1] - blocks[-1].height]
                            choppedDist = distance(blocks[-1].getRightCorner(), newRight)
                            blocks[-1].length -= choppedDist
                        if blocks[-1].getBottomCorner()[0] < blocks[-2].getBottomCorner()[0]:
                            newBottom = [blocks[-2].getBottomCorner()[0], blocks[-2].getBottomCorner()[-1] - blocks[-1].height]
                            choppedDist = distance(blocks[-1].getBottomCorner(), newBottom)
                            blocks[-1].x, blocks[-1].y = newBottom[0], newBottom[1]
                            blocks[-1].length -= choppedDist   
                    
                    # Scrolls down with new blocks
                    for block in blocks:
                        block.y += 20
                        
                    # Creates new block after current one is placed
                    if score % 2 == 0:
                        dir = "right"
                    else:
                        dir = "left"
                    if score % 5 == 0:
                        speed = abs(blocks[-1].speed) + 1
                    else:
                        speed = abs(blocks[-1].speed)
                    randAscii = random.randint(65,90)
                    randLetter = chr(randAscii)
                    newBlock = Block(blocks[-1].x, blocks[-1].y - blocks[-1].height, blocks[-1].length, blocks[-1].width, speed, dir, randLetter)
                    blocks.append(newBlock)
                    
        movingBlock = blocks[-1]
        
        if movingBlock.direction == "right":
            if (movingBlock.y >= displayHeight) or (movingBlock.y - movingBlock.width/math.sqrt(2)) <= 0:
                movingBlock.speed = - movingBlock.speed
        else:
            if (movingBlock.y >= displayHeight) or (movingBlock.y - movingBlock.length/math.sqrt(2)) <= 0:
                movingBlock.speed = - movingBlock.speed
            
        movingBlock.moveBlock()
        
        # Draws score at the top of the screen
        scoreFont = pygame.font.Font("NewAmsterdam.ttf",70)
        scoreTitle = scoreFont.render("Score: " + str(score),True,BLUE,PINK)
        scoreTitleRect = scoreTitle.get_rect(center=(displayWidth/2, displayHeight/8))
        gameDisplay.blit(scoreTitle, scoreTitleRect)
        
        
        for block in blocks: 
            
            
            # removes the block if it goes off the screen and is not the moving block
            if block.y - block.length/math.sqrt(2) - block.width/math.sqrt(2) > displayHeight and blocks.index(block) != len(blocks) -1:
                blocks.remove(block)

            
            # draws one block
            pygame.draw.polygon(gameDisplay, WHITE, block.getTopPoints())
            pygame.draw.polygon(gameDisplay,LIGHTBLUE, block.getLeftPoints())
            pygame.draw.polygon(gameDisplay,BLUE, block.getRightPoints())
            
            # draws and resizes letter on block with the size
            if block.width < 30 or block.length < 30:
                letterFont = pygame.font.Font("CODE Bold.otf",15)
            elif block.width < 50 or block.length < 50:
                letterFont = pygame.font.Font("CODE Bold.otf",25)
            else:
                letterFont = pygame.font.Font("CODE Bold.otf",40)
            letterTitle = letterFont.render(block.letter,True,PINK,WHITE)
            letterTitleRect = letterTitle.get_rect(center=(block.getCenter()[0], block.getCenter()[1]))
            gameDisplay.blit(letterTitle, letterTitleRect)
            
    

        pygame.display.update()
    
def endGame(score):

    end = True
    
    while end:
        
        gameDisplay.fill(PINK)
        titleFont = pygame.font.Font("NewAmsterdam.ttf",120)
        testTitle = titleFont.render("Final Score: " + str(score),True,BLUE,PINK)
        testTitleRect = testTitle.get_rect(center=(displayWidth/2, displayHeight/8))
        gameDisplay.blit(testTitle, testTitleRect)
        
        pygame.draw.line(gameDisplay, BLUE, (margin2 * 3, displayHeight/5), (displayWidth - margin2 * 3, displayHeight/5), 3)
        
        buttonFont = pygame.font.Font("TheLightFont.ttf",20)
        tryFont = pygame.font.Font("TheLightFont.ttf", 60)
        
        buttonW, buttonH = 180, 40
        x1 = margin1
        y1 = displayHeight - buttonH - margin1
        backButton = pygame.Rect(x1, y1, buttonW, buttonH)
        
        # creates try again button
        
        tryButtonW, tryButtonH = 300, 80
        x3 = displayWidth/2 - tryButtonW/2
        y3 = displayHeight/2 - tryButtonH/2
        gameButton = pygame.Rect(x3, y3, tryButtonW, tryButtonH)
        
        # changes colors for hovering
        if onButton(backButton):
            pygame.draw.rect(gameDisplay, GRAYYELLOW, backButton)
            backName = buttonFont.render("BACK TO MAIN MENU",True,BLUE,GRAYYELLOW)
            
        else:
            pygame.draw.rect(gameDisplay, LIGHTYELLOW, backButton)
            backName = buttonFont.render("BACK TO MAIN MENU",True,BLUE,LIGHTYELLOW)
        if onButton(gameButton):
            pygame.draw.rect(gameDisplay, GRAYYELLOW, gameButton)
            gameName = tryFont.render("TRY AGAIN",True,BLUE,GRAYYELLOW)
        else:
            pygame.draw.rect(gameDisplay, LIGHTYELLOW, gameButton)
            gameName = tryFont.render("TRY AGAIN",True,BLUE,LIGHTYELLOW)
        
        # creates text on back to main menu button
        x2 = margin1 + buttonW/2
        y2 = displayHeight - buttonH/2 - margin1
        backRect = backName.get_rect(center=(x2, y2))
        gameDisplay.blit(backName, backRect)
        
        #creates text on try again button
        x4 = displayWidth/2
        y4 = displayHeight/2
        gameRect = gameName.get_rect(center=(x4,y4))
        gameDisplay.blit(gameName, gameRect)
    
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == MOUSEBUTTONDOWN:
                if onButton(backButton):
                    startScreen()
                if onButton(gameButton):
                    gameScreen()

        pygame.display.update()
    
    
def testScreen():

    test = True
    # Create a sample listener and controller
    listener = MainListener()
    controller = Leap.Controller()
    # Have the sample listener receive events from the controller
    controller.add_listener(listener)
    
    while test:
        
        gameDisplay.fill(PINK)
        titleFont = pygame.font.Font("NewAmsterdam.ttf",120)
        testTitle = titleFont.render("Test Mode",True,BLUE,PINK)
        testTitleRect = testTitle.get_rect(center=(displayWidth/2, displayHeight/8))
        gameDisplay.blit(testTitle, testTitleRect)
        
        pygame.draw.line(gameDisplay, BLUE, (margin2 * 3, displayHeight/5), (displayWidth - margin2 * 3, displayHeight/5), 3)
        
        buttonFont = pygame.font.Font("TheLightFont.ttf",20)
        
        buttonW, buttonH = 180, 40
        x1 = margin1
        y1 = displayHeight - buttonH - margin1
        backButton = pygame.Rect(x1, y1, buttonW, buttonH)
        
        if onButton(backButton):
            pygame.draw.rect(gameDisplay, GRAYYELLOW, backButton)
            backName = buttonFont.render("BACK TO MAIN MENU",True,BLUE,GRAYYELLOW)
        else:
            pygame.draw.rect(gameDisplay, LIGHTYELLOW, backButton)
            backName = buttonFont.render("BACK TO MAIN MENU",True,BLUE,LIGHTYELLOW)
        
        # creates text on back to main menu button
        x2 = margin1 + buttonW/2
        y2 = displayHeight - buttonH/2 - margin1
        backRect = backName.get_rect(center=(x2, y2))
        gameDisplay.blit(backName, backRect)
    
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == MOUSEBUTTONDOWN:
                if onButton(backButton):
                    startScreen()

        pygame.display.update()
        
startScreen()
quit()
