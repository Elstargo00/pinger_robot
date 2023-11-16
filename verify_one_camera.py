from pypylon import pylon
from ultralytics import YOLO
import torch

from PingerVision.Camera_communication import CameraProcessor

CAMERA_CONFIG = "/home/elstargo00/Projects/pinger_robot/cam_config.pfs"

if __name__ == "__main__":

    model = YOLO("./model/best.pt")
    acc = "cuda" if torch.cuda.is_available() else "cpu"
    model.to(acc)

    processor = CameraProcessor(0, CAMERA_CONFIG)
    img_list = processor.continuous_capture(False)

    print(img_list)