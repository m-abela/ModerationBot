import discord
from discord.ext import commands
from pymongo import MongoClient

class python_challenges(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.cluster = MongoClient(
            "mongodb+srv://maxcodez:zbndxaPz1BNseBgl@cluster0.hqubn.mongodb.net/<dbname>?retryWrites=true&w=majority")
        self.db = self.cluster["discord"]
        self.info = self.db["info"]
        self.challenges = self.db["challenges"]
        self.scores = self.db["challengescores"]
        self.challenge = self.info.find_one({"name":"challenge"})["value"]
        self.botchannel = self.info.find_one({"name":"botchannel"})["value"]
        self.modlog = self.info.find_one({"name":"modlog"})["value"]
        self.moderation = self.db["moderation"]

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        guild = discord.utils.find(lambda g : g.id == payload.guild_id, self.client.guilds)
        author = discord.utils.find(lambda m : m.id == payload.user_id, guild.members)
        challenge = self.challenges.find_one({"messageid":str(payload.message_id)})
        if payload.channel_id == self.challenge:
            info = self.scores.find_one({"id":str(author.id)})
            if info == None:
                mydict = {"id" : str(author.id), "question" : str(challenge["id"]), "score" : "0"}
                self.scores.insert_one(mydict)
                embed = discord.Embed(description=f"Please send your answer! You can try more than once no worries!")
                await author.send(embed=embed)
            else:
                try:
                    info[str(challenge["id"])] == "done"
                    embed = discord.Embed(description=f"You've already done this challenge!")
                    await author.send(embed=embed)
                except:
                    self.scores.update_one({"id":str(author.id)},{"$set":{"question": str(challenge["id"])}})
                    embed = discord.Embed(description=f"Please send your answer! You can try more than once no worries!")
                    await author.send(embed=embed)

    @commands.Cog.listener()
    async def on_message(self, message):
        if (message.guild is None) and (not message.author.bot):
            challenge = self.scores.find_one({"id":str(message.author.id)})
            answer = self.challenges.find_one({"id":int(challenge["question"])})
            if message.content == answer["answer"]:
                self.scores.update({"id":str(message.author.id)},{"$set":{challenge["question"]:"done"}})
                self.scores.update_one({"id":str(message.author.id)},{"$set":{"question": ""}})
                self.scores.update_one({"id":str(message.author.id)},{"$set":{"score":str(int(challenge["score"])+1)}})
                embed = discord.Embed(title=f"That answer was correct!", description="")
                embed.add_field(name="Points:", value=int(challenge["score"])+1, inline=False)
                embed.set_thumbnail(url=message.author.avatar_url)
                await message.author.send(embed=embed)
            else:
                embed = discord.Embed(description=f"That's not right!")
                await message.author.send(embed=embed)
  
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def setquestion(self, ctx, answer, *args):
        modlog = discord.utils.get(ctx.guild.channels, id=self.modlog)
        chall = discord.utils.get(ctx.guild.channels, id=self.challenge)
        challengeid = self.challenges.find_one({"id":"true"})
        self.challenges.update_one({"id":"true"},{"$set":{"challengeid":(challengeid["challengeid"]+1)}})

        question = ' '.join(args)
        embed = discord.Embed(title=f"Challenge #{challengeid['challengeid']}", description="")
        embed.add_field(name="Challenge:", value=question, inline=False)
        sent = await chall.send(embed=embed)
        await sent.add_reaction("🟥")

        mydict = {"id" : (challengeid["challengeid"]+1), "answer" : answer, "messageid":str(sent.id)}
        self.challenges.insert_one(mydict)
        
        embed = discord.Embed(title="Question set", description="")
        embed.add_field(name="Question:", value=question, inline=False)
        embed.add_field(name="Answer:", value=answer, inline=False)
        embed.set_thumbnail(url=ctx.author.avatar_url)
        await ctx.send(embed=embed)

    @commands.command()
    async def challengestats(self, ctx):
      if ctx.channel.id == self.botchannel:
          stats = self.scores.find_one({"id":str(ctx.author.id)})
          if stats is None:
              embed = discord.Embed(description=f"You haven't done any challenges! No rank!",
                                  color=0xb91919)
              await ctx.channel.send(embed=embed)
          else:
              xp = stats["score"]
              rankings = self.scores.find().sort("score",-1)
              rank = 0
              for x in rankings:
                rank += 1
                if stats["id"] == (x["id"]):
                  break

              embed = discord.Embed(title="{}'s challenge stats".format(ctx.author.name), description="")
              embed.add_field(name="Name", value=ctx.author.mention, inline=True)              
              embed.add_field(name="Points", value=xp, inline=True)
              embed.add_field(name="Rank", value=f"{rank}/{ctx.guild.member_count}",inline=True)
              embed.set_thumbnail(url=ctx.author.avatar_url)
              await ctx.channel.send(embed=embed)

def setup(client):
    client.add_cog(python_challenges(client))
