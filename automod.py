import json
import discord
from discord.ext import commands
import asyncio
from replit import db

spam_detect = []

with open("data.json", "r") as datab:
    config = json.load(datab)
    logchannel = config["log_channel"]
    personal_blacklist = config["personal_blacklist"]
    regular_blacklist = config["regular_blacklist"]
    bot_channels = config["bot_channels"]

class autmod(commands.Cog):
    def __init__(self, client):
        self.client = client
    

    '''
    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        guild = discord.utils.find(lambda g : g.id == payload.guild_id, self.client.guilds)
        author = discord.utils.find(lambda m : m.id == payload.user_id, guild.members)
        
        guild = discord.utils.find(lambda g : g.id == payload.guild_id, self.client.guilds)
        if payload.emoji.name == "😤":
            channelsend = discord.utils.get(guild.channels, id=payload.channel_id)
            message = await channelsend.fetch_message(payload.message_id)
            muterole = discord.utils.get(guild.roles, name="mute")
            reaction = discord.utils.get(message.reactions, emoji=payload.emoji.name)
            ismuted = False
            if muterole in message.author.roles:
                ismuted = True

            if (reaction.count > 1) and (ismuted == False):
                await channelsend.send(f"https://discord.com/channels/719103069828284478/{channelsend.id}/{message.id}")
                await message.author.add_roles(muterole)
                await channelsend.send(f"{message.author.mention} was muted... until unmuted?")
      '''
            

    @commands.command()
    @commands.has_any_role("MaxCodez")
    async def clearmute(self, ctx, member: discord.Member, *, reason=None): 
        keys = db.keys()
        for key in keys:
            print(key)
            del key
    @commands.Cog.listener()
    async def on_ready(self):
        while True:
            await asyncio.sleep(10)
            spam_detect.clear()

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        for i in range(len(regular_blacklist)):
            if regular_blacklist[i] in str(after.content).lower():
                await after.delete()
        
        for i in range(len(personal_blacklist)):
            if personal_blacklist[i] in str(after.content).lower():
                await after.delete()
                await after.author.guild.ban(after.author, reason="blacklisted word")
                modlog = discord.utils.get(after.guild.channels, id=int(logchannel))
                embed = discord.Embed(
                    description="{0} banned for using blacklisted word: {1}".format(after.author.mention,personal_blacklist[i]),
                    color=0xdddd1e)
                await modlog.send(embed=embed)
        
        if (("@everyone" in after.content) or ("@here" in after.content)) and (after.author.id != 359252304576380931):
            await after.delete()
        
        if "<@!359252304576380931>" in after.content or "@MaxCodez" in after.content:
            await after.delete()

    @commands.Cog.listener()
    async def on_message(self, message):
        for i in range(len(personal_blacklist)):
            if personal_blacklist[i] in str(message.content).lower():
                await message.delete()
                await message.author.guild.ban(message.author, reason="blacklisted word")
                modlog = discord.utils.get(message.guild.channels, id=int(logchannel))
                embed = discord.Embed(
                    description="{0} banned for using blacklisted word: {1}".format(message.author.mention,personal_blacklist[i]),
                    color=0xdddd1e)
                await modlog.send(embed=embed)
        for i in range(len(regular_blacklist)):
            if regular_blacklist[i] in str(message.content).lower():
                await message.delete()

        if (("@everyone" in message.content) or ("@here" in message.content)) and (message.author.id != 359252304576380931):
            await message.delete()

        if "<@!359252304576380931>" in message.content or "@MaxCodez" in message.content:
            await message.delete()
            embed = discord.Embed(
                description="{0} HAHA didn't you see rule 9? If you need help ping a code helper in <#719103243459756052>".format(
                    message.author.mention), color=0xdddd1e)
            await message.channel.send(embed=embed)

        counter = 0
        for i in range(len(spam_detect)):
            if spam_detect[i] == str(message.author.id):
                counter += 1
        spam_detect.append(str(message.author.id))
        if (counter > 5) and (message.channel.id not in bot_channels):
            print(spam_detect)
            await message.author.send("you have been kicked for spamming too much")
            await message.guild.ban(message.author, reason="spam")
            await asyncio.sleep(1)
            await message.guild.unban(message.author)
            spam_detect.clear()
            modlog = discord.utils.get(message.guild.channels, id=int(logchannel))
            embed = discord.Embed(description="{} has been kicked after spamming".format(message.author.mention), color=0xdddd1e)
            await modlog.send(embed=embed)

def setup(client):
    client.add_cog(autmod(client))
    '''
    @commands.command()
    @commands.has_any_role("Python helper", "Moderator", "admin", "MaxCodez")
    async def afk(self, ctx, *args):
        msg = (' '.join(args))
        db[str(ctx.author.id)] = msg
        await ctx.channel.send("AFK set")
    '''
