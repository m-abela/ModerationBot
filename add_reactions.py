import discord
import json
from discord.ext import commands

with open("data.json", "r") as db:
    config = json.load(db)
    add_votes_channels = config["add_votes_channels"]

class add_reaction(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_message(self, message):
        yes = discord.utils.get(message.guild.emojis, name='YesCodez')
        no = discord.utils.get(message.guild.emojis, name='NoCodez')
        if message.channel.id in add_votes_channels:
            await message.add_reaction(yes)
            await message.add_reaction(no)
def setup(client):
    client.add_cog(add_reaction(client))
