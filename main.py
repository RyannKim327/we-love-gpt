from flask import Flask, render_template, request
from flask_cors import CORS
from utils.gist import fetch_gist, update_gist
from utils.user_handler import register

from utils.handler import get_chat_handler, post_chat_handler

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


@app.route("/api/chat/", methods=["POST", "GET"])
def api_chat():
    websearch = True

    if request.method == "POST":
        # TODO: Post Request

        req = request.get_json()

        if req and "websearch" in req:
            websearch = req["websearch"]
        
        return post_chat_handler(req['messages'], websearch)
    

    else:
        # TODO: Get Request

        return get_chat_handler()


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
