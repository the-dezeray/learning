from rich.live import Live
from pynput.keyboard  import Listener
from rich.console import Console
from rich.table import Table
from rich.traceback import install
from rich.panel import Panel


class KeyboardController:
    def __init__(self):
        pass    
    def execute_on_key(self, key):
        input_string :str= str(key)
        input_string = input_string.replace("'","")

        match input_string:
             case "Key.up":
                  pass
             case "Key.down":
                  pass
             case "Key.left":
                  pass
             case "Key.right":
                  pass
             case "Key.enter":
                  pass
             case "Key.esc":
                 print("Exiting")
                 exit()
            
        # print(input_string)

def box(item) -> Panel:
    string = str(item)
    return Panel(string, border_style="bold red")
table = Table.grid()
table.add_column()
table.add_column()
table.add_column()
a = [ 0 for _ in range(9)]

for i in range(0,len(a),3):
    t = a[i:i+3]
    table.add_row(box(a[0]),box(a[1]),box(a[2]))
keyboard_controller = KeyboardController()




with Listener(on_press= keyboard_controller.execute_on_key) as key_listener:
        with Live(table, refresh_per_second=10) as Live:
            while True:
                pass
        key_listener.join()