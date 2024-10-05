# Check - Turning to-dos into ta-das!
A TODO application in the terminal. Instead of creating todo lists in Notepad or other boring editors, you can get to feel more like a hacker with "Check".

![Check](https://github.com/ilarisilander/check/blob/master/check.PNG)

# Table of contents
<!--ts-->
   * [Table of contents](#table-of-contents)
   * [Pre-requisites](#pre-requisites)
   * [Installation](#installation)
   * [User: How to](#user-how-to)
   * [Dev: How to](#dev-how-to)
<!--te-->

# Pre-requisites
* Python 3.8 or higher

Download Python [here](https://www.python.org/downloads/)

# Installation
Download the latest release [here](https://github.com/ilarisilander/check/releases)
Click on "assets" at the bottom of the release that you want.
Download the .whl file.

Install pipx
```bash
pip install pipx
```

Install Check
```bash
pipx install path/to/the/file.whl
pipx ensurepath
```

When the pipx installation is done, you run pipx ensurepath and then Check is ready to be used!

# User: How to
The best way to understand what can be done with Check
```bash
check --help
```

### Add a task to the todo list
```bash
check add --title "Add some functionality" --description "Description of the task"
```
This is what is required to create a task.
You can also add --priority, --size and --jira/--only-jira

### List everything
```bash
check list --all
```
This will list all tables (todo, active and done).
Instead of --all, you can use --todo or --active.

### Start a task
```bash
check start --id 5 (the number represents the ID of the task, which you can find by listing tasks)
```
This will move the task with ID 5 to "active".

### Move task to done
```bash
check done --id 5
```
This will move the task with ID 5 to "done".

# Dev: How to

Preparation
```bash
python -m venv my_venv
source my_venv/Scripts/activate
pip install -r requirements.txt
```

Creating the wheel (run the setup.py)
```bash
python setup.py sdist bdist_wheel
```

Install the wheel as pipx package
```bash
pipx install dist/<wheel package>
```