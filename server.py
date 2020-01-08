import time

import flask
import datetime
from flask import request

app = flask.Flask(__name__)
messages = [
    {'username': 'John', 'time': time.time(), 'text': 'Hello World'}
]
password_storage = {}

@app.route('/')
def hello():
    return 'Hello world'


@app.route('/status')
def status():
    return {
        'status': True,
        'datetime': time.time().strftime('%Y-%m-%d %H:%M:%S'),
        'message_count': len(messages),
        'users_count': len(password_storage)
    }


@app.route('/send', methods=['POST'])
def send_method():
    """
    JSON {"username": str,"text": str}
    username, text - not empty
    :return: {"ok": bool}
    """
    username = str(request.json['username'])
    password = str(request.json['password'])
    text = str(request.json['text'])

    if username not in password_storage:
        password_storage[username] = password


    # validate
    if not isinstance(username, str) or len(username) == 0:
        return {'ok': False}
    if not isinstance(text, str) or len(text) == 0:
        return {'ok': False}
    if password_storage[username] != password:
        return {'ok': False}

    messages.append({'username': username, 'time': time.time(), 'text': text})

    return {'ok': True}


@app.route('/messages')
def messages_method():
    """
    Param after - отметка времени, после которой будут сообщений
    :return: {"messages": [
    {"username": str,'time' : str, "text": str}]}
    ...
    """
    after = float(request.args['after'])
    filtered_messages = [message for message in messages if message['time'] > after]
    print(after)
    return {'messages': filtered_messages}

if __name__ == '__main__':
    app.run()
