import itertools
from datetime import datetime, timedelta
from collections import Counter

class TimeSerializer(object):
    """ Provides methods for computing time series data"""

    def __init__(self):
        """
        Args:
            posts (list): list of post sqlalchemy post objects
        """
        

    def today(self):
        return datetime.now()


    def get_days_ago(self, days):
        return datetime.now() - timedelta(days=days)

    def get_weeks_ago(self, weeks):
        return datetime.now()- timedelta(weeks=weeks)

    def hourly_activity(self, data):
        data = sorted(data, key=lambda x: x.created)
        groupings =  itertools.groupby(data, key=lambda x: x.created.hour)
        data =  [{'date': str(self.today() - timedelta(hours=hour)), 'count': len(list(group))}
            for hour, group in groupings]
        # active_hours = set()
        # for record in data:
        #     for date, count in record.iteritems():
        #         print date
        #         active_hours.add(datetime.strptime(date, '%a, %d'))
        # for hour in range(0, 23):
        #     if hour not in active_hours:
        #         data.append({'date': str(self.today - timedelta(hours=hour)),
        #                     'count': 0})
        return data


