from utils.gist import *

def register(req, id):
    gist = fetch_gist()
    if not gist:
        return { "status": 400, "response": "Invalid GIST"}

    if "error" in gist.keys():
        return { "status": 400, "response": "Invalid GIST"}


    if gist["prompts"].get(id) == None:
        gist["prompts"][id] = []

        # Adding roleplay
        if req.method == "POST":
            if req and "roleplay" in req:
                gist["prompts"][id] = [
                    {"role": "user", "content": req.get("roleplay")},
                    {"role": "system", "content": "Okay"},
                ]

        update_gist(gist)
        return {"status": 200, "response": f"{id} User ID is now registered"}
    else:
        return {"status": 200, "response": "This user is already existed"}