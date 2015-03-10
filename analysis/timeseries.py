from datetime import datetime
from collections import Counter

class TimeSerializer(object):

    def __init__(self, posts):
        self.posts = posts

    def hourly(self):
        counter = Counter()
        for post in self.posts:
            hour = post.created.hour
            counter[str(hour)] += 1
        return dict(counter)

    def daily(self):
        counter = Counter()
        for post in self.posts:
            day = post.created.strftime('%A')
            counter[day] += 1
        return dict(counter)
