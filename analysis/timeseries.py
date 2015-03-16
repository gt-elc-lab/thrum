from datetime import datetime
from collections import Counter

class TimeSerializer(object):
    """ Provides methods for computing time series data"""

    def __init__(self, posts):
        """
        Args:
            posts (list): list of post sqlalchemy post objects
        """
        self.posts = posts

    def hourly(self):
        """ Sums the number of post for every hour"""
        counter = Counter()
        for post in self.posts:
            hour = post.created.hour
            counter[str(hour)] += 1
        return dict(counter)

    def daily(self):
        """ Computes the number of post for every day"""
        counter = Counter()
        for post in self.posts:
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