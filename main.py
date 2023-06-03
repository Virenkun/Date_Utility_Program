from datetime import datetime, timedelta
import pytz

class DateUtility:
    def __init__(self, holiday_file):
        self.holiday_file = holiday_file

    def convert_dt(self, from_date, from_date_TZ, to_date_TZ):
        """
        Converts a datetime object from one timezone to another timezone.
        :param from_date: The datetime object to convert
        :type from_date: datetime
        :param from_date_TZ: The timezone of the from_date
        :type from_date_TZ: str
        :param to_date_TZ: The timezone to convert to
        :type to_date_TZ: str
        :return: The converted datetime object
        :rtype: datetime
        """
        from_tz = pytz.timezone(from_date_TZ)
        to_tz = pytz.timezone(to_date_TZ)
        localized_date = from_tz.localize(from_date)
        converted_date = localized_date.astimezone(to_tz)
        return converted_date

    def add_dt(self, from_date, number_of_days):
        """
        Adds a number of days to a given date.
        :param from_date: The starting date
        :type from_date: datetime
        :param number_of_days: The number of days to add
        :type number_of_days: int
        :return: The resulting datetime object
        :rtype: datetime
        """
        return from_date + timedelta(days=number_of_days)

    def sub_dt(self, from_date, number_of_days):
        """
        Subtracts a number of days from a given date.
        :param from_date: The starting date
        :type from_date: datetime
        :param number_of_days: The number of days to subtract
        :type number_of_days: int
        :return: The resulting datetime object
        :rtype: datetime
        """
        return from_date - timedelta(days=number_of_days)

    def get_days(self, from_date, to_date):
        """
        Calculates the number of days between two dates.
        :param from_date: The starting date
        :type from_date: datetime
        :param to_date: The ending date
        :type to_date: datetime
        :return: The number of days between the two dates
        :rtype: int
        """
        return (to_date - from_date).days

    def get_days_exclude_we(self, from_date, to_date):
        """
        Calculates the number of days between two dates, excluding weekends (Saturday and Sunday).
        :param from_date: The starting date
        :type from_date: datetime
        :param to_date: The ending date
        :type to_date: datetime
        :return: The number of days between the two dates excluding weekends
        :rtype: int
        """
        days = (to_date - from_date).days + 1
        weekends = sum((from_date + timedelta(days=i)).weekday() >= 5 for i in range(days))
        return days - weekends

    def get_days_since_epoch(self, from_date):
        """
        Calculates the number of days since the epoch (January 1, 1970) to a given date.
        :param from_date: The date to calculate the number of days since the epoch
        :type from_date: datetime
        :return: The number of days since the epoch
        :rtype: int
        """
        epoch = datetime.utcfromtimestamp(0)
        return (from_date - epoch).days

    def get_business_days(self, from_date, to_date):
        """
        Calculates the number of business days between two dates, excluding weekends and holidays.
        :param from_date: The starting date
        :type from_date: datetime
        :param to_date: The ending date
        :type to_date: datetime
        :return: The number of business days between the two dates excluding weekends and holidays
        :rtype: int
        """
        days = (to_date - from_date).days + 1
        weekends = sum((from_date + timedelta(days=i)).weekday() >= 5 for i in range(days))
        holidays = self.load_holidays()
        business_days = days - weekends
        for holiday in holidays:
            if from_date <= holiday <= to_date and holiday.weekday() < 5:
                business_days -= 1
        return business_days

    def load_holidays(self):
        """
        Loads holidays from the holiday_file.
        :return: A list of holiday datetime objects
        :rtype: list
        """
        holidays = []
        with open(self.holiday_file, 'r') as file:
            for line in file:
                tz, date, holiday = line.strip().split(',')
                holiday_date = datetime.strptime(date, '%Y%m%d').date()
                holidays.append(holiday_date)
        return holidays


utility = DateUtility('holidays.dat')

from_date = datetime(2023, 1, 1)
to_date = datetime(2023, 1, 31)

converted_date = utility.convert_dt(from_date, 'UTC', 'US/Eastern')
added_date = utility.add_dt(from_date, 5)
subtracted_date = utility.sub_dt(from_date, 10)
days_between = utility.get_days(from_date, to_date)
days_exclude_weekends = utility.get_days_exclude_we(from_date, to_date)
days_since_epoch = utility.get_days_since_epoch(from_date)
business_days = utility.get_business_days(from_date, to_date)

print(converted_date)
print(added_date)
print(subtracted_date)
print(days_between)
print(days_exclude_weekends)
print(days_since_epoch)
print(business_days)