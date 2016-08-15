import json
import requests


def push_notification(to,message):
    url = 'https://fcm.googleapis.com/fcm/send'
    headers = {'content-type': 'application/json','Authorization':'key=AIzaSyDsu3JuIZq5F7VGeQzHiKjw5jLBL2T5sjs'
    }
    payload = {
        'to': to,
        'data': {
            'body': message
        }}
    r = requests.post(url, data=json.dumps(payload), headers=headers)