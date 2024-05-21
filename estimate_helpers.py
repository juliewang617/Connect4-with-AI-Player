from flask import Flask, render_template, session, redirect, url_for
from flask_session import Session
from tempfile import mkdtemp
import numpy as np 
from dataclasses import dataclass 

@dataclass
class square: 
    player: str 
    location: tuple[int, int]

@dataclass 
class board: 
    height: int 
    width: int 
    coords: list[list[square]]

# estimate vertically 
def estimate_vert(b: board) -> float: 

    sum = 0 

    for col in range(b.width): 

        i = 0

        while (i < b.height): 

            try: # check for 4 in a column (WIN)
                if (b.coords[i][col] == 
                    b.coords[i+1][col] ==
                    b.coords[i+2][col] ==
                    b.coords[i+3][col] and 
                    (b.coords[i][col])): 
                    if b.coords[i][col] == "P1": 
                        sum += 10000. 
                    else: 
                        sum += -10000. 
            except: 
                pass 

            try: # check for 3 in a column 
                if (not b.coords[i][col] and 
                    b.coords[i+1][col] ==
                    b.coords[i+2][col] ==
                    b.coords[i+3][col] and 
                    b.coords[i+1][col]): 

                    if b.coords[i+1][col] == "P1": 
                        sum += 10. 
                    else: 
                        sum += -10. 
            except: 
                pass 
         
            try: # check for 2 in a column
                if (not b.coords[i][col] and 
                    not b.coords[i+1][col] and
                    b.coords[i+2][col] ==
                    b.coords[i+3][col] and 
                    b.coords[i+2][col]): 
                    if b.coords[i+2][col] == "P1": 
                        sum += 5.
                    else: 
                        sum += -5.
            except: 
                pass 

            try: # check for 1 in a column
                if (not b.coords[i][col] and 
                    not b.coords[i+1][col] and
                    not b.coords[i+2][col] and
                    b.coords[i+3][col]): 
                    if b.coords[i+3][col] == "P1": 
                        sum += 1.
                    else: 
                        sum += -1.
            except: 
                pass 

            i = i + 1
    
    #print("VERT EST: " + str(sum))
        
    return sum  

