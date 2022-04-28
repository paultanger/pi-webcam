from flask import Flask, request, render_template, Response, send_file
from flask_basicauth import BasicAuth
import sys, os
import cv2
import cvlib as cv
from cvlib.object_detection import draw_bbox
import picamera
import time
from datetime import datetime, timedelta
import tempfile
from io import BytesIO
from collections import Counter
from twilio.rest import Client
sys.path.insert(0, '../src/')
#sys.path.append(os.path.join(os.path.dirname(sys.path[0]), '../src/'))
import funcs as myfuncs
import hen_door as door_funcs

# setup pins
open_door_pin = 17
close_door_pin = 18

open_door_pin = 26
close_door_pin = 20 

# setup hen door - these are pins
door_funcs.setup(open_door_pin, close_door_pin)

# for log..
print('-------------------------------------------------------------')
print('----------------- new app instance --------------------------')
print('-------------------------------------------------------------')
print(f'app start time: {datetime.now()}')

# setup twilio stuff
# these are stored in /etc/rc.local
account_sid = os.environ.get('TWILIO_ACCOUNT_SID')
auth_token = os.environ.get('TWILIO_AUTH_TOKEN')
twilio_phone = os.environ.get('TWILIO_PHONE_NUM')
my_phone = os.environ.get('MY_PHONE_NUM')
# mer_phone = os.environ['MER_PHONE_NUM']

client = Client(account_sid, auth_token)

# wait a bit before trying camera
time.sleep(2)

# this determines if you want to start the video cam
if len(sys.argv) > 2:
    start_cam = False
    #vc = None
else:
    start_cam = True
    # vc = cv2.VideoCapture(0) # zero is the default camera on pi
    # check available cameras, framerate combinations:
    # libcamera-raw --list-cameras 640x480 1296x972 1920x1080 2592x1944
    # try with new bullseye libcamera stuff instead:
    gst_str = ('libcamerasrc ! ' + 'video/x-raw,' +
                'width=1920, height=1080,' +
                'framerate=30/1 ! ' +
                'videoconvert ! appsink')
    vc = cv2.VideoCapture(gst_str, cv2.CAP_GSTREAMER)

# initialize text time as 30 minutes earlier than app start
mins_30 = timedelta(minutes=30)
global text_time
text_time = datetime.now() - mins_30
print(f'app starting time minus 30 mins: {text_time}')

# app = Flask(__name__)
app = Flask(__name__, root_path='./')# template_folder = 'templates/')
# app = Flask(__name__, root_path='./', static_url_path='/Users/pault/Desktop/github/media/', 
# app = Flask(__name__, root_path='./', static_url_path='/Users/pault/Desktop/github/media/') 

#vc.set(cv2.CAP_PROP_FRAME_WIDTH, 720)

# or another way
# https://www.pyimagesearch.com/2017/02/06/faster-video-file-fps-with-cv2-videocapture-and-opencv/

# allow the camera to warmup
time.sleep(2)

# convert to opencv compatible
# image = np.empty((240 * 320 * 3,), dtype=np.uint8)
# camera.capture(image, 'bgr')
# image = image.reshape((240, 320, 3))

# setup login
app.config['BASIC_AUTH_USERNAME'] = os.environ['app_user']
app.config['BASIC_AUTH_PASSWORD'] = os.environ['app_pass']
basic_auth = BasicAuth(app)

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
        
        # if empty, exit
        if not rval:
            break
        # resizing the frame size according to our need
        frame = cv2.resize(frame, (640, 480)) # width height default 640 x 480

        # flip frame (depending on how we setup the camera)
        frame = cv2.flip(frame, 0)

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


