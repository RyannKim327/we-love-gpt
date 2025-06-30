# import base64
# import json
# from io import BytesIO
#
# import g4f

import json
from json.decoder import JSONDecodeError

from aiohttp.typedefs import JSONDecoder
from flask import Flask, render_template, request
from flask_cors import CORS
from g4f import Client, Provider

from utils.gist import fetch_gist, update_gist

app = Flask(__name__, static_url_path="/static")
text_model = "llama-3.3-70b"
image_model = "sdxl-turbo"

CORS(app, resources={r"/api/*": {"origins": "*"}})


@app.route("/")
def main():
    return app1()


@app.route("/api")
def app1():
    return render_template("index.html")


@app.errorhandler(404)
def error(err):
    return {
        "status": 404,
        "response": "Page not found, kindly check to our documentation",
        "redirect": request.host,
    }


# @app.route("/api/chat/clear/", methods=["GET"])
# def clear():
#     gist = fetch_gist()
#     req = request.get_json()
#     if req and "u" in req:
#         gist["prompts"][req.get("u")] = []
#         update_gist(gist)
#         return {"status": 200, "response": "Your past queries are cleared"}
#     return {"status": 404, "response": "The user is undefined"}


def generate_image(prompt):
    client = Client()
    response = client.images.generate(
        # provider=Provider.Copilot,
        model=image_model,
        prompt=prompt,
        response_format="url",
    )
    return response.data[0].url
    # {"status": 200, "responses": [i.url for i in response.data]}


def checkImager(prompt):
    client = Client()
    format = {"img": "boolean", "message": "string"}
    response = client.chat.completions.create(
        model=text_model,
        messages=[
            {
                "role": "user",
                "content": f'I have this prompt: "{prompt}". I want you to identify it based on the format I will given. The format was {json.dumps(format)}. If is that an image, imagine that you\'ve generate the image, create a prompt for an image generator that nearly related to the prompt, or enhance the prompt given to make it more understandable by the AI. The response, please `make it one line and remove the unwanted characters to prevent json parse error',
            }
        ],
    )
    try:
        # print(response.choices[0].message.content)
        res = json.loads(response.choices[0].message.content)
        # print(res)
        if res["img"]:
            generated_image = generate_image(res["message"])
            return {
                "status": 200,
                "response": f"{res['message']}<br><br>![generated image]({generated_image})",
                "image": generated_image,
            }
    except JSONDecodeError as e:
        return checkImager(prompt)


@app.route("/api/chat/", methods=["POST", "GET"])
def api_chat():
    client = Client()

    if request.method == "POST":
        req = request.get_json()
        websearch = True
        if req and "websearch" in req:
            websearch = req["websearch"]

        img = checkImager(req["messages"][len(req["messages"]) - 1]["content"])

        if img:
            return img

        client = Client()
        response = client.chat.completions.create(
            model=text_model,
            # provider=Provider.Together,
            web_search=websearch,
            messages=req["messages"],
        )
        return {"status": 200, "response": response.choices[0].message.content}
    else:
        base = {}
        req = request.args
        msgs = [{"role": "user", "content": str(req.get("message"))}]

        if req and "message" not in req:
            return {"status": 404, "response": "Undefined message query"}
        if req and "u" in req:
            gist = fetch_gist()
            base = gist
            if req.get("message") == "clear" or req.get("message") == "cls":
                gist["prompts"][req.get("u")] = []
                update_gist(gist)
                return {"status": 200, "response": "Queries are now cleared"}
            else:  # if req.get("u") in gist["users"]:
                try:
                    if gist["prompts"][req.get("u")]:
                        msgs = gist["prompts"][req.get("u")]
                        msgs.append({"role": "user", "content": req.get("message")})
                except:
                    gist["prompts"][req.get("u")] = [
                        {"role": "user", "content": req.get("message")}
                    ]

        websearch = True

        if req and "websearch" in req:
            websearch = req.get("websearch")

        img = checkImager(msgs["messages"][len(msgs["messages"]) - 1]["content"])

        if img:
            return img

        response = client.chat.completions.create(
            # provider=Provider.Together,
            model=text_model,
            messages=msgs,
            web_search=websearch,
        )

        if req and "u" in req:
            msgs.append(
                {
                    "role": "system",
                    "content": response.choices[0].message.content,
                }
            )
            base["prompts"][req.get("u")] = msgs
            # gist.get("prompt").get(req.get("u")) = msgs
            update_gist(base)
        return {"status": 200, "response": response.choices[0].message.content}, 200


@app.route("/api/generate/", methods=["GET"])
def api_generate():
    return {"status": 200, "responses": generate_image(request.args.get("message"))}


@app.route("/api/register/<string:id>/", methods=["POST", "GET"])
def register(id):
    gist = fetch_gist()
    req = request.args  # request.get_json()

    if gist["prompts"].get(id) == None:
        gist["prompts"][id] = []
        if req and "roleplay" in req:
            gist["prompts"][id] = [
                {"role": "user", "content": req.get("roleplay")},
                {"role": "system", "content": "Okay"},
            ]
        update_gist(gist)
        return {"status": 200, "response": f"{id} User ID is now registered"}
    else:
        return {"status": 200, "response": "This user is already existed"}


if __name__ == "__main__":
    app.run("0.0.0.0", 7000)

# NOTE: To test, execute flask --app main.py --debug run
