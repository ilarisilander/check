""" Module to handle validations """
import re
from datetime import datetime


class Deadline:

    def is_corret_format(date_string: str) -> bool:
        """ Check that the date has the correct format

        The correct format: 2024-08-02
        """
        pattern = r'^\d{4}-\d{2}-\d{2}$'
        return re.match(pattern, date_string) is not None

    def is_newer_than_old_date(deadline: str) -> bool:
        """ Check that the date is not older than the current date

        You should not be able to have a deadline which is older than
        the current date, since you cannot travel back in time
        """
        input_date = datetime.strptime(deadline, '%Y-%m-%d')
        current_date = datetime.now().date()
        if input_date.date() < current_date:
            return False
        return True
