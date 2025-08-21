"""INFO:
Author: @RyannKim327
Date Modified: 07-08-2025
Purpose: A handler for text based generated response
"""

from g4f.client import Client

from core.image import checkImager
from utils.setup import text_model


def chat_handler(prompt, websearch=False):
    client = Client()
    img = checkImager(prompt)

    if img:
        return img

    response = client.chat.completions.create(
        # provider=Provider.Together,
        model=text_model,
        messages=prompt,
        web_search=websearch,
    )
    return {
        "status": 200,
        "text": response.choices[0].message.content,
        "response": response.choices[0].message.content,
    }
