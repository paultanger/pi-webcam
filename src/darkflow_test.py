# only works when running from darkflow dir..
from darkflow.net.build import TFNet
import cv2

options = {"model": "/home/pi/github/darkflow/cfg/yolo.cfg", "load": "/home/pi/yolo_pretrained_weights/yolov2.weights", "threshold": 0.1}
tfnet = TFNet(options)

imgcv = cv2.imread("/home/pi/github/darkflow/sample_img/egg.png")
result = tfnet.return_predict(imgcv)
print(result)
