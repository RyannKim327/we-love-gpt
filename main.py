import json
from json.decoder import JSONDecodeError

from flask import Flask, render_template, request
from flask_cors import CORS
from g4f import Client

from utils.gist import fetch_gist, update_gist

app = Flask(__name__, static_url_path="/static")
text_model = "gpt-4o-mini"  # "llama-3.3-70b"
image_model = "flux"

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
                "response": f"{res['message']}<br>Prompt: {res['prompt']}<br><br>![generated image]({generated_image})",
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


@app.route("/api/chat/", methods=["POST", "GET"])
def api_chat():
    messages = []
    websearch = True

    if request.method == "POST":
        # TODO: Post Request

        req = request.get_json()
        messages = req["messages"]

        if req and "websearch" in req:
            websearch = req["websearch"]

    else:
        # TODO: Get Request

        base = {}
        req = request.args

        if req and "message" not in req:
            return {"status": 404, "response": "Undefined message query"}

        if req and "u" in req:
            # TODO: To identify if there's a user from a get request

            gist = fetch_gist()
            base = gist

            # TODO: Clear all past prompts
            if req.get("message") == "/clear" or req.get("message") == "/cls":
                gist["prompts"][req.get("u")] = []
                update_gist(gist)
                return {"status": 200, "response": "Queries are now cleared"}

            else:
                # TODO: To handle user and data information...

                try:
                    if gist["prompts"][req.get("u")]:
                        messages = gist["prompts"][req.get("u")]
                        messages.append({"role": "user", "content": req.get("message")})

                except:
                    gist["prompts"][req.get("u")] = [
                        {"role": "user", "content": req.get("message")}
                    ]

        messages.append({"role": "user", "content": str(req.get("message"))})

        if req and "websearch" in req:
            websearch = req.get("websearch")

        if req and "u" in req:
            update_gist(base)

    chat = chat_handler(messages, websearch)
    return chat


@app.route("/api/generate/", methods=["GET"])
def api_generate():
    return {"status": 200, "responses": generate_image(request.args.get("message"))}


@app.route("/api/register/<string:id>/", methods=["POST", "GET"])
def register(id):
    gist = fetch_gist()
    if gist:
        return { "status": 400, "response": "Invalid GIST"}

    if "error" in gist.keys():
        return { "status": 400, "response": "Invalid GIST"}

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
