from fake_useragent import UserAgent
import requests
import uuid
import calendar
import datetime
import json

ua = UserAgent()


def completionID():
  """Generates an ID with the format 'chatcmpl-random_part'

  Returns:
      str: The generated ID.
  """
  prefix = "chatcmpl-" 
  random_part = uuid.uuid4().hex[:29] 
  return f"{prefix}{random_part}"

 
def generate(messages):
    """ Supports GPT-3.5-turbo
    
    """

    headers = {
        'authority': 'litebot.mmahmad.com',
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9',
        'content-type': 'application/json',
        'origin': 'https://litebot.mmahmad.com',
        'referer': 'https://litebot.mmahmad.com/',
        'sec-ch-ua-mobile': '?0',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': ua.random
    }



    json_data = {
        'messages': messages,
    }

    response = requests.post('https://litebot.mmahmad.com/api/chat', headers=headers, json=json_data)

    json_build = {
        "id": completionID(),
        "object": "chat.completion",
        "created": calendar.timegm(datetime.datetime.utcnow().utctimetuple()),
        "choices" : [
            {
                "message": {
                    "role": "assistant",
                    "content": response.text
                },
                "finish_reason": "stop",
                "index": 0
            }
        ],
        "elpased": response.elapsed.total_seconds(),
        "src": 9
    }
    
    return json.dumps(json_build)
