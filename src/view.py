""" Module for displaying things in the CLI application """

from constants import TODO_PATH, CURRENT_DATE
from rich.table import Table
from rich.console import Console
from file_handler import JsonFile

class Display:
    def __init__(self) -> None:
        self.console = Console()

    def tasks(self, category: str):
        todo_dict = JsonFile.read(TODO_PATH)
        task_dict = JsonFile.get_all_tasks(todo_dict)

        table = Table(title=category.upper())
        table.add_column("ID", style="white", justify="center")
        table.add_column("Title", style="white", justify="center")
        table.add_column("Description", style="white", justify="center")
        table.add_column("Priority", style="white", justify="center")
        table.add_column("Size", style="white", justify="center")
        table.add_column("Deadline", style="white", justify="center")
        table.add_column("Create Date", style="white", justify="center")
        table.add_column("Done Date", style="white", justify="center")
        table.add_column("Done", style="white", justify="center")

        for task, info in task_dict[category].items():
            table.add_row(
                task,
                info['title'],
                info['description'],
                str(info['priority']),
                str(info['size']),
                str(info['deadline']),
                str(info['create_date']),
                str(info['done_date']),
                str(info['is_done']),
            )

        self.console.print(table)