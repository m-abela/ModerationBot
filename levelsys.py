import json
import discord
from discord.ext import commands
from pymongo import MongoClient

with open("data.json", "r") as db:
    config = json.load(db)
    bot_channel = config["bot_channel"]
    talk_channels = config["talk_channels"]
    monthly_leaderboard = config['monthly_leaderboard']
    noranks = config['noranks']

level = ["MaxCodez Kouhai", "MaxCodez Senpai", "Peak Programmer"]
levelnum = [5,10,15]

class levelling(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.cluster = MongoClient("mongodb+srv://maxcodez:zbndxaPz1BNseBgl@cluster0.hqubn.mongodb.net/<dbname>?retryWrites=true&w=majority")
        self.db = self.cluster["discord"]
        self.levelling = self.db["levelling"]

    ##dont allow levelling for some
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.channel.id in talk_channels:
            stats = self.levelling.find_one({"id":message.author.id})
            if message.author.id not in noranks:
                if stats is None:
                    mydict = {"id": message.author.id, "xp": 100}
                    self.levelling.insert_one(mydict)
                else:
                    self.levelling.update_one({"id":message.author.id}, {"$set":{"xp":stats["xp"]+5}})
                    xp = stats["xp"]+5
                    lvl = 0
                    while True:
                        if xp < ((50*(lvl**2))+(50*lvl)):
                            #lvl -= 1
                            break
                        lvl += 1
                    xp -= ((50 * ((lvl-1) ** 2)) + (50 * (lvl-1)))
                    if xp == 0:
                        await message.channel.send(f"Well done {message.author.mention}! You leveled up to **level: {lvl}**")
                        for i in range(len(level)):
                            if lvl == levelnum[i]:
                                await message.author.add_roles(discord.utils.get(message.author.guild.roles, name=level[i]))
                                embed = discord.Embed(
                                description=f"{message.author.mention} you have gotten role **{level[i]}**!!!", color=0xb91919)
                                embed.set_thumbnail(url=message.author.avatar_url)
                                await message.channel.send(embed=embed)

    @commands.command()
    async def rank(self, ctx):
      if ctx.channel.id == bot_channel:
          stats = self.levelling.find_one({"id":ctx.author.id})
          if stats is None:
              embed = discord.Embed(description=f"You haven't sent any messages in #general, no rank!",
                                  color=0xb91919)
              await ctx.channel.send(embed=embed)
          else:
              xp = stats["xp"]
              lvl = 0
              rank = 0
              while True:
                  if xp < ((50*(lvl**2))+(50*lvl)):
                      #lvl -= 1
                      break
                  lvl += 1
              xp -= ((50 * ((lvl-1) ** 2)) + (50 * (lvl-1)))
              boxes = int((xp / (200 * ((1 / 2) * (lvl))) * 20))
              rankings = self.levelling.find().sort("xp",-1)

              for x in rankings:
                rank += 1
                if stats["id"] == (x["id"]):
                  break

              embed = discord.Embed(title="{}'s level stats".format(ctx.author.name), description="")
              embed.add_field(name="Name", value=ctx.author.mention, inline=True)
              embed.add_field(name="XP", value=f"{xp}/{int(200 * ((1 / 2) * lvl))}", inline=True)
              embed.add_field(name="Level", value=lvl, inline=True)
              embed.add_field(name="Rank", value=f"{rank}/{ctx.guild.member_count}", inline=True)
              embed.add_field(name="Progress Bar [lvl]",
                              value=boxes * "️️:blue_square:" + (20 - boxes) * ":white_large_square:", inline=False)
              embed.set_thumbnail(url=ctx.author.avatar_url)
              await ctx.channel.send(embed=embed)

    @commands.command()
    async def getrank(self, ctx, member: discord.User):
      if ctx.channel.id == bot_channel:
          stats = self.levelling.find_one({"id":member.id})
          if stats is None:
              embed = discord.Embed(description=f"You haven't sent any messages in #general, no rank!",
                                  color=0xb91919)
              await ctx.channel.send(embed=embed)
          else:
              xp = stats["xp"]
              lvl = 0
              rank = 0
              while True:
                  if xp < ((50*(lvl**2))+(50*lvl)):
                      #lvl -= 1
                      break
                  lvl += 1
              xp -= ((50 * ((lvl-1) ** 2)) + (50 * (lvl-1)))
              boxes = int((xp / (200 * ((1 / 2) * (lvl))) * 20))
              rankings = self.levelling.find().sort("xp",-1)

              for x in rankings:
                rank += 1
                if stats["id"] == (x["id"]):
                  break

              embed = discord.Embed(title="{}'s level stats".format(member.name), description="")
              embed.add_field(name="Name", value=member.mention, inline=True)
              embed.add_field(name="XP", value=f"{xp}/{int(200 * ((1 / 2) * lvl))}", inline=True)
              embed.add_field(name="Level", value=lvl, inline=True)
              embed.add_field(name="Rank", value=f"{rank}/{ctx.guild.member_count}", inline=True)
              embed.add_field(name="Progress Bar [lvl]",
                              value=boxes * "️️:blue_square:" + (20 - boxes) * ":white_large_square:", inline=False)
              embed.set_thumbnail(url=member.avatar_url)
              await ctx.channel.send(embed=embed)
              
    @commands.command()
    async def dashboard(self, ctx):
        if (ctx.channel.id == bot_channel) or (ctx.channel.id == monthly_leaderboard):
            rankings = self.levelling.find().sort("xp",-1)
            i = 1
            embed = discord.Embed(title="Rankings:", color=0x397882)
            for x in rankings:
                try:
                    temp = ctx.guild.get_member(x["id"])
                    tempxp = x["xp"]
                    embed.add_field(name=f"{i}: {temp.name}", value=f"Total XP: {tempxp}", inline=False)
                    i +=1
                except:
                    print("gg")
                if i == 10:
                  break
            await ctx.channel.send(embed=embed)

    @commands.has_any_role("MaxCodez")
    @commands.command()
    async def clearlevels(self, ctx):
        peakpro = discord.utils.get(ctx.guild.roles, name="Peak Programmer")
        senpai = discord.utils.get(ctx.guild.roles, name="MaxCodez Senpai")
        kouhai = discord.utils.get(ctx.guild.roles, name="MaxCodez Kouhai")
        async for members in ctx.guild.fetch_members(limit=None):
            if peakpro in members.roles:
                await members.remove_roles(discord.utils.get(ctx.guild.roles, name="Peak Programmer"))
            if senpai in members.roles:
                await members.remove_roles(discord.utils.get(ctx.guild.roles, name="MaxCodez Senpai"))
            if kouhai in members.roles:
                await members.remove_roles(discord.utils.get(ctx.guild.roles, name="MaxCodez Kouhai"))
        self.levelling.delete_many({})
        await ctx.channel.send("done")



def setup(client):
    client.add_cog(levelling(client))
