import json
import discord
from discord.ext import commands

with open("data.json", "r") as db:
    config = json.load(db)
    logchannel = config["log_channel"]


class logger(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        modlog = discord.utils.get(message.guild.channels, id=int(logchannel))
        embed = discord.Embed(title="Message deleted", color=0x7a869b)
        embed.add_field(name="Author: ", value=f"{message.author.mention}")
        embed.add_field(name="Channel: ", value=f"{message.channel}")
        embed.add_field(name="Message: ", value=message.content, inline=False)
        embed.set_thumbnail(url=message.author.avatar_url)
        await modlog.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_join(self, member):
        modlog = discord.utils.get(member.guild.channels, id=int(logchannel))
        embed = discord.Embed(title="Member joined!", color=0x7a869b)
        embed.add_field(name="Member: ", value=member.mention, inline=True)
        embed.add_field(name="No: ", value=member.guild.member_count, inline=True)
        embed.set_thumbnail(url=member.avatar_url)
        await modlog.send(embed=embed)
        await modlog.send(f"<@{member.id}>")

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        modlog = discord.utils.get(member.guild.channels, id=int(logchannel))
        embed = discord.Embed(title="Member left :(", color=0x7a869b)
        embed.add_field(name="Member: ", value=member.mention, inline=True)
        embed.add_field(name="Left: ", value=member.guild.member_count, inline=True)
        embed.set_thumbnail(url=member.avatar_url)
        await modlog.send(embed=embed)

def setup(client):
    client.add_cog(logger(client))