from abc import abstractmethod, ABC # abc enables abstractions for classes
from math import acos, degrees
import mediapipe as mp # Library for extrapolating landmarks of a human from an image

# 
mp_pose_landmarks = mp.solutions.pose.PoseLandmark

def distance(x, y):
    return (x ** 2 + y ** 2) ** 0.5
    
def distance_between_landmarks(detection_result, pointA: int, pointB: int):
    landmarks = detection_result.landmark
    landmarkA, landmarkB = landmarks[pointA], landmarks[pointB]
    return distance(landmarkA.x - landmarkB.x, landmarkA.y - landmarkB.y)

def find_angle_between_landmarks(detection_result, pointA: int, pointB: int, pointC: int):
    """
    Calculate the angle formed by three landmarks.
    
    @params:
        detection_result: The result from a Mediapipe pose detection.
        pointA (int): Index of the first landmark.
        pointB (int): Index of the second landmark.
        pointC (int): Index of the third landmark.
    
    @returns:
        float: Angle between the three landmarks in degrees.
    """
    edgeAB = distance_between_landmarks(detection_result, pointA, pointB)
    edgeAC = distance_between_landmarks(detection_result, pointA, pointC)
    edgeCB = distance_between_landmarks(detection_result, pointC, pointB)
    angle = degrees(acos((edgeCB ** 2 + edgeAB ** 2 - edgeAC ** 2) / (2 * edgeAB * edgeCB)))
    if angle > 180:
        angle = 360 - angle
    if angle < 0:
        angle += 360
    return angle

class Recognizer(ABC):    
    """
    Abstract base class for exercise recognizers.
    """
    @abstractmethod
    def run(self, detection_results, time_elapsed: float) -> bool:
        """
        Process detection results and update the recognizer state.
        
        @params:
            detection_results: The result from a Mediapipe pose detection.
            time_elapsed (float): Time elapsed since the last update.
        
        @returns:
            bool: Whether the exercise was successfully detected.
        """
        pass
    
    @abstractmethod
    def report_stats(self):
        """
        Report Internal Statistics, i.e. rep count
        """
        pass
    
    @abstractmethod
    def reset(self):
        """
        Reset method to reset Recognizer to its initial state
        """
        pass
        
class Squats(Recognizer):
    def __init__(self):    
        self.count = 0
        self.in_squat_position = False
    
    def run(self, detection_results, time_elapsed: float) -> bool:
        left_knee_angle = find_angle_between_landmarks(detection_results, mp_pose_landmarks.LEFT_HIP, mp_pose_landmarks.LEFT_KNEE, mp_pose_landmarks.LEFT_ANKLE)
        right_knee_angle = find_angle_between_landmarks(detection_results, mp_pose_landmarks.RIGHT_HIP, mp_pose_landmarks.RIGHT_KNEE, mp_pose_landmarks.RIGHT_ANKLE)
        
        if left_knee_angle < 90 or right_knee_angle < 90:
            if not self.in_squat_position:
                self.in_squat_position = True
                self.count += 1
                return True
        else:
            self.in_squat_position = False
            
        return False
    
    def report_stats(self):
        return self.count
    
    def reset(self):
        self.count = 0
        
class BicepCurls(Recognizer):
    def __init__(self):    
        self.count = 0
        self.in_curl_position = False
    
    def run(self, detection_results, time_elapsed: float) -> bool:
        left_elbow_angle = find_angle_between_landmarks(detection_results, mp_pose_landmarks.LEFT_SHOULDER, mp_pose_landmarks.LEFT_ELBOW, mp_pose_landmarks.LEFT_WRIST)
        right_elbow_angle = find_angle_between_landmarks(detection_results, mp_pose_landmarks.RIGHT_SHOULDER, mp_pose_landmarks.RIGHT_ELBOW, mp_pose_landmarks.RIGHT_WRIST)
        
        if left_elbow_angle < 60 or right_elbow_angle < 60:
            if not self.in_curl_position:
                self.in_curl_position = True
                self.count += 1
                return True
        else:
            self.in_curl_position = False
            
        return False
    
    def report_stats(self):
        return self.count
    
    def reset(self):
        self.count = 0
        
class JumpingJacks(Recognizer):
    def __init__(self):    
        self.count = 0
        self.in_jump_position = False
    
    def run(self, detection_results, time_elapsed: float) -> bool:
        left_arm_angle = find_angle_between_landmarks(detection_results, mp_pose_landmarks.LEFT_WRIST, mp_pose_landmarks.LEFT_SHOULDER, mp_pose_landmarks.LEFT_HIP)
        right_arm_angle = find_angle_between_landmarks(detection_results, mp_pose_landmarks.RIGHT_WRIST, mp_pose_landmarks.RIGHT_SHOULDER, mp_pose_landmarks.RIGHT_HIP)
        
        if left_arm_angle > 160 or right_arm_angle > 160:
            if not self.in_jump_position:
                self.in_jump_position = True
                self.count += 1
                return True
        else:
            self.in_jump_position = False
            
        return False
    
    def report_stats(self):
        return self.count
    
    def reset(self):
        self.count = 0