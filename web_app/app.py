from flask import Flask, request, render_template, Response, send_file
import sys, os
import cv2
import picamera
import time
from io import BytesIO

# app = Flask(__name__)
app = Flask(__name__, root_path='./')# template_folder = 'templates/')
# app = Flask(__name__, root_path='./', static_url_path='/Users/pault/Desktop/github/media/', 
# app = Flask(__name__, root_path='./', static_url_path='/Users/pault/Desktop/github/media/') 

vc = cv2.VideoCapture(0) # zero is the default camera on pi
#vc.set(cv2.CAP_PROP_FRAME_WIDTH, 720)

# or another way
# https://www.pyimagesearch.com/2017/02/06/faster-video-file-fps-with-cv2-videocapture-and-opencv/

# allow the camera to warmup
time.sleep(1)

# convert to opencv compatible
# image = np.empty((240 * 320 * 3,), dtype=np.uint8)
# camera.capture(image, 'bgr')
# image = image.reshape((240, 320, 3))

def gen():
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


@app.route('/video_feed', methods=['GET'])
def video_feed():
    """
    Video streaming route. Put this in the src attribute of an img tag.
    """
    return Response(gen(), mimetype='multipart/x-mixed-replace; boundary=frame')

# @app.route('/video_feed', methods=['GET'])
# def video_feed():
#     """
#     Video streaming route. Put this in the src attribute of an img tag.
#     """
#     with picamera.PiCamera() as camera:
#         camera.resolution = (640, 480)
#         stream = BytesIO()
#         for foo in camera.capture_continuous(stream, format='jpeg'):
#             stream.truncate()
#             stream.seek(0)
#         return send_file(stream, mimetype='image/jpeg')

@app.route('/', methods=['GET'])
def home():
    return render_template("index.html")


@app.route('/view_cam', methods=['GET'])
def view_cam():
    return render_template("view_cam.html")


@app.route('/query', methods=['GET', 'POST'])
def query():
    return render_template("query.html")


@app.route('/results', methods=['GET', 'POST'])
def results():
    pass
    # try:
    #     pass
    #     # n_sample = int(request.form['n_sample'])
    #     # predict_type = request.form['predict_type']
    # except:
    #     return f"""You have entered an incorrect value or something isn't quite working right.
    #                 Sorry about that!  Hit the back button and try again."""

    # return render_template('results.html', 
    #                         predict_text=predict_text, 
    #                         actual_text=actual_text, 
    #                         img_paths=img_paths,
    #                         data=result.to_html(index=False, classes=["table", "text-right", "table-hover"], border=0))


if __name__ == '__main__':
    # test with 
    # python app.py local
    # run with
    # python app.py prod
    if sys.argv[1] == 'local':
        app.run(host='0.0.0.0', port=8080, debug=True)
    else:
        app.run(host='0.0.0.0', port=33507, debug=False)