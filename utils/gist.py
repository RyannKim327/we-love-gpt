import json
import os

import requests

GITHUB_TOKEN = os.getenv("GH_TOKEN")
GIST_ID = os.getenv("GIST_ID")
FILE_NAME = os.getenv("FILE")


def fetch_gist() -> dict:
    if not GITHUB_TOKEN or not GIST_ID or not FILE_NAME:
        print("Missing required environment variables.")
        return {"error": "Missing required environment variables."}

    url = f"https://api.github.com/gists/{GIST_ID}"
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json",
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        new_data = json.loads(data["files"][FILE_NAME]["content"])
        return new_data
    except requests.exceptions.RequestException as error:
        print("GIST: Error fetching Gist:", error)
        return fetch_gist()


def update_gist(data2):
    if not GITHUB_TOKEN or not GIST_ID or not FILE_NAME:
        print("Missing required environment variables.")
        return ""

    url = f"https://api.github.com/gists/{GIST_ID}"
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}

    try:
        # Fetch the existing Gist
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        # Convert data2 to JSON string if not a string already
        if not isinstance(data2, str):
            data2 = json.dumps(data2, indent=2)

        # Update the Gist
        update_payload = {"files": {FILE_NAME: {"content": data2}}}
        update_response = requests.patch(url, headers=headers, json=update_payload)
        update_response.raise_for_status()

        print("GIST: Gist updated successfully!")
    except requests.exceptions.RequestException as error:
        print("GIST: Error updating Gist:", error)
        update_gist(data2)
