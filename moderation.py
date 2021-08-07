'''set thumbnail of the codez sensei for each mod message'''

import discord
import asyncio
from discord.ext import commands
from pymongo import MongoClient
from datetime import datetime, timedelta


class moderation(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.cluster = MongoClient("mongodb+srv://maxcodez:zbndxaPz1BNseBgl@cluster0.hqubn.mongodb.net/<dbname>?retryWrites=true&w=majority")
        self.db = self.cluster["discord"]
        self.info = self.db["info"]
        self.moderation = self.db["moderation"]
    
    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if (isinstance(error, commands.MissingRequiredArgument)):
            embed = discord.Embed(description=f"**{ctx.author.mention}** Argument missing", color=0x4DC8E9)
            await ctx.send(embed=embed)
        if isinstance(error, commands.MissingAnyRole):
            embed = discord.Embed(
                description=f"**{ctx.author.mention}** does not have enough power for this command.",
                color=0x4DC8E9)
            await ctx.send(embed=embed)
        if isinstance((error, commands.UserNotFound)):
            embed = discord.Embed(description=f"Hey I couldn't find student **{ctx.author.mention}**",
                                  color=0x4DC8E9)
            await ctx.send(embed=embed)

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def purge(self, ctx, arg: int):
        try:
            await ctx.channel.purge(limit=(int(arg) + 1))
        except discord.Forbidden:
            embed = discord.Embed(description=f"insufficient privelages to purge messages", color=0x4DC8E9)
            await ctx.send(embed=embed)
    
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def unban(self, ctx, arg: int):
        banned = await ctx.guild.bans()
        for entry in banned:
            if entry.user.id == arg:
                await ctx.guild.unban(entry.user)
                embed = discord.Embed(description=f"{entry.user.name} has been unbanned!", color=0x4DC8E9)
                await ctx.channel.send(embed=embed)
        

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason=None):
        try:
            await member.kick()
            embed = discord.Embed(description=f'I have kicked {member.mention}', color=0x4DC8E9)
            await ctx.send(embed=embed)
        except discord.Forbidden:
            embed = discord.Embed(description=f"insufficient privelages to kick {member.mention}", color=0x4DC8E9)
            await ctx.send(embed=embed)
    
    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.User = None, reason=None):
        try:
            if reason == None:
                reason = "Not abiding by server rules!"
            message = f"You have been banned from {ctx.guild.name} for {reason}"
            await ctx.guild.ban(member, reason=reason)
            embed = discord.Embed(description=f"{member.mention} was banned\nReason: {reason}", color=0x4DC8E9)
            await ctx.send(embed=embed)
            await member.send(message)
        except discord.Forbidden:
            embed = discord.Embed(description=f"Could not send a message to {member.mention}!!", color=0x4DC8E9)
            await ctx.send(embed=embed)
    
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def lockchannel(self, ctx):
        student = int(self.info.find_one({"name":"student"})["value"])
        await ctx.channel.set_permissions(ctx.guild.get_role(student), overwrite=discord.PermissionOverwrite(send_messages=False))
        embed = discord.Embed(description=f"Locking down channel!", color=0x4DC8E9)
        await ctx.send(embed=embed)
    
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def unlockchannel(self, ctx):
        student = int(self.info.find_one({"name":"student"})["value"])
        await ctx.channel.set_permissions(ctx.guild.get_role(student), overwrite=discord.PermissionOverwrite(send_messages=None))
        embed = discord.Embed(description=f"Unlocking channel!", color=0x4DC8E9)
        await ctx.send(embed=embed)
        
    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def slow(self, ctx, seconds: int):
        await ctx.channel.edit(slowmode_delay=seconds)
        embed = discord.Embed(description=f"Set the slowmode delay in this channel to {seconds} seconds", color=0x4DC8E9)
        await ctx.send(embed=embed)
    
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def setupmute(self, ctx, muterole):
        mute = discord.utils.get(ctx.guild.roles, name=muterole)
        for channel in ctx.guild.text_channels:
            await channel.set_permissions(mute, overwrite=discord.PermissionOverwrite(send_messages=False))
        for channel in ctx.guild.voice_channels:
            await channel.set_permissions(mute, overwrite=discord.PermissionOverwrite(speak=False))
        embed = discord.Embed(description=f"Mute role set up!", color=0x4DC8E9)
        await ctx.send(embed=embed)
    
    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def mute(self, ctx, member: discord.Member, duration, *, reason=None):
        unit = duration[-1]
        if unit == 'm':
            time = int(duration[:-1]) * 60
        elif unit == 'h':
            time = int(duration[:-1]) * 60 * 60
        else:
            await ctx.send('Invalid Unit! Use `m`, or `h`.')
            return None
        await member.add_roles(discord.utils.get(ctx.guild.roles, name="Detention"))
        embed = discord.Embed(description=f"{member.mention} muted for {duration}", color=0x4DC8E9)
        await ctx.send(embed=embed)

        set_time = datetime.now() + timedelta(seconds=time)
        setting_time = format(set_time, '%H:%M')
        print(setting_time)
        mydict = {"mute" : str(member.id), "time" : setting_time}
        self.moderation.insert_one(mydict)


    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def unmute(self, ctx, member: discord.Member):
        embed = discord.Embed(description=f"{member.mention} has been unmuted", color=0x4DC8E9)
        await ctx.send(embed=embed)
        self.moderation.delete_one({"mute":str(member.id)})
        await member.remove_roles(discord.utils.get(ctx.guild.roles, name="Detention"))


def setup(client):
    client.add_cog(moderation(client))
