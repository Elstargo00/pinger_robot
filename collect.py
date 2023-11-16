
from pypylon import pylon
from ultralytics import YOLO
import torch

from PingerVision.Camera_communication import detect_cameras, CameraProcessor


CAMERA_CONFIG1 = ""

if __name__ == "__main__":

    # initiate model
    model = YOLO("./model/best.pt")
    acc = "cuda" if torch.cuda.is_available() else "cpu"
    model.to(acc)

    # device
    devices = detect_cameras()
    processor = CameraProcessor(device=devices[0], config_path=CAMERA_CONFIG1, model=model)
    processor.oneshot_capture()