from .actions import JumpingJacks, Squats, BicepCurls, Recognizer, find_angle_between_landmarks
from typing import Dict, List, Type
from helper import Actor
import mediapipe as mp
import numpy as np
import pygame
import cv2

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

DEFAULT_RESOLUTION = (800, 600)

class PoseAnalyzer:
    MAX_LANDMARKS = 33
    ACTION_RECOGNIZERS = {
        'jumping jacks': JumpingJacks,
        # 'lunges': Squats,
        'bicep curls': BicepCurls,
        'squats': Squats
    }
    
    def __init__(self, *args, **kwargs):
        self.pose = mp_pose.Pose(*args, **kwargs)
        self.detection_result = None
        self.recognizers: Dict[str, Type[Recognizer]] = {}
        self.initialize_recognizers()
        
    def initialize_recognizers(self):
        self.recognizers.clear()
        self.recognizers = {action: recognizer() for action, recognizer in self.ACTION_RECOGNIZERS.items()}
    
    @staticmethod
    def draw_hand_landmarks(frame, detection_result):
        """
        Draw the hand landmarks
        """
        if detection_result.pose_landmarks:     
            mp_drawing.draw_landmarks(frame, detection_result.pose_landmarks, mp_pose.POSE_CONNECTIONS)
    
    def is_landmark_visible(self, pointA: int):
        return self.detection_result.landmarks[pointA].visibility > 0.5
    
    def is_results_available(self):
        return self.detection_result
    
    def process_frame(self, frame):
        result = self.pose.process(frame)
        self.detection_result = result.pose_landmarks
        return result
    
    def recognize_pose(self, frame, time_elapsed):
        if not self.detection_result:
            return
        
        for action, recognizer in self.recognizers.items():
            if recognizer.run(self.detection_result, time_elapsed):
                print(f'You just did a {action} ! You\'ve done {recognizer.report_stats()} {action} !')
                
    def report_stats(self, action: str=None):
        if action is None:
            return {action: recognizer.report_stats() for action, recognizer in self.recognizers.items()}
        else:
            assert action.lower() in self.ACTION_RECOGNIZERS, f'\"{action.lower()}\" is not a supported action'
            return self.recognizers[action.lower()].report_stats()
    
    def reset_recognizer(self, action: str):
        assert action.lower() in self.ACTION_RECOGNIZERS, f'\"{action.lower()}\" is not a supported action'
        self.recognizers[action.lower()].reset()
        
    def reset_all_recognizers(self):
        for recognizer in self.recognizers.values():
            recognizer.reset()

class Camera(Actor):    
    def __init__(self, *args, **kwargs):
        self._cap = None
        self.pose = PoseAnalyzer(min_detection_confidence = 0.85, min_tracking_confidence  = 0.85)
        
        default_width, default_height = DEFAULT_RESOLUTION
        width = kwargs.pop('width', default_width)
        height = kwargs.pop('height', default_height)
        
        super().__init__(self, *args, **kwargs)
        self.width, self.height = width, height
    
    def initialize_camera(self, video_mode, dims):
        """
        Initialize Camera
        @param video_mode 0 = Webcam, 1 = External Webcam
        @param dimensions dimensions of the video frame
        """
        width, height = dims
        self.time_elapsed = 0
        self._cap = cv2.VideoCapture(video_mode)
        self._cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        self._cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
    
    def close_camera(self):
        """
        Delete the Camera
        """
        self._cap.release()
        self._cap = None
    
    def isOpen(self):
        return self._cap.isOpened()
    
    def return_camera_frame(self):
        """
        Read a frame from the camera
        """
        assert self._cap, 'Video aint opened yet son of a btcih'
        ret, frame = self._cap.read()   
        frame = Camera.process_camera_frame(frame)
        return ret, frame
    
    def draw(self, screen, *args, border=(0, 0, 0), **kwargs):
        if self.hidden:
            return
        
        ret, frame = self.return_camera_frame()
        
        if not ret:
            return pygame.Surface((self.width, self.height))
        
        detection_result = self.pose.process_frame(frame)
        self.pose.recognize_pose(frame, self.time_elapsed)
        
        if self.pose.is_results_available():
            PoseAnalyzer.draw_hand_landmarks(frame, detection_result)
            # cv2.putText(frame, f'{find_angle_between_landmarks(detection_result.pose_landmarks, mp_pose.PoseLandmark.LEFT_SHOULDER,  mp_pose.PoseLandmark.LEFT_ELBOW,  mp_pose.PoseLandmark.LEFT_WRIST)}', (10, 30), cv2.FONT_HERSHEY_SCRIPT_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA)
            self.prompt_user(frame, detection_result)
        
        self._surf = Camera.convert_frame_surface(frame, (self.width, self.height))
        super().draw()

    @staticmethod
    def get_average_brightness(frame):
        gray_scale = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        average_brightness = gray_scale.mean()
        return average_brightness

    
    def prompt_user(self, frame, results):
        pose_markers = results.pose_landmarks
        if not pose_markers:
            return
        
        visible_landmarks = 0
        # TODO: replace this with pose's visibility
        for lm in pose_markers.landmark:
            visible_landmarks += (lm.visibility > 0.5)
        
        if visible_landmarks < PoseAnalyzer.MAX_LANDMARKS:
            return 'do stuff pls :pray: thx'
        
    @staticmethod
    def process_camera_frame(frame):
        """
        Preprocessing image frame
        """
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        return frame
    
    @staticmethod
    def convert_frame_surface(frame, dims):
        """
        Convert Frame to a Pygame Surface
        """
        frame = cv2.flip(frame, 1)
        surface = pygame.surfarray.make_surface(np.rot90(frame))
        surface = pygame.transform.scale(surface, dims)
        return surface
    
camera = Camera()
Pose = camera.pose