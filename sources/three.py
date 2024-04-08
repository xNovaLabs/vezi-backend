from fake_useragent import UserAgent
import requests
import uuid
import calendar
import datetime
import json
import urllib3
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
    """ Supports GPT-3.5-turbo, GPT-4-0125-preview *gpt-4, GPT-4-32K *gpt432k
    
    """
    headers = {
        'authority': 'chatgpt.forecastle.ai',
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9',
        'content-type': 'application/json',
        'origin': 'https://chatgpt.forecastle.ai',
        'referer': 'https://chatgpt.forecastle.ai/',
        'sec-ch-ua-mobile': '?0',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': ua.random
    }


    if model.lower() == "gpt-4-32k":
        model = "gpt432k"
        name = "GPT-4-32K"
    elif model.lower() == "gpt-4-0125-preview":
        model = "gpt-4"
        name = model.upper()

    name = model.upper()



    json_data = {
        'model': {
            'id': model,
            'name': name,
        },
        'messages': messages,
        'key': '',
        'prompt': prompt,
        'temperature': temperature,
    }

    response = requests.post('http://chatgpt.forecastle.ai/api/chat', headers=headers, json=json_data, verify=False)

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
        "src": 3
    }
    
    return json.dumps(json_build)
