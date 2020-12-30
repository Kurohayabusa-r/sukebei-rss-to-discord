import feedparser
from discord_webhook import DiscordWebhook, DiscordEmbed
import time
import datetime
import os


webhook_urls = ['Your webhook url']
webhook = DiscordWebhook(url=webhook_urls)
limit = 9

def run_bot():
    # in this case i'm monitoring all uploads by superelmo on sukebei.nyaa
    NewsFeed = feedparser.parse('https://sukebei.nyaa.si/?page=rss&u=superelmo')
    for entry in NewsFeed.entries[:limit]:
        if entry.id not in blacklist:
            embed = DiscordEmbed(title=entry.title, description='{}\n{}'.format(entry.id, entry.published), color=29183)
            
            embed.add_embed_field(name='Hash', value=entry.nyaa_infohash, inline=True)
            embed.add_embed_field(name='Size', value=entry.nyaa_size, inline=True)
            
            embed.set_timestamp()
            webhook.add_embed(embed)

            response = webhook.execute()
            webhook.remove_embed(0)

            blacklist.append(str(entry.id))
            with open("database.txt", "a") as f:
                f.write(str(entry.id) + "\n")
                f.close()

            time.sleep(1800)

def blacklisted_posts():
    if not os.path.isfile("database.txt"):
        blacklist = []
    else:
        with open("database.txt", "r") as f:
            blacklist = f.read()
            blacklist = blacklist.split("\n")
            f.close()

    return blacklist

blacklist = blacklisted_posts()
while True:
    run_bot()