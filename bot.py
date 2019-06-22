import praw
import configparser

r_o = False

config = configparser.ConfigParser()
config.read('config.ini')

client_id = config.get('default', 'client_id')
client_secret=config.get('default', 'client_secret')
user_agent = config.get('default', 'user_agent')
# print(f'{client_id, client_secret, user_agent}')
username = config.get('default', 'username')
password = config.get('default', 'password')


'''

You need an instance of the Reddit class to do anything with PRAW. 
There are two distinct states a Reddit instance can be in: read-only, and authorized.

'''

# Read-only Reddit Instances

'''
To create a read-only Reddit instance, you need three pieces of information:

1. client ID
2. client secret
3. user agent

'''

if r_o:
    reddit = praw.Reddit(client_id=client_id,
                         client_secret=client_secret,
                         user_agent=user_agent)

    print(reddit.read_only)  # Output: True
    # output 10 'hot' submissions
    for submission in reddit.subreddit('learnpython').hot(limit=10):
        print(submission.title)

# Authorized Reddit Instances
'''
In order to create an authorized Reddit instance, two additional pieces of information are required for script 
applications (see Authenticating via OAuth for other application types):

1. your Reddit user name
2. your Reddit password

'''


reddit = praw.Reddit(client_id=client_id,
                     client_secret=client_secret,
                     user_agent=user_agent,
                     username=username,
                     password=password)

print(reddit.read_only)  # Output: False

# obtain a subreddit

subreddit = reddit.subreddit('romania')
print("Name\n" + subreddit.display_name)
print("Title:\n" + subreddit.title)
print("Description:\n" + subreddit.description)

# Obtain a submission instance from a subreddit
count = 1
for submission in subreddit.hot(limit=10):
    print(f'Submission no: {count}:\n', f'Title:{submission.title}', f'Score: {submission.score}',
          f'Id: {submission.id}', f'{submission.url}', sep='\n')
    count += 1

