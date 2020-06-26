import os
from random import choice
from string import ascii_letters
from flask import Flask, render_template, redirect, request
from neuro import get_data

app = Flask(__name__)
BASE_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
UPLOAD_FOLDER = os.path.join(BASE_DIR, "NeyroButi", "static", "photo")


@app.route('/', methods=['GET'])
def index():
    return render_template("index.html")


@app.route('/upload', methods=['POST'])
def upload():
    filename = ''.join(choice(ascii_letters) for _ in range(100))
    request.files["photo"].save(os.path.join(UPLOAD_FOLDER, filename + ".jpg"))
    return redirect("result?photo={}".format(filename))


@app.route('/result', methods=['GET'])
def result():
    photo = request.args.get("photo")
    return render_template("result.html", photo=photo, data=get_data(photo))


app.run(host="0.0.0.0", port=9090)