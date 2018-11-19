import pygame, sys
from pygame.locals import *
import os
import Leap, sys, thread, time
from Leap import CircleGesture, KeyTapGesture, ScreenTapGesture, SwipeGesture

pygame.init()
displayWidth = 800
displayHeight = 600
gameDisplay = pygame.display.set_mode((displayWidth, displayHeight))
pygame.display.set_caption("Term Project")
clock = pygame.time.Clock()

BLUE = (100, 100, 255)
LIGHTBLUE = (153, 204, 255)
LIGHTYELLOW = (255, 255, 153)
CORAL = (240, 128, 128)

signData = {"Thumb Metacarpal" : (0, 0, 0),
            "Thumb Proximal" : (0, 0, 0),
            "Thumb Intermediate" : (0, 0, 0),
            "Thumb Distal" : (0, 0, 0),
            "Index Metacarpal" : (0, 0, 0),
            "Index Proximal" : (0, 0, 0),
            "Index Intermediate" : (0, 0, 0),
            "Index Distal" : (0, 0, 0),
            "Middle Metacarpal" : (0, 0, 0),
            "Middle Proximal" : (0, 0, 0),
            "Middle Intermediate" : (0, 0, 0),
            "Middle Distal" : (0, 0, 0),
            "Ring Metacarpal" : (0, 0, 0),
            "Ring Proximal" : (0, 0, 0),
            "Ring Intermediate" : (0, 0, 0),
            "Ring Distal" : (0, 0, 0),
            "Pinky Metacarpal" : (0, 0, 0),
            "Pinky Proximal" : (0, 0, 0),
            "Pinky Intermediate" : (0, 0, 0),
            "Pinky Distal" : (0, 0, 0)}

oneHand = False

class SampleListener(Leap.Listener):
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
        # Get the most recent frame and report some basic information
        frame = controller.frame()
        # Get hands
        for hand in frame.hands:

            handType = "Left hand" if hand.is_left else "Right hand"
            
            # if len(frame.hands) == 1:
            #     print("hello")
            #     oneHand = True
            
            # Get the hand's normal vector and direction
            normal = hand.palm_normal
            direction = hand.direction
            
            # signData.append(direction)

            # Get arm bone
            arm = hand.arm
            # signData["Wrist position"] = (arm.wrist_position.x, arm.wrist_position.y, arm.wrist_position.z)

            # Get fingers
            for finger in hand.fingers:
                # self.finger_names[finger.type]
                # finger.width
                # signData[self.finger_names[finger.type] + " " + "direction"] = (finger.direction.x, finger.direction.y, finger.direction.z)
                # Get bones
                for b in range(0, 4):
                    bone = finger.bone(b)
                    signData[self.finger_names[finger.type] + " " + self.bone_names[bone.type]] = (bone.direction.x, bone.direction.y, bone.direction.z) 

                        
def main():
    # Create a sample listener and controller
    listener = SampleListener()
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
        # creates the title of the game
        titleFont = pygame.font.SysFont("None",100)
        titleName = titleFont.render("Learn ASL",True,BLUE,LIGHTBLUE)
        titleRect = titleName.get_rect(center=(displayWidth/2, displayHeight/2 - 100))
        gameDisplay.blit(titleName, titleRect)
        # creates button for dictionary mode
        buttonW, buttonH = 250, 80
        x1 = displayWidth/2 - buttonW/2
        y1 = displayHeight/2 - buttonH/2
        dictionaryButton = pygame.Rect(x1, y1, buttonW, buttonH)
        pygame.draw.rect(gameDisplay, LIGHTYELLOW, dictionaryButton)
        # creates text on button
        buttonFont = pygame.font.SysFont("None",50)
        buttonName = buttonFont.render("Dictionary",True,BLUE,LIGHTYELLOW)
        buttonRect = buttonName.get_rect(center=(displayWidth/2, displayHeight/2))
        gameDisplay.blit(buttonName, buttonRect)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == MOUSEBUTTONDOWN:
                if onButton(dictionaryButton):
                    dictionaryScreen()
        
        pygame.display.update()
        
        
