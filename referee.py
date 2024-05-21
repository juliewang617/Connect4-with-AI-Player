from flask import Flask, render_template, session, redirect, url_for
from flask_session import Session
from tempfile import mkdtemp
from connect4 import *
from ai_player import * 

app = Flask(__name__)

app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False 
app.config["SESSION_TYPE"] = "filesystem" 
Session(app)

# MAIN ROUTE
@app.route("/")
def index(): 
    if "state" not in session: 
        session["state"] = initialState()

    return render_template("game.html", 
                           board = session["state"].board, 
                           player = session["state"].player, 
                           legal_moves = legal_moves(session["state"]),
                           status = session["state"].status)

@app.route("/play/<int:move>") 
def play(move):
    if "state" in session:  
        session["state"] = next_state(session["state"], move)
        # print("VALUE: " + str(estimate_value(session["state"])))
        # print("VALUE: " + str(estimate_horz(session["state"].board, session["state"].player)))
    return redirect(url_for("index"))

@app.route("/aiplay") 
def aiplay():
    if "state" in session: 
        session["state"] = next_state(session["state"], pick_move(session["state"]))
    return redirect(url_for("index"))

@app.route("/restart") 
def restart():
    if "state" in session:  
        session["state"] = initialState()
    return redirect(url_for("index"))