def gen_predict():
#def gen_predict(text_time=text_time):
    '''
    This might only work if someone is actually streaming it to trigger this.. hmmm
    
    '''
    # TODO: fix this.. every time a page is running it will start a new timer..
    # mins_30 = timedelta(minutes=30)
    # text_time = datetime.now() - mins_30
    # setup global var as something we can modify here
    global text_time
    while True:
        rval, frame = vc.read() 

        # if empty, exit
        if not rval:
            break

        # resizing the frame size according to our need
        frame = cv2.resize(frame, (640, 480)) # width height default 640 x 480

        # flip frame (depending on how we setup the camera)
        frame = cv2.flip(frame, 0)

        # seems like 45% conf eliminates multiple guesses on same egg I think
        # for nms, .5 is not enough..
        # bbox, label, conf = cv.detect_common_objects(frame, confidence=.35, model='yolov4')
        bbox, label, conf = cv.detect_common_objects(frame, confidence=.3, model='yolov4-tiny') #, nms_thresh=0.4)
        output_image = draw_bbox(frame, bbox, label, conf, write_conf=True)
        time_stamp = datetime.now().strftime('%Y %m %d %H:%M:%S') 
        if label == []:
            cv2.putText(output_image, f'no predictions, {time_stamp}', (7, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (100, 255, 0), 1, cv2.LINE_AA)
        else:
            cv2.putText(output_image, f'{time_stamp}', (7, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (100, 255, 0), 1, cv2.LINE_AA)
            #cv2.imwrite('pic.jpg', output_image) 
        
            # here is where I can check if it predicts orange (egg), and alert me.. 
            # possible predictions, this is a set
            egg_labels = {'sports ball', 'orange', 'apple', 'bowl', 'clock', 'mouse'}
            labels = [lab for lab in label if lab in egg_labels]
            # only keep labels in this group
            label_count = Counter(labels)
            # since the fake egg is one.. we only care if more than one..
            # if they are both predicted as the same thing, the set only counts 1
            # if any(item in egg_labels for item in label):
            # if len(egg_labels.intersection(set(label))) > 1:
            
            if len(label_count) > 1 or max(label_count.values(), default=-999) > 1:
                # determine if I have been texted in the last 30 mins?
                time_diff = (datetime.now() - text_time).total_seconds()
                min_diff = divmod(time_diff, 60)[0]
                if min_diff >= 30:
                    # text me..
                    # client.messages.create(body = "a possible egg!",from_= twilio_phone,to = my_phone)
                    # text me
                    message = client.messages \
                    .create(
                        body = "a possible egg!",
                        from_= twilio_phone,
                        to = my_phone
                    )
                    # restart time to wait 30 mins before doing again
                    #global text_time
                    # also round it so it doesn't consider ms if two pages running..
                    text_time = datetime.now().replace(second=0, microsecond=0)
                    print(f'sent text and resetting time to {text_time}')
                    app.logger.info(f'sent text and resetting time to {text_time}')

        byteArray = cv2.imencode('.jpg', output_image)[1].tobytes()
        # don't do this for every frame
        time.sleep(3)
        yield (b'--frame\r\n' 
               b'Content-Type: image/jpeg\r\n\r\n' + byteArray + b'\r\n') 


@app.route('/video_feed', methods=['GET'])
def video_feed():
    """
    Video streaming route. Put this in the src attribute of an img tag.
    """
    return Response(gen(), mimetype='multipart/x-mixed-replace; boundary=frame')
    #return Response(myfuncs.gen(vc), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/predict_feed', methods=['GET'])
def predict_feed():
    """
    This is the detect version of the feed with predictions..
    """
    return Response(gen_predict(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/view_predict', methods=['GET'])
def view_predict():
        return render_template("view_predict.html")

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

@app.route('/stop_feed', methods=['GET', 'POST'])
def stop_feed():
    # TODO: get this working with new gstreamer..
    cv2.waitKey(500)
    vc.release()
    cv2.destroyAllWindows()
    time.sleep(1)
    # del vc
    return render_template("setup_recordings.html")


@app.route('/start_feed', methods=['GET', 'POST'])
def start_feed():
    global vc
    # vc = cv2.VideoCapture(0)
    gst_str = ('libcamerasrc ! ' + 'video/x-raw,' +
            'width=1920, height=1080,' +
            'framerate=30/1 ! ' +
            'videoconvert ! appsink')
    vc = cv2.VideoCapture(gst_str, cv2.CAP_GSTREAMER)
    time.sleep(2)
    return render_template("view_cam.html")


@app.route('/', methods=['GET'])
def home():
    return render_template("index.html")


@app.route('/view_cam', methods=['GET'])
def view_cam():
    if start_cam:
        return render_template("view_cam.html")
    else:
        return f"""cam not started"""


@app.route('/setup_recordings', methods=['GET'])
@basic_auth.required
def setup_recordings():
    return render_template("setup_recordings.html")


@app.route('/get_file', methods=['GET', 'POST'])
def get_file():
    return send_file(the_file, as_attachment=True)


@app.route('/results', methods=['GET', 'POST'])
def results():
    record_time = float(request.form['record_time']) * 60
    try:
        # start the recording..
        global the_file
        the_file = myfuncs.video_save(record_time)
        return render_template('results.html',
                            record_time=record_time/60,
                            the_file=the_file)

    except:
        return f"""something isn't quite working right."""
    

    # return render_template('results.html', 
    #                         predict_text=predict_text, 
    #                         actual_text=actual_text, 
    #                         img_paths=img_paths,
    #                         data=result.to_html(index=False, classes=["table", "text-right", "table-hover"], border=0))


@app.route('/hen_door', methods=['GET', 'POST'])
@basic_auth.required
def hen_door():
    return render_template("hen_door.html")


@app.route('/door_open', methods=['GET', 'POST'])
def door_open():
    try:
        door_funcs.setup(open_door_pin, close_door_pin)
        door_funcs.activate_door('open', 25, open_door_pin, close_door_pin)
    except:
        return render_template("index.html")
    return render_template("hen_door.html")


@app.route('/door_close', methods=['GET', 'POST'])
def door_close():
    try:
        door_funcs.setup(open_door_pin, close_door_pin)
        door_funcs.activate_door('close', 26, open_door_pin, close_door_pin)
    except:
        return render_template("index.html")
    return render_template("hen_door.html")


@app.route('/custom_door', methods=['GET', 'POST'])
def custom_door():
    time = float(request.form['time'])
    direction = request.form['direction']
    try:
        door_funcs.setup(open_door_pin, close_door_pin)
        door_funcs.activate_door(direction, time, open_door_pin, close_door_pin)
    except:
        return render_template("index.html")
    return render_template("hen_door.html")


@app.route('/view_logs', methods=['GET', 'POST'])
@basic_auth.required
def view_logs():
    return render_template("view_logs.html")


@app.route('/view_logs_result', methods=['GET', 'POST'])
def view_logs_result():
    log_file = request.form['log_file']
    if log_file == 'door_log':
        log_file = '/etc/python_log_files/door_log.log'
    else:
        log_file = '/etc/python_log_files/app_log.log'
    try:
        # pull up log file
        with open(log_file, "r") as file:
            content = file.read()
        return render_template("view_logs_result.html", log_file=log_file, content=content)
    except:
        return render_template("index.html")

if __name__ == '__main__':
    # test with 
    # python app.py local 
    # run with
    # python app.py prod 
    # if you don't want the cam to start:
    # python app.py prod False
    print('starting app..')
    if sys.argv[1] == 'local':
        app.run(host='0.0.0.0', port=8080, debug=True)
    else:
        app.run(host='0.0.0.0', port=33507, debug=False)
