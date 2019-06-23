from flask import Flask, request
import json
import requests
import os
from flask_sqlalchemy import SQLAlchemy
import praw

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
db = SQLAlchemy(app)

reddit = praw.Reddit(client_id=os.environ.get('client_id'),
                     client_secret=os.environ.get('client_secret'),
                     user_agent=os.environ.get('user_agent'))
# Facebook Page Access Token
PAT = os.environ.get('PAT')

quick_replies_list = [{
    "content_type":"text",
    "title":"Jokes",
    "payload":"Jokes",
}]

@app.route('/', methods=['GET'])
def handle_verification():
    if request.args.get("hub.verify_token") == os.environ.get("verify_token"):
        return request.args.get("hub.challenge")
    else:
        return "Error invalid token"


@app.route('/', methods=['POST'])
def handle_messages():
    print("Handling messages")
    payload = request.get_data()
    print(payload)

    for sender, message in messaging_events(payload):
        print(f'Incoming from {sender}: {message}')
        send_message(PAT, sender, message)
    return "OK"


def messaging_events(payload):
    """Generate tuples of (sender_id, message_text) from the provided payload.

    """
    data = json.loads(payload)

    for item in data:
        print(item)

    messaging_events = data["entry"][0]["messaging"]
    print(f'Messaging events: {messaging_events}')
    for event in messaging_events:
        if "message" in event and "text" in event["message"]:
            yield event["sender"]["id"], event["message"]["text"]
        else:
            print(f'EVENT!!!!!: {event}')
            yield event["sender"]["id"], "Can't echo this!"


def send_message(token, recipient, text):
    """Send the message text to recipient with id recipient.
    """
    url = "https://graph.facebook.com/v3.3/me/messages"
    subreddit_name = ''
    if "joke" in text.lower():
        subreddit_name = "Jokes"

    myUser = get_or_create(db.session, Users, name=recipient)


    if subreddit_name == "Jokes":
        for submission in reddit.subreddit(subreddit_name).hot(limit=None):
            if submission.is_self and submission.link_flair_text is None:
                query_result = Posts.query.filter(Posts.name == submission.id).first()
                if query_result is None:
                    myPost = Posts(submission.id, submission.title)
                    myUser.posts.append(myPost)
                    db.session.commit()
                    payload = submission.title
                    payload_text = submission.selftext
                    break
                elif myUser not in query_result.users:
                    myUser.posts.append(query_result)
                    db.session.commit()
                    payload = submission.title
                    payload_text = submission.selftext
                    break
                else:
                    continue
    r = requests.post(url=url,
                          params={"access_token": token},
                          data=json.dumps({
                              "recipient": {"id": recipient},
                              "message": {"text": payload}
                          }),
                          headers={'Content-type': 'application/json'})

    r = requests.post(url=url,
                          params={"access_token": token},
                          data=json.dumps({
                              "recipient": {"id": recipient},
                              "message": {"text": payload_text,
                                          "quick_replies": quick_replies_list}
                          }),
                          headers={'Content-type': 'application/json'})
    if r.status_code != requests.codes.ok:
        print(r.text)




def get_or_create(session, model, **kwargs):
    instance = session.query(model).filter_by(**kwargs).first()
    if instance:
        return instance
    else:
        instance = model(**kwargs)
        session.add(instance)
        session.commit()
        return instance


relationship_table = db.Table('relationship_table',
                              db.Column('user_id', db.Integer, db.ForeignKey('users.id'), nullable=False),
                              db.Column('post_id', db.Integer, db.ForeignKey('posts.id'), nullable=False),
                              db.PrimaryKeyConstraint('user_id', 'post_id'))

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    posts = db.relationship('Posts', secondary=relationship_table, backref='users')

    def __init__(self, name=None):
        self.name = name


class Posts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    url = db.Column(db.String, nullable=False)

    def __init__(self, name=None, url=None):
        self.name = name
        self.url = url

if __name__=='__main__':
    app.run()