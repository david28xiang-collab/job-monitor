import requests
import os


def send_discord(message):
    webhook_url = "https://discord.com/api/webhooks/1519424142678429696/V0FCshEXgPy-HhR9c3yamETXYlJdfb_ReGYRYEdcUgkTLabAMsoX1yulsinG6ketVIbI"

    requests.post(
        webhook_url,
        json={
            "content": message
        }
    )