from flask import Flask, render_template, session, redirect, url_for
from flask_session import Session
from tempfile import mkdtemp
import numpy as np 
from dataclasses import dataclass 
from connect4 import * 

# if state is terminal or depht = 0, return value 
# if player is max, check every legal move and check which one leads to max val
# if player is min
def minimax(state: state, player: str, depth: int, alpha: float, beta: float) -> float: 
    lm = legal_moves(state)

    if depth == 0 or (not lm): 
        return estimate_value(state) 
    
    # generate list of possible states from legal moves
    child_states = map(lambda move: next_state(state, move), legal_moves(state))

    match player: 
        case "P1": 
            max_eval = -100000
            for child_state in child_states: 
                eval = minimax(child_state, switch_player(player), depth - 1, alpha, beta)
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval) 
                if beta <= alpha: 
                    break 
            return max_eval
        case "P2": 
            min_eval = 100000
            for child_state in child_states: 
                eval = minimax(child_state, switch_player(player), depth - 1, alpha, beta)
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha: 
                    break 
            return min_eval 

# picks the next best move
def pick_move(state: state) -> int: 
    lm = legal_moves(state)

    if not lm: 
        raise KeyError("no possible moves")
    
    best_move = lm[0]
    best_val = minimax(
        next_state(state, best_move), 
        switch_player(state.player), 
        3, -100000, 100000
    )

    for curr_move in lm: 
        curr_val = minimax(
            next_state(state, curr_move), 
            switch_player(state.player), 
            3, -100000, 100000
        )

        match state.player: 
            case "P1": 
                if curr_val >= best_val: 
                    best_move = curr_move 
                    best_val = curr_val 
            case "P2": 
                if curr_val <= best_val: 
                    best_move = curr_move 
                    best_val = curr_val 

    print(state.player + " chooses the move " + str(best_move))
    
    return best_move 

    
            


    





