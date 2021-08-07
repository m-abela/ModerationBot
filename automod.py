import discord
from discord.ext import commands
import asyncio
from datetime import datetime
from pymongo import MongoClient
spam_detect = []
gif_detect = []

class automod(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.cluster = MongoClient("mongodb+srv://maxcodez:zbndxaPz1BNseBgl@cluster0.hqubn.mongodb.net/<dbname>?retryWrites=true&w=majority")
        self.db = self.cluster["discord"]
        self.info = self.db["info"]
        self.moderation = self.db["moderation"]
        self.bots = self.info.find_one({"name":"bots"})["value"]
        self.bot_channel = (self.info.find_one({"name":"botchannel"})["value"])
        self.norank = self.info.find_one({"name":"bots"})["value"]
        self.regular_blacklist = self.info.find_one({"name":"swear"})["value"]
        self.personal_blacklist = self.info.find_one({"name":"blacklist"})["value"]
        self.logchannel = self.info.find_one({"name":"log"})["value"]

            

    @commands.Cog.listener()
    async def on_ready(self):
        guild = self.client.get_guild(799977201898487818)
        channelsend = discord.utils.get(guild.channels, id=self.logchannel)
        self.gif_counter(self)
        while True:
            time = datetime.now().strftime('%H:%M')
            await asyncio.sleep(10)
            spam_detect.clear()
            gif_detect.clear()
            info = self.moderation.find_one({"time":time})
            if info != None:
                self.moderation.delete_one({"time":time})
                member = discord.utils.find(lambda m : m.id == int(info["mute"]), guild.members)
                await member.remove_roles(discord.utils.get(guild.roles, name="Detention"))
                embed = discord.Embed(description=f"**{member.name}** was unmuted", color=0x4DC8E9)
                await channelsend.send(embed=embed)

            
            

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        for i in range(len(self.regular_blacklist)):
            if self.regular_blacklist[i] in str(after.content).lower():
                await after.delete()
        
        for i in range(len(self.personal_blacklist)):
            if self.personal_blacklist[i] in str(after.content).lower():
                await after.delete()
                await after.author.guild.ban(after.author, reason="blacklisted word")
                modlog = discord.utils.get(after.guild.channels, id=self.logchannel)
                embed = discord.Embed(
                    description="{0} banned for using blacklisted word: {1}".format(after.author.mention,self.personal_blacklist[i]),
                    color=0x4DC8E9)
                await modlog.send(embed=embed)
        
        if (("@everyone" in after.content) or ("@here" in after.content)) and (after.author.id != 359252304576380931):
            await after.delete()
        
        if "<@!359252304576380931>" in after.content or "@MaxCodez" in after.content:
            await after.delete()

    


    @commands.Cog.listener()
    async def on_message(self, message):
        for i in range(len(self.personal_blacklist)):
            if self.personal_blacklist[i] in str(message.content).lower():
                await message.delete()
                await message.author.guild.ban(message.author, reason="blacklisted word")
                modlog = discord.utils.get(message.guild.channels, id=int(self.logchannel))
                embed = discord.Embed(
                    description="{0} banned for using blacklisted word: {1}".format(message.author.mention,self.personal_blacklist[i]),
                    color=0x4DC8E9)
                await modlog.send(embed=embed)
        for i in range(len(self.regular_blacklist)):
            if self.regular_blacklist[i] in str(message.content).lower():
                await message.delete()

        if (("@everyone" in message.content) or ("@here" in message.content)) and (message.author.id not in self.bots):
            await message.delete()

        if ("<@!359252304576380931>" in message.content or "@MaxCodez" in message.content) and (message.author.id not in self.bots):
            await message.delete()
            embed = discord.Embed(
                description="Max is a busy guy! If he isn't already here it's probably for a good reason!".format(message.author.mention), color=0x4DC8E9)
            await message.channel.send(embed=embed)
        '''
        if "https" in message.content:
            gif_detect.append(message.author.id)
        gif_counter = 0
        for i in range(len(gif_detect)):
            if gif_detect[i] == (message.author.id):
                gif_counter += 1
      
        counter = 0
        for i in range(len(spam_detect)):
            if spam_detect[i] == str(message.author.id):
                counter += 1
        spam_detect.append(str(message.author.id))

        if (counter > 7) or (gif_counter > 1):
                print(spam_detect)
                await message.author.send("you have been kicked for spamming too much")
                await message.guild.ban(message.author, reason="spam")
                await asyncio.sleep(1)
                await message.guild.unban(message.author)
                spam_detect.clear()
                modlog = discord.utils.get(message.guild.channels, id=int(self.logchannel))
                embed = discord.Embed(description="{} has been kicked after spamming".format(message.author.mention), color=0x4DC8E9)
                await modlog.send(embed=embed)
        '''
    
    @commands.Cog.listener()
    async def on_message_delete(self, message):
        modlog = discord.utils.get(message.guild.channels, id=int(self.logchannel))
        embed = discord.Embed(title="Message deleted", color=0x7a869b)
        embed.add_field(name="Author: ", value=f"{message.author.mention}")
        embed.add_field(name="Channel: ", value=f"{message.channel}")
        embed.add_field(name="Message: ", value=message.content, inline=False)
        embed.set_thumbnail(url=message.author.avatar_url)
        await modlog.send(embed=embed)

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        modlog = discord.utils.get(before.guild.channels, id=int(self.logchannel))
        embed = discord.Embed(title="Message edited", color=0x4DC8E9)
        embed.add_field(name="Author: ", value=f"{before.author.mention}")
        embed.add_field(name="Channel: ", value=f"{before.channel}")
        embed.add_field(name="Before: ", value=before.content, inline=False)
        embed.add_field(name="After: ", value=after.content, inline=False)
        embed.set_thumbnail(url=before.author.avatar_url)
        await modlog.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        modlog = discord.utils.get(member.guild.channels, id=int(self.logchannel))
        embed = discord.Embed(title="Member left :(", color=0x4DC8E9)
        embed.add_field(name="Member: ", value=member.mention, inline=True)
        embed.add_field(name="Left: ", value=member.guild.member_count, inline=True)
        embed.set_thumbnail(url=member.avatar_url)
        await modlog.send(embed=embed)

    

def setup(client):
    client.add_cog(automod(client))

