""" INFO:
  Author: @RyannKim327
  Date Modified: 07-08-2025
  Purpose: A general handler for method and access
"""

from core.text import chat_handler

def get_chat_handler(prompt: dict, websearch=False):
    return chat_handler(prompt=[prompt], websearch=websearch)
    pass

def post_chat_handler(prompt, websearch=False):
    return chat_handler(prompt=prompt, websearch=websearch)