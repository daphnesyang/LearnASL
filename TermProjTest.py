import pygame, sys
from pygame.locals import *
import os
import Leap, sys, thread, time
from Leap import CircleGesture, KeyTapGesture, ScreenTapGesture, SwipeGesture
from Block import Block
import math

pygame.init()
displayWidth = 800
displayHeight = 600
gameDisplay = pygame.display.set_mode((displayWidth, displayHeight))
pygame.display.set_caption("Term Project")
clock = pygame.time.Clock()

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
        
        
def isA(signData):
    signA = {'Middle direction': (-0.12259446829557419, -0.7422619462013245, 0.6588003635406494),
            'Index position': (-20.34893798828125, -47.27545928955078, -15.374573707580566),
            'Thumb direction': (-0.31459930539131165, -0.3205173909664154, -0.8934740424156189),
            'Pinky direction': (-0.3808663487434387, -0.778164803981781, 0.49939993023872375),
            'Index direction': (0.17356082797050476, -0.784588634967804, 0.5952287912368774),
            'Pinky position': (16.863195419311523, -38.91485595703125, -7.1452436447143555),
            'Middle position': (-10.75601577758789, -51.36969757080078, -11.78918743133545),
            'Ring direction': (-0.22775235772132874, -0.7808622121810913, 0.5817069411277771),
            'Ring position': (4.046058654785156, -49.00689697265625, -9.245894432067871),
            'Thumb position': (-46.08635711669922, -31.666282653808594, -28.132286071777344)}

    for point in signData:
        for i in range(0,3):
            #print(point, abs(signData[point][i] - signA[point][i]))
            if abs(signData[point][i] - signA[point][i]) >= 20:
                return False
    return True

    
def isB(signData):
    signB = {'Middle direction': (0.0, -0.09695833921432495, -0.9897810816764832),
            'Index position': (0.0, 1.362518310546875, -89.27637481689453),
            'Thumb direction': (0.0, -0.09617394208908081, -0.9925882816314697),
            'Pinky direction': (-0.0, -0.1064680814743042, -0.993479311466217),
            'Index direction': (0.0, -0.03934100642800331, -0.9922375679016113),
            'Pinky position': (0.0, -4.2476043701171875, -66.86676788330078),
            'Middle position': (0.0, -1.4759674072265625, -98.37427520751953),
            'Ring direction': (-0.0, -0.17012502253055573, -0.985412061214447),
            'Ring position': (0.0, -7.00799560546875, -89.08325958251953),
            'Thumb position': (0.0, -5.3599395751953125, -17.735065460205078)}
    for point in signData:
        for i in range(0,3):
            #print(point, abs(signData[point][i] - signB[point][i]))
            if abs(signData[point][i] - signB[point][i]) >= 20:
                return False
    return True
    
def isC(signData):
    signC = {'Middle direction': (-0.11509914696216583, -0.988159716129303, -0.10145197808742523),
            'Index position': (-16.696165084838867, -32.5296630859375, -51.2198600769043),
            'Thumb direction': (-0.009697690606117249, -0.1362699717283249, -0.9906242489814758),
            'Pinky direction': (-0.21735993027687073, -0.7622607946395874, -0.6096828579902649),
            'Index direction': (0.053516894578933716, -0.9912512898445129, -0.12065136432647705),
            'Pinky position': (22.929630279541016, -37.313629150390625, -49.67544937133789),
            'Middle position': (-3.4170799255371094, -35.87608337402344, -54.4104118347168),
            'Ring direction': (-0.22275136411190033, -0.9580744504928589, 0.18020832538604736),
            'Ring position': (3.870600700378418, -60.292083740234375, -24.482906341552734),
            'Thumb position': (-35.851539611816406, -8.44818115234375, -29.826080322265625)}
    for point in signData:
        for i in range(0,3):
            #print(point, abs(signData[point][i] - signC[point][i]))
            if abs(signData[point][i] - signC[point][i]) >= 30:
                return False
    return True
    
def isD(signData):
    signD = {'Middle direction': (-0.14766627550125122, -0.9684712886810303, 0.2006441354751587),
            'Index position': (-26.90310287475586, 15.46893310546875, -87.02784729003906),
            'Thumb direction': (0.31990450620651245, -0.6040832996368408, -0.7298934459686279),
            'Pinky direction': (-0.36852264404296875, -0.926325798034668, 0.07817703485488892),
            'Index direction': (-0.08077648282051086, 0.12260140478610992, -0.9891632795333862),
            'Pinky position': (17.658294677734375, -47.5909423828125, -20.312198638916016),
            'Middle position': (-11.244749069213867, -64.1679916381836, -30.720794677734375),
            'Ring direction': (-0.21881134808063507, -0.9654781222343445, 0.14132824540138245),
            'Ring position': (4.519590377807617, -59.88311004638672, -27.41565704345703),
            'Thumb position': (-7.20628547668457, -55.367286682128906, -15.808856964111328)}
    for point in signData:
        for i in range(0,3):
            #print(point, abs(signData[point][i] - signD[point][i]))
            if abs(signData[point][i] - signD[point][i]) >= 30:
                return False
    return True    
    
