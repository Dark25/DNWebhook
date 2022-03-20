import db
import network
from discord_webhook import DiscordWebhook, DiscordEmbed
from dotenv import load_dotenv
from os import getenv
from time import sleep

if __name__ == '__main__':
    db.make_table()

    load_dotenv()
    WEBHOOK_LINK = getenv("WEBHOOK_LINK")
    IP = getenv("IP")

    webhook = DiscordWebhook(url=WEBHOOK_LINK)
    embedStart = DiscordEmbed(title='Server Notice', description='Server Started', color=242424)
    embedMaintenance = DiscordEmbed(title='Server Notice', description='Server Maintenance', color=242424)

    while True:
        webhook.remove_embed(0) if len(webhook.embeds) > 0 else None
        statusNow = network.check_port(IP)
        lastRow = db.check_last_row()
        statusLog = lastRow[2] if lastRow is not None else lastRow
        lastIp = lastRow[1] if lastRow is not None else lastRow

        if statusNow == "Online" and statusLog == "Offline" and IP == lastIp:
            print("Server started!!")
            webhook.add_embed(embedStart)
            response = webhook.execute()
        elif statusNow == "Offline" and statusLog == "Online" and IP == lastIp:
            print("Server maintenance")
            webhook.add_embed(embedMaintenance)
            response = webhook.execute()

        db.insert_status(IP, statusNow)
        sleep(30)
