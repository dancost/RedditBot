from urllib.parse import quote_plus

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


QUESTIONS = ["what is", "who is", "who are"]
REPLY_TEMPLATE = "[Let me google that for you](http://lmgtfy.com/?q={})"


def main():
    reddit = praw.Reddit(client_id=client_id,
                         client_secret=client_secret,
                         user_agent=user_agent,
                         username=username,
                         password=password)

    subreddit = reddit.subreddit("AskReddit")

    for submission in subreddit.stream.submissions():
        process_submission(submission)
        break


def process_submission(submission):
    # Ignore long titles
    if len(submission.title.split()) > 10:
        return

    normalized_title = submission.title.lower()
    for question_phrase in QUESTIONS:
        if question_phrase in normalized_title:
            url_title = quote_plus(submission.title)
            reply_text = REPLY_TEMPLATE.format(url_title)
            print(f"Replying to {submission.title}")
            submission.reply(reply_text)
            # Stop after first reply made


if __name__ == "__main__":
    main()
