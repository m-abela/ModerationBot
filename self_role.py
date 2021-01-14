import discord
from discord.ext import commands
import json

with open("data.json", "r") as db:
    config = json.load(db)
    reaction_channel = config["reaction_channel"]

class self_role(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if payload.channel_id == reaction_channel:
            guild = discord.utils.find(lambda g : g.id == payload.guild_id, self.client.guilds)
            member = discord.utils.find(lambda m : m.id == payload.user_id, guild.members)
            if payload.emoji.name == "🍿":
                await member.add_roles(discord.utils.get(guild.roles, name="Movie Night"))
            if payload.emoji.name == "😎":
                await member.add_roles(discord.utils.get(guild.roles, name="Coding Stream"))
            if payload.emoji.name == "🎧":
                await member.add_roles(discord.utils.get(guild.roles, name="Music Stream"))
            if payload.emoji.name == "🎮":
                await member.add_roles(discord.utils.get(guild.roles, name="Games Night"))
            if payload.emoji.name == "💙":
                await member.add_roles(discord.utils.get(guild.roles, name="Python Lover"))
            if payload.emoji.name == "❤️":
                await member.add_roles(discord.utils.get(guild.roles, name="Unity Addict"))

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        if payload.channel_id == reaction_channel:
            guild = discord.utils.find(lambda g : g.id == payload.guild_id, self.client.guilds)
            member = discord.utils.find(lambda m : m.id == payload.user_id, guild.members)
            if payload.emoji.name == "🍿":
                await member.remove_roles(discord.utils.get(guild.roles, name="Movie Night"))
            if payload.emoji.name == "😎":
                await member.remove_roles(discord.utils.get(guild.roles, name="Coding Stream"))
            if payload.emoji.name == "🎧":
                await member.remove_roles(discord.utils.get(guild.roles, name="Music Stream"))
            if payload.emoji.name == "🎮":
                await member.remove_roles(discord.utils.get(guild.roles, name="Games Night"))
            
            if payload.emoji.name == "💙":
                await member.remove_roles(discord.utils.get(guild.roles, name="Python Lover"))
            if payload.emoji.name == "❤️":
                await member.remove_roles(discord.utils.get(guild.roles, name="Unity Addict"))
      
    @commands.command()
    @commands.has_any_role("MaxCodez")
    async def setuproles(self, ctx):
        embed = discord.Embed(description='''
        React for notifications for these events!
        🍿 - Movie night!
        😎 - Coding stream
        🎧 - Music stream
        🎮 - Games night
        ''', color=0x397882)

        sent = await ctx.send(embed=embed)
        await sent.add_reaction("🍿"), await sent.add_reaction("😎"), await sent.add_reaction("🎧"), await sent.add_reaction("🎮")
        embed = discord.Embed(description='''
        What do you need help with?
        💙 - Python 
        ❤️ - Unity
        ''', color=0xb91919)
        sent = await ctx.send(embed=embed)
        await sent.add_reaction("💙")
        await sent.add_reaction("❤️")

def setup(client):
    client.add_cog(self_role(client))