from bangtal import *
from enum import Enum

setGameOption(GameOption.ROOM_TITLE, False)
setGameOption(GameOption.INVENTORY_BUTTON, False)
setGameOption(GameOption.MESSAGE_BOX_BUTTON, False)

Main = Scene('20153182', 'Images/background.png')

class State(Enum):
    BLANK = 0
    POSSIBLE = 1
    BLACK = 2
    WHITE = 3

class Turn(Enum):
    BLACK = 0
    WHITE = 1

stone = []
turn = Turn.BLACK

def setState(x, y, state):
    object = stone[y][x]
    object.state = state

    if state == State.BLANK:
        object.setImage("Images/blank.png")
    elif state == State.BLACK:
        object.setImage("Images/black.png")
    elif state == State.WHITE:
        object.setImage("Images/white.png")
    elif turn == Turn.BLACK:
        object.setImage("Images/black possible.png")
    else:
        object.setImage("Images/white possible.png")
        
def stone_onMouseAction(x, y):
    global turn

    object = stone[y][x]

    if object.state == State.POSSIBLE:
        if turn == Turn.BLACK:
            setState(x, y, State.BLACK)
            reverse_xy(x, y)
            turn = Turn.WHITE
            
        else:
            setState(x, y, State.WHITE)
            reverse_xy(x, y)
            turn = Turn.BLACK

    if not setPossible():
        if turn == Turn.BLACK:
            turn = Turn.WHITE
        else:
            turn = Turn.BLACK

        if not setPossible():
            showMessage("게임이 종료되었습니다.")


def setPossible_xy_dir(x, y, dx, dy):
    if turn == Turn.BLACK:
        mine = State.BLACK
        other = State.WHITE
    
    else:
        mine = State.WHITE
        other = State.BLACK

    possible = False

    while True:
        x = x + dx
        y = y + dy

        if x < 0 or x > 7: return False
        if y < 0 or y > 7: return False

        object = stone[y][x]
        if object.state == other:
            possible = True
        elif object.state == mine:
            return possible # False?
        else:
            return False

def setPossible_xy(x, y):
    object = stone[y][x]
    if object.state == State.BLACK: return False
    if object.state == State.WHITE: return False
    setState(x, y, State.BLANK)

    if (setPossible_xy_dir(x, y, 0, 1)): return True
    if (setPossible_xy_dir(x, y, 1, 1)): return True
    if (setPossible_xy_dir(x, y, 1, 0)): return True
    if (setPossible_xy_dir(x, y, 1, -1)): return True
    if (setPossible_xy_dir(x, y, 0, -1)): return True
    if (setPossible_xy_dir(x, y, -1, -1)): return True
    if (setPossible_xy_dir(x, y, -1, 0)): return True
    if (setPossible_xy_dir(x, y, -1, 1)): return True
    return False

def setPossible():
    possible = False

    for y in range(8):
        for x in range(8):
            if setPossible_xy(x, y):
                setState(x, y, State.POSSIBLE)
                possible = True

    return possible

def reverse_xy_dir(x, y, dx, dy):
    if turn == Turn.BLACK:
        mine = State.BLACK
        other = State.WHITE
    
    else:
        mine = State.WHITE
        other = State.BLACK

    possible = False

    while True:
        x = x + dx
        y = y + dy

        if x < 0 or x > 7: return
        if y < 0 or y > 7: return

        object = stone[y][x]
        if object.state == other:
            possible = True
        elif object.state == mine:
            if possible:
                while True:
                    x = x - dx
                    y = y - dy

                    object = stone[y][x]
                    if object.state == other:
                        setState(x, y, mine)
                    else:
                        return
        else:
            return


def reverse_xy(x, y):
    reverse_xy_dir(x, y, 0, 1)
    reverse_xy_dir(x, y, 1, 1)
    reverse_xy_dir(x, y, 1, 0)
    reverse_xy_dir(x, y, 1, -1)
    reverse_xy_dir(x, y, 0, -1)
    reverse_xy_dir(x, y, -1, -1)
    reverse_xy_dir(x, y, -1, 0)
    reverse_xy_dir(x, y, -1, 1)
    return False


for y in range(8):
    stone.append([])

    for x in range(8):
        object = Object('Images/blank.png')
        object.locate(Main, 40 + x*80, 40 + y*80)
        object.state = State.BLANK
        object.show()
        
        object.onMouseAction = lambda mx, my, action, ix = x, iy = y: stone_onMouseAction(ix, iy)

        stone[y].append(object)



setState(3, 3, State.BLACK)
setState(3, 4, State.WHITE)
setState(4, 3, State.WHITE)
setState(4, 4, State.BLACK)


startGame(Main)