from discord.ext import commands
import discord
import json
from replit import db as database

with open("data.json", "r") as db:
    config = json.load(db)
    welcome_channel = config["welcome_channel"]


class welcomer(commands.Cog):
    def __init__(self, client):
        self.client = client
        with open("data.json", "r") as db:
            config = json.load(db)
            self.welcome_channel = config["welcome_channel"]

    @commands.Cog.listener()
    async def on_member_join(self, member):
        await member.add_roles(discord.utils.get(member.guild.roles, name="member"))
        embed = discord.Embed(title="Welcome to the MaxCodez discord server!",
                              description=f"{member.mention} please check out the rules in <#730786455676256327>, after that you can collect roles in <#731378784212746320>. We hope you enjoy your stay in our server!")
        embed.set_image(url='https://cdn.discordapp.com/attachments/730786455676256327/731141378494693386/Screenshot_2020-07-10_at_9.34.35_PM.png')
        embed.set_footer(text=f"Member count: {member.guild.member_count}")
        welcome_channel = discord.utils.get(member.guild.channels, id=self.welcome_channel)
        await welcome_channel.send(embed=embed)
        if database["m"+str(member.id)] == "yes":
            await member.add_roles(discord.utils.get(member.guild.roles, name="mute"))

def setup(client):
    client.add_cog(welcomer(client))