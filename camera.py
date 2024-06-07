from helper import Actor
import mediapipe as mp
import numpy as np
import pygame
from math import acos, degrees
import cv2

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

prev_pose = 'down'
count = 0
def jump_jack(results, frame):
    global prev_pose, count
    
    landmarks = results.landmark

    left_wrist = landmarks[mp_pose.PoseLandmark.LEFT_WRIST]
    right_wrist = landmarks[mp_pose.PoseLandmark.RIGHT_WRIST]
    left_ankle = landmarks[mp_pose.PoseLandmark.LEFT_ANKLE]
    right_ankle = landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE]

    def calculate_distance(point1, point2):
        return ((point1.x - point2.x) ** 2 + (point1.y - point2.y) ** 2) ** 0.5

    hand_distance = calculate_distance(left_wrist, right_wrist)

    if hand_distance > 0.5:  
        if prev_pose == "down":
            count += 0.5
            prev_pose = "up"
    else:   
        prev_pose = "down"

    cv2.putText(frame, f'Jumping Jacks: {count}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA)

class PoseAnalyzer:
    MAX_LANDMARKS = 33
    def __init__(self, *args, **kwargs):
        self.pose = mp_pose.Pose(*args, **kwargs)
        self.detection_result = None
        self.count = 0

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
    
    def distance_between_landmarks(self, pointA: int, pointB: int):
        landmarks = self.detection_result.landmark
        landmarkA, landmarkB = landmarks[pointA], landmarks[pointB]
        return ((landmarkA.x - landmarkB.x) ** 2 + (landmarkA.y - landmarkB.y) ** 2) ** 0.5
    
    def find_angle_between_landmarks(self, pointA: int, pointB: int, pointC: int):
        edgeAB = self.distance_between_landmarks(pointA, pointB)
        edgeAC = self.distance_between_landmarks(pointA, pointC)
        edgeCB = self.distance_between_landmarks(pointC, pointB)
        angle = degrees(acos((edgeCB ** 2 + edgeAB ** 2 - edgeAC ** 2) / (2 * edgeAB * edgeCB)))
        return angle
                
    def recognize_pose(self, frame):
        if self.detection_result:
            jump_jack(self.detection_result, frame)

class Camera(Actor):
    def __init__(self, *args, **kwargs):
        self._cap = None
        self._pose_estimator = PoseAnalyzer(min_detection_confidence = 0.85, min_tracking_confidence  = 0.85)
        self.dims = kwargs.pop('dims', (800, 600))
        if kwargs.get('video_mode'):
            self.initialize_camera(kwargs.pop('video_mode', self.dims))
        super().__init__(self, *args, **kwargs)
    
    def initialize_camera(self, video_mode, dims):
        """
        Initialize Camera
        @param video_mode 0 = Webcam, 1 = External Webcam
        @param dimensions dimensions of the video frame
        """
        self.dims = dims
        width, height = dims
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
    
    def draw(self, screen):
        if self.hidden:
            return
        
        ret, frame = self.return_camera_frame()
        
        if not ret:
            return pygame.Surface(self.dims)
        
        detection_result = self._pose_estimator.process_frame(frame)
        self._pose_estimator.recognize_pose(frame)
        
        if self._pose_estimator.is_results_available():
            PoseAnalyzer.draw_hand_landmarks(frame, detection_result)
            self.prompt_user(frame, detection_result)
            # Camera.get_average_brightness(frame)
            print(self._pose_estimator.find_angle_between_landmarks(11, 13, 15))
        
        self._surf = Camera.convert_frame_surface(frame, self.dims)
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