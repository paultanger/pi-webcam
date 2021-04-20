
import cv2
import matplotlib.pyplot as plt
import cvlib as cv
from cvlib.object_detection import draw_bbox
im = cv2.imread('apple-256261_640.jpg')
bbox, label, conf = cv.detect_common_objects(im)
output_image = draw_bbox(im, bbox, label, conf)
plt.imshow(output_image)
plt.show()


from darkflow.net.build import TFNet
import cv2

#options = {"model": "cfg/yolov3.cfg", "load": "/home/pi/yolo_pretrained_weights/yolov3.weights", "threshold": 0.1}
#options = {"model": "cfg/yolov2.cfg", "load": "/home/pi/yolo_pretrained_weights/yolov2.weights", "threshold": 0.1}
options = {"model": "cfg/yolo.cfg", "load": "/home/pi/yolo_pretrained_weights/yolov2.weights", "threshold": 0.1}

tfnet = TFNet(options)

imgcv = cv2.imread("./sample_img/sample_dog.jpg")
result = tfnet.return_predict(imgcv)
print(result)

# or this
# https://machinelearningmastery.com/how-to-perform-object-detection-with-yolov3-in-keras/
# https://raw.githubusercontent.com/experiencor/keras-yolo3/master/yolo3_one_file_to_detect_them_all.py
# other weights 
# https://github.com/tensorflow/models/blob/master/research/object_detection/g3doc/tf2_detection_zoo.md


# darknet is slower .. try doing it directly too..

weights_file = '/home/pi/yolo_pretrained_weights/yolov3.weights'

from abc import ABC, abstractmethod
 
 
class ObjectDetector(ABC):
    @abstractmethod
    def detect(self, frame, threshold=0.0):
        Pass
        
# initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 32
rawCapture = PiRGBArray(camera, size=(640, 480))

# allow the camera to warm up
time.sleep(0.1)

for frame in camera.capture_continuous(rawCapture, format="bgr",
                                       use_video_port=True):

    # grab the raw NumPy array representing the image, then 
    # initialize the timestamp and occupied/unoccupied text
    image = frame.array

    result = predictor.detect(image)

    for obj in result:
        logger.info('coordinates: {} {}. class: "{}". confidence: {:.2f}'.
                    format(obj[0], obj[1], obj[3], obj[2]))

        cv2.rectangle(image, obj[0], obj[1], (0, 255, 0), 2)
        cv2.putText(image, '{}: {:.2f}'.format(obj[3], obj[2]),
                    (obj[0][0], obj[0][1] - 5),
                    cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 0), 2)


    # show the frame
    cv2.imshow("Stream", image)
    key = cv2.waitKey(1) & 0xFF