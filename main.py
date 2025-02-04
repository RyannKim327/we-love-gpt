from flask import Flask, render_template, request
from g4f.client import Client

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

    req = request.args
    messages = []
    if req and "user" in req:
        messages.append({"role": "user", "content": str(req.get("message"))})
    else:
        messages = [{"role": "user", "content": str(req.get("message"))}]
    websearch = False
    if req and "websearch" in req:
        websearch = req.get("websearch")
    client = Client()
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        web_search=websearch,
    )

    if req and "user" in req:
        messages.append(
            {
                "role": "system",
                "content": response.choices[0].message.content,
            }
        )
    return {"status": 200, "response": response.choices[0].message.content}, 200


if __name__ == "__main__":
    app.run("0.0.0.0", 3000)
