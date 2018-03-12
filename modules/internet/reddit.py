import praw
from random import randint
import requests


CLIENT_ID = 'pZFgLRkTG_qLxQ'
CLIENT_SECRET = ''
PASSWORD = ''


def get_image(subreddit):
    if not has_loaded:
        load_secure()
    data = praw.Reddit(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        user_agent='Null Discord Bot',
        username='forlornsisu',
        password=PASSWORD
    ).subreddit(subreddit).hot(limit=100)
    url = None
    while not url:
        pos = randint(3, 99)
        count = 0
        for post in data:
            if count == pos:
                if not post.over_18 and post.post_hint == 'image':
                    url = post.url
                    break
            count += 1
    resp = requests.get(url, stream=True)
    resp.raise_for_status()
    return resp.raw


has_loaded = False


def load_secure():
    secure = open('reddit_secure.txt').read().split('\n')
    global CLIENT_SECRET
    global PASSWORD
    CLIENT_SECRET = secure[0]
    PASSWORD = secure[1]

