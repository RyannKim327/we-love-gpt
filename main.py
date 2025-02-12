import json

import g4f
import requests as req
from flask import Flask, render_template, request
from g4f.client import Client
from g4f.Provider.Blackbox import Blackbox
from werkzeug.datastructures import headers

from utils.gist import fetch_gist, update_gist

app = Flask(__name__, static_url_path="/static")


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
        "redirect": "https://we-love-gpt.onrender.com",
    }


@app.route("/api/chat/", methods=["POST", "GET"])
def chat():
    if request.method == "POST":
        req = request.get_json()
        websearch = False
        if req and "websearch" in req:
            websearch = req["websearch"]
        client = Client()
        response = client.chat.completions.create(
            model="gpt-4o-mini", messages=req["messages"], web_search=websearch
        )
        return {"status": 200, "response": response.choices[0].message.content}
    else:
        base = {}
        req = request.args
        msgs = [{"role": "user", "content": str(req.get("message"))}]

        if req and not "message" in req:
            return {"status": 404, "response": "Undefined message query"}
        if req and "u" in req:
            gist = fetch_gist()
            base = gist
            # if req.get("u") in gist["users"]:
            try:
                if gist["prompts"][req.get("u")]:
                    msgs = gist["prompts"][req.get("u")]
                    msgs.append({"role": "user", "content": req.get("message")})
            except:
                gist["prompts"][req.get("u")] = [
                    {"role": "user", "content": req.get("message")}
                ]

        websearch = False

        if req and "websearch" in req:
            websearch = req.get("websearch")

        client = Client()
        response = client.chat.completions.create(
            model="gpt-4o-mini",
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


# @app.route("/api/vision/", methods=["GET"])
# def vision():
#     req = request.get_json()
#     if req and "q" in req:
#         data = req.post(`https://api.deepai.org/origami-3d-generator`, data={
#             headers={
#
#             }
#         })

if __name__ == "__main__":
    app.run("0.0.0.0", 3000)
