import click

from rich.console import Console
from src.task import Create, Read, Update, Delete
from src.setup_data import Files

console = Console()


@click.group()
def check():
    files = Files()
    files.ensure_appdata_dir()
    files.ensure_settings_file()
    files.ensure_todo_file()

@click.command(help='List tasks')
@click.option('--all', 'flags', flag_value='all', multiple=True, is_flag=True, default=[], help='List all tasks from all levels')
@click.option('--todo', 'flags', flag_value='todo', multiple=True, is_flag=True, default=[], help='List all tasks from "todo"')
@click.option('--in-progress', 'flags', flag_value='in_progress', multiple=True, is_flag=True, default=[], help='List all tasks from "in progress"')
@click.option('--done', 'flags', flag_value='done', multiple=True, is_flag=True, default=[], help='List all tasks from "done"')
def list(flags: tuple):
    if len(flags) > 1 or len(flags) == 0:
        raise click.UsageError('Options --all, --todo, --in-progress, and --done are mutually exclusive. Choose one.')
    else:
        flag = flags[0]
        read = Read()
        read.tasks(flag)

@click.command(help='Delete a task')
@click.option('--id', required=True)
def delete(id: str):
    delete = Delete()
    try:
        delete.task(id)
    except Exception as e:
        click.echo(e)

@click.command(help='Add a new task to the todo list')
@click.option('--title', required=True, help='Title of the task')
@click.option('--description', required=True, help='Description of the task')
@click.option('--priority', default='medium', help='Task priority: low, medium, high, critical')
@click.option('--size', default='medium', help='Task size: small, medium, large')
@click.option('--deadline', default='None', help='Deadline of the task')
def add(title: str, description: str, priority: str, size: str, deadline: str):
    create = Create(title, description, priority, size, deadline)
    try:
        create.new_task()
    except Exception as e:
        click.echo(e)
    click.echo(f'Task added to the todo list')

@click.command(help='Start a task, moving the task to in-progress')
@click.option('--id', required=True, help='The ID of the task that will be moved to in progress')
def start(id: str):
    Update.start_task(id)

@click.command(help='Move a task to done')
@click.option('--id', required=True, help='The ID of the task that will be moved to done')
def done(id: str):
    Update.end_task(id)


check.add_command(start)
check.add_command(add)
check.add_command(delete)
check.add_command(done)
check.add_command(list)


if __name__ == '__main__':
    try:
        check()
    except click.UsageError as e:
        click.echo(e)