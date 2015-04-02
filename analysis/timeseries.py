import itertools
from datetime import datetime, timedelta
from collections import Counter
from nltk.corpus import stopwords

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
        result = []
        data = sorted(data, key=lambda x: x.created)
        groupings =  itertools.groupby(data, key=lambda x: x.created.hour)
        for hour, group in groupings:
            record = {'date': str(self.today() - timedelta(hours=hour)), 'count': len(list(group))}
            result.append(record)
        return result


    def weekly_activity(self, data):
        data = sorted(data, key=lambda x: x.created)
        groupings =  itertools.groupby(data, key=lambda x: x.created.hour)
        data =  [{'date': str(self.today() - timedelta(week=week)), 'count': len(list(group))}
            for week, group in groupings]
        return data
