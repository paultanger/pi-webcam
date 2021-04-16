from flask import Flask, request, render_template
import sys, os

# app = Flask(__name__)
app = Flask(__name__, root_path='./')# template_folder = 'templates/')
# app = Flask(__name__, root_path='./', static_url_path='/Users/pault/Desktop/github/media/', 
# app = Flask(__name__, root_path='./', static_url_path='/Users/pault/Desktop/github/media/') 


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
    try:
        pass
        # n_sample = int(request.form['n_sample'])
        # predict_type = request.form['predict_type']

    except:
        return f"""You have entered an incorrect value or something isn't quite working right.
                    Sorry about that!  Hit the back button and try again."""

    # return render_template('results.html', 
    #                         predict_text=predict_text, 
    #                         actual_text=actual_text, 
    #                         img_paths=img_paths,
    #                         data=result.to_html(index=False, classes=["table", "text-right", "table-hover"], border=0))


if __name__ == '__main__':
    if len(sys.argv) > 1:
        app.run(host='0.0.0.0', port=33507, debug=False)
    else:
        app.run(host='0.0.0.0', port=8080, debug=True)