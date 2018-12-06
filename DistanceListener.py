import os

import Leap, sys, thread, time
from Leap import CircleGesture, KeyTapGesture, ScreenTapGesture, SwipeGesture


signData = {"Thumb position" : (0, 0, 0),
            "Thumb direction" : (0, 0, 0),
            "TI distance" : 0,
            "Index position" : (0, 0, 0),
            "Index direction" : (0, 0, 0),
            "IM distance" : 0,
            "Middle position" : (0, 0, 0),
            "Middle direction" : (0, 0, 0),
            "MR distance" : 0,
            "Ring position" : (0, 0, 0),
            "Ring direction" : (0, 0, 0),
            "RP distance" : 0,
            "Pinky position" : (0, 0, 0),
            "Pinky direction" : (0, 0, 0),}

def distance(point1, point2):
    x1, y1, z1 = point1[0], point1[1], point1[2]
    x2, y2, z2 = point2[0], point2[1], point2[2]
    return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2 + (z1 - z2) ** 2)   

class DistanceListener(Leap.Listener):
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
        
            fingertips = {}
            for finger in hand.fingers:
                fingertipPos = finger.bone(3).next_joint
                fingertips[self.finger_names[finger.type]] = fingertipPos
                transformed_position = hand_transform.transform_point(finger.tip_position)
                transformed_direction = hand_transform.transform_direction(finger.direction)
                signData[self.finger_names[finger.type] + " position"] = (transformed_position.x, transformed_position.y, transformed_position.z)
                signData[self.finger_names[finger.type] + " direction"] = (transformed_direction.x, transformed_direction.y, transformed_direction.z)
            for i in range(len(fingertips) - 1):
                signData[self.finger_names[i][0] + self.finger_names[i + 1][0] + "distance"] = distance(fingertips[i], fingertips[i + 1])


    def state_string(self, state):
        if state == Leap.Gesture.STATE_START:
            return "STATE_START"

        if state == Leap.Gesture.STATE_UPDATE:
            return "STATE_UPDATE"

        if state == Leap.Gesture.STATE_STOP:
            return "STATE_STOP"

        if state == Leap.Gesture.STATE_INVALID:
            return "STATE_INVALID"