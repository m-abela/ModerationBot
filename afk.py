from discord.ext import commands
import discord

afak= []

class test(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_message(self, message):
      for i in range(len(afak)):
        if ((f"<@!{afak[i]}>" in message.content) and (not message.author.bot)):
          await message.channel.send(f"<@!{afak[i]}> is away right now! They said: {afak[i+1]}")
          return None
          break
      
    @commands.Cog.listener()
    async def on_typing(self,channel,user,when):
      if user.id in afak:
          afak.remove(user.id)
          await channel.send(f"{user.mention} has returned!")
          return None

    @commands.command()
    async def afk(self, ctx, *args):
      msg = ' '.join(args)
      afak.append(ctx.author.id)
      afak.append(msg)
      await ctx.send("afk set!")


def setup(client):
    client.add_cog(test(client))
