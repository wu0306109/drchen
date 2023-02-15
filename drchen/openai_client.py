import os

import openai

API_KEY = os.environ.get('OPENAI_API_KEY')

openai.api_key = API_KEY


def request(prompt: str) -> str:
    response = openai.Completion.create(
        model='text-davinci-003',
        prompt=prompt,
        temperature=0.7,
        max_tokens=128,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
    )
    str.removeprefix('/n/n')
    return response.choices[0].text.removeprefix('\n\n')
