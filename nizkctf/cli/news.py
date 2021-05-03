from ..news import News
from ..repo import contents


def submit(msg_text):
    for _ in contents.retry_push('Added news'):
        News().add(msg_text)

