import mediapipe as mp
import numpy as np
import pygame
import cv2

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

prev_pose = 'down'
count = 0
def jump_jack(results, frame):
    global prev_pose, count
    if not results.pose_landmarks:
        return
    
    landmarks = results.pose_landmarks.landmark

    left_wrist = landmarks[mp_pose.PoseLandmark.LEFT_WRIST]
    right_wrist = landmarks[mp_pose.PoseLandmark.RIGHT_WRIST]
    left_ankle = landmarks[mp_pose.PoseLandmark.LEFT_ANKLE]
    right_ankle = landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE]

    def calculate_distance(point1, point2):
        return ((point1.x - point2.x) ** 2 + (point1.y - point2.y) ** 2) ** 0.5

    hand_distance = calculate_distance(left_wrist, right_wrist)
    foot_distance = calculate_distance(left_ankle, right_ankle)

    if hand_distance > 0.5:  
        if prev_pose == "down":
            count += 0.5
            prev_pose = "up"
    else:   
        prev_pose = "down"

    cv2.putText(frame, f'Jumping Jacks: {count}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA)

class PoseAnalyzer:
    def __init__(self, *args, **kwargs):
        self.pose = mp_pose.Pose(*args, **kwargs)
        self.landmarks = None
        self.count = 0

    @staticmethod
    def draw_hand_landmarks(frame, detection_result):
        """
        Draw the hand landmarks
        """
        if detection_result.pose_landmarks:     
            mp_drawing.draw_landmarks(frame, detection_result.pose_landmarks, mp_pose.POSE_CONNECTIONS)
    
    def process_frame(self, frame):
        self.landmarks = self.pose.process(frame)
        return self.landmarks
    
    def recognize_pose(self, frame, detection_result):
        jump_jack(detection_result, frame)
        

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
    
    def isOpen(self):
        return self._cap.isOpened()
    
    def return_camera_frame(self):
        """
        Read a frame from the camera
        """
        _, frame = self._cap.read()   
        frame = Camera.process_camera_frame(frame)
        return frame
    
    def draw(self, dimensions):
        frame = self.return_camera_frame()
        
        detection_result = self._pose_estimator.process_frame(frame)
        PoseAnalyzer.draw_hand_landmarks(frame, detection_result)
        self._pose_estimator.recognize_pose(frame, detection_result)

        surface = Camera.convert_frame_surface(frame, dimensions)
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
        frame = cv2.flip(frame, 1)
        surface = pygame.surfarray.make_surface(np.rot90(frame))
        surface = pygame.transform.scale(surface, dimensions)
        return surface