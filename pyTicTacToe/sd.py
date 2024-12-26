from rich.table import Table
from rich.console import Console
a = Table(show_lines=False)
a.add_column("Column 1",style='bold black')
a.add_column("Column 2")
a.add_column("Column 2")
a.add_row("Hello", "World", "!")

a.add_row("Hello", "World", "!")
a.add_row("Hello", "World", "!")



console = Console()
console.print(a)