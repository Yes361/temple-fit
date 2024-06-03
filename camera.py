import mediapipe as mp
import numpy as np
import pygame
import cv2

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

class PoseAnalyzer:
    def __init__(self, *args, **kwargs):
        self.pose = mp_hands.Hands(*args, **kwargs)

    def process_frame(self, frame):
        landmarks = self.pose.process(frame)
        return landmarks

class Camera:
    def __init__(self):
        self._cap = None
        self._pose_estimator = PoseAnalyzer(min_detection_confidence = 0.85, min_tracking_confidence  = 0.85)
    
    def initialize_camera(self, video_mode, dimensions=(640, 480)):
        width, height = dimensions
        self._cap = cv2.VideoCapture(video_mode)
        self._cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        self._cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
    
    def close_camera(self):
        self._cap.release()
        self._cap = None
        
    def get_time_running(self):
        return self._cap.get(cv2.CAP_PROP_POS_MSEC)
    
    def return_camera_frame(self, width, height):
        ret, frame = self._cap.read()
        
        frame = Camera.process_camera_frame(frame)
        surface = Camera.convert_frame_surface(frame, (width, height))
        return surface
    
    @staticmethod
    def process_camera_frame(frame):
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = np.rot90(frame)
        return frame
    
    @staticmethod
    def convert_frame_surface(frame, dimensions):
        frame = pygame.surfarray.make_surface(frame)
        frame = pygame.transform.scale(frame, dimensions)
        return frame