# estimate horizontally
def estimate_horz(b: board) -> float: 
    # 4 in a row = max/min value 
    # any order of 3 in a block of 4 = 5.0 
    # any order of 2 in a block of 4 = 2.5 
    # 1 piece with nothing next to it = 1.0 

    sum = 0. 

    for row in range(b.height): 

        i = 0

        while (i < b.width): 

            try: # 4 in a row
                if (b.coords[row][i] == 
                    b.coords[row][i + 1] ==
                    b.coords[row][i + 2] ==
                    b.coords[row][i + 3] and 
                    b.coords[row][i]): 
                    if b.coords[row][i] == "P1": 
                        sum += 10000. 
                    else: 
                        sum += -10000. 
            except: 
                pass 

            try: # 3 in a row 
                if (b.coords[row][i] == 
                    b.coords[row][i + 1] ==
                    b.coords[row][i + 2] and
                    not b.coords[row][i + 3] and 
                    b.coords[row][i]): 
                    if b.coords[row][i] == "P1": 
                        sum += 10. 
                    else: 
                        sum += -10. 
            except: 
                pass

            try: # 3 in a row 
                if (b.coords[row][i] == 
                    b.coords[row][i + 1] ==
                    b.coords[row][i + 3] and
                    not b.coords[row][i + 2] and 
                    b.coords[row][i]): 
                    if b.coords[row][i] == "P1": 
                        sum += 10. 
                    else: 
                        sum += -10. 
            except: 
                pass

            try: # 3 in a row 
                if (b.coords[row][i] == 
                    b.coords[row][i + 2] ==
                    b.coords[row][i + 3] and
                    not b.coords[row][i + 1] and 
                    b.coords[row][i]): 
                    if b.coords[row][i] == "P1": 
                        sum += 10. 
                    else: 
                        sum += -10. 
            except: 
                pass

            try: # 3 in a row 
                if (b.coords[row][i + 1] == 
                    b.coords[row][i + 2] ==
                    b.coords[row][i + 3] and
                    not b.coords[row][i] and 
                    b.coords[row][i + 1]): 
                    if b.coords[row][i+1] == "P1": 
                        sum += 10. 
                    else: 
                        sum += -10. 
            except: 
                pass

            try: # 2 in a row 
                if (b.coords[row][i] == 
                    b.coords[row][i + 1] and
                    not b.coords[row][i + 2] and
                    not b.coords[row][i + 3] and 
                    b.coords[row][i]): 
                    if b.coords[row][i] == "P1": 
                        sum += 5. 
                    else: 
                        sum += -5.
            except: 
                pass

            try: # 2 in a row 
                if (b.coords[row][i] == 
                    b.coords[row][i + 2] and
                    not b.coords[row][i + 1] and
                    not b.coords[row][i + 3] and 
                    b.coords[row][i]): 
                    if b.coords[row][i] == "P1": 
                        sum += 5. 
                    else: 
                        sum += -5. 
            except: 
                pass

            try: # 2 in a row 
                if (b.coords[row][i] == 
                    b.coords[row][i + 3] and
                    not b.coords[row][i + 1] and
                    not b.coords[row][i + 2] and 
                    b.coords[row][i]): 
                    if b.coords[row][i] == "P1": 
                        sum += 5.
                    else: 
                        sum += -5. 
            except: 
                pass

            try: # 2 in a row 
                if (b.coords[row][i + 1] == 
                    b.coords[row][i + 2] and
                    not b.coords[row][i] and
                    not b.coords[row][i + 3] and 
                    b.coords[row][i+1]): 
                    if b.coords[row][i+1] == "P1": 
                        sum += 5. 
                    else: 
                        sum += -5. 
            except: 
                pass

            try: # 2 in a row 
                if (b.coords[row][i + 1] == 
                    b.coords[row][i + 3] and
                    not b.coords[row][i] and
                    not b.coords[row][i + 2] and 
                    b.coords[row][i+1]): 
                    if b.coords[row][i+1] == "P1": 
                        sum += 5. 
                    else: 
                        sum += -5. 
            except: 
                pass

            try: # 2 in a row 
                if (b.coords[row][i + 2] == 
                    b.coords[row][i + 3] and
                    not b.coords[row][i] and
                    not b.coords[row][i + 1] and 
                    b.coords[row][i+2]): 
                    if b.coords[row][i+2] == "P1": 
                        sum += 5. 
                    else: 
                        sum += -5. 
            except: 
                pass

            try: # 1 in a row 
                if (b.coords[row][i] and 
                    not b.coords[row][i + 1] and
                    not b.coords[row][i + 2] and
                    not b.coords[row][i + 3]): 
                    if b.coords[row][i] == "P1": 
                        sum += 1. 
                    else: 
                        sum += -1.
            except: 
                pass

            try: # 1 in a row 
                if (b.coords[row][i + 1] and 
                    not b.coords[row][i] and
                    not b.coords[row][i + 2] and
                    not b.coords[row][i + 3]): 
                    if b.coords[row][i + 1] == "P1": 
                        sum += 1. 
                    else: 
                        sum += -1.
            except: 
                pass

            try: # 1 in a row 
                if (b.coords[row][i + 2] and 
                    not b.coords[row][i] and
                    not b.coords[row][i + 1] and
                    not b.coords[row][i + 3]): 
                    if b.coords[row][i + 2] == "P1": 
                        sum += 1. 
                    else: 
                        sum += -1.
            except: 
                pass

            try: # 1 in a row 
                if (b.coords[row][i + 3] and 
                    not b.coords[row][i] and
                    not b.coords[row][i + 1] and
                    not b.coords[row][i + 2]): 
                    if b.coords[row][i + 3] == "P1": 
                        sum += 1. 
                    else: 
                        sum += -1.
            except: 
                pass

            i = i + 1 

    #print("HORZ EST: " + str(sum))

    return sum 

# estimate diagonally -- BROKENNN

