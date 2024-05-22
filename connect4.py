import copy
from flask import Flask, render_template, session, redirect, url_for
from flask_session import Session
from tempfile import mkdtemp
import numpy as np 
from dataclasses import dataclass 
from estimate_helpers import estimate_diag, estimate_horz, estimate_vert 

app = Flask(__name__)

app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False 
app.config["SESSION_TYPE"] = "filesystem" 
Session(app)

######## 

# DATATYPES 

@dataclass
class square: 
    player: str 
    location: tuple[int, int]

@dataclass 
class board: 
    height: int 
    width: int 
    coords: list[list[square]]

@dataclass 
class state: 
    status: str 
    player: str 
    board: board 

# constants 
BOARD_HEIGHT = 5
BOARD_WIDTH = 7 

########

# switches the current player 
def switch_player(player : str) -> str: 
    match player: 
        case "P1": 
            return "P2"
        case "P2": 
            return "P1"

# create the initial state 
def initialState() -> state: 
    return state("Ongoing", 
                 "P1", 
                 board(BOARD_HEIGHT, BOARD_WIDTH, 
                       np.empty((BOARD_HEIGHT, BOARD_WIDTH), dtype=object)))

# define legal moves every round (where each int represents a column)
def legal_moves(s : state) -> list[int]: 
    match s.status: 
        case "Draw": 
            return []
        case "Win": 
            return []
        case "Ongoing": 
            output = []
            for i in range(s.board.width): 
                if not s.board.coords[0][i]:
                    output.append(i)
            return output 

# update the board 
def update_board(board: board, player: str, move: int) -> tuple[board, tuple[int, int]]: 
    board_copy = copy.deepcopy(board)
    updated_coords = np.transpose(board_copy.coords)
    i = board_copy.height - 1
    while (i >= 0):  
        if not updated_coords[move][i]: 
            board_copy.coords[i][move] = player
            break 
        i = i - 1
    return [board_copy, tuple([i, move])]

# check for vertical win
def check_vert_win(b: board, player: str, move_coords: tuple[int, int]) -> bool: 
    # 0 gives row, 1 gives col
    row = move_coords[0]
    col = move_coords[1]
    try: 
        if (b.coords[row+1][col] == player
            and b.coords[row+2][col] == player
            and b.coords[row+3][col] == player): 
            #print("VERT WIN DETECTED")
            return True 
    except: 
        pass

    return False 

# check for horizontal win
def check_horz_win(b: board, player: str, move_coords: tuple[int, int]) -> bool: 
    row = move_coords[0]
    col = move_coords[1]
    try: 
        if (b.coords[row][col+1] == player
            and b.coords[row][col+2] == player
            and b.coords[row][col+3] == player): 
            #print("HORZ WIN DETECTED")
            return True 
    except: 
        pass

    try: 
        if (col >= 3
            and b.coords[row][col-1] == player
            and b.coords[row][col-2] == player
            and b.coords[row][col-3] == player): 
            #print("HORZ WIN DETECTED")
            return True
    except: 
        pass 

    try: 
        if (col >= 1
            and b.coords[row][col-1] == player
            and b.coords[row][col+1] == player
            and b.coords[row][col+2] == player): 
            #print("HORZ WIN DETECTED")
            return True
    except: 
        pass

    try: 
        if (col >= 2
            and b.coords[row][col-1] == player
            and b.coords[row][col-2] == player
            and b.coords[row][col+1] == player): 
            #print("HORZ WIN DETECTED")
            return True
    except: 
        pass

    return False 

# check for diagonal win
def check_diag_win(b: board, player: str, move_coords: tuple[int, int]) -> bool: 
    row = move_coords[0]
    col = move_coords[1]

    try: 
        if (b.coords[row+1][col+1] == player
            and b.coords[row+2][col+2] == player
            and b.coords[row+3][col+3] == player): 
            #print("DIAG WIN DETECTED")
            return True 
    except: 
        pass

    try: 
        if (col >= 3 
            and b.coords[row+1][col-1] == player
            and b.coords[row+2][col-2] == player
            and b.coords[row+3][col-3] == player): 
            #print("DIAG WIN DETECTED")
            return True 
    except: 
        pass

    try: 
        if (row >= 1 and col >= 1 
            and b.coords[row-1][col-1] == player
            and b.coords[row+1][col+1] == player
            and b.coords[row+2][col+2] == player): 
            #print("DIAG WIN DETECTED")
            return True 
    except: 
        pass

    try: 
        if (row >= 1 and col >= 2
            and b.coords[row-1][col+1] == player
            and b.coords[row+1][col-1] == player
            and b.coords[row+2][col-2] == player): 
            #print("DIAG WIN DETECTED")
            return True 
    except: 
        pass

    try: 
        if (row >= 2 and col >= 2
            and b.coords[row-1][col-1] == player
            and b.coords[row-2][col-2] == player
            and b.coords[row+1][col+1] == player): 
            #print("DIAG WIN DETECTED")
            return True 
    except: 
        pass

    try: 
        if (row >= 2 and col >= 1
            and b.coords[row-1][col+1] == player
            and b.coords[row-2][col+2] == player
            and b.coords[row+1][col-1] == player): 
            #print("DIAG WIN DETECTED")
            return True 
    except: 
        pass

    try: 
        if (row >= 3 and col >= 3
            and b.coords[row-1][col-1] == player
            and b.coords[row-2][col-2] == player
            and b.coords[row-3][col-3] == player): 
            #print("DIAG WIN DETECTED")
            return True 
    except: 
        pass

    try: 
        if (row >= 3
            and b.coords[row-1][col+1] == player
            and b.coords[row-2][col+2] == player
            and b.coords[row-3][col+3] == player): 
            #print("DIAG WIN DETECTED")
            return True 
    except: 
        pass
    


    return False

        
# returns the next state 
def next_state(s: state, move: int) -> state: 
    match s.status: 
        case "Draw": 
            return s 
        case "Win": 
            return s
        case "Ongoing": 
            result = update_board(s.board, s.player, move)
            updated_board = result[0]
            move_coords = result[1]
            if (check_vert_win(updated_board, s.player, move_coords) or 
                  check_horz_win(updated_board, s.player, move_coords) or 
                  check_diag_win(updated_board, s.player, move_coords)): 
                return state("Win", s.player, updated_board)
            elif legal_moves(state("Ongoing", s.player, updated_board)) == []: 
                return state("Draw", s.player, updated_board)
            else: 
                return state("Ongoing", switch_player(s.player), updated_board)

# estimate value 
def estimate_value(state: state) -> float: 
    match (state.status, state.player): 
        case ("Win", "P1"): 
            return 10000. 
        case ("Win", "P2"): 
            return -10000. 
        case ("Draw", _): 
            return 0 
        case ("Ongoing", _): 
            return (estimate_vert(state.board)
                    + estimate_horz(state.board)
                    + estimate_diag(state.board))
            
