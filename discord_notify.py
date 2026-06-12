import requests

WEBHOOK_URL = "https://discord.com/api/webhooks/1514779296458346600/INtAL1KPXJy1ZSQgMrkYDEu44KGzGwmxA5S6flkXtzHTyr3-1BoGn85z6So6VHR0nBSa"

def send_discord(message):

    requests.post(
        WEBHOOK_URL,
        json={
            "content": message
        }
    )