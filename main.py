import os

# Suppress Tensorflow info and warning messages.
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"

from flask import Flask, render_template, Response, request
from camera import WebCamera, Video
from camera import get_img
from werkzeug.utils import secure_filename
import time


# Generate timestamp.
timestr = time.strftime("%Y%m%d-%H%M%S")

# To generate predictions and return image.
def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b"--frame\r\n" b"Content-Type: image/jpeg\r\n\r\n" + frame + b"\r\n\r\n")


app = Flask(__name__)


# Home Page.
@app.route("/")
def index():
    return render_template("home.html")


# Live video feed.
@app.route("/live")
def live():
    return Response(gen(WebCamera()), mimetype="multipart/x-mixed-replace; boundary=frame")


# Upload images.
@app.route("/upload", methods=["GET", "POST"])
def upload():
    result = {"pred": 0}
    if request.method == "POST":
        try:
            image = request.files["inpfile"]  # Get the file.
            # Get secured file name and add timestamp to make it unique.
            filename = timestr + "-" + secure_filename(image.filename)
            save_path = os.path.join("uploaded_images", filename)
            image.save(save_path)

        except:
            return "Failure in uploading, please try again!"

        try:
            cwd = os.getcwd()
            path = str(cwd + "/" + save_path)

            result["pred"] = get_img(img_path=path)

            return render_template("upload.html", res=result)
        except:
            return "We could not identify the faces in this image, please try with another image!"

    return render_template("upload.html", res=result)


# Present choice of pre loaded videos.
@app.route("/video")
def video():
    return render_template("video.html")


# Video of Presidential Debate.
@app.route("/video1")
def video1():
    return Response(gen(Video(id=1)), mimetype="multipart/x-mixed-replace; boundary=frame")


# Video of facial expressions.
@app.route("/video2")
def video2():
    return Response(gen(Video(id=2)), mimetype="multipart/x-mixed-replace; boundary=frame")


# About project page.
@app.route("/aboutproj")
def aboutproj():
    return render_template("aboutproj.html")


# About us page.
@app.route("/aboutus")
def aboutus():
    return render_template("aboutus.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=False)
