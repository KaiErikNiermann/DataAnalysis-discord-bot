import re
import datetime 
from datetime import date

class dateParser: 
    def __init__(self, dateString):
        self.dateString = dateString

    def isValidDate(self):
        """
        matches date by the formats
        1. yyyy-mm-dd | mm-dd-yyyy | dd-mm-yyyy
        2. yyyy/mm/dd | mm/dd/yyyy | dd/mm/yyyy
        3. yyyy.mm.dd | mm.dd.yyyy | dd.mm.yyyy
        """
        date_pattern = re.compile("(\d{4}|\d{2})([-./])(\d{2})\2(\d{2}|\d{4})")
        return (date_pattern).match(self.dateString)

    def parse(self):
        if self.isValidDate():
            # split string by non-digit characters
            date_components = re.split(r"\D+", self.dateString)

            year = date_components[0] if len(date_components[0]) == 4 else date_components[2]
            month = date_components[1]
            day = date_components[0] if len(date_components[0]) == 2 else date_components[2]
            return datetime.datetime(year, month, day)
        return None
