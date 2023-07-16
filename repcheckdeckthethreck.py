#!/usr/bin/env python
# coding: utf-8


get_ipython().system('pip install mediapipe opencv-python')

import cv2
import mediapipe as mp
import numpy as np
import threading
import time
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

def get_angle(a,b,c):
    a = np.array(a)
    b = np.array(b)
    c = np.array(c)
    
    radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])
    angle = np.abs(radians*180.0/np.pi)
    
    if angle >180.0:
        angle = 360-angle
        
    return angle 


cap = cv2.VideoCapture(0)

counter = 0 
stage = None


with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
    while cap.isOpened():
        ret, frame = cap.read()
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image.flags.writeable = False
        results = pose.process(image)
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        try:
            landmarks = results.pose_landmarks.landmark
            
            # Get left coordinates
            left_shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
            left_elbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x,landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
            left_wrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x,landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]
            
            # Calculate left angle
            left_angle = get_angle(left_shoulder, left_elbow, left_wrist)
            
            # Get right coordinates
            right_shoulder = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
            right_elbow = [landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].y]
            right_wrist = [landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].y]
            
            # Calculate right angle
            right_angle = get_angle(right_shoulder, right_elbow, right_wrist)
            
          
            # Bench counter logic
            if left_angle > 160 and right_angle >160:
                stage = "up"
            if (left_angle < 60 and stage =='up') and right_angle<60:
                stage="down"
                counter +=1
                print(counter)
                
        except:
            pass
        
        # Render bench counter
        cv2.rectangle(image, (0,0), (1000,73), (0, 128, 0), -1)
        
        # Count Reps
        cv2.putText(image, 'REPS', (15,12),
                    cv2.FONT_HERSHEY_COMPLEX, 0.5, (0,0,0), 1, cv2.LINE_AA)
        cv2.putText(image, str(counter), 
                    (10,60), 
                    cv2.FONT_HERSHEY_COMPLEX, 2, (255,255,255), 2, cv2.LINE_AA)
        
        
        # Up or Down
        cv2.putText(image, 'STAGE', (95,12), 
                    cv2.FONT_HERSHEY_COMPLEX, 0.5, (0,0,0), 1, cv2.LINE_AA)
        cv2.putText(image, stage, 
                    (90,60), 
                    cv2.FONT_HERSHEY_COMPLEX, 2, (255,255,255), 2, cv2.LINE_AA)
        
        #Calorie data
        cv2.putText(image, 'CALORIES BURNED', (285, 12),
                    cv2.FONT_HERSHEY_COMPLEX, 0.5, (0,0,0), 1, cv2.LINE_AA)
        cv2.putText(image, str(counter*0.24), 
                    (280,60), 
                    cv2.FONT_HERSHEY_COMPLEX, 2, (255,255,255), 2, cv2.LINE_AA)

        mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                 mp_drawing.DrawingSpec(color=(200,231,20), thickness=2, circle_radius=2), 
                                mp_drawing.DrawingSpec(color=(22,43,232), thickness=2, circle_radius=2) 
                                 )                       
        
        cv2.imshow('Based Stupid Gang', image)
        
        key = cv2.waitKey(10)
        if key & 0xFF == ord('r'):
            counter=0
            stage = None

        if key & 0xFF == ord('x'):
            break


    cap.release()
    cv2.destroyAllWindows()