def isE(signData):
    signE = {'Middle direction': (-0.1341893970966339, -0.8451904654502869, 0.5173453092575073),
            'Index position': (-19.97177505493164, -34.586639404296875, -32.34907150268555),
            'Thumb direction': (0.23294733464717865, -0.4462568163871765, -0.8640546202659607),
            'Pinky direction': (-0.34612298011779785, -0.9327086210250854, -0.10125898569822311),
            'Index direction': (0.007777102291584015, -0.8596974611282349, 0.5107443928718567),
            'Pinky position': (20.987438201904297, -35.15906524658203, -32.88402557373047),
            'Middle position': (-8.258373260498047, -38.12126922607422, -32.984344482421875),
            'Ring direction': (-0.20808924734592438, -0.9781015515327454, 0.004028234630823135),
            'Ring position': (8.19601058959961, -46.58356475830078, -42.25594711303711),
            'Thumb position': (-1.4318466186523438, -41.566551208496094, -23.13913917541504)}
            
    for point in signData:
        for i in range(0,3):
            #print(point, abs(signData[point][i] - signE[point][i]))
            if abs(signData[point][i] - signE[point][i]) >= 20:
                return False
    return True   


def drawLetter(letter):
    letterFont = pygame.font.SysFont("None", 200)
    letterName = letterFont.render(letter,True,BLUE,PINK)
    letterRect = letterName.get_rect(center=(displayWidth/2, displayHeight/2 + margin2))
    gameDisplay.blit(letterName, letterRect)

def inputScreen():
    # Create a sample listener and controller
    listener = MainListener()
    controller = Leap.Controller()
    # Have the sample listener receive events from the controller
    controller.add_listener(listener)

    #Textbox
    gameDisplay.fill(WHITE) # draw screen fill
    boxHeight = 60
    textbox = pygame.Rect(0,displayHeight/3*2 - boxHeight/2,displayWidth,boxHeight)
    pygame.draw.rect(gameDisplay, LIGHTYELLOW, textbox)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                sign = sign[:-1]
            elif event.key == pygame.K_RETURN:
                sign = Letter(signData)
            elif event.key == pygame.K_SPACE:
                sign += " "
            else:
                sign += event.unicode
    
    pygame.display.update()
    
    
def helpScreen():
    help = True
    # # Create a sample listener and controller
    # listener = MainListener()
    # controller = Leap.Controller()
    # # Have the sample listener receive events from the controller
    # controller.add_listener(listener)
    
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
 
        if isA(signData):
            drawLetter("A")
        if isB(signData):
            drawLetter("B")
        if isC(signData):
            drawLetter("C")
        if isD(signData):
            drawLetter("D")
        if isE(signData):
            drawLetter("E")
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == MOUSEBUTTONDOWN:
                if onButton(backButton):
                    startScreen()
                    diction = False

        pygame.display.update()
        
def gameScreen():

    game = True
    # Create a sample listener and controller
    listener = MainListener()
    controller = Leap.Controller()
    # Have the sample listener receive events from the controller
    controller.add_listener(listener)
    
    while game:
        
        gameDisplay.fill(PINK)
        titleFont = pygame.font.Font("NewAmsterdam.ttf",120)
        gameTitle = titleFont.render("Game Mode",True,BLUE,PINK)
        gameTitleRect = gameTitle.get_rect(center=(displayWidth/2, displayHeight/8))
        gameDisplay.blit(gameTitle, gameTitleRect)
        
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
    
        testBlock = Block(600,500,100, 300,10,"right","A")
    
        blocks = [testBlock]
        
        clock.tick(30)
        
        for block in blocks:

            block.moveBlock()
            
            topPointsList = [[block.x, block.y],
                            [block.x + block.length/math.sqrt(2), block.y - block.length/math.sqrt(2)],
                            [block.x + block.length/math.sqrt(2) - block.width/math.sqrt(2), block.y - block.length/math.sqrt(2) - block.width/math.sqrt(2)],
                            [block.x - block.width/math.sqrt(2), block.y - block.width/math.sqrt(2)]]
            leftPointsList = [[block.x, block.y],
                            [block.x, block.y + block.height],
                            [block.x - block.width/math.sqrt(2), block.y + block.height - block.width/math.sqrt(2)],
                            [block.x - block.width/math.sqrt(2), block.y - block.width/math.sqrt(2)]]
            rightPointsList = [[block.x, block.y],
                            [block.x, block.y + block.height],
                            [block.x + block.length/math.sqrt(2), block.y + block.height - block.length/math.sqrt(2)],
                            [block.x + block.length/math.sqrt(2), block.y - block.length/math.sqrt(2)]]
            
            # left = [block.x + block.length/math.sqrt(2)/2 - block.width/math.sqrt(2),
            #         block.y - block.length/math.sqrt(2) - block.width/math.sqrt(2)/2]
            # right = [block.x + block.length/math.sqrt(2)/2,
            #         block.y - block.length/math.sqrt(2)/2]
            # letterX = block.x + block.length/math.sqrt(2)/2 - block.width/math.sqrt(2)/2
            # letterY = block.y - (block.length/math.sqrt(2) + block.length/math.sqrt(2)/2)/2 - block.width/math.sqrt(2)/4
            
            pygame.draw.polygon(gameDisplay, WHITE, topPointsList)
            pygame.draw.polygon(gameDisplay,LIGHTBLUE, leftPointsList)
            pygame.draw.polygon(gameDisplay,BLUE, rightPointsList)
            
            # letterFont = pygame.font.Font("TheLightFont.ttf",80)
            # letterTitle = letterFont.render(block.letter,True,PINK,WHITE)
            # letterTitleRect = letterTitle.get_rect(center=(letterX, letterY))
            # gameDisplay.blit(letterTitle, letterTitleRect)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == MOUSEBUTTONDOWN:
                if onButton(backButton):
                    startScreen()

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
