import discord
from discord.ext import commands
import random
import asyncio
from pymongo import MongoClient


class python_challenges(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.houses = ["Selenium", "PyautoGUI", "NumPy", "DateTime"]
        self.cluster = MongoClient(
            "mongodb+srv://maxcodez:zbndxaPz1BNseBgl@cluster0.hqubn.mongodb.net/<dbname>?retryWrites=true&w=majority")
        self.db = self.cluster["discord"]
        self.dailychallenge = self.db["dailychallenge"]

    @commands.command()
    @commands.has_any_role("Moderator", "MaxCodez", "Python Challenge Manager")
    async def sortinghat(self, ctx, member: discord.Member):
        embed = discord.Embed(description=f"Hm I'm thinking... 🎩", color=0xb91919)
        await ctx.channel.send(embed=embed)
        await asyncio.sleep(2)
        sel = 0
        pyau = 0
        nump = 0
        datet = 0
        selrole = discord.utils.get(ctx.guild.roles, name="Selenium")
        pyaurole = discord.utils.get(ctx.guild.roles, name="PyautoGUI")
        numprole = discord.utils.get(ctx.guild.roles, name="NumPy")
        daterole = discord.utils.get(ctx.guild.roles, name="DateTime")
        for members in ((ctx.guild.members)):
            if selrole in members.roles:
                sel += 1
            if pyaurole in members.roles:
                pyau +=1
            if numprole in members.roles:
                nump +=1
            if daterole in members.roles:
                datet +=1
        X = min(sel, pyau, nump, datet)
        print(X)
        if X == sel:
            selected = "Selenium"
        elif X == pyau:
            selected = "PyautoGUI"
        elif X == nump:
            selected = "NumPy"
        elif X == datet:
            selected = "DateTime"
        
        #selected = random.choice(self.houses)
        await member.add_roles(discord.utils.get(ctx.guild.roles, name=selected))
        embed = discord.Embed(description=f"Your house is **{selected}**! Please read through <#788171135136825364>!",
                              color=0xb91919)
        await ctx.channel.send(embed=embed)
        temprole = discord.utils.get(ctx.guild.roles, name=selected)
        commch = discord.utils.get(ctx.guild.channels, id=int(788779357829070849))
        embed = discord.Embed(description=f"**{member.mention}** is joining {selected}!!! Please give him a big welcome {temprole.mention}",color=0xb91919)
        await commch.send(embed=embed)

    @commands.command()
    async def teaminfo(self, ctx):
        for roles in ctx.author.roles:
            if str(roles) in self.houses:
                house = str(roles)
        teammembers = []
        selrole = discord.utils.get(ctx.guild.roles, name=house)
        for members in (ctx.guild.members):
            if selrole in members.roles:
                teammembers.append(members.mention)
        stats = self.dailychallenge.find_one({"team": house})
        points = stats["points"]
        rank = 0
        rankings = self.dailychallenge.find().sort("points",-1)
        for x in rankings:
            rank += 1
            if x["team"] == house:
                break
        embed = discord.Embed(title="Team {} stats".format(house), description="")
        embed.add_field(name="Points", value=f"{points}", inline=True)
        embed.add_field(name="Rank", value=f"{rank}/4", inline=True)
        print("still ok")
        for i in range(len(teammembers)):
            embed.add_field(name=f"Member: {i+1}", value=f"{teammembers[i]}", inline=False)
        await ctx.channel.send(embed=embed)



    @commands.command()
    async def submit(self, ctx, answer):
        house = ""
        embed = discord.Embed(description=f"let me check the database!", color=0xb91919)
        await ctx.channel.send(embed=embed)
        await asyncio.sleep(2)
        ans = self.dailychallenge.find_one({"answer": answer})
        for roles in ctx.author.roles:
            if str(roles) in self.houses:
                house = str(roles)
                print("YESSS")
        if ans is None:
            embed = discord.Embed(description=f"Sorry bud, but this is incorrect :( 🐠", color=0xb91919)
            await ctx.channel.send(embed=embed)
        else:
            if ans[house] == "False":
                    stats = self.dailychallenge.find_one({"team": house})
                    self.dailychallenge.update_one({"dailychallenge": "True"}, {"$set": {house: "True"}})
                    if stats is None:
                        mydict = {"team": house, "points": 1}
                        self.dailychallenge.insert_one(mydict)
                        embed = discord.Embed(description=f"WHATTTT YOU GOT IT RIGHT!? 🐠. Your team has **1** points",
                                              color=0xb91919)
                    else:
                        points = stats["points"]
                        temppoints = 5
                        stats2 = self.dailychallenge.find_one({"dailychallenge": "True"})
                        if stats2["Selenium"] == "True":
                            temppoints -= 1
                        if stats2["PyautoGUI"] == "True":
                            temppoints -= 1
                        if stats2["NumPy"] == "True":
                            temppoints -= 1
                        if stats2["DateTime"] == "True":
                            temppoints -= 1
                        self.dailychallenge.update_one({"team": house}, {"$set": {"points": stats["points"] + temppoints}})
                        embed = discord.Embed(description=f"WHATTTT YOU GOT IT RIGHT!? 🐠. Your team has **{points+temppoints}** points",color=0xb91919)
                    await ctx.channel.send(embed=embed)
            else:
                embed = discord.Embed(description=f"Your house has already got its point for today! 🐠", color=0xb91919)
                await ctx.channel.send(embed=embed)

    @commands.command()
    @commands.has_any_role("Moderator", "MaxCodez", "Python Challenge Manager")
    async def setquestion(self, ctx, answer, *args):
        stats = self.dailychallenge.find_one({"dailychallenge": "True"})
        self.dailychallenge.delete_one(stats)
        question = ' '.join(args)
        mydict = {"dailychallenge": "True", "question": question, "answer": answer, "Selenium": "False",
                  "PyautoGUI": "False", "NumPy": "False", "DateTime": "False"}
        self.dailychallenge.insert_one(mydict)
        embed = discord.Embed(title="Question set", description="")
        embed.add_field(name="Question:", value=question, inline=False)
        embed.add_field(name="Answer:", value=answer, inline=False)
        embed.set_thumbnail(url=ctx.author.avatar_url)
        await ctx.channel.send(embed=embed)

    @commands.command()
    @commands.has_any_role("MaxCodez", "Python Challenge Manager")
    async def challengeinfo(self, ctx):
        completed = 0
        stats = self.dailychallenge.find_one({"dailychallenge": "True"})
        embed = discord.Embed(title="Challenge info", description="")
        embed.add_field(name="Question:", value=stats["question"], inline=False)
        embed.add_field(name="Answer:", value=stats["answer"], inline=False)
        if stats["Selenium"] == "True":
            completed += 1
        if stats["PyautoGUI"] == "True":
            completed += 1
        if stats["NumPy"] == "True":
            completed += 1
        if stats["DateTime"] == "True":
            completed += 1
        embed.add_field(name="Selenium:", value=stats["Selenium"], inline=True)
        embed.add_field(name="PyautoGUI:", value=stats["PyautoGUI"], inline=True)
        embed.add_field(name="NumPy:", value=stats["NumPy"], inline=True)
        embed.add_field(name="DateTime:", value=stats["DateTime"], inline=True)
        ##embed.add_field(name="Teams completed: ",value=2*completed * "️️:blue_square:" + (8 - (2*completed)) * ":white_large_square:", inline=False)
        await ctx.channel.send(embed=embed)


    @commands.command()
    async def teamleaderboard(self, ctx):
        rankings = self.dailychallenge.find().sort("points",-1)
        i = 1
        embed = discord.Embed(title="Team rankings:", description="")
        for x in rankings:
            try:
                tempteam = x["team"]
                temppoint = x["points"]
                embed.add_field(name=f"{i}: {tempteam}", value=f"Points: {temppoint}", inline=False)
                i += 1
            except:
                pass
        await ctx.channel.send(embed=embed)

    @commands.command()
    @commands.has_any_role("Moderator", "MaxCodez", "Python Challenge Manager")
    async def setteampoints(self, ctx, member: discord.Member, points):
        for roles in member.roles:
            if str(roles) in self.houses:
                house = str(roles)
        self.dailychallenge.update_one({"team": house}, {"$set": {"points": int(points)}})
        embed = discord.Embed(description=f"**{house}** points have been set to {points}! 🐠", color=0xb91919)
        await ctx.channel.send(embed=embed)

def setup(client):
    client.add_cog(python_challenges(client))
