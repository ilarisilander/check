import click

from rich.console import Console
from task import Create, Delete


console = Console()

@click.group()
def task():
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
def new(title: str, description: str, priority: str, size: str, deadline: str):
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

task.add_command(delete)
task.add_command(new)

if __name__ == '__main__':
    task()