def estimate_diag(b: board) -> float: 
        # 4 diagonally = max/min value 
    # any order of 3 in a block of 4 = 5.0 
    # any order of 2 in a block of 4 = 2.5 
    # 1 piece in a block of 4 = 1.0 

    sum = 0 

    for row in range(b.height): 

        i = 0 

        while (i < b.width): 

            try: # 4 diag
                if (b.coords[row][i] == 
                    b.coords[row + 1][i + 1] ==
                    b.coords[row + 2][i + 2] ==
                    b.coords[row + 3][i + 3] and 
                    (b.coords[row][i])): 
                    if b.coords[row][i] == "P1": 
                        sum += 10000. 
                    else: 
                        sum += -10000. 
            except: 
                pass 

            try: # 4 antidiag
                if (b.coords[row][i] == 
                    b.coords[row - 1][i + 1] ==
                    b.coords[row - 2][i + 2] ==
                    b.coords[row - 3][i + 3] and 
                    b.coords[row][i]): 
                    if b.coords[row][i] == "P1": 
                        sum += 10000. 
                    else: 
                        sum += -10000. 
            except: 
                pass

            try: # 3 diag
                if (b.coords[row][i] == 
                    b.coords[row + 1][i + 1] ==
                    b.coords[row + 2][i + 2] and
                    not b.coords[row + 3][i + 3] and 
                    b.coords[row][i]): 
                    if b.coords[row][i] == "P1": 
                        sum += 10. 
                    else: 
                        sum += -10. 
            except: 
                pass 

            try: # 3 diag
                if (b.coords[row][i] == 
                    b.coords[row + 1][i + 1] ==
                    b.coords[row + 3][i + 3] and
                    not b.coords[row + 2][i + 2] and 
                    b.coords[row][i]): 
                    if b.coords[row][i] == "P1": 
                        sum += 10. 
                    else: 
                        sum += -10. 
            except: 
                pass 

            try: # 3 diag
                if (b.coords[row][i] == 
                    b.coords[row + 2][i + 2] ==
                    b.coords[row + 3][i + 3] and
                    not b.coords[row + 1][i + 1] and 
                    b.coords[row][i]): 
                    if b.coords[row][i] == "P1": 
                        sum += 10. 
                    else: 
                        sum += -10. 
            except: 
                pass

            try: # 3 diag
                if (b.coords[row + 1][i + 1] == 
                    b.coords[row + 2][i + 2] ==
                    b.coords[row + 3][i + 3] and
                    not b.coords[row][i] and 
                    b.coords[row + 1][i + 1]): 
                    if b.coords[row + 1][i + 1] == "P1": 
                        sum += 10. 
                    else: 
                        sum += -10. 
            except: 
                pass

            ###

            try: # 3 anti-diag
                if (b.coords[row][i] == 
                    b.coords[row + 1][i - 1] ==
                    b.coords[row + 2][i - 2] and
                    not b.coords[row + 3][i - 3] and 
                    b.coords[row][i]): 
                    if b.coords[row][i] == "P1": 
                        sum += 10. 
                    else: 
                        sum += -10. 
            except: 
                pass 

            try: # 3 anti-diag
                if (b.coords[row][i] == 
                    b.coords[row + 1][i - 1] ==
                    b.coords[row + 3][i - 3] and
                    not b.coords[row + 2][i - 2] and 
                    b.coords[row][i]): 
                    if b.coords[row][i] == "P1": 
                        sum += 10. 
                    else: 
                        sum += -10. 
            except: 
                pass 

            try: # 3 anti-diag
                if (b.coords[row][i] == 
                    b.coords[row + 2][i - 2] ==
                    b.coords[row + 3][i - 3] and
                    not b.coords[row + 1][i - 1] and 
                    b.coords[row][i]): 
                    if b.coords[row][i] == "P1": 
                        sum += 10. 
                    else: 
                        sum += -10. 
            except: 
                pass

            try: # 3 anti-diag
                if (b.coords[row + 1][i - 1] == 
                    b.coords[row + 2][i - 2] ==
                    b.coords[row + 3][i - 3] and
                    not b.coords[row][i] and 
                    b.coords[row + 1][i - 1]): 
                    if b.coords[row + 1][i - 1] == "P1": 
                        sum += 10. 
                    else: 
                        sum += -10. 
            except: 
                pass

            ###

            try: # 2 diag
                if (b.coords[row][i] == 
                    b.coords[row + 1][i + 1] and
                    not b.coords[row + 2][i + 2] and
                    not b.coords[row + 3][i + 3] and 
                    b.coords[row][i]): 
                    if b.coords[row][i] == "P1": 
                        sum += 5. 
                    else: 
                        sum += -5. 
            except: 
                pass

            try: # 2 diag
                if (b.coords[row][i] == 
                    b.coords[row + 2][i + 2] and
                    not b.coords[row + 1][i + 1] and
                    not b.coords[row + 3][i + 3] and 
                    b.coords[row][i]): 
                    if b.coords[row][i] == "P1": 
                        sum += 5. 
                    else: 
                        sum += -5. 
            except: 
                pass

            try: # 2 diag
                if (b.coords[row][i] == 
                    b.coords[row + 3][i + 3] and
                    not b.coords[row + 1][i + 1] and
                    not b.coords[row + 2][i + 2] and 
                    b.coords[row][i]): 
                    if b.coords[row][i] == "P1": 
                        sum += 5. 
                    else: 
                        sum += -5. 
            except: 
                pass

            try: # 2 diag
                if (b.coords[row + 1][i + 1] == 
                    b.coords[row + 2][i + 2] and
                    not b.coords[row][i] and
                    not b.coords[row + 3][i + 3] and 
                    b.coords[row + 1][i + 1]): 
                    if b.coords[row + 1][i + 1] == "P1": 
                        sum += 5. 
                    else: 
                        sum += -5. 
            except: 
                pass

            try: # 2 diag
                if (b.coords[row + 2][i + 2] == 
                    b.coords[row + 3][i + 3] and
                    not b.coords[row][i] and
                    not b.coords[row + 1][i + 1] and 
                    b.coords[row + 2][i + 2]): 
                    if b.coords[row + 2][i + 2] == "P1": 
                        sum += 5. 
                    else: 
                        sum += -5. 
            except: 
                pass

            try: # 2 diag
                if (b.coords[row + 1][i + 1] == 
                    b.coords[row + 3][i + 3] and
                    not b.coords[row][i] and
                    not b.coords[row + 2][i + 2] and 
                    b.coords[row + 1][i + 1]): 
                    if b.coords[row + 1][i + 1] == "P1": 
                        sum += 5. 
                    else: 
                        sum += -5. 
            except: 
                pass

            ### 

            try: # 2 anti-diag
                if (b.coords[row][i] == 
                    b.coords[row + 1][i - 1] and
                    not b.coords[row + 2][i - 2] and
                    not b.coords[row + 3][i - 3] and 
                    b.coords[row][i]): 
                    if b.coords[row][i] == "P1": 
                        sum += 5. 
                    else: 
                        sum += -5. 
            except: 
                pass

            try: # 2 anti-diag
                if (b.coords[row][i] == 
                    b.coords[row + 2][i - 2] and
                    not b.coords[row + 1][i - 1] and
                    not b.coords[row + 3][i - 3] and 
                    b.coords[row][i]): 
                    if b.coords[row][i] == "P1": 
                        sum += 5. 
                    else: 
                        sum += -5. 
            except: 
                pass

            try: # 2 anti-diag
                if (b.coords[row][i] == 
                    b.coords[row + 3][i - 3] and
                    not b.coords[row + 1][i - 1] and
                    not b.coords[row + 2][i - 2] and 
                    b.coords[row][i]): 
                    if b.coords[row][i] == "P1": 
                        sum += 5. 
                    else: 
                        sum += -5. 
            except: 
                pass

            try: # 2 anti-diag
                if (b.coords[row + 1][i - 1] == 
                    b.coords[row + 2][i - 2] and
                    not b.coords[row][i] and
                    not b.coords[row + 3][i - 3] and 
                    b.coords[row + 1][i - 1]): 
                    if b.coords[row + 1][i - 1] == "P1": 
                        sum += 5. 
                    else: 
                        sum += -5. 
            except: 
                pass

            try: # 2 anti-diag
                if (b.coords[row + 2][i - 2] == 
                    b.coords[row + 3][i - 3] and
                    not b.coords[row][i] and
                    not b.coords[row + 1][i - 1] and 
                    b.coords[row + 2][i - 2]): 
                    if b.coords[row + 2][i - 2] == "P1": 
                        sum += 5. 
                    else: 
                        sum += -5. 
            except: 
                pass

            try: # 2 anti-diag
                if (b.coords[row + 1][i - 1] == 
                    b.coords[row + 3][i - 3] and
                    not b.coords[row][i] and
                    not b.coords[row + 2][i - 2] and 
                    b.coords[row + 1][i - 1]): 
                    if b.coords[row + 1][i - 1] == "P1": 
                        sum += 5. 
                    else: 
                        sum += -5. 
            except: 
                pass

            ###

            try: # 1 diag
                if (b.coords[row][i] and 
                    not b.coords[row + 1][i + 1] and
                    not b.coords[row + 2][i + 2] and
                    not b.coords[row + 3][i + 3]): 
                    if b.coords[row][i] == "P1": 
                        sum += 1. 
                    else: 
                        sum += -1. 
            except: 
                pass

            try: # 1 diag
                if (b.coords[row + 1][i + 1] and 
                    not b.coords[row][i] and
                    not b.coords[row + 2][i + 2] and
                    not b.coords[row + 3][i + 3]): 
                    if b.coords[row + 1][i + 1] == "P1": 
                        sum += 1. 
                    else: 
                        sum += -1. 
            except: 
                pass

            try: # 1 diag
                if (b.coords[row + 2][i + 2] and 
                    not b.coords[row][i] and
                    not b.coords[row + 1][i + 1] and
                    not b.coords[row + 3][i + 3]): 
                    if b.coords[row + 2][i + 2] == "P1": 
                        sum += 1. 
                    else: 
                        sum += -1. 
            except: 
                pass

            try: # 1 diag
                if (b.coords[row + 3][i + 3] and 
                    not b.coords[row][i] and
                    not b.coords[row + 1][i + 1] and
                    not b.coords[row + 2][i + 2]): 
                    if b.coords[row + 3][i + 3] == "P1": 
                        sum += 1. 
                    else: 
                        sum += -1. 
            except: 
                pass

            ###

            try: # 1 anti-diag
                if (b.coords[row][i] and 
                    not b.coords[row + 1][i - 1] and
                    not b.coords[row + 2][i - 2] and
                    not b.coords[row + 3][i - 3]): 
                    if b.coords[row][i] == "P1": 
                        sum += 1. 
                    else: 
                        sum += -1. 
            except: 
                pass

            try: # 1 anti-diag
                if (b.coords[row + 1][i - 1] and 
                    not b.coords[row][i] and
                    not b.coords[row + 2][i - 2] and
                    not b.coords[row + 3][i - 3]): 
                    if b.coords[row + 1][i - 1] == "P1": 
                        sum += 1. 
                    else: 
                        sum += -1. 
            except: 
                pass

            try: # 1 anti-diag
                if (b.coords[row + 2][i - 2] and 
                    not b.coords[row][i] and
                    not b.coords[row + 1][i - 1] and
                    not b.coords[row + 3][i - 3]): 
                    if b.coords[row + 2][i - 2] == "P1": 
                        sum += 1. 
                    else: 
                        sum += -1. 
            except: 
                pass

            try: # 1 anti-diag
                if (b.coords[row + 3][i - 3] and 
                    not b.coords[row][i] and
                    not b.coords[row + 1][i - 1] and
                    not b.coords[row + 2][i - 2]): 
                    if b.coords[row + 3][i - 3] == "P1": 
                        sum += 1. 
                    else: 
                        sum += -1. 
            except: 
                pass




            i = i + 1

    #print("DIAG EST: " + str(sum))

    return sum 