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

 
def generate(model: str, messages, temperature = 0.6, frequency_penalty = 0, presence_penalty = 0, top_p = 1, stream = False):
    """ Supports GPT-3.5-turbo, GPT-3.5-turbo-1106,  GPT-3.5-turbo-16k, GPT-4, GPT-4-1106-preview, GPT-4-vision-preview
    
    """


    cookies = {
        'LOBE_LOCALE': 'en-US',
        'LOBE_THEME_PRIMARY_COLOR': 'undefined',
        'LOBE_THEME_NEUTRAL_COLOR': 'undefined',
        'LOBE_THEME_APPEARANCE': 'dark',
    }

    headers = {
        'authority': 'chat.boringmarketing.com',
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9',
        'content-type': 'application/json',
        'origin': 'https://chat.boringmarketing.com',
        'referer': 'https://chat.boringmarketing.com/chat?session=inbox',
        'sec-ch-ua-mobile': '?0',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': ua.random,
        'x-lobe-chat-access-code': '',
        'x-openai-api-key': '',
        'x-openai-end-point': '',
    }

    body = {
        'model':  model,
        'stream': stream,
        'frequency_penalty': frequency_penalty,
        'presence_penalty': presence_penalty,
        'temperature': temperature,
        'top_p': top_p,
        'messages': messages
    }

    response = requests.post('https://chat.boringmarketing.com/api/openai/chat', cookies=cookies, headers=headers, json=body)


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
            },
        ],
        "elpased": response.elapsed.total_seconds(),
        "src": 1
    }

    return json.dumps(json_build)

