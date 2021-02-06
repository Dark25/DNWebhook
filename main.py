import os
import db
import network
from discord_webhook import DiscordWebhook, DiscordEmbed
from dotenv import load_dotenv
from time import sleep

if __name__ == '__main__':
    db.make_table()

    load_dotenv()
    WEBHOOK_LINK = os.getenv("WEBHOOK_LINK")
    IP = os.getenv("IP")

    webhook = DiscordWebhook(url=WEBHOOK_LINK)
    while True:
        # statusNow = api.fetch_api()
        statusNow = network.check_port(IP)
        statusLog = db.check_last_row()[1] if db.check_last_row() is not None else db.check_last_row()
        db.insert_status((statusNow, ))
        if statusNow == "Online" and statusLog == "Offline":
            print("Server started!")
            embed = DiscordEmbed(title='Server Notice', description='Server Started', color=242424)
            webhook.add_embed(embed)
            response = webhook.execute()
        elif statusNow == "Offline" and statusLog == "Online":
            print("Server maintenance")
            embed = DiscordEmbed(title='Server Notice', description='Server Maintenance', color=242424)
            webhook.add_embed(embed)
            response = webhook.execute()
        sleep(30)
