"""INFO:
Author: @RyannKim327
Date Modified: 07-08-2025
Purpose: A handler for image and text generator and to identify if the user ask for image
"""

import json
from json.decoder import JSONDecodeError

from g4f.client import Client

from utils.setup import image_model, text_model


def generate_image(prompt):
    client = Client()
    response = client.images.generate(
        model=image_model,
        prompt=prompt,
        response_format="url",
    )
    return response.data[0].url


def checkImager(prompt):
    client = Client()
    format = json.dumps({"img": "boolean", "message": "string", "prompt": "string"})
    msg = [
        {
            "role": "user",
            "content": f"""Check weather the prompt from user is asking for image generator, if the user ask you to generate image please generate, if not then dont generate and return to "img" key is False from the format I gave to you.
    Your response must be in single line and with this format: {format}.
    This was a strict method to identify if the user still asking to generate image, to know that, observe the last prompt if it ask for image or not.
    You've may also use it to identify it weather the user asking for clarifications to the image or not.
    If is that an image, imagine that you\'ve generate the image, create a prompt, and explain and identify detail by detail what about to request for an image generator that nearly related to the prompt, or enhance the prompt given to make it more understandable by the AI.
    """.strip(),
        }
    ]
    response = client.chat.completions.create(model=text_model, messages=(msg + prompt))

    try:
        res = json.loads(response.choices[0].message.content)
        if res["img"] and len(res["prompt"]) > 10:
            generated_image = generate_image(res["prompt"])

            return {
                "status": 200,
                "text": res["message"],
                "propmpt": f"{res['message']}\nPropmpt: {res['propmpt']}",
                "response": f"{res['message']}<br>Prompt: {res['prompt']}<br><br>![generated image]({generated_image})",
                "image": generated_image,
            }

    except JSONDecodeError as e:
        return checkImager(prompt)
