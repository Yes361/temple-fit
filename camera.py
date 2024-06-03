import mediapipe as mp
import numpy as np
import pygame
import cv2

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

class PoseAnalyzer:
    def __init__(self, *args, **kwargs):
        self.pose = mp_hands.Hands(*args, **kwargs)

    def process_frame(self, frame):
        landmarks = self.pose.process(frame)
        return landmarks
    
    @staticmethod
    def draw_hand_landmarks(frame, detection_result):
        """
        Draw the hand landmarks
        """
        if detection_result.multi_hand_landmarks:     
            for hand_landmarks in detection_result.multi_hand_landmarks:
                mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

class Camera:
    def __init__(self):
        self._cap = None
        self._pose_estimator = PoseAnalyzer(min_detection_confidence = 0.85, min_tracking_confidence  = 0.85)
    
    def initialize_camera(self, video_mode, dimensions):
        """
        Initialize Camera
        @param video_mode 0 = Webcam, 1 = External Webcam
        @param dimensions dimensions of the video frame
        """
        width, height = dimensions
        self._cap = cv2.VideoCapture(video_mode)
        self._cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        self._cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
    
    def close_camera(self):
        """
        Delete the Camera
        """
        self._cap.release()
        self._cap = None
        
    def get_time_running(self):
        """
        Get time since the camera started
        """
        return self._cap.get(cv2.CAP_PROP_POS_MSEC)
    
    def return_camera_frame(self, width, height):
        """
        Read a frame from the camera
        """
        ret, frame = self._cap.read()
        
        frame = Camera.process_camera_frame(frame)
        
        detection_result = self._pose_estimator.process_frame(frame)
        PoseAnalyzer.draw_hand_landmarks(frame, detection_result)

        surface = Camera.convert_frame_surface(frame, (width, height))
        return surface
    
    @staticmethod
    def process_camera_frame(frame):
        """
        Preprocessing image frame
        """
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        return frame
    
    @staticmethod
    def convert_frame_surface(frame, dimensions):
        """
        Convert Frame to a Pygame Surface
        """
        frame = np.rot90(frame)
        frame = pygame.surfarray.make_surface(frame)
        frame = pygame.transform.scale(frame, dimensions)
        return frame