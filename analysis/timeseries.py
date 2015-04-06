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
        self.now = datetime.now()

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


    def weekly_buckets(self, data, school, vanilla=False):
        data = sorted(data, key=lambda x: x.created)
        buckets = itertools.groupby(data, key=lambda x: int(x.created.strftime('%U')))
        if vanilla:
            return buckets 
        output = []
        for bucket, items in buckets:
            # datetime objects don't have a week field so we have to find the
            # week of the post with respect to the current time. 
            # strftime('%U') gives you the current week in the year as a string
            offset = int(self.now.strftime('%U')) - bucket
            date = self.now - timedelta(weeks=offset)
            count = len(list(items))
            output.append({'date': str(date), 'count': count, 'college':school, })
        return output