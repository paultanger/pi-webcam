import cv2
import matplotlib.pyplot as plt
import cvlib as cv
from cvlib.object_detection import draw_bbox
import time
import picamera
import picamera.array
import tempfile
import io
import numpy as np


def capture_save():
    '''
    '''

    # setup tempfile
    tempf = tempfile.NamedTemporaryFile(suffix='.jpg', delete=False)
    with picamera.PiCamera() as camera:
        camera.resolution = (1024, 768)
        camera.start_preview()
        # Camera warm-up time
        time.sleep(2)
        camera.capture(tempf.name)
    tempf.close()
    return tempf.name


def video_save(length):
    '''
    '''

    # setup tempfile
    tempf = tempfile.NamedTemporaryFile(suffix='.h264', delete=False)

    with picamera.PiCamera() as camera:
        #camera.resolution = (640, 480)
        camera.start_recording(tempf.name)
        camera.wait_recording(length)
        camera.stop_recording()
    tempf.close()
    return tempf.name


def vid_2_stream(stream_obj, length, return_arr=False):
    '''
    '''

    if return_arr:
        with picamera.PiCamera() as camera:
            camera.start_preview()
            time.sleep(2)
            with picamera.array.PiRGBArray(camera) as stream:
                camera.capture(stream, format='bgr')
                # At this point the image is available as stream.array
                image_arr = stream.array
        return image_arr
    else:
        with picamera.PiCamera() as camera:
            camera.resolution = (640, 480)
            camera.start_recording(stream_obj, format='h264', quality=23)
            camera.wait_recording(length)
            # for i in range(2, 11):
            #   camera.split_recording('%d.h264' % i)
            #   camera.wait_recording(length)
            camera.stop_recording()
    
    return stream_obj


def cv2_predict(img_path):
    '''
    '''

    # setup tempfile
    tempf = tempfile.NamedTemporaryFile(suffix='.jpg', delete=False)

    imgcv = cv2.imread(img_path)
    bbox, label, conf = cv.detect_common_objects(imgcv)
    output_image = draw_bbox(imgcv, bbox, label, conf)
    plt.imsave(tempf.name, output_image)

    return tempf.name


def gen(vc):
    """
    Video streaming generator function.
    """ 
    # used to record the time when we processed last frame
    prev_frame_time = 0
    # used to record the time at which we processed current frame
    new_frame_time = 0
    while True:
        rval, frame = vc.read() 
        #frame = camera.get_frame()
        #breakpoint()
        # resizing the frame size according to our need
        #frame = cv2.resize(frame, (1920, 1080)) # width height default 480 x 640

        # font which we will be using to display FPS
        font = cv2.FONT_HERSHEY_SIMPLEX
        # time when we finish processing for this frame
        new_frame_time = time.time()

        # fps will be number of frame processed in given time frame
        # since their will be most of time error of 0.001 second
        # we will be subtracting it to get more accurate result
        fps = 1/(new_frame_time-prev_frame_time)
        prev_frame_time = new_frame_time

        # convert for display
        fps = f'frames per sec: {str(int(fps))}'

        # puting the FPS count on the frame
        cv2.putText(frame, fps, (7, 20), font, 0.5, (100, 255, 0), 1, cv2.LINE_AA)
        
        #picam.annotate_text = fps

        #cv2.imwrite('pic.jpg', frame) 
        # or instead of writing to disk
        byteArray = cv2.imencode('.jpg', frame)[1].tobytes()
        #yield (b'--frame\r\n' 
        #       b'Content-Type: image/jpeg\r\n\r\n' + open('pic.jpg', 'rb').read() + b'\r\n') 
        yield (b'--frame\r\n' 
               b'Content-Type: image/jpeg\r\n\r\n' + byteArray + b'\r\n') 