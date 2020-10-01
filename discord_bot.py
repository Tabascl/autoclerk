import requests
import time


class DiscordBot:
    def __init__(self, hook):
        self.hook = hook

    def update(self, event):
        self.post_text(event)

    def post_text(self, update):
        print("Sending update")

        response = requests.post(self.hook, json=update.payload)
        
        if response.status_code == 429:
            timeout = response.json()['retry_after']

            print("Rate limiting occurs, timout: {}ms".format(timeout))
            time.sleep(timeout/1000)

            print("Resending...")
            response = requests.post(self.hook, json=update.payload)
            
