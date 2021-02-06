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
        lastRow = db.check_last_row()
        statusLog = lastRow[2] if lastRow is not None else lastRow
        lastIp = lastRow[1] if lastRow is not None else lastRow
        db.insert_status(statusNow, IP)
        if statusNow == "Online" and statusLog == "Offline" and IP == lastIp:
            print("Server started!")
            embed = DiscordEmbed(title='Server Notice', description='Server Started', color=242424)
            webhook.add_embed(embed)
            response = webhook.execute()
        elif statusNow == "Offline" and statusLog == "Online" and IP == lastIp:
            print("Server maintenance")
            embed = DiscordEmbed(title='Server Notice', description='Server Maintenance', color=242424)
            webhook.add_embed(embed)
            response = webhook.execute()
        sleep(30)
