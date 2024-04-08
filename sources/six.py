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

 
def generate(model: str, messages, prompt = "You are ChatGPT, a large language model trained by OpenAI. Follow the user's instructions carefully. Respond using markdown.", temperature = 1):
    """ Supports GPT-3.5-turbo
    
    """

    
    headers = {
        'Accept': '*/*',
        'Accept-Language': 'en-US,en;q=0.9',
        'Connection': 'keep-alive',
        'Content-Type': 'application/json',
        'Origin': 'http://8.210.69.23:9092',
        'Referer': 'http://8.210.69.23:9092/',
        'User-Agent': ua.random,
    }



    json_data = {
        'model': {
            'id': model,
            'name': model.upper(),
        },
        'messages': messages,
        'key': '',
        'prompt': prompt,
        'temperature': temperature,
    }

    response = requests.post('http://8.210.69.23:9092/api/chat', headers=headers, json=json_data, verify=False)

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
        "src": 6
    }
    
    return json.dumps(json_build)
