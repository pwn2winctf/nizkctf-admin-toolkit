# -*- encoding: utf-8 -*-

from __future__ import unicode_literals, division, print_function,\
                       absolute_import
from ..news import News
from ..repo import contents


def submit(msg_text):
    for _ in contents.retry_push('Added news'):
        News().add(msg_text)

