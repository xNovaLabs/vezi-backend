from fake_useragent import UserAgent
import requests
import uuid
import urllib3
import calendar
import datetime
import json

urllib3.disable_warnings()
ua = UserAgent()


def completionID():
  """Generates an ID with the format 'chatcmpl-random_part'

  Returns:
      str: The generated ID.
  """
  prefix = "chatcmpl-" 
  random_part = uuid.uuid4().hex[:29] 
  return f"{prefix}{random_part}"

 
def generate(model: str, messages, prompt = "You are ChatGPT, a large language model trained by OpenAI. Follow the user's instructions carefully. Respond using markdown.", temperature = 1):
    """ Supports GPT-3.5-turbo, GPT-4-1106-preview, GPT-4, GPT-4-32k
    
    """


    headers = {
        'authority': 'svelte-chatbot-ui.pages.dev',
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9',
        'content-type': 'text/plain;charset=UTF-8',
        'origin': 'https://svelte-chatbot-ui.pages.dev',
        'referer': 'https://svelte-chatbot-ui.pages.dev/',
        'sec-ch-ua-mobile': '?0',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': ua.random
    }

    if model.lower() == "gpt-4-1106-preview":
        maxLength = 384000
        tokenLimit = 128000
        name = "GPT-4-TURBO"
    elif model.lower() == "gpt-4-32k":
        maxLength = 96000
        tokenLimit = 32000
        name = model.upper()
    elif model.lower() == "gpt-4":
        maxLength = 24000
        tokenLimit = 8000
        name = model.upper()
    elif model.lower() == "gpt-3.5-turbo":
        maxLength = 12000
        tokenLimit = 4000
        name = "GPT-3.5"
    else:
        name = model.upper()
        maxLength = 0
        tokenLimit = 0



    json_data = {
        'model': {
            'id': model,
            'maxLength': maxLength,
            'name': name,
            'tokenLimit': tokenLimit
        },
        'messages': messages,
        'key': '',
        'prompt': prompt,
        'temperature': temperature,
    }

    response = requests.post('https://svelte-chatbot-ui.pages.dev/api/chat', headers=headers, json=json_data, verify=False)

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
        "elpased": response.elapsed.total_seconds()
    }
    
    return json.dumps(json_build)
