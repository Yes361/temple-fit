from helper import Actor
from pygame.math import Vector2
from abc import abstractmethod, ABC
from math import acos, degrees
from typing import Dict, List
import mediapipe as mp
import numpy as np
import pygame
import cv2

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose
mp_pose_landmarks = mp_pose.PoseLandmark

IMPLEMENTED_ACTIONS = ['Jumping Jacks']
DEFAULT_RESOLUTION = (800, 600)
    
def distance(x, y):
    return (x ** 2 + y ** 2) ** 0.5
    
def distance_between_landmarks(detection_result, pointA: int, pointB: int):
    landmarks = detection_result.landmark
    landmarkA, landmarkB = landmarks[pointA], landmarks[pointB]
    return distance(landmarkA.x - landmarkB.x, landmarkA.y - landmarkB.y)

def find_angle_between_landmarks(detection_result, pointA: int, pointB: int, pointC: int):
    edgeAB = distance_between_landmarks(detection_result, pointA, pointB)
    edgeAC = distance_between_landmarks(detection_result, pointA, pointC)
    edgeCB = distance_between_landmarks(detection_result, pointC, pointB)
    angle = degrees(acos((edgeCB ** 2 + edgeAB ** 2 - edgeAC ** 2) / (2 * edgeAB * edgeCB)))
    return angle

def dot_product(detection_result, pointA: int, pointB: int, pointC: int):
    landmarks = detection_result.landmark
    landmarkA, landmarkB, landmarkC = landmarks[pointA], landmarks[pointB], landmarks[pointC]
    edgeAB = Vector2(landmarkA.x - landmarkB.x, landmarkA.y - landmarkB.y).normalize()
    edgeCB = Vector2(landmarkC.x - landmarkB.x, landmarkC.y - landmarkB.y).normalize()
    return Vector2.dot(edgeAB, edgeCB)

class Recognizer(ABC):    
    @abstractmethod
    def run(self, detection_results, time_elapsed: float) -> bool:
        pass

# class JumpingJacks(Recognizer):
#     """
#     Welcome to ur WORST NIGHTMARE
#     """
#     def __init__(self):    
#         self.count = 0
#         self.prev_pose = 'down'
    
#     def run(self, detection_results, time_elapsed: float) -> bool:
#         hand_distance = distance_between_landmarks(detection_results, mp_pose_landmarks.LEFT_WRIST, mp_pose_landmarks.RIGHT_WRIST)
#         foot_distance = distance_between_landmarks(detection_results, mp_pose_landmarks.LEFT_ANKLE, mp_pose_landmarks.RIGHT_ANKLE)
        
#         if hand_distance > 0.5:
#             if self.prev_pose == "down":
#                 self.prev_pose = "up"
#                 self.count += 1
#                 return True
#         else:   
#             self.prev_pose = "down"
        
#         return False

class PoseAnalyzer:
    MAX_LANDMARKS = 33
    # ACTION_RECOGNIZERS = {
    #     'Jumping Jacks': JumpingJacks
    # }
    
    def __init__(self, *args, **kwargs):
        self.pose = mp_pose.Pose(*args, **kwargs)
        self.detection_result = None
    #     self.recognizers: Dict[str, any] = {}
    #     self.initialize_recognizers()
        
    # def initialize_recognizers(self):
    #     self.recognizers.clear()
    #     self.recognizers = {action: recognizer() for action, recognizer in self.ACTION_RECOGNIZERS.items()}
    
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
        
        # for action, recognizer in self.recognizers.items():
        #     if recognizer.run(self.detection_result, time_elapsed):
        #         print(f'You just did a {action} ! You\'ve done {recognizer.count} {action} !')
        
        print('rah')

class Camera(Actor):    
    def __init__(self, *args, **kwargs):
        self._cap = None
        self._pose = PoseAnalyzer(min_detection_confidence = 0.85, min_tracking_confidence  = 0.85)
        
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
        self.width, self.height = dims
        self.time_elapsed = 0
        self._cap = cv2.VideoCapture(video_mode)
        self._cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.width)
        self._cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height)
    
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
        
        detection_result = self._pose.process_frame(frame)
        self._pose.recognize_pose(frame, self.time_elapsed)
        
        if self._pose.is_results_available():
            PoseAnalyzer.draw_hand_landmarks(frame, detection_result) # Debug
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