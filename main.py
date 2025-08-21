""" INFO:
  Author: @RyannKim327
  Date Modified: 07-08-2025
  Purpose: Main process where the system works
"""

from flask import Flask, render_template, request
from flask_cors import CORS
from utils.user_handler import register

from utils.handler import get_chat_handler, post_chat_handler
from core.image import generate_image

app = Flask(__name__, static_url_path="/static")
CORS(app, resources={r"/api/*": {"origins": "*"}})

@app.route("/")
def main():
    return app1()

@app.route("/api")
def app1():
    return render_template("index.html", url=request.host)

@app.errorhandler(404)
def error(err):
    return {
        "status": 404,
        "response": "Page not found, kindly check to our documentation",
        "redirect": request.host,
    }

<<<<<<< HEAD
=======

def generate_image(prompt):
    client = Client()
    response = client.images.generate(
        # provider=Provider.Copilot,
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
    #   {
    #       "role": "user",
    #       "content": f'I have this prompt: "{prompt}". I want you to identify it based on the format I will given. The format was {json.dumps(format)}. If is that an image, imagine that you\'ve generate the image, create a prompt for an image generator that nearly related to the prompt, or enhance the prompt given to make it more understandable by the AI. The response, please `make it one line and remove the unwanted characters to prevent json parse error',
    #   }
    response = client.chat.completions.create(model=text_model, messages=msg + prompt)
    try:
        # print(response.choices[0].message.content)
        res = json.loads(response.choices[0].message.content)
        # print(res)
        if res["img"] and len(res["prompt"]) > 10:
            generated_image = generate_image(res["prompt"])
            return {
                "status": 200,
                "propmt": f"{res['messsage']}<br>Propmpt: {res['propmt']}",
                "text": res["message"],
                "response": f"{res['message']}<br>![generated image]({generated_image})",
                "image": generated_image,
            }
    except JSONDecodeError as e:
        return checkImager(prompt)


def chat_handler(prompt, websearch=True):
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
    return {"status": 200, "response": response.choices[0].message.content}


>>>>>>> 17228cd (08-21-25 19:23)
@app.route("/api/chat/", methods=["POST", "GET"])
def api_chat():
    websearch = False

    if request.method == "POST":
        # TODO: Post Request

        req = request.get_json()
        if req and "websearch" in req:
            websearch = req["websearch"]
        
        return post_chat_handler(req['messages'], websearch)
    
    else:
        # TODO: Get Request
        return get_chat_handler(request.args.get("message"), websearch=request.args.get("websearch"))

@app.route("/api/generate/", methods=["GET"])
def api_generate():
    return {"status": 200, "responses": generate_image(request.args.get("message"))}

@app.route("/register/<string:id>/", methods=["POST", "GET"])
def register(id):
    req = request.args
    return register(req, id)

if __name__ == "__main__":
    app.run("0.0.0.0", 7000)

# NOTE: To test, execute flask --app main.py --debug run