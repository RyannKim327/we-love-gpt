from flask import Flask, render_template, request
from g4f.client import Client

app = Flask(__name__)


@app.route("/")
def main():
    return app1()


@app.route("/api")
def app1():
    return render_template("index.html")


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

    req = request.args
    websearch = False
    if req and "websearch" in req:
        websearch = req.get("websearch")
    client = Client()
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": str(req.get("message"))}],
        web_search=websearch,
    )
    return {"status": 200, "response": response.choices[0].message.content}


app.run("0.0.0.0", 3000)
