import click

from rich.console import Console
from task import Create, Read, Delete

console = Console()


@click.group()
def task():
    pass

@click.command()
@click.option('--all', 'flags', flag_value='all', multiple=True, is_flag=True, default=[], help='List all tasks from all levels')
@click.option('--todo', 'flags', flag_value='todo', multiple=True, is_flag=True, default=[], help='List all tasks from "todo"')
@click.option('--in-progress', 'flags', flag_value='in_progress', multiple=True, is_flag=True, default=[], help='List all tasks from "in progress"')
@click.option('--done', 'flags', flag_value='done', multiple=True, is_flag=True, default=[], help='List all tasks from "done"')
def list(flags):
    if len(flags) > 1 or len(flags) == 0:
        raise click.UsageError('Options --all, --todo, --in-progress, and --done are mutually exclusive. Choose one.')
    else:
        flag = flags[0]
        read = Read()
        read.tasks(flag)
        

@click.command()
@click.option('--id', required=True)
def done(id: str):
    pass

@click.command()
@click.option('--id', required=True)
def delete(id: str):
    delete = Delete()
    try:
        delete.task(id)
    except Exception as e:
        click.echo(e)

@click.command()
@click.option('--title', required=True, help='Title of the task')
@click.option('--description', required=True, help='Description of the task')
@click.option('--priority', help='Task priority: low, medium, high, critical')
@click.option('--size', help='Task size: small, medium, large')
@click.option('--deadline', help='Deadline of the task')
def add(title: str, description: str, priority: str, size: str, deadline: str):
    create = Create(
        title,
        description,
        priority='medium',
        size='medium',
        deadline=None
    )
    try:
        create.new_task()
    except Exception as e:
        click.echo(e)
    click.echo(f'Task added to the todo list')


task.add_command(add)
task.add_command(delete)
task.add_command(done)
task.add_command(list)


if __name__ == '__main__':
    try:
        task()
    except click.UsageError as e:
        click.echo(e)