from core.text import chat_handler

def get_chat_handler(prompt: dict, websearch=True):
    return chat_handler([prompt])
    pass

def post_chat_handler(prompt, websearch=True):
    return chat_handler(prompt, websearch)