from discord.ext import commands
import discord
import json
from replit import db

with open("data.json", "r") as datab:
    config = json.load(datab)
    app_channel = config["app_channel"]
    guildnum = config["guild"]
    roleapp = config["roleapp"]

class role_application(commands.Cog):
    def __init__(self, client):
        self.client = client


    @commands.Cog.listener()
    async def on_message(self, message):
        guild = self.client.get_guild(719103069828284478)
        appchannel = discord.utils.get(guild.channels, id=int(792761089125384263))
        if (message.guild is None) and (not message.author.bot):
            try:
                apps = db["A"+str(message.author.id)]
                print(apps)
                if apps == "helper":
                    embed = discord.Embed(title=f"Application for role code helper!")
                    embed.add_field(name="Name", value=message.author.mention, inline=False)
                    embed.add_field(name="Reason", value=message.content, inline=False)
                    embed.set_thumbnail(url=message.author.avatar_url)
                    await appchannel.send(embed=embed)
                    await message.author.send("Your application has been submitted!")
                    db["A"+str(message.author.id)] = "done"
                elif apps == "mod":
                    embed = discord.Embed(title=f"Application for role moderator!")
                    embed.add_field(name="Name", value=message.author.mention, inline=False)
                    embed.add_field(name="Reason", value=message.content, inline=False)
                    embed.set_thumbnail(url=message.author.avatar_url)
                    await appchannel.send(embed=embed)
                    await message.author.send("Your application has been submitted!")
                    db["A"+str(message.author.id)] = "done"
            except:
                pass

    @commands.command()
    @commands.has_any_role("MaxCodez")
    async def setupapp(self, ctx):
        embed = discord.Embed(description="React 🔼 for Code helper and 🔽 for moderator application")
        sent = await ctx.send(embed=embed)
        await sent.add_reaction("🔼")
        await sent.add_reaction("🔽")


    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        guild = discord.utils.find(lambda g: g.id == payload.guild_id, self.client.guilds)
        member = discord.utils.find(lambda m: m.id == payload.user_id, guild.members)
        if payload.channel_id == roleapp:
            try:
                user = db["A"+str(payload.user_id)]
                await member.send("Woah cool the jets, you've already applied in the last 7 days!")
            except:
                if payload.emoji.name == "🔼":
                    db["A"+str(payload.user_id)] = "helper"
                    embed = discord.Embed(title="You Have applied for Code Helper!",description=
                    '''
                    Respond to this message with the following:
                    1. How much experience you have coding and in what languages
                    2. Why you want this role
                    don't mess it up! You can only send one message!
                    ''', color=0xb91919)
                    await member.send(embed=embed)
                elif payload.emoji.name == "🔽":
                    db["A"+str(payload.user_id)] = "mod"
                    embed = discord.Embed(title="You Have applied for Moderator!", description='''
                    Respond to this message with the following:
                    1. if you're above the age of 16
                    2. Your experience as a moderator in other servers
                    3. Why you want this role
                    don't mess it up! You can only send one message!
                    ''', color=0xb91919)
                    await member.send(embed=embed)

    @commands.command()
    @commands.has_any_role("MaxCodez")
    async def clearapps(self, ctx):
        matches = db.prefix("A")
        print(matches)
        for i in range(len(matches)):
            del db[f"{matches[i]}"]
        embed = discord.Embed(description="Apps cleared!", color=0xb91919)
        await ctx.channel.send(embed=embed)

def setup(client):
    client.add_cog(role_application(client))