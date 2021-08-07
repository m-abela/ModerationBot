import discord
from discord.ext import commands
from pymongo import MongoClient
from datetime import datetime, timedelta

class commod(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.cluster = MongoClient(
            "mongodb+srv://maxcodez:zbndxaPz1BNseBgl@cluster0.hqubn.mongodb.net/<dbname>?retryWrites=true&w=majority")
        self.db = self.cluster["discord"]
        self.moderation = self.db["moderation"]
        self.info = self.db["info"]
        self.modlog = self.info.find_one({"name":"modlog"})["value"]
        self.ignore = self.info.find_one({"name":"bots"})["value"]

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        guild = discord.utils.find(lambda g : g.id == payload.guild_id, self.client.guilds)
        modlog = discord.utils.get(guild.channels, id=self.modlog)
        channelsend = discord.utils.get(guild.channels, id=payload.channel_id)
        message = await channelsend.fetch_message(payload.message_id)
        author = discord.utils.find(lambda m : m.id == payload.user_id, guild.members)
        mutetime = [2, 6, 24]

        if ((payload.emoji.name == "NoCodez") and (payload.user_id == 359252304576380931)):
                modmsg = self.moderation.find_one({"modmsg":str(payload.message_id)})
                if modmsg != None:
                    embed = discord.Embed(title=f"Misconduct for ticket #{modmsg['ticket']}!", color=0x4DC8E9) 
                    for i in range(len(modmsg["tags"])):
                        try:
                            member = discord.utils.find(lambda m : m.id == int(modmsg["tags"][i]), guild.members)
                            await member.send("You\'ve been banned from the MaxCodez academy for misuse of the moderation system...")
                            await guild.ban(member, reason="not adiding by server rules")
                            embed.add_field(name=f"**{member.name}:**", value="has been banned for the misuse of the community moderation", inline=False)
                            self.moderation.delete_one({"id":str(member.id)})
                        except:
                            embed.add_field(name=f"**{member.name}:**", value="Could not be sent a message", inline=False)
                    embed.set_image(url="https://cdn.discordapp.com/attachments/847101178940227594/853527175033782301/Screenshot_2021-06-13_at_2.51.11_PM.png")
                    await modlog.send(embed=embed)
                    mute = self.moderation.find_one({"mute": modmsg["victim"]})
                    if mute != None:
                        self.moderation.delete_one({"mute" : modmsg["victim"]})
                        member = discord.utils.find(lambda m : m.id == int(modmsg["victim"]), guild.members)
                        await member.remove_roles(discord.utils.get(guild.roles, name="Detention"))
                        embed = discord.Embed(description=f"{member.mention} has been unmuted", color=0x4DC8E9)
                        await modlog.send(embed=embed)
                    
                    banned = await guild.bans()
                    for entry in banned:
                        if entry.user.id == int(modmsg["victim"]):
                            await guild.unban(entry.user)
                            embed = discord.Embed(description=f"{entry.user.name} has been unbanned!", color=0x4DC8E9)
                            await modlog.send(embed=embed)
                            return None
                    self.moderation.delete_one({"modmsg":str(payload.message_id)})
                    return None
        
        if payload.emoji.name == "warn":
            if ((message.author.id in self.ignore) or (payload.user_id == message.author.id)):
                await message.remove_reaction(payload.emoji, author)
                return None
            
            twice = self.moderation.find_one({"victim":str(message.author.id)})
            if twice != None:
                if ((twice["messageid"] != str(payload.message_id)) and (twice["modmsg"] == "")):
                    await message.remove_reaction(payload.emoji, author)
                    return None

            muted = self.moderation.find_one({"mute":str(message.author.id)})
            if muted != None:
                await message.remove_reaction(payload.emoji, author)
                return None

            info = self.moderation.find_one({"messageid":str(payload.message_id)})
            if info != None:
                self.moderation.update({'messageid': str(message.id)},{'$push': {'tags': str(payload.user_id)}})
                reaction = discord.utils.get(message.reactions, emoji=payload.emoji)
                if (reaction.count > 1) and (info["modmsg"] == ""):
                    person = self.moderation.find_one({"id":str(message.author.id)})
                    if person == None:
                        mydict = {"id": str(message.author.id), "strikes": "1", "member":"true"}
                        self.moderation.insert_one(mydict)
                        self.moderation.update({"id":str(message.author.id)}, { "$set": { "reasons": [message.content]}}, multi=True)
                        strikes = 1
                    else:
                        self.moderation.update({'id': str(message.author.id)},{'$push': {'reasons': str(message.content)}})
                        strikes = int(person["strikes"])+1
                        self.moderation.update_one({"id":str(message.author.id)},{"$set":{"strikes":str(strikes)}})
                    if strikes < 4:
                        embed = discord.Embed(description=f"{message.author.mention} muted for **{mutetime[strikes-1]} hours**", color=0x4DC8E9)
                        await channelsend.send(embed=embed)
                        ticket = self.moderation.find_one({'messageid': str(message.id)})
                        embed = discord.Embed(title=f"Ticket #{ticket['ticket']}", color=0x4DC8E9)
                        embed.add_field(name="**Student:**", value=message.author.mention, inline=False)
                        embed.add_field(name="**Message link:**", value=f"https://discord.com/channels/799977201898487818/{channelsend.id}/{message.id}",inline=False)
                        embed.add_field(name="Strike:", value=strikes,inline=False)
                        embed.set_thumbnail(url=message.author.avatar_url)
                        embed.set_image(url="https://cdn.discordapp.com/attachments/847101178940227594/853527178737877012/Screenshot_2021-06-13_at_2.51.33_PM.png")
                        sent = await modlog.send(embed=embed)
                        await sent.add_reaction("<:NoCodez:800550542593097759>")
                        self.moderation.update_one({"messageid":str(message.id)},{"$set":{"modmsg":str(sent.id)}})
                        await message.author.add_roles(discord.utils.get(guild.roles, name="Detention")) 
                        set_time = datetime.now() + timedelta(hours=mutetime[strikes-1])
                        setting_time = format(set_time, '%H:%M')
                        mydict = {"mute" : str(message.author.id), "time" : setting_time}
                        self.moderation.insert_one(mydict)
                    else:
                        self.moderation.delete_one({"id" :str(message.author.id)})
                        ticket = self.moderation.find_one({'messageid': str(message.id)})
                        embed = discord.Embed(title=f"Ticket #{ticket['ticket']}", color=0x4DC8E9)
                        embed.add_field(name="**Student:**", value=message.author.mention,inline=False)
                        embed.add_field(name="**Message link:**", value=f"https://discord.com/channels/799977201898487818/{channelsend.id}/{message.id}",inline=False)
                        embed.add_field(name="Status:", value="banned!")
                        embed.set_thumbnail(url=message.author.avatar_url)
                        embed.set_image(url="https://cdn.discordapp.com/attachments/847101178940227594/853527181967097856/Screenshot_2021-06-13_at_2.51.50_PM.png")
                        sent = await modlog.send(embed=embed)
                        await sent.add_reaction("<:NoCodez:800550542593097759>")
                        self.moderation.update_one({"messageid":str(message.id)},{"$set":{"modmsg":str(sent.id)}})
                        embed = discord.Embed(description=f"{message.author.mention} has been banned!", color=0x4DC8E9)
                        await channelsend.send(embed=embed)
                        try:
                            await message.author.send("You have been banned by community moderation!")
                            await guild.ban(message.author, reason="not adiding by server rules")
                        except:
                            pass
                            await guild.ban(message.author, reason="not adiding by server rules")
            else:
                #embed = discord.Embed(description="One warn reaction has been placed on this message", color=0x4DC8E9)
                #await message.channel.send(embed=embed)
                await message.add_reaction("👍")
                ticket = self.moderation.find_one({"id":"true"})
                mydict = {"messageid" : str(payload.message_id), "modmsg" : "", "victim" : str(message.author.id), "ticket":str(int(ticket["ticket"])+1)}
                self.moderation.insert_one(mydict)
                self.moderation.update({"messageid" :str(payload.message_id)}, { "$set": { "tags": [str(payload.user_id)] }}, multi=True)
                self.moderation.update({"id" :"true"}, {"$set": { "ticket": ticket["ticket"]+1}})

    
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def approve(self, ctx, ticketnum):
        try:
            ticket = self.moderation.find_one({"ticket":ticketnum})
            message = await ctx.channel.fetch_message(int(ticket["modmsg"]))
            author = discord.utils.find(lambda m : m.id == int(ticket["victim"]), ctx.guild.members)
            print(author)
            ##await message.delete()
            self.moderation.delete_one({"ticket":(ticketnum)})
            embed = discord.Embed(title=f"**Ticket {ticketnum}** approved!", color=0x4DC8E9)
            embed.add_field(name="**Punished:**", value=author.mention, inline=False)
            embed.add_field(name="**ticket link:**", value=f"https://discord.com/channels/799977201898487818/{message.channel.id}/{message.id}", inline=False)
            await message.remove_reaction("<:NoCodez:800550542593097759>")
            embed.set_thumbnail(url=author.avatar_url)
            embed.set_image(url="https://cdn.discordapp.com/attachments/847101178940227594/853527181024297000/Screenshot_2021-06-13_at_2.52.03_PM.png")
            await ctx.channel.send(embed=embed)
        except:
            embed = discord.Embed(description=f"ticket {ticketnum} could not be approved!", color=0x4DC8E9)
            await ctx.send(embed=embed)


    @commands.command()
    @commands.has_permissions(administrator=True)
    async def cleartickets(self, ctx):
        ticketnum = self.moderation.find_one({"id":"true"})["ticket"]
        for i in range(ticketnum):
            test = self.moderation.find_one({"ticket":str(i+1)})
            if test != None:
                self.moderation.find_one({"ticket":str(i+1)})
        self.moderation.update_one({"id":"true"},{"$set":{"ticket":0}})
        embed = discord.Embed(description=f"**{ticketnum} tickets** have been cleared!", color=0x4DC8E9)
        await ctx.channel.send(embed=embed)

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def clearstrikes(self, ctx, member: discord.Member):
        self.moderation.delete_one({"id":str(member.id)})
        embed = discord.Embed(description=f"**{member.mention} strikes** have been cleared!", color=0x4DC8E9)
        await ctx.send(embed=embed)

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def setstrikes(self, ctx, member: discord.Member, num):
        person = self.moderation.find_one({"id":str(member.id)})
        if person != None:
            self.moderation.update_one({"id":str(member.id)}, {"$set":{"strikes":num}})
        else:
            mydict = {"id": str(ctx.message.author.id), "strikes": num, "member":"true"}
            self.moderation.insert_one(mydict)
        embed = discord.Embed(description=f"{member.mention} strikes set to {num}", color=0x4DC8E9)
        await ctx.send(embed=embed)

def setup(client):
    client.add_cog(commod(client))
