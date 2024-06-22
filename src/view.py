""" Module for displaying things in the CLI application """

from src.constants import TODO_PATH, SETTINGS_PATH, CURRENT_DATE
from rich.table import Table
from rich.text import Text
from rich.console import Console
from src.file_handler import JsonFile

class Display:
    def __init__(self) -> None:
        self.console = Console()
        self.settings_dict = JsonFile.read(SETTINGS_PATH)


    def tasks(self, category: str):
        todo_dict = JsonFile.read(TODO_PATH)
        task_dict = JsonFile.get_all_tasks(todo_dict)

        table = Table(title=category.upper(), show_lines=True, style='steel_blue3')
        table.add_column("ID", style="white", justify="center", width=3)
        table.add_column("Title", style="white", justify="center", width=20)
        table.add_column("Description", style="white", justify="center", width=25)
        table.add_column("Priority", style="white", justify="center", width=8)
        table.add_column("Size", style="white", justify="center", width=6)
        table.add_column("Deadline", style="white", justify="center", width=10)
        table.add_column("Create Date", style="white", justify="center", width=10)
        table.add_column("Done Date", style="white", justify="center", width=10)
        table.add_column("Done", style="white", justify="center", width=4)

        for task, info in task_dict[category].items():
            table.add_row(
                task,
                info['title'],
                info['description'],
                self.add_color(str(info['priority']), 'priority'),
                self.add_color(str(info['size']), 'size'),
                self.add_color(str(info['deadline']), 'deadline'),
                str(info['create_date']),
                str(info['done_date']),
                self.add_color(str(info['is_done']), 'is_done')
            )

        self.console.print(table)

    def add_color(self, text_value: str, category: str):
        color = self.settings_dict[category]['colors'][text_value]
        return Text(text_value, style=color)
