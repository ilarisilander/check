import click

from rich.console import Console
from src.task import Create, Read, Update, Delete
from src.setup_data import Files

console = Console()

__version__ = '0.1.2'


@click.group()
@click.version_option(version=__version__, prog_name='check')
def check():
    files = Files()
    files.ensure_appdata_dir()
    files.ensure_settings_file()
    files.ensure_todo_file()

@click.command(help='List tasks')
@click.option('-a', '--all', 'flags', flag_value='all', multiple=True, is_flag=True, default=[], help='List all tasks from all levels')
@click.option('-t', '--todo', 'flags', flag_value='todo', multiple=True, is_flag=True, default=[], help='List all tasks from "todo"')
@click.option('-ac', '--active', 'flags', flag_value='active', multiple=True, is_flag=True, default=[], help='List all tasks from "active"')
@click.option('-d', '--done', 'flags', flag_value='done', multiple=True, is_flag=True, default=[], help='List all tasks from "done"')
def list(flags: tuple):
    if len(flags) > 1 or len(flags) == 0:
        raise click.UsageError('Options --all, --todo, --active, and --done are mutually exclusive. Choose one.')
    else:
        flag = flags[0]
        read = Read()
        read.tasks(flag)

@click.command(help='Delete a task')
@click.option('-i', '--id', required=True)
def delete(id: str):
    delete = Delete()
    try:
        delete.task(id)
    except Exception as e:
        click.echo(e)

@click.command(help='Add a new task to the todo list')
@click.option('-t', '--title', required=True, help='Title of the task')
@click.option('-ds', '--description', required=True, help='Description of the task')
@click.option('-p', '--priority', default='medium', help='Task priority: low, medium, high, critical')
@click.option('-s', '--size', default='medium', help='Task size: small, medium, large')
@click.option('-dl', '--deadline', default='None', help='Deadline of the task')
def add(title: str, description: str, priority: str, size: str, deadline: str):
    create = Create(title, description, priority, size, deadline)
    try:
        create.new_task()
    except Exception as e:
        click.echo(e)
    click.echo(f'Task added to the todo list')

@click.command(help='Start a task, moving the task to active')
@click.option('-i', '--id', required=True, help='The ID of the task that will be moved to active')
def start(id: str):
    Update.start_task(id)

@click.command(help='Move a task to done')
@click.option('-i', '--id', required=True, help='The ID of the task that will be moved to done')
def done(id: str):
    Update.end_task(id)

@click.command(help='Change the contents of a task')
@click.option('-i', '--id', required=True, help='The ID of the task')
@click.option('-t', '--title', default=None, help='Title of the task')
@click.option('-ds', '--description', default=None, help='Description of the task')
@click.option('-p', '--priority', default=None, help='Task priority: low, medium, high, critical')
@click.option('-s', '--size', default=None, help='Task size: small, medium, large')
@click.option('-dl', '--deadline', default=None, help='Deadline of the task')
def change(id: str, title: str, description: str, priority: str, size: str, deadline: str):
    filtered_options = filter_options(
        title=title,
        description=description,
        priority=priority,
        size=size,
        deadline=deadline)
    Update.change_task(id, **filtered_options)

def filter_options(**kwargs):
    filtered_kwargs = {}
    for key, value in kwargs.items():
        if not value is None:
            filtered_kwargs[key] = value
    return filtered_kwargs

@click.command(help='Move task to another phase (todo, active). Moving to done can only be done with the "done" command')
@click.option('-i', '--id', required=True, help='The ID of the task')
@click.option('-d', '--destination', required=True, help='The destination where the task will be moved to')
def move(id, destination):
    if is_valid_option(destination):
        Update.move_task(id, destination)
    else:
        raise click.UsageError('Option --destination can only take "todo", "active" or "done"')

def is_valid_option(option):
    valid_options = ['todo', 'active']
    if option in valid_options:
        return True
    return False


check.add_command(add)
check.add_command(start)
check.add_command(list)
check.add_command(change)
check.add_command(move)
check.add_command(delete)
check.add_command(done)


if __name__ == '__main__':
    try:
        check()
    except click.UsageError as e:
        click.echo(e)