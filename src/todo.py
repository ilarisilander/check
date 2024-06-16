import click
from rich.console import Console


console = Console()

@click.group()
def task():
    pass

@click.command()
@click.option('--id', prompt=True)
def done(id: int):
    click.echo(f'Task {id} moved to done')

@click.command()
@click.option('--description', prompt=True)
def new(description: str):
    click.echo(f'Task added to the todo list: {description}')

task.add_command(done)
task.add_command(new)

if __name__ == '__main__':
    task()