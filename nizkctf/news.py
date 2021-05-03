# -*- encoding: utf-8 -*-

from __future__ import unicode_literals, division, print_function,\
     absolute_import
import time
from .repo import contents
from .serializable import SerializableList

NEWS_FILE = 'news.json'


class News(SerializableList):
    pretty_print = True

    def __init__(self):
        super(News, self).__init__()

    def path(self):
        return contents.get_path(NEWS_FILE)


    def add(self, msg_text):
        current_time = int(time.time())
        message = {"msg": msg_text, "time": current_time}

        self.append(message)
        self.save()
