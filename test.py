import requests
from openai import OpenAI


client = OpenAI(
    api_key="sk-hynix",
    base_url="http://127.0.0.1:8000/v1"
)

chat_completion = client.chat.completions.create(
    stream=False,
    model="gpt-4-vision-preview",
    temperature=1,
    presence_penalty = 0,
    frequency_penalty = 0,
    top_p = 1,
    messages=[
        {
            "role": "user",
            "content": 'There are 50 books in a library. Sam decides to read 5 of the books. How many books are there now? If there are 45 books, say "1". Else, if there is the same amount of books, say "2".',
        },
    ],
)
print(chat_completion.choices[0].message.content)
