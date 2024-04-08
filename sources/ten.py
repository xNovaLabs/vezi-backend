from fake_useragent import UserAgent
import requests
import urllib3
import uuid
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

 
def generate(model: str, messages, prompt = "You are ChatGPT, a large language model trained by OpenAI. Follow the user's instructions carefully. Respond using markdown."):
    """ Supports GPT-3.5-turbo, GPT-4-0125-preview *GPT-4
    
    """

    headers = {
        'Accept': '*/*',
        'Accept-Language': 'en-US,en;q=0.9',
        'Connection': 'keep-alive',
        'Content-Type': 'application/json',
        'Origin': 'https://chat.nolanwindham.com/api/chat',
        'Referer': 'https://chat.nolanwindham.com/api/chat/',
        'User-Agent': ua.random,
    }

    if model.lower() == "gpt-4-0125-preview":
        model = "gpt-4"


    json_data = {
        'model': {
            'id': model,
            'name': model.upper(),
        },
        'messages': messages,
        'key': '',
        'prompt': prompt,
    }

    response = requests.post('https://chat.nolanwindham.com/api/chat', headers=headers, json=json_data, verify=False)

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
        "src": 10
    }
    
    return json.dumps(json_build)
