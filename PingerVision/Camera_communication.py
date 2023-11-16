from pypylon import pylon
import cv2
import os
import supervision as sv
from PingerVision.utils import get_current_time

# CAPTURE_DIRECTORY = "/home/elstargo00/Projects/pinger_robot/captures"



class CameraProcessor:

    box_annotator = sv.BoxAnnotator(
        thickness=2,
        text_thickness=2,
        text_scale=1
    )

    def __init__(self, device_id, config_path):
        # Initialize camera parameters
        self.camera, self.converter = self.init_camera(device_id, config_path)
        self.frame_count = 0
        self.mem_pool = []
        self.signal = False

    def check_signal(self):
        """Check signal from PLC return True / False"""
        ...


    def init_camera(self, device_id, config_path):

        def detect_cameras():
            return pylon.TlFactory.GetInstance().EnumerateDevices()
    
        devices = detect_cameras()

        # print(devices[device_id])

        camera = pylon.InstantCamera(pylon.TlFactory.GetInstance().CreateDevice(devices[device_id]))

        camera.StartGrabbing(pylon.GrabStrategy_LatestImageOnly)

        # load config
        # pylon.FeaturePersistence.Load(config_path, camera.GetNodeMap(), True)

        converter = pylon.ImageFormatConverter()
        converter.OutputPixelFormat = pylon.PixelType_BGR8packed
        converter.OutputBitAlignment = pylon.OutputBitAlignment_MsbAligned

        print("Initiate Camera & Converter")

        return camera, converter


    def get_frame(self, grabResult):
        # Capture a single frame from the camera
        image = self.converter.Convert(grabResult)
        image = image.GetArray()
        return image


        

    def continuous_capture(self):
        """
        - Continuous capturing & save to disk
        - Continuous capturing & save to memory 
        - Process the images (per frame)
        - Process the images (from source)
        """
        try:
            while self.camera.IsGrabbing():
                grabResult = self.camera.RetrieveResult(5000, pylon.TimeoutHandling_ThrowException)

                if grabResult.GrabSucceeded():

                    frame = self.get_frame(grabResult)
                    cv2.namedWindow("current_frame", cv2.WINDOW_NORMAL) # for visualization
                    cv2.imshow("current_frame", frame) # for visualization

                    g = cv2.waitKey(1)
                    if g == ord('g'): # Check PLC signal
                        self.signal = True
                        print("Start recording...")
                    elif g == ord('h'): # Check PLC signal
                        self.signal = False

                    if self.signal:
                        if self.frame_count % 50 == 0:
                            self.mem_pool.append(frame)


                    # k = cv2.waitKey(1)
                    # if k == ord('c'):
                    #     if save:
                    #         frame_name = f"frame_{get_current_time()}.png"
                    #         frame_path = os.path.join(CAPTURE_DIRECTORY, frame_name)
                    #         cv2.imwrite(frame_path, frame) # write to disk
                    #         print(f"Captured {frame_name}")
                    #     self.mem_pool.append(frame) # write to memory
                        
                    # elif k == 27:  # Press 'Esc' to exit
                    #     break

                    self.frame_count += 1

                    if (len(self.mem_pool) > 30): # check PLC signal
                        self.signal = False
                        return self.mem_pool

                grabResult.Release()

        except KeyboardInterrupt:  # Or some other stopping criterion
            self.release_camera()


    # def oneshot_capture(self):
    #     try:
    #         while self.camera.IsGrabbing():
    #             grabResult = self.camera.RetrieveResult(5000, pylon.TimeoutHandling_ThrowException)

    #             if grabResult.GrabSucceeded():

    #                 frame = self.get_frame(grabResult)
    #                 cv2.namedWindow("current_frame", cv2.WINDOW_NORMAL)
    #                 cv2.imshow("current_frame", frame)

    #                 k = cv2.waitKey(1)
    #                 if k == ord('c') == 0:
    #                     # frame = self.get_frame(grabResult)
    #                     frame_name = f"frame_{get_current_time()}.png"
    #                     frame_path = os.path.join(CAPTURE_DIRECTORY, frame_name)
    #                     cv2.imwrite(frame_path, frame)
    #                     print(f"Captured {frame_name}")

    #                     isProtruded = self.process_frame(frame)

    #                     if isProtruded:
    #                         print(f"Protruded Detected!") 
    #                         cv2.imshow("Protruded Detected!", frame)
    #                         cv2.waitKey(500)

    #                 elif k == 27:  # Press 'Esc' to exit
    #                     break

    #                 self.frame_count += 1

    #             grabResult.Release()

    #     except KeyboardInterrupt:  # Or some other stopping criterion
    #         self.release_camera()

    def release_camera(self):
        # Release the camera and clean up
        self.camera.StopGrabbing()

