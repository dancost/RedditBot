from flask import Flask, request
import json
import requests
import os
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Facebook Page Access Token
PAT = os.environ.get('PAT')


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

    messaging_events = data["entry"][0]["messaging"]
    print(messaging_events)
    for event in messaging_events:
        if "message" in event and "text" in event["message"]:
            yield event["sender"]["id"], event["message"]["text"]
        else:
            continue
            # yield event["sender"]["id"], "Can't echo this!"


def send_message(token, recipient, text):
    """Send the message text to recipient with id recipient.
    """
    url = "https://graph.facebook.com/v2.6/me/messages"
    r = requests.post(url=url,
                     params={"access_token": token},
                     data=json.dumps({
                         "recipient": {"id": recipient},
                         "message": {"text": text}
                     }),
                     headers={'Content-type': 'application/json'})
    if r.status_code != 200:
        print(r.content)


if __name__=='__main__':
    app.run()


