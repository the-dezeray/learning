from collections import Counter

BOARD_EMPTY = 0
BOARD_PLAYER_X = 1
BOARD_PLAYER_O = -1

DISPLAY_PLAYER = 'X'
DISPLAY_COMPUTER = 'O'
DISPLAY_EMPTY = ' '
def get_turn(s):
    counter = Counter(s)
    x_places = counter[1]
    o_places = counter[-1]

    if x_places + o_places == 9:
        return None
    elif x_places > o_places:
        return BOARD_PLAYER_O 
    else:
        return BOARD_PLAYER_X

def actions(s):
    play = get_turn(s)
    actions_list = [(play, i) for i in range(len(s)) if s[i] == BOARD_EMPTY]
    return actions_list

def result(s, a):
    (play, index) = a
    s_copy = s.copy()
    s_copy[index] = play
    return s_copy

def terminal(s):
    for i in range(3):
        if s[3 * i] == s[3 * i + 1] == s[3 * i + 2] != BOARD_EMPTY:
            return s[3 * i]
        if s[i] == s[i + 3] == s[i + 6] != BOARD_EMPTY:
            return s[i]

    if s[0] == s[4] == s[8] != BOARD_EMPTY:
        return s[0]
    if s[2] == s[4] == s[6] != BOARD_EMPTY:
        return s[2]

    if get_turn(s) is None:
        return 0
    
    return None

def utility(s, cost):
    term = terminal(s)
    if term is not None:
        return (term, cost)
    
    action_list = actions(s)
    utils = []
    for action in action_list:
        new_s = result(s, action)
        utils.append(utility(new_s, cost + 1))

    score = utils[0][0]
    idx_cost = utils[0][1]
    play = get_turn(s)
    if play == BOARD_PLAYER_X:
        for i in range(len(utils)):
           if utils[i][0] > score:
                score = utils[i][0]
                idx_cost = utils[i][1]
    else:
        for i in range(len(utils)):
           if utils[i][0] < score:
                score = utils[i][0]
                idx_cost = utils[i][1]
    return (score, idx_cost) 

def minimax(s):
    action_list = actions(s)
    utils = []
    for action in action_list:
        new_s = result(s, action)
        utils.append((action, utility(new_s, 1)))

    if len(utils) == 0:
        return ((0,0), (0, 0))

    sorted_list = sorted(utils, key=lambda l : l[0][1])
    action = min(sorted_list, key = lambda l : l[1])
    return action


def print_board(s):
    def convert(num):
        if num == BOARD_PLAYER_X:
            return 'X'
        if num == BOARD_PLAYER_O:
            return 'O'
        return '_'

    i = 0
    for _ in range(3):
        for _ in range(3):
            print(convert(s[i]), end=' ')
            i += 1
        print()

from rich.live import Live
from pynput.keyboard  import Listener
from rich.console import Console
from rich.table import Table
from rich.traceback import install
from rich.panel import Panel

def get_index(x, y):
    return 3 * y + x
class KeyboardController:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.core = None

    def execute_on_key(self, key):
        input_string :str= str(key)
        input_string = input_string.replace("'","")

        match input_string:
            case "Key.up":
                self.y -= 1
                self.y = max(0, self.y)  # Ensure self.y is not less than 0
            case "Key.down":
                self.y += 1
                self.y = min(2, self.y)  # Ensure self.y is not greater than 2
            case "Key.left":
                self.x -= 1
                self.x = max(0, self.x)  # Ensure self.x is not less than 0
            case "Key.right":
                self.x += 1
                self.x = min(2, self.x)  # Ensure self.x is not greater than 2
            case "Key.enter":
                core.play(x = self.x, y = self.y)
            case "Key.esc":
                print("Exiting")
                exit()
        core.update()       
    def play(self):
            pass        
        # print(input_string)

def box(item) -> Panel:
    
    style = ""
    if item.value == BOARD_PLAYER_X:
        item.value = DISPLAY_PLAYER
    elif item.value == BOARD_PLAYER_O:
        item.value = DISPLAY_COMPUTER  
    elif item.value == BOARD_EMPTY:
        item.value = DISPLAY_EMPTY   

    if item.selected:
        style = "bold green"
    string = str(item.value)
    return Panel(string, border_style=style)


class square:
    def __init__(self,value:int = 0):
        self.selected = False
        self.value = value

keyboard_controller = KeyboardController()

class Core:
    def __init__(self, keyboard_controller: KeyboardController = None):
        self.keyboard_controller = keyboard_controller
        self.keyboard_controller.core= self
        self.live = None
        self.a = [ BOARD_EMPTY for _ in range(9)]
    def play(self,x,y):
        turn = get_turn(self.a)
        if turn == BOARD_PLAYER_X:
            index = get_index(x,y)


        
            if self.a[index] is not BOARD_EMPTY:
                return None
            else:
                self.a[index] = BOARD_PLAYER_X
                self.update()
                action = minimax(self.a)
                self.a = result(self.a, action[0])
                self.update()
            if terminal(self.a) is not None:
                        exit()


    def build_table(self) -> Table:
        table = Table.grid(expand=True)
        table.add_column()
        table.add_column()
        table.add_column()


        bap = [square(value = i) for i in self.a]
        x = self.keyboard_controller.x
        y = self.keyboard_controller.y
        bap[3 * y+ x].selected = True

        for i in range(0,len(bap),3):
            t = bap[i:i+3]
            table.add_row(box(t[0]),box(t[1]),box(t[2]))
        return table 
    def update(self):
         core.live.update(self.build_table())  

try:
    core = Core(keyboard_controller = keyboard_controller)
    with Listener(on_press= keyboard_controller.execute_on_key) as key_listener:
            with Live(core.build_table(),screen=True, refresh_per_second=10) as core.live:
                while True:
                    pass
            key_listener.join()
except KeyboardInterrupt:
    print("Exiting")
    exit()