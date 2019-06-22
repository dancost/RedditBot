import praw
from praw.models import MoreComments
import configparser


config = configparser.ConfigParser()
config.read('./utils/config.ini')

client_id = config.get('default', 'client_id')
client_secret=config.get('default', 'client_secret')
user_agent = config.get('default', 'user_agent')
# print(f'{client_id, client_secret, user_agent}')
username = config.get('default', 'username')
password = config.get('default', 'password')

# Create reddit object
reddit = praw.Reddit(client_id=client_id,
                     client_secret=client_secret,
                     user_agent=user_agent,
                     username=username,
                     password=password)

submission = reddit.submission(id='3g1jfi')

for top_level_comment in submission.comments:
    if isinstance(top_level_comment, MoreComments):
        continue
    print(top_level_comment.body)

submission.comments.replace_more(limit=None)

for top_level_comment in submission.comments:
    for second_level_comment in top_level_comment.replies:
        print(second_level_comment.body)

for comment in submission.comments.list():
    print(comment.body)