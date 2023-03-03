import os

import openai

API_KEY = os.environ.get('OPENAI_API_KEY')

openai.api_key = API_KEY


def request(prompt: str) -> str:
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message["content"].removeprefix('\n\n')
