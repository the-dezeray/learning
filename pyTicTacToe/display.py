from rich.live import Live
from pynput.keyboard  import Listener
from rich.console import Console
from rich.table import Table
from rich.traceback import install
from rich.panel import Panel
BOARD_EMPTY = 0
BOARD_PLAYER_X = 1
BOARD_PLAYER_O = -1 
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
    string = str(item.value)
    style = ""
    if item.selected:
        style = "bold green"
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
        self.a = [ None for _ in range(9)]
    def play(self,x,y):
        index = get_index(x,y)
        if self.a[index] is not None:
            return None
        else:
            self.a[index] = BOARD_PLAYER_X
            self.update()

    def build_table(self) -> Table:
        table = Table.grid()
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
core = Core(keyboard_controller = keyboard_controller)
with Listener(on_press= keyboard_controller.execute_on_key) as key_listener:
        with Live(core.build_table(), refresh_per_second=10) as core.live:
            while True:
                pass
        key_listener.join()