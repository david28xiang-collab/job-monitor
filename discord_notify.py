import requests
import os


def send_discord(message):
    webhook_url = "https://discord.com/api/webhooks/1514779296458346600/INtAL1KPXJy1ZSQgMrkYDEu44KGzGwmxA5S6flkXtzHTyr3-1BoGn85z6So6VHR0nBSa"

    requests.post(
        webhook_url,
        json={
            "content": message
        }
    )