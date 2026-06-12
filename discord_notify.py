import requests
import os

webhook_url = os.environ["DISCORD_WEBHOOK"]

def send_discord(message):

    requests.post(
        webhook_url,
        json={
            "content": message
        }
    )