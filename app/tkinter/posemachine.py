import os
# Repo root and dataset folder (override with EPEM_ROOT / EPEM_DATA_DIR).
REPO_ROOT = os.environ.get("EPEM_ROOT", os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
DATA_DIR = os.environ.get("EPEM_DATA_DIR", os.path.join(os.path.dirname(REPO_ROOT), "exercise-pose-data"))
import sys

sys.path.append(REPO_ROOT)
from keypoints_extractor import KeypointsExtractor
from detectors_keras_api.initial_pose_detector_keras import InitialPoseDetector
from detectors_keras_api.right_hand_detector_keras import RightHandUpDetector


class PoseMachine():
    __instance = None

    @staticmethod
    def get_instance():
        if PoseMachine.__instance == None:
            PoseMachine()
        return PoseMachine.__instance

    def __init__(self):
        """ Virtually private constructor. """
        if PoseMachine.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            self.target_id = ""
            self.exercise_type = ""
            self.pose_predictions = []
            self.kp_extractor = KeypointsExtractor()
            self.init_pose_detector = InitialPoseDetector()
            self.right_hand_up_detector = RightHandUpDetector()
            PoseMachine.__instance = self
    
    @staticmethod
    def dispose():
        PoseMachine.__instance = None


if __name__ == "__main__":
    pm1 = PoseMachine.get_instance()
    pm2 = PoseMachine.get_instance()

    print("pm1 kp_extractor -->", pm1.kp_extractor)
    print("pm2 kp_extractor -->", pm2.kp_extractor)