import praw
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

