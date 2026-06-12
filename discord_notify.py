import requests
import os


def send_discord(message):
    webhook_url = os.environ["DISCORD_WEBHOOK"]

    requests.post(
        webhook_url,
        json={
            "content": message
        }
    )