def isA(signData):
    signA = {"Thumb Metacarpal" : (0, 0, 0),
            "Thumb Proximal" : (0.625715, -0.0826577, 0.77566),
            "Thumb Intermediate" : (0.471937, 0.0112348, 0.881561),
            "Thumb Distal" : (0.789927, -0.203823, 0.578335),
            "Index Metacarpal" : (0.380931, -0.0480936, 0.92335),
            "Index Proximal" : (0.207414, 0.93859, 0.275731),
            "Index Intermediate" : (-0.395757, 0.494317, -0.773968),
            "Index Distal" : (-0.483214, -0.137658, -0.864612),
            "Middle Metacarpal" : (0.251279, -0.0383372, 0.967155),
            "Middle Proximal" : (0.274882, 0.942102, 0.192052),
            "Middle Intermediate" : (-0.103881, 0.395146, -0.912726),
            "Middle Distal" : (-0.258559, -0.203323, -0.944355),
            "Ring Metacarpal" : (0.103487, -0.0235215, 0.994353),
            "Ring Proximal" : (0.314881, 0.92596, 0.208441),
            "Ring Intermediate" : (0.0618712, 0.369638, -0.927114),
            "Ring Distal" : (-0.131693, -0.216614, -0.967334),
            "Pinky Metacarpal" : (-0.0402554, -0.0488057, 0.997997),
            "Pinky Proximal" : (0.416864, 0.875937, 0.242812),
            "Pinky Intermediate" : (0.340155, 0.279459, -0.897885),
            "Pinky Distal" : (0.0665021, -0.258406, -0.963745)}
    for point in signData:
        for i in range(0,3):
            print(point, abs(signData[point][i] - signA[point][i]))
            if abs(signData[point][i] - signA[point][i]) >= 1:
                return False
    return True
    

    
def isB(signData):
    signB = {"Thumb Metacarpal" : (0, 0, 0),
            "Thumb Proximal" : (0.172054, -0.066833, 0.982818),
            "Thumb Intermediate" : (0.294613, 0.0239381, 0.955317),
            "Thumb Distal" : (0.158182, -0.0768187, 0.984417),
            "Index Metacarpal" : (0.272423, -0.273709, 0.922426),
            "Index Proximal" : (0.0614628, 0.360839, 0.930601),
            "Index Intermediate" : (0.036534, 0.433046, 0.900631),
            "Index Distal" : (0.0208503, 0.476636, 0.878853),
            "Middle Metacarpal" : (0.398526, -0.232775, 0.887126),
            "Middle Proximal" : (0.0237803, 0.264265, 0.964157),
            "Middle Intermediate" : (-0.00460256, 0.319069, 0.94772),
            "Middle Distal" : (-0.0227221, 0.353392, 0.935199),
            "Ring Metacarpal" : (0.527875, -0.17969, 0.830096),
            "Ring Proximal" : (0.0795112, 0.214753, 0.973427),
            "Ring Intermediate" : (0.0494628, 0.261944, 0.963815),
            "Ring Distal" : (0.0299204, 0.292054, 0.955934),
            "Pinky Metacarpal" : (0.64591, -0.162807, 0.745851),
            "Pinky Proximal" : (-0.211487, 0.608837, 0.764585),
            "Pinky Intermediate" : (-0.688679, 0.699724, 0.19002),
            "Pinky Distal" : (-0.789266, 0.596065, -0.14753)}
    for point in signData:
        for i in range(0,3):
            print(point, abs(signData[point][i] - signB[point][i]))
            if abs(signData[point][i] - signB[point][i]) >= 1:
                return False
    return True


def drawLetter(letter):
    letterFont = pygame.font.SysFont("None", 80)
    letterName = letterFont.render(letter,True,BLUE,CORAL)
    letterRect = letterName.get_rect(center=(displayWidth/2, displayHeight/4))
    gameDisplay.blit(letterName, letterRect)

def dictionaryScreen():
    diction = True
    # Create a sample listener and controller
    listener = SampleListener()
    controller = Leap.Controller()
    # Have the sample listener receive events from the controller
    controller.add_listener(listener)
    
    while diction:
        
        gameDisplay.fill(CORAL)
        # if oneHand == True:
        if isA(signData):
            drawLetter("A")
        if isB(signData):
            drawLetter("B")
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        pygame.display.update()
        
startScreen()
quit()
