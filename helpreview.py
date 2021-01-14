import discord
from discord.ext import commands
import pymongo
from pymongo import MongoClient
##make sure only useable in certain rooms? check if python helper!!

class helperstats(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.cluster = MongoClient("mongodb+srv://maxcodez:zbndxaPz1BNseBgl@cluster0.hqubn.mongodb.net/<dbname>?retryWrites=true&w=majority")
        self.db = self.cluster["discord"]
        self.helpsys = self.db["helpsys"]

    @commands.command()
    async def givestar(self, ctx, member: discord.User):
        stats = self.helpsys.find_one({"id":member.id})
        if stats is None:
            mydict = {"id": member.id, "stars": 1}
            self.helpsys.insert_one(mydict)
        else:
            self.helpsys.update_one({"id":member.id}, {"$set":{"stars":stats["stars"]+1}})
        embed = discord.Embed(description=f"star given to {member.mention}! ⭐️", color=0xb91919)
        await ctx.channel.send(embed=embed)
    
    @commands.has_any_role("MaxCodez")
    @commands.command()
    async def setstar(self, ctx, member: discord.User, num: int):
        stats = self.helpsys.find_one({"id":member.id})
        if stats is None:
            mydict = {"id": member.id, "stars": num}
            self.helpsys.insert_one(mydict)
        else:
            self.helpsys.update_one({"id":member.id}, {"$set":{"stars":num}})
        embed = discord.Embed(description=f"stars set for {member.mention}! ⭐️", color=0xb91919)
        await ctx.channel.send(embed=embed)

    @commands.command()
    @commands.has_any_role("Moderator","MaxCodez")
    async def removestar(self, ctx, member: discord.User):
        stats = self.helpsys.find_one({"id":member.id})
        if stats is None:
            embed = discord.Embed(description=f"{member.mention} is not a python helper! :( ⭐️", color=0xb91919)
        else:
            newstar = stats["stars"]-1
            self.helpsys.update_one({"id":member.id}, {"$set":{"stars":newstar}})
            embed = discord.Embed(description=f"star removed from {member.mention}:( ⭐️", color=0xb91919)
        await ctx.channel.send(embed=embed)

    @commands.command()
    @commands.has_any_role("Python helper", "Moderator", "MaxCodez")
    async def helpstats(self, ctx):
        stats = self.helpsys.find_one({"id":ctx.author.id})
        if stats is None:
            embed = discord.Embed(description=f"Does not exist! :( ⭐️", color=0xb91919)
            await ctx.channel.send(embed=embed)
        else:
            embed = discord.Embed(title="{}'s help stats".format(ctx.author.name), description="")
            embed.add_field(name="Name", value=ctx.author.mention, inline=True)
            embed.add_field(name="Helped: ", value=stats["stars"], inline=True)
            embed.set_thumbnail(url=ctx.author.avatar_url)
            await ctx.channel.send(embed=embed)

    @commands.command()
    @commands.has_any_role("Python helper", "Moderator",  "MaxCodez")
    async def gethelpstats(self, ctx, member:discord.Member = None):
        stats = self.helpsys.find_one({"id":member.id})
        if stats is None:
            embed = discord.Embed(description=f"Does not exist! :( ⭐️", color=0xb91919)
            await ctx.channel.send(embed=embed)
        else:
            embed = discord.Embed(title="{}'s help stats".format(member.name), description="")
            embed.add_field(name="Name", value=member.mention, inline=True)
            embed.add_field(name="Helped: ", value=stats["stars"], inline=True)
            embed.set_thumbnail(url=member.avatar_url)
            await ctx.channel.send(embed=embed)

    @commands.command()
    @commands.has_any_role("MaxCodez")
    async def purgehelpers(self, ctx):
        removed = []
        rankings = self.helpsys.find().sort("stars",-1)
        for x in rankings:
            if x["stars"] < 2:
                member = ctx.guild.get_member(x["id"])
                await member.remove_roles(discord.utils.get(ctx.guild.roles, name="Python helper"))
                await member.send("You have been removed as a python helper due to inactivity")
                self.helpsys.delete_one(x)
                removed.append(member.name)
        await ctx.send(f"Removed: {removed}")

    @commands.command()
    @commands.has_any_role("MaxCodez", "Moderator")
    async def falseassign(self, ctx, member: discord.Member):
        stats = self.helpsys.find_one({"id":member.id})
        self.helpsys.delete_one(stats)
        embed = discord.Embed(
            description=f"{member.mention} has been removed as a python helper for abusing the star system :((",
            color=0xb91919)
        await ctx.channel.send(embed=embed)
        await member.remove_roles(discord.utils.get(ctx.guild.roles, name="Python helper"))
        await member.send("You have been removed as a python helper due to false assignment")

    @commands.command()
    @commands.has_any_role("Python helper", "Moderator", "MaxCodez")
    async def helpleaderboard(self, ctx):
        rankings = self.helpsys.find().sort("stars",-1)
        i = 1
        embed = discord.Embed(title="Help Rankings:", color=0x397882)
        for x in rankings:
            try:
                temp = ctx.guild.get_member(x["id"])
                print(temp.name)
                temphelped = x["stars"]
                embed.add_field(name=f"{i}: {temp.name}", value=f"Helped: {temphelped}",inline=False)
                i = i + 1
            except:
                pass
            if i == 10:
                break
        await ctx.channel.send(embed=embed)

def setup(client):
    client.add_cog(helperstats(client))
