""" Test module """
from task import Create


if __name__ == '__main__':
    create = Create('title', 'description', 'high', 'small', None)
    create.new_task()