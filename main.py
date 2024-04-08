from quart import Quart, render_template, websocket, request
from sources import one, two, three, four, six, seven, eight, nine, ten, eleven
import random
import json

app = Quart(__name__)

@app.route("/v1/chat/completions", methods=['POST'])
async def chat():
    data = await request.get_data()
    data = json.loads(data)

    try:
        x = data["model"]
        x = data["messages"]
        x = data["frequency_penalty"]
        x = data["presence_penalty"]
        x = data["top_p"]
        x = data["stream"]
        x = data["temperature"]
    except:
        return "Missing required parameters."

    with open('keys.json') as f:
        apikey = json.load(f)
    go = False
    for key in apikey:
        print(key)
        if key['key'] == request.headers.get('Authorization').replace("Bearer ", ""):
            go = True
    
    if (go):
        match data["model"]:
            case "gpt-3.5-turbo":
                load = random.choice([1, 2, 3, 6, 7, 8, 9, 10, 11])

                match (load):
                    case 1:
                        print(1)
                        return one.generate(data["model"], data["messages"], data["temperature"], data["frequency_penalty"], data["presence_penalty"], data["top_p"], data["stream"])
                    case 2:
                        print(2)
                        return two.generate(data["model"], data["messages"], temperature=data["temperature"])
                    case 3:
                        print(3)
                        return three.generate(data["model"], data["messages"], temperature=data["temperature"])
                    case 6:
                        print(6)
                        return six.generate(data["model"], data["messages"], temperature=data["temperature"])
                    case 7:
                        print(7)
                        return seven.generate(data["model"], data["messages"], temperature=data["temperature"])
                    case 8:
                        print(8)
                        return eight.generate(data["model"], data["messages"], temperature=data["temperature"])
                    case 9:
                        print(9)
                        return nine.generate(data["messages"])
                    case 10:
                        print(10)
                        ten.generate(data["model"], data["messages"])
                    case 11:
                        print(11)
                        return eleven.generate(data["model"], data["messages"], temperature=data["temperature"])
                    case _:
                        return "Something went wrong."
            case "gpt-3.5-turbo-1106":
                return one.generate(data["model"], data["messages"], data["temperature"], data["frequency_penalty"], data["presence_penalty"], data["top_p"], data["stream"])

            case "gpt-3.5-turbo-16k":
                return one.generate(data["model"], data["messages"], data["temperature"], data["frequency_penalty"], data["presence_penalty"], data["top_p"], data["stream"])

            case "gpt-4":
                load = random.choice([1, 11])

                if load == 1:
                    return one.generate(data["model"], data["messages"], data["temperature"], data["frequency_penalty"], data["presence_penalty"], data["top_p"], data["stream"])
                else:
                    return eleven.generate(data["model"], data["messages"], temperature=data["temperature"])
            case "gpt-4-32k":
                load = random.choice([3, 11])

                if load == 11:
                    print('11')
                    return eleven.generate(data["model"], data["messages"], temperature=data["temperature"])
                else:
                    return three.generate(data["model"], data["messages"], temperature=data["temperature"])
            
            case "gpt-4-1106-preview":
                load = random.choice([1, 11])

                if load == 1:
                    return one.generate(data["model"], data["messages"], data["temperature"], data["frequency_penalty"], data["presence_penalty"], data["top_p"], data["stream"])
                else:
                    return eleven.generate(data["model"], data["messages"], temperature=data["temperature"])
            case "gpt-4-0125-preview":
                load = random.choice([2, 3, 8, 10])

                if load == 2:
                    return two.generate(data["model"], data["messages"], temperature=data["temperature"])
                elif load == 3:
                    return three.generate(data["model"], data["messages"], temperature=data["temperature"])
                elif load == 8:
                    return eight.generate(data["model"], data["messages"], temperature=data["temperature"])
                else:
                    return ten.generate(data["model"], data["messages"])

            case "gpt-4-vision-preview":
                return one.generate(data["model"], data["messages"], data["temperature"], data["frequency_penalty"], data["presence_penalty"], data["top_p"], data["stream"])
                
            case _:
                return "Invalid model."
    else:
        return "Invalid api key. Get an API Key for Free @ https://discord.gg/vezi"




@app.route("/v1/models")
async def models():
    body = """
    [
    {
        "model": "gpt-3.5-turbo"
    },
    {
        "model": "gpt-3.5-turbo-1106"
    },
    {
        "model": "gpt-3.5-turbo-16k"
    },
    {
        "model": "gpt-4"
    },
    {
        "model": "gpt-4-32k"
    },
    {
        "model": "gpt-4-1106-preview"
    },
    {
        "model": "gpt-4-0125-preview"
    },
    {
        "model": "gpt-4-vision-preview"
    }
]
    """
    return json.loads(body)

