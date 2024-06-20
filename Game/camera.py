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
    """
    Analyzes poses detected in video frames using MediaPipe and recognizes specific exercises.
    """
    LANDMARK_COUNT_THRES = 10
    ACTION_RECOGNIZERS = {
        'jumping jacks': JumpingJacks,
        'bicep curls': BicepCurls,
        'squats': Squats
    }
    IMPLEMENTED_ACTIONS = list(ACTION_RECOGNIZERS.keys())
    
    def __init__(self, *args, **kwargs):
        self.pose = mp_pose.Pose(*args, **kwargs)
        self.detection_result = None
        self.recognizers: Dict[str, Type[Recognizer]] = {}
        self.initialize_recognizers()
        
    def initialize_recognizers(self):
        self.recognizers.clear()
        self.active_recognizers = PoseAnalyzer.ACTION_RECOGNIZERS.keys()
        self.recognizers = {action: recognizer() for action, recognizer in self.ACTION_RECOGNIZERS.items()}
    
    @staticmethod
    def draw_hand_landmarks(frame, detection_result):
        """
        Draw the hand landmarks on the frame.
        
        @params:
            frame: The video frame.
            detection_result: The result from a MediaPipe pose detection.
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
        """
        Recognize poses in the frame and update the recognizer states.
        
        @params:
            frame: The video frame.
            time_elapsed: Time elapsed since the last update.
        """

        if not self.detection_result:
            return
        
        for action in self.active_recognizers:
            if self.recognizers[action].run(self.detection_result, time_elapsed):
                print(f'You just did a {action} ! You\'ve done {self.recognizers[action].report_stats()} {action} !')\
                    
    def set_active_recognizer(self, *active_list):
        self.active_recognizers = active_list[0] if type(active_list[0]) == list else active_list
                
    def report_stats(self, action: str=None):
        """
        Report statistics of the recognized actions.
        
        @params:
            action (str): Specific action to report stats for.
        
        @@returns:
            dict or int: Statistics data.
        """
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
    """
    Handles camera operations and integrates with PoseAnalyzer for pose detection and recognition.
    """
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
        Initialize the camera.
        
        @params:
            video_mode: 0 for Webcam, 1 for External Webcam.
            dims: Dimensions of the video frame.
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
    
    def draw(self, screen, *args, **kwargs):
        """
        Draw the current frame and detected poses on the screen.
        """
        if self.hidden:
            return
        
        ret, frame = self.return_camera_frame()
        
        if not ret:
            return pygame.Surface((self.width, self.height))
        
        detection_result = self.pose.process_frame(frame)
        
        if self.pose.is_results_available():
            PoseAnalyzer.draw_hand_landmarks(frame, detection_result)
            if self.prompt_user(frame, detection_result):
                self.pose.recognize_pose(frame, self.time_elapsed)
            
            
        self._surf = Camera.convert_frame_surface(frame, (self.width, self.height))
        super().draw()

    @staticmethod
    def get_average_brightness(frame):
        gray_scale = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        average_brightness = gray_scale.mean()
        return average_brightness

    
    def prompt_user(self, frame, results) -> bool:
        """
        Display a prompt to the user based on the visibility of landmarks.
        
        @params:
            frame: The video frame.
            results: The result from a MediaPipe pose detection.
            
        @returns:
            Boolean representing if the Camera can see most of the User's body
        """
        pose_markers = results.pose_landmarks
        if not pose_markers:
            cv2.putText(frame, 'Reposition Thyself', (400, 300), cv2.FONT_HERSHEY_SIMPLEX, 10, (255, 0, 0), 2, cv2.LINE_AA)
            return False
        
        visible_landmarks = sum((lm.visibility > 0.5) for lm in pose_markers.landmark)
        
        if visible_landmarks < PoseAnalyzer.LANDMARK_COUNT_THRES:
            cv2.putText(frame, 'Reposition Thyself', (0, 300), cv2.FONT_HERSHEY_SIMPLEX, 3, (255, 0, 0), 2, cv2.LINE_AA)
            return False
        return True
        
    @staticmethod
    def process_camera_frame(frame):
        """
        Preprocess the camera frame.
        
        @params:
            frame: The video frame.
        
        @returns:
            The processed frame.
        """
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        return frame
    
    @staticmethod
    def convert_frame_surface(frame, dims):
        """
        Convert a frame to a pygame surface.
        
        @params:
            frame: The video frame.
            dims: The dimensions to scale the surface to.
        
        @returns:
            pygame.Surface: The converted surface.
        """
        frame = cv2.flip(frame, 1)
        surface = pygame.surfarray.make_surface(np.rot90(frame))
        surface = pygame.transform.scale(surface, dims)
        return surface
    
camera = Camera()
Pose = camera.pose