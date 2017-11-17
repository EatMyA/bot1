import pynder
import config
import time
import datetime
import requests
from messages import messages
from time import sleep
from random import randint

requests.packages.urllib3.disable_warnings()  # Find way around this...

session = pynder.Session(config.FACEBOOK_AUTH_TOKEN)


def log(msg):
    print '[' + str(datetime.datetime.now()) + ']' + ' ' + msg


def send(match, message_no):
    for m in messages[message_no]:
        session._api._post('/user/matches/' + match['id'],
                           {"message": m})
        sleep(randint(5, 15))
    log('Sent message ' + str(message_no) + ' to ' + match['person']['name'])


def check_swipes():
    swipes_remaining = session.likes_remaining
    if swipes_remaining  == 0:
        return 'Send messages'

def message(match):
    ms = match['messages']
    khaled = session.profile.id
    if not ms:
        send(match, 0)
        return
    said = False
    count = 0
    name = match['person']['name']
    for m in ms:
        if m['from'] == khaled:
            count += 1
            said = False
        elif ' ' in m['message'].lower():
            said = True
    if count >= len(messages):
        log('Finished conversation with ' + name)
        return
    if said:
        send(match, count)
    else:
        log('No new messages from ' + name)


def like_or_nope():
    if randint(1, 100) == 31:
        return 'nope'
    else:
        return 'like'

def handle_likes():
    while True:
        try:
            users = session.nearby_users()
            for u in users:
                status = check_swipes()
                if status == 'Send messages':
                    log('Out of swipes.')
                    return
                action = like_or_nope()
                if action == 'like':
                    u.like()
                    log('Liked ' + u.name)
                    sleep(randint(1, 10))
                else:
                        u.dislike()
                        log('Disliked ' + u.name)
                        sleep(randint(1, 5))
        except ValueError:
            continue
        except pynder.errors.RequestError:
            continue



def handle_matches():
    log(str(len(session._api.matches(''))) + ' matches')
    matches = session._api.matches('')
    for m in matches:
        message(m)


while True:
    handle_likes()
    handle_matches()
    log('Pausing for ten minutes...')
    time.sleep(600)
