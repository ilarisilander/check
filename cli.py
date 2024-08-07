import click

from rich.console import Console
from src.task import Create, Read, Update, Delete
from src.setup_data import Files
from src.settings_handler import Todo
from src.constants import APP_VERSION, TODO_PATH
from src.file_handler import JsonFile
from src.view import Display
from src.validate import Deadline

console = Console()


@click.group()
@click.version_option(version=APP_VERSION, prog_name='check')
def check():
    files = Files()
    files.ensure_appdata_dir()
    files.ensure_deleted_dir()
    files.ensure_settings_file()
    if not files.ensure_todo_file():
        if click.confirm(f'There is no todo lists in {TODO_PATH}. Do you want to create a list?', default=True):
            while True:
                list_name = click.prompt('Enter list name', type=str)
                if Todo.is_valid_list_name(list_name):
                    JsonFile.create_todo_file(TODO_PATH, list_name)
                    Todo.create_todo_list(list_name)
                    Todo.change_active_todo_list(list_name)
                    break
                else:
                    click.echo('Invalid file name. Example valid name: games_todo.')
        else:
            raise click.UsageError('You need to create a list to use the functions of Check')

@click.group()
def todo():
    """ Handle todo lists """
    pass

# Check commands
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
    if not deadline == 'None':
        if not Deadline.is_corret_format(deadline):
            raise click.UsageError('Correct format for deadline is: YYYY-MM-DD. Example: 2024-08-02')
        if not Deadline.is_newer_than_old_date(deadline):
            raise click.UsageError('Deadline date cannot be older than today unless you are a time traveller')
    create = Create(title, description, priority, size, deadline)
    try:
        create.new_task()
        click.echo(f'Task added to the todo list')
    except Exception as e:
        click.echo(e)

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

def filter_options(**kwargs) -> dict:
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

@click.command(help='Search for a task')
@click.option('-t', '--title', default=None, help='Title of the task')
@click.option('-ds', '--description', default=None, help='Description of the task')
@click.option('-p', '--priority', default=None, help='Task priority: low, medium, high, critical')
@click.option('-s', '--size', default=None, help='Task size: small, medium, large')
@click.option('-dl', '--deadline', default=None, help='Deadline of the task')
@click.option('-d', '--is-done', default=None, help='Is task done? "yes" or "no"')
def search(title, description, priority, size, deadline, is_done):
    filtered_options = filter_options(
        title=title,
        description=description,
        priority=priority,
        size=size,
        deadline=deadline,
        is_done=is_done)
    read = Read()
    read.search_task(**filtered_options)

# Todo commands
@click.command()
@click.option('-n', '--name', required=True, help='Name of the todo list that you want to use. Eg. todo_application')
def use(name: str):
    """ Todo list to use """
    if not Todo.is_valid_list_name(name):
        raise click.UsageError(f'{name} is not a valid name. Please use this format: file_name')
    if not Todo.list_exists(name):
        if click.confirm(f'There is no todo list named {name}. Do you want to create it?', default=True):
            Todo.create_todo_list(name)
            Todo.change_active_todo_list(name)
    if not Todo.is_active_list(name):
        Todo.change_active_todo_list(name)

@click.command()
@click.option('-n', '--name', required=True, help='Name of the new todo list. Eg. friday_chores')
@click.option('-u', '--use', is_flag=True, help='Use the new todo list that is created')
def new(name: str, use: bool):
    """ Create a new todo list """
    if not Todo.is_valid_list_name(name):
        raise click.UsageError(f'{name} is not a valid name. Please use this format: file_name')
    if not Todo.list_exists(name):
        JsonFile.create_todo_file(TODO_PATH, name)
        Todo.create_todo_list(name)
    if use:
        Todo.change_active_todo_list(name)

@click.command()
@click.option('-n', '--name', required=True, help='Name of the list to remove')
def remove(name: str):
    """ Remove an inactive list """
    if not Todo.list_exists(name):
        raise click.UsageError(f'There is no list named {name}')
    if Todo.get_active_todo_list() == name:
        raise click.UsageError(f'Cannot remove {name} when it is active')
    if click.confirm(f'Are you sure that you want to remove the todo list named "{name}" permanently?' , default=False):
        Todo.remove_todo_list(name)
        Todo.remove_todo_file(name)
        click.echo(f'Todo list named "{name}" has been removed, or rather moved to the data/lists/deleted directory')

@click.command()
def show():
    """ Display todo lists """
    display = Display()
    display.todo_lists()

# Sub-commands for 'check'
check.add_command(add)
check.add_command(start)
check.add_command(list)
check.add_command(search)
check.add_command(change)
check.add_command(move)
check.add_command(delete)
check.add_command(done)
check.add_command(todo)

# Sub-commands for 'todo'
todo.add_command(new)
todo.add_command(use)
todo.add_command(show)
todo.add_command(remove)


if __name__ == '__main__':
    try:
        check()
    except click.UsageError as e:
        click.echo(e)
    except click.ClickException as e:
        click.echo(e)
    except Exception as e:
        click.echo(e)