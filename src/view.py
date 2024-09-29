""" Module for displaying things in the CLI application """

from pathlib import Path
from rich.table import Table
from rich.text import Text
from rich.console import Console
from src.file_handler import JsonFile
from src.settings_handler import Todo
from src.constants import TODO_PATH, SETTINGS_PATH, CURRENT_DATE

class Display:
    def __init__(self) -> None:
        self.console = Console()
        self.settings_dict = JsonFile.read(SETTINGS_PATH)

    def todo_lists(self):
        lists_dict = self.settings_dict['lists']
        self.console.print(lists_dict['active'], ' <- active', style='bold green')
        for each in lists_dict['inactive']:
            self.console.print(each)

    def tasks(self, category: str):
        active_list = Todo.get_active_todo_list()
        active_list_path = Path(TODO_PATH) / (active_list + '.json')
        todo_dict = JsonFile.read(active_list_path)
        task_dict = JsonFile.get_all_tasks(todo_dict)

        table = Table(title=category.upper(), show_lines=True, style='steel_blue3')
        table.add_column("ID", style="white", justify="center", width=5)
        table.add_column("Title", style="white", justify="center", width=25)
        table.add_column("Description", style="white", justify="center", width=30)
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
                self.add_color(str(info['priority']), 'priority'),
                self.add_color(str(info['size']), 'size'),
                self.add_color(str(info['deadline']), 'deadline'),
                str(info['create_date']),
                str(info['done_date']),
                self.add_color(str(info['is_done']), 'is_done')
            )

        self.console.print(table)

    def filtered_tasks(self, todos: dict):
        # TODO: Repetitive code, this should be refactored
        table = Table(title='SEARCH_RESULT', show_lines=True, style='steel_blue3')
        table.add_column("ID", style="white", justify="center", width=5)
        table.add_column("Title", style="white", justify="center", width=25)
        table.add_column("Description", style="white", justify="center", width=30)
        table.add_column("Priority", style="white", justify="center")
        table.add_column("Size", style="white", justify="center")
        table.add_column("Deadline", style="white", justify="center")
        table.add_column("Create Date", style="white", justify="center")
        table.add_column("Done Date", style="white", justify="center")
        table.add_column("Done", style="white", justify="center")

        for task, info in todos.items():
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
        if not category == 'deadline':
            color = self.settings_dict[category]['colors'][text_value]
        else:
            # TODO: Make some better coloring of deadlines
            color = 'white'
        return Text(text_value, style=color)
