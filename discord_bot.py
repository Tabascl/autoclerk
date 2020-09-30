import requests


class DiscordBot:
    def __init__(self, hook):
        self.hook = hook

    def update(self, event):
        self.post_text(event)

    def post_text(self, update):
        print("Sending update")

        response = requests.post(self.hook, json=update.payload)
        pass
