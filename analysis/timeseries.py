from datetime import datetime, timedelta
from collections import Counter

class TimeSerializer(object):
    """ Provides methods for computing time series data"""

    def __init__(self):
        """
        Args:
            posts (list): list of post sqlalchemy post objects
        """
        

    def hourly(self, posts):
        """ Sums the number of post for every hour"""
        counter = Counter()
        for hour in range(0, 24):
            counter[str(hour)] = 0

        for post in posts:
            hour = post.created.hour
            counter[str(hour)] += 1

        return [{'hour': hour, 'count':count} for hour, count in counter.iteritems()] 

    def daily(self, posts):
        """ Computes the number of post for every day"""
        counter = Counter()
        for post in posts:
            # this gets you the day of the week as a string
            day = post.created.strftime('%A')
            counter[day] += 1
        return dict(counter)

    def average_hourly(self, days):
        """ Computes the number of post per day every day"""
        counter = Counter()
        for post in self.posts:
            hour = post.created.hour
            counter[str(hour)] += 1
        
        for hour, posts in counter.iteritems():
            counter[hour] = posts / days
        return dict(counter)

    @staticmethod
    def today():
        return datetime.now()

    @staticmethod
    def get_days_ago(days):
        return datetime.now() - timedelta(days=days)

    @staticmethod
    def get_weeks_ago(weeks):
        return datetime.now()- timedelta(weeks=weeks)