import multiprocessing
from multiprocessing import Pool
from pypylon import pylon
from ultralytics import YOLO
import torch
import cv2
from PingerVision.utils import get_current_time
import os


from PingerVision.Camera_communication import CameraProcessor

CAMERA_CONFIG = "/home/elstargo00/Projects/pinger_robot/cam_config.pfs"
CAPTURE_DIRECTORY = "/home/elstargo00/Projects/pinger_robot/captures"


def camera_worker(device_id, config_path):
    try:
        print(f"Trying to create camera processor with id: {device_id}")
        processor = CameraProcessor(device_id, config_path)
        print("Camera processor created successfully!")

    except Exception as e:
        print(f"Error in camera_worker: {e}")

    else: 
        return processor.continuous_capture()

def process_imgs(img_list, model):
    # isProtruded = False
    # results = model(source=img_list, verbose=False)
    # for i, result in enumerate(results):
    for i, _ in enumerate(len(img_list)):
        # currentProtruded += bool(len([result.names[int(res.boxes.cls)] for res in result]))
        # isProtruded += currentProtruded

        # if currentProtruded: # use this setting in the interpretation mode 
        if True: # use this setting in capturing mode
            frame_name = f"frame_{get_current_time()}.png"
            frame_path = os.path.join(CAPTURE_DIRECTORY, frame_name)
            cv2.imwrite(frame_path, img_list[i]) # write to disk
            print(f"Captured {frame_name}")

    return bool(isProtruded)


if __name__ == "__main__":

    # model = YOLO("./model/best.pt")
    model = None
    # acc = "cuda" if torch.cuda.is_available() else "cpu"
    # model.to(acc)

    multiprocessing.set_start_method("spawn")

    print("Start pool")
    # 3 processor CPU
    with Pool(processes=3) as pool:
        # while True:
        list_batch = pool.starmap(
            camera_worker,
            [
                (0, CAMERA_CONFIG, ),
                (1, CAMERA_CONFIG, ), 
                (2, CAMERA_CONFIG, )
            ]
        )
        # print(len(list_batch))
        # print(list_batch)

    # GPU
    # for somelist in list_batch:
        # print(len(somelist))
    img_list = [item for sublist in list_batch for item in sublist]
    isProtruded = process_imgs(img_list, model)

    # print(f"Protruded Detected!") if isProtruded else print("Pallet is clean")
    # print("End pool")