import discord
import asyncio
from discord.ext import commands
import json
from datetime import datetime
import pymongo
from pymongo import MongoClient
from replit import db as banana

with open("data.json", "r") as datab:
    config = json.load(datab)
    logchannel = config["log_channel"]
    igchannels = config["ig_channels"]

class moderation(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.cluster = MongoClient("mongodb+srv://maxcodez:zbndxaPz1BNseBgl@cluster0.hqubn.mongodb.net/<dbname>?retryWrites=true&w=majority")
        self.db = self.cluster["discord"]
        self.warnsys = self.db["warns"]
        self.strikemod = self.db["modtrack"]
    
    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if (isinstance(error, commands.MissingRequiredArgument)):
            embed = discord.Embed(description=f"**{ctx.author.mention}** Argument missing!", color=0xb91919)
            await ctx.send(embed=embed)
        if isinstance(error, commands.MissingAnyRole):
            embed = discord.Embed(
                description=f"**{ctx.author.mention}** does not have the roles required for this command!",
                color=0xb91919)
            await ctx.send(embed=embed)
        if isinstance((error, commands.UserNotFound)):
            embed = discord.Embed(description=f"**{ctx.author.mention}** Could not find user mentioned!",
                                  color=0xb91919)
            await ctx.send(embed=embed)

    @commands.command()
    @commands.has_any_role("Moderator", "admin", "MaxCodez")
    async def purge(self, ctx, arg: int):
        try:
            await ctx.channel.purge(limit=(int(arg) + 1))
            embed = discord.Embed(description=f"{arg} messages purged, sending something bad eh :laughing:",
                                  color=0xb91919)
            await ctx.send(embed=embed)
        except discord.Forbidden:
            embed = discord.Embed(description=f"insufficient privelages to purge messages", color=0xb91919)
            await ctx.send(embed=embed)
        modlog = discord.utils.get(ctx.guild.channels, id=int(logchannel))
        embed = discord.Embed(
            description="{0} purged **{1}** messages in {2}".format(ctx.author.mention, arg , ctx.channel),
            color=0xb91919)
        await modlog.send(embed=embed)

    @commands.command()
    @commands.has_any_role("Moderator", "admin", "MaxCodez")
    async def kick(self, ctx, member: discord.Member, *, reason=None):
        maxrole = discord.utils.get(ctx.guild.roles, name="MaxCodez")
        modrole = discord.utils.get(ctx.guild.roles, name="Moderator")
        senrole = discord.utils.get(ctx.guild.roles, name="Senior Mods")
        if (maxrole in ctx.author.roles) or (modrole not in member.roles) or (senrole in ctx.author.roles):
            try:
                await member.kick()
                embed = discord.Embed(description=f'User {member.mention} has been kicked', color=0xb91919)
                await ctx.send(embed=embed)
                modlog = discord.utils.get(ctx.guild.channels, id=int(logchannel))
                await modlog.send(embed=embed)
            except discord.Forbidden:
                embed = discord.Embed(description=f"insufficient privelages to kick {member.mention}", color=0xb91919)
                await ctx.send(embed=embed)
        else:
            embed = discord.Embed(description=f"Hey! Not Cool!", color=0xb91919)
            await ctx.channel.send(embed=embed)

    @commands.command()
    @commands.has_any_role("Moderator", "admin", "MaxCodez")
    async def ban(self, ctx, member: discord.Member = None, reason=None):
        maxrole = discord.utils.get(ctx.guild.roles, name="MaxCodez")
        modrole = discord.utils.get(ctx.guild.roles, name="Moderator")
        senrole = discord.utils.get(ctx.guild.roles, name="Senior Mods")
        if (maxrole in ctx.author.roles) or (modrole not in member.roles) or (senrole in ctx.author.roles):
            try:
                if reason == None:
                    reason = "Not abiding by server rules!"
                message = f"You have been banned from {ctx.guild.name} for {reason}"
                await ctx.guild.ban(member, reason=reason)
                embed = discord.Embed(description=f"{member.mention} was banned\nReason: {reason}", color=0xb91919)
                await ctx.send(embed=embed)
                await member.send(message)
                modlog = discord.utils.get(ctx.guild.channels, id=int(logchannel))
                await modlog.send(embed=embed)
            except discord.Forbidden:
                embed = discord.Embed(description=f"Could not send message to {member.mention}!!", color=0xb91919)
                await ctx.send(embed=embed)
        else:
            embed = discord.Embed(description=f"Hey! Not Cool!", color=0xb91919)
            await ctx.channel.send(embed=embed)
            

    @commands.command()
    @commands.has_any_role("Senior Mods", "admin", "MaxCodez")
    async def lockchannel(self, ctx):
        embed = discord.Embed(description=f"Locking down channel!", color=0xb91919)
        await ctx.send(embed=embed)
        await ctx.channel.set_permissions(ctx.guild.get_role(731130377917169708), overwrite=discord.PermissionOverwrite(send_messages=False))

    @commands.command()
    @commands.has_any_role("Senior Mods", "admin", "MaxCodez")
    async def unlockchannel(self, ctx):
        embed = discord.Embed(description=f"Unlocking channel!", color=0xb91919)
        await ctx.send(embed=embed)
        await ctx.channel.set_permissions(ctx.guild.get_role(731130377917169708), overwrite=discord.PermissionOverwrite(send_messages=None))

    @commands.command()
    @commands.has_any_role("MaxCodez")
    async def lockdown(self, ctx):
        server = ctx.guild
        embed = discord.Embed(description=f"Locking down {server.name}", color=0xb91919)
        await ctx.send(embed=embed)
        for channel in server.channels:
            if channel.id not in igchannels:
                await channel.set_permissions(ctx.guild.default_role, send_messages=False)

    @commands.command()
    @commands.has_any_role("MaxCodez")
    async def unlockdown(self, ctx):
        server = ctx.guild
        embed = discord.Embed(description=f"Unlocking {server.name}", color=0xb91919)
        await ctx.send(embed=embed)
        for channel in server.channels:
            await channel.set_permissions(ctx.guild.default_role, send_messages=None)

    @commands.command()
    @commands.has_any_role("Moderator","admin", "MaxCodez")
    async def slow(self, ctx, seconds: int):
        await ctx.channel.edit(slowmode_delay=seconds)
        await ctx.send(f"Set the slowmode delay in this channel to {seconds} seconds!")
    
    @commands.command()
    @commands.has_any_role("Trainee mod", "Moderator", "admin", "MaxCodez")
    async def warn(self, ctx, member: discord.Member, *, reason=None):
        maxrole = discord.utils.get(ctx.guild.roles, name="MaxCodez")
        modrole = discord.utils.get(ctx.guild.roles, name="Moderator")
        senrole = discord.utils.get(ctx.guild.roles, name="Senior Mods")
        if maxrole in ctx.author.roles or (modrole not in member.roles) or (senrole in ctx.author.roles):
            now = datetime.now()
            date = now.strftime("%m/%d/%Y")
            warns = self.warnsys.find_one({"id":member.id})
            if warns is None:
                mydict = {"id": member.id, "warnings": reason, "dates":date, "personel":f"{ctx.author.id}"}
                self.warnsys.insert_one(mydict)
            else:
                tempwarn = warns["warnings"]
                tempdates = warns["dates"]
                temppersonel = warns["personel"]
                person = str(ctx.author.id)
                self.warnsys.update_one({"id":member.id}, {"$set":{"warnings":tempwarn+","+reason, "dates":tempdates+","+date, "personel":temppersonel+","+person}})
            embed = discord.Embed(title=f"Warn", description=f"{member.mention} has been warned in {ctx.guild.name}",color=0xb91919)
            embed.add_field(name="Date", value=date, inline=True)
            embed.add_field(name="Moderator", value=ctx.author.mention, inline=True)
            embed.add_field(name="Reason", value=reason, inline=False)
            embed.set_thumbnail(url=member.avatar_url)
            await ctx.send(embed=embed)
            await member.send(embed=embed)
        else:
            embed = discord.Embed(description=f"Hey! Not Cool!", color=0xb91919)
            await ctx.channel.send(embed=embed)


    @commands.command()
    @commands.has_any_role("Trainee mod", "Moderator", "admin", "MaxCodez")
    async def getwarns(self, ctx, member: discord.Member):
        try:
            warn = self.warnsys.find_one({"id":member.id})
            embed = discord.Embed(title=f"Warn logs", description=f"{member.mention} warns:", color=0xb91919)
            warns = warn["warnings"].split(",")
            date = warn["dates"].split(",")
            mod = warn["personel"].split(",")
            print(warns, date, mod)
            for i in range(len(warns)):
                try:
                    currmod = ctx.guild.get_member(int(mod[i]))
                    embed.add_field(name=f"Warn {i+1}:", value=f'''
                    date: {date[i]}
                    Mod: {currmod.mention}
                    Warn: {warns[i]}
                    ''', inline=False)
                except:
                    pass      
        except:
            embed = discord.Embed(description="No warns!", color=0xb91919)
        await ctx.send(embed=embed)
    
    @commands.command()
    @commands.has_any_role("Senior Mods", "MaxCodez")
    async def clearwarns(self, ctx, member: discord.Member):
        warn = self.warnsys.find_one({"id":member.id})
        self.warnsys.delete_one(warn)
        embed = discord.Embed(description=f"{member.mention} warns cleared!", color=0xb91919)
        await ctx.send(embed=embed)
    
    @commands.command()
    @commands.has_any_role("MaxCodez")
    async def setupmute(self, ctx):
        mute = discord.utils.get(ctx.guild.roles, name="mute")
        for channel in ctx.guild.text_channels:
            await channel.set_permissions(mute, overwrite=discord.PermissionOverwrite(send_messages=False))
        for channel in ctx.guild.voice_channels:
            await channel.set_permissions(mute, overwrite=discord.PermissionOverwrite(speak=False))
              
        embed = discord.Embed(description=f"Mute role set up!", color=0xb91919)
        await ctx.send(embed=embed)

    @commands.command()
    @commands.has_any_role("Trainee mod", "Moderator", "MaxCodez")
    async def mute(self, ctx, member: discord.Member, duration, *, reason=None):
        maxrole = discord.utils.get(ctx.guild.roles, name="MaxCodez")
        modrole = discord.utils.get(ctx.guild.roles, name="Moderator")
        senrole = discord.utils.get(ctx.guild.roles, name="Senior Mods")
        if (maxrole in ctx.author.roles) or (modrole not in member.roles) or (senrole in ctx.author.roles):
            banana["m"+str(member.id)] = "yes"
            unit = duration[-1]
            if unit == 's':
                time = int(duration[:-1])
                longunit = 'seconds'
            elif unit == 'm':
                time = int(duration[:-1]) * 60
                longunit = 'minutes'
            elif unit == 'h':
                time = int(duration[:-1]) * 60 * 60
                longunit = 'hours'
            else:
                await ctx.send('Invalid Unit! Use `s`, `m`, or `h`.')
                return
            await member.add_roles(discord.utils.get(ctx.guild.roles, name="mute"))
            embed = discord.Embed(description=f"{member.mention} muted for {duration}", color=0xb91919)
            await ctx.send(embed=embed)
            await asyncio.sleep(time)
            await member.remove_roles(discord.utils.get(ctx.guild.roles, name="mute"))
            del banana["m" + str(member.id)]
        else:
            embed = discord.Embed(description=f"Hey! Not Cool!", color=0xb91919)
            await ctx.channel.send(embed=embed)
            
    @commands.command()
    @commands.has_any_role("MaxCodez", "Server Admin")
    async def unmute(self, ctx, member: discord.Member):
        await member.remove_roles(discord.utils.get(ctx.guild.roles, name="mute"))
        embed = discord.Embed(description=f"{member.mention} unmuted", color=0xb91919)
        await ctx.send(embed=embed)
        del banana["m" + str(member.id)]
    
    
    
    @commands.command()
    @commands.has_any_role("Trainee mod", "Moderator", "MaxCodez")
    async def report(self, ctx, *, args):
        banana = ctx.author.mention + ": " + args
        print(banana)
        modlog = discord.utils.get(ctx.guild.channels, id=int(792761089125384263))
        embed = discord.Embed(description="Mod mail sent!", color=0xb91919)
        await ctx.send(embed=embed)

        now = datetime.now()
        date = now.strftime("%m/%d/%Y")
        embed = discord.Embed(title=f"Report", description=f"{args}",color=0xb91919)
        embed.add_field(name="Date", value=date, inline=True)
        embed.add_field(name="Reporter: ", value=ctx.author.mention, inline=True)
        embed.set_thumbnail(url=ctx.author.avatar_url)
        await modlog.send(embed=embed)
    
    @commands.command()
    @commands.has_any_role("Senior Mods", "MaxCodez")
    async def strike(self, ctx, member: discord.Member, *, reason=None):
        modlog = discord.utils.get(ctx.guild.channels, id=int(792761089125384263))
        now = datetime.now()
        date = now.strftime("%m/%d/%Y")
        modrole = discord.utils.get(ctx.guild.roles, name="Moderator")
        if modrole not in member.roles:
            embed = discord.Embed(description=f"{member.mention} not a mod!")
            await ctx.send(embed=embed)
            return None
        strikes = self.strikemod.find_one({"id":member.id})
        if strikes is None:
            mydict = {"id": member.id, "reasons": reason, "dates":date, "personel":f"{ctx.author.id}"}
            self.strikemod.insert_one(mydict)
            count = []
        else:
            tempreasons = strikes["reasons"]
            count = tempreasons.split(",")
            tempdates = strikes["dates"]
            temppersonel = strikes["personel"]
            person = str(ctx.author.id)
            self.strikemod.update_one({"id":member.id}, {"$set":{"reasons":tempreasons+","+reason, "dates":tempdates+","+date, "personel":temppersonel+","+person}}) 
        embed = discord.Embed(title=f"Strike", description=f"{member.mention} has been striked in {ctx.guild.name}")
        embed.add_field(name="Date", value=date, inline=True)
        embed.add_field(name="Senior", value=ctx.author.mention, inline=True)
        embed.add_field(name="Number of strikes", value=len(count)+1, inline=False)
        embed.add_field(name="Reason", value=reason, inline=False)
        embed.set_thumbnail(url=member.avatar_url)
        await ctx.send(embed=embed)
        await modlog.send(embed=embed)

        if len(count)+1 >= 3:
            print("kick time")
            embed = discord.Embed(description=f"{member.mention} has been demoted! :(")
            await ctx.channel.send(embed=embed)
            await member.remove_roles(discord.utils.get(ctx.guild.roles, name="Moderator"))
        await member.send(embed=embed)
        await member.send(embed=embed)
    
    @commands.command()
    @commands.has_any_role("Senior Mods", "MaxCodez")
    async def getstrikes(self, ctx, member: discord.Member):
        try:
            strikes = self.strikemod.find_one({"id":member.id})
            embed = discord.Embed(title=f"Strike logs", description=f"{member.mention} strikes:")
            strike = strikes["reasons"].split(",")
            date = strikes["dates"].split(",")
            mod = strikes["personel"].split(",")
            print(strike, date, mod)
            for i in range(len(strike)):
                try:
                    currmod = ctx.guild.get_member(int(mod[i]))
                    embed.add_field(name=f"Warn {i+1}:", value=f'''
                    date: {date[i]}
                    Mod: {currmod.mention}
                    Reason: {strike[i]}
                    ''', inline=False)
                except:
                    pass      
        except:
            embed = discord.Embed(description="No strikes!")
        await ctx.send(embed=embed)
    
    @commands.command()
    @commands.has_any_role("Senior Mods", "MaxCodez")
    async def promote(self, ctx, member: discord.Member): 
        modrole = discord.utils.get(ctx.guild.roles, name="Moderator")
        trainrole = discord.utils.get(ctx.guild.roles, name="Trainee mod")
        if trainrole in member.roles:
            await member.add_roles(discord.utils.get(ctx.guild.roles, name="Moderator"))
            await member.remove_roles(discord.utils.get(ctx.guild.roles, name="Trainee mod"))
        elif (modrole not in member.roles) and (trainrole not in member.roles):
            await member.add_roles(discord.utils.get(ctx.guild.roles, name="Trainee mod"))
        embed = discord.Embed(description=f"{member.mention} has been promoted!")
        await ctx.channel.send(embed=embed)
    
    @commands.command()
    @commands.has_any_role("Senior Mods", "MaxCodez")
    async def demote(self, ctx, member: discord.Member): 
        modrole = discord.utils.get(ctx.guild.roles, name="Moderator")
        trainrole = discord.utils.get(ctx.guild.roles, name="Trainee mod")
        if trainrole in member.roles:
            await member.remove_roles(discord.utils.get(ctx.guild.roles, name="Trainee mod"))
            embed = discord.Embed(description=f"{member.mention} has been demoted :(((")
            await ctx.channel.send(embed=embed)
            return None
        if modrole in member.roles:
            await member.add_roles(discord.utils.get(ctx.guild.roles, name="Trainee mod"))
            await member.remove_roles(discord.utils.get(ctx.guild.roles, name="Moderator"))
            embed = discord.Embed(description=f"{member.mention} has been demoted :(((")
            await ctx.channel.send(embed=embed)
            return None
        
    
    @commands.command()
    @commands.has_any_role("Trainee mod", "Moderator","Senior Mods", "MaxCodez")
    async def onduty(self, ctx):
        await ctx.author.edit(nick="[On Duty] "+ ctx.author.name)
        embed = discord.Embed(description=f"{ctx.author.mention} is set to on duty!")
        await ctx.channel.send(embed=embed)

    @commands.command()
    @commands.has_any_role("Trainee mod", "Moderator", "admin", "MaxCodez")
    async def offduty(self, ctx):
        await ctx.author.edit(nick="[Off Duty] "+ ctx.author.name)
        embed = discord.Embed(description=f"{ctx.author.mention} is set to off duty!")
        await ctx.channel.send(embed=embed)
    
    @commands.command()
    @commands.has_any_role("Trainee mod", "Moderator", "admin", "MaxCodez")
    async def lurking(self, ctx):
        await ctx.author.edit(nick="[Lurking] "+ ctx.author.name)
        embed = discord.Embed(description=f"{ctx.author.mention} is set to sneaky sneaky hehe!")
        await ctx.channel.send(embed=embed)

def setup(client):
    client.add_cog(moderation(client))
