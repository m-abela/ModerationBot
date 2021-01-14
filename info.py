from discord.ext import commands
import discord
import json
import datetime

with open("data.json", "r") as db:
    config = json.load(db)
    rules = config["rules"]

class info(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(aliases=['rules'])
    async def rule(self, ctx, *, rule_no : int):
        with open("data.json", "r") as db:
            config = json.load(db)
            rules = config["rules"]
        try:
            await ctx.send(rules[rule_no-1])
        except:
            await ctx.send("Invalid rule number given!")

    @commands.command()
    async def avatar(self, ctx, member: discord.Member=None):
        if member is None:
            member=ctx.author
        embed = discord.Embed(title=f'{member.display_name}\'s profile picture',
                      url= f'{member.avatar_url}',
                      timestamp=datetime.datetime.utcnow())
        embed.set_image(url=f'{member.avatar_url}')
        await ctx.send(embed=embed)

    @commands.command()
    async def whois(self, ctx, member:discord.Member=None):
        embed = discord.Embed(title="{}'s info".format(member.name), description="")
        embed.add_field(name="Name", value=member.name, inline=True)
        embed.add_field(name="ID", value=member.id, inline=True)
        embed.add_field(name="Status", value=member.status, inline=True)
        embed.add_field(name="Roles", value=member.top_role)
        embed.add_field(name="Joined", value=member.joined_at)
        embed.add_field(name="Created", value=member.created_at)
        embed.set_thumbnail(url=member.avatar_url)
        await ctx.send(embed=embed)
def setup(client):
    client.add_cog(info(client))
