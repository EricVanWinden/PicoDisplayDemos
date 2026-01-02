import threading
from flask import Flask, jsonify, render_template
from web_button import BUTTON_STATES
from web_graphics import DRAW_COMMANDS

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("home.html")


@app.route("/frame")
def frame():
    return jsonify(DRAW_COMMANDS)


@app.route("/button/<btn>/<state>")
def button(btn, state):
    BUTTON_STATES[btn] = (state == "down")
    return "ok"


def start_server():
    app.run(host="0.0.0.0", port=5000, debug=False)


def start_web_display():
    thread = threading.Thread(target=start_server, daemon=True)
    thread.start()
