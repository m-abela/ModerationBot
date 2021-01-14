from webserver import keep_alive
from discord.ext import commands
import discord, json

import automod, helpreview, helproom, info, levelsys, logger, misc, moderation, python_help, self_role, welcome, python_challenges

cogs = [automod, helpreview, helproom, info, levelsys, logger, misc, moderation, python_help, self_role, welcome, python_challenges]

with open("data.json", "r") as datab:
    config = json.load(datab)
    token = config["log_channel"]
    reaction_channel = config["reaction_channel"]

i = discord.Intents.all()
client = commands.Bot(command_prefix='?', intents=i)

for i in range(len(cogs)):
    cogs[i].setup(client)

keep_alive()
client.run("NzcxMTAzMzM2MjA3MjIwNzU2.X5nP8Q.b_Z2WK8Z7x5ev39MGbgJK5EGvGg")
##banana