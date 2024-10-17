""" The entry point for the Check CLI application

__author__ = "Ilari Silander"

Using Click for the CLI arguments and commands.
Using Rich for the console output (the visuals).
"""
import click

from rich.console import Console
from src.task import Create, Read, Update, Delete
from src.setup_data import Files
from src.configuration import Jira
from src.settings_handler import Todo
from src.constants import APP_VERSION, TODO_PATH
from src.file_handler import JsonFile
from src.view import Display
from src.validate import Priority, Size
from src.todo import List
# Import simple_vira if it exists
try:
    from simple_vira import Api
except ImportError:
    pass

console = Console()


@click.group()
@click.version_option(version=APP_VERSION, prog_name='check')
def check():
    files = Files()
    files.ensure_appdata_dir()
    files.ensure_deleted_dir()
    files.ensure_settings_file()
    files.ensure_jira_config_file()
    if not files.ensure_todo_file():
        if click.confirm(f'There is no todo lists in {TODO_PATH}. Do you want to create a list?', default=True):
            while True:
                list_name = click.prompt('Enter list name', type=str)
                if Todo.is_valid_list_name(list_name):
                    JsonFile.create_todo_file(TODO_PATH, list_name)
                    Todo.create_todo_list(list_name)
                    Todo.change_active_todo_list(list_name)
                    break
                click.echo('Invalid file name. Example valid name: games_todo.')
        else:
            raise click.UsageError('You need to create a list to use the functions of Check')

@click.group()
def todo():
    """ Handle todo lists

    It's needed to add other commands to this group to make it work.
    """
    pass

@click.group()
def jira():
    """ Handle special commands related to Jira

    It's needed to add other commands to this group to make it work.
    """
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
@click.option('-j', '--jira', is_flag=True, help='Send information to Jira')
@click.option('-oj', '--only-jira', is_flag=True, help='Send only information to Jira')
def add(title: str, description: str, priority: str, size: str, jira: bool, only_jira: bool):
    issue = None
    if jira and only_jira:
        raise click.UsageError('Options --jira and --only-jira are mutually exclusive. Choose one.')
    if not Priority.is_valid_option(priority):
        raise click.UsageError('Priority can only be low, medium, high or critical')
    if not Size.is_valid_option(size):
        raise click.UsageError('Size can only be small, medium or large')

    if jira or only_jira:
        try:
            config = Jira()
            base_url = config.get_base_url()
            api_token = config.get_api_token()
            user_token = config.get_user_token()
            project = config.get_project()
            work_group = config.get_leading_work_group()
            issue_type = config.get_issue_type_story()
        except Exception as config_error:
            click.echo(config_error)

        try:
            api = Api(base_url, api_token, user_token)
            issue = api.create_issue(title, description, project, issue_type, work_group)
            click.echo(f'Issue added to Jira with ID: {issue}')
            if issue == None:  # If issue was not created in Jira, then the task will not be created locally
                raise click.UsageError('Issue could not be created in Jira. Task will not be added to the todo list')
        except Exception as e:
            click.echo(e)

    if not only_jira:
        create = Create(title, description, priority, size, issue)
        try:
            create.new_task()
            click.echo('Task added to the todo list')
        except Exception as e:
            click.echo(e)

@click.command(help='Start a task, moving the task to active')
@click.option('-i', '--id', required=True, help='The ID of the task that will be moved to active')
def start(id: str):
    # JIRA SECTION
    issue = List.get_issue_from_task(id)
    if not issue is None:
        config = Jira()
        base_url = config.get_base_url()
        api_token = config.get_api_token()
        user_token = config.get_user_token()
        assignee = config.get_assignee()
        api = Api(base_url, api_token, user_token)
        assigned = api.assign_issue(issue, assignee['name'])
        if not assigned:
            raise click.UsageError('Could not assign the issue to the assignee')
        click.echo(f'Issue assigned to {assignee["name"]}')

        in_progress = config.get_transitions_in_progress()
        transitioned = api.transition_issue(issue, in_progress)
        if not transitioned:
            raise click.UsageError('Could not transition the issue to "In Progress"')
        click.echo('Issue transitioned to "In Progress"')
    elif issue is None:
        click.echo('No Jira issue found for this task')
    # CHECK SECTION
    update = Update()
    update.start_task(id)

@click.command(help='Move a task to done')
@click.option('-i', '--id', required=True, help='The ID of the task that will be moved to done')
@click.option('-c', '--comment', default='Done', help='Comment for the task')
def done(id: str, comment: str):
    issue = List.get_issue_from_task(id)
    if not issue == None:
        config = Jira()
        base_url = config.get_base_url()
        api_token = config.get_api_token()
        user_token = config.get_user_token()
        api = Api(base_url, api_token, user_token)

        done = config.get_transitions_done()
        moved_to_done = api.move_issue_to_done(issue, done, comment)
        if not moved_to_done:
            raise click.UsageError('Could not transition the Jira issue to "Done"')
        click.echo('Jira issue moved to done')
    elif issue == None:
        click.echo('No Jira issue found for this task')
    update = Update()
    update.end_task(id)

@click.command(help='Change the contents of a task')
@click.option('-i', '--id', required=True, help='The ID of the task')
@click.option('-t', '--title', default=None, help='Title of the task')
@click.option('-ds', '--description', default=None, help='Description of the task')
@click.option('-p', '--priority', default=None, help='Task priority: low, medium, high, critical')
@click.option('-s', '--size', default=None, help='Task size: small, medium, large')
def change(id: str, title: str, description: str, priority: str, size: str):
    update = Update()
    filtered_options = filter_options(
        title=title,
        description=description,
        priority=priority,
        size=size
    )
    if not filtered_options:
        raise click.UsageError('No options were given to change')
    if 'priority' in filtered_options and not Priority.is_valid_option(priority):
        raise click.UsageError('Priority can only be low, medium, high or critical')
    if 'size' in filtered_options and not Size.is_valid_option(size):
        raise click.UsageError('Size can only be small, medium or large')
    update.change_task(id, **filtered_options)

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
    update = Update()
    if is_valid_option(destination):
        update.move_task(id, destination)
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
@click.option('-d', '--is-done', default=None, help='Is task done? "yes" or "no"')
def search(title, description, priority, size, is_done):
    filtered_options = filter_options(
        title=title,
        description=description,
        priority=priority,
        size=size,
        is_done=is_done)
    read = Read()
    read.search_task(**filtered_options)

# Todo commands
@click.command()
@click.option('-n', '--name', required=True, help='Name of the todo list that you want to use. Eg. todo_application')
def use(name: str):
    """ Todo list to use """
    todo = Todo()
    if not todo.is_valid_list_name(name):
        raise click.UsageError(f'{name} is not a valid name. Please use this format: file_name')
    if not todo.list_exists(name):
        if click.confirm(f'There is no todo list named {name}. Do you want to create it?', default=True):
            todo.create_todo_list(name)
            todo.change_active_todo_list(name)
    if not todo.is_active_list(name):
        todo.change_active_todo_list(name)

@click.command()
@click.option('-n', '--name', required=True, help='Name of the new todo list. Eg. friday_chores')
@click.option('-u', '--use', is_flag=True, help='Use the new todo list that is created')
def new(name: str, use: bool):
    """ Create a new todo list """
    todo = Todo()
    if not todo.is_valid_list_name(name):
        raise click.UsageError(f'{name} is not a valid name. Please use this format: file_name')
    if not todo.list_exists(name):
        JsonFile.create_todo_file(TODO_PATH, name)
        todo.create_todo_list(name)
    if use:
        todo.change_active_todo_list(name)

@click.command()
@click.option('-n', '--name', required=True, help='Name of the list to remove')
def remove(name: str):
    """ Remove an inactive list """
    todo = Todo()
    if not todo.list_exists(name):
        raise click.UsageError(f'There is no list named {name}')
    if todo.get_active_todo_list() == name:
        raise click.UsageError(f'Cannot remove {name} when it is active')
    if click.confirm(f'Are you sure that you want to remove the todo list named "{name}" permanently?' , default=False):
        todo.remove_todo_list(name)
        todo.remove_todo_file(name)
        click.echo(f'Todo list named "{name}" has been removed, or rather moved to the data/lists/deleted directory')

@click.command()
def show():
    """ Display todo lists """
    display = Display()
    display.todo_lists()

# Jira commands
# @click.command()


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
