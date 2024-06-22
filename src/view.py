""" Module for displaying things in the CLI application """

from constants import TODO_PATH, SETTINGS_PATH, CURRENT_DATE
from rich.table import Table
from rich.text import Text
from rich.console import Console
from file_handler import JsonFile

class Display:
    def __init__(self) -> None:
        self.console = Console()
        self.settings_dict = JsonFile.read(SETTINGS_PATH)


    def tasks(self, category: str):
        todo_dict = JsonFile.read(TODO_PATH)
        task_dict = JsonFile.get_all_tasks(todo_dict)

        table = Table(title=category.upper(), show_lines=True)
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
                self.priority_with_color(str(info['priority'])),
                str(info['size']),
                self.deadline_with_color(str(info['deadline'])),
                str(info['create_date']),
                str(info['done_date']),
                self.is_done_with_color(str(info['is_done']))
            )

        self.console.print(table)

    def priority_with_color(self, priority: str):
        color = self.settings_dict['priority']['colors'][priority]
        return Text(priority, style=color)

    def is_done_with_color(self, is_done: str):
        color = self.settings_dict['is_done']['colors'][is_done]
        return Text(is_done, style=color)

    def deadline_with_color(self, deadline: str):
        color = self.settings_dict['deadline']['colors'][deadline]
        return Text(deadline, style=color)
