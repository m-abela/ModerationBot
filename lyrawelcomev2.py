from discord.ext import commands
import discord
from pymongo import MongoClient
''':cherry_blossom::hibiscus: :rose::tulip:'''
class welcome(commands.Cog):
    def __init__(self, client):
        self.client = client
  
    @commands.Cog.listener()
    async def on_member_join(self, member):

        guild = member.guild
        await member.add_roles(discord.utils.get(guild.roles, name="Student"))
        embed = discord.Embed(title="Welcome to the MaxCodez Academy!",
                  description=f"{member.mention} please check out the rules and info <#857042462144725004>, We hope you enjoy your stay in our server!")
        embed.set_image(url='https://cdn.discordapp.com/attachments/857042462144725005/857970887310180432/Screenshot_2021-06-13_at_3.00.04_PM.png')
        embed.set_footer(text=f"Member count: {guild.member_count}")
        welcome_channel = discord.utils.get(guild.channels, id=857042462144725005)
        await welcome_channel.send(embed=embed)

        embed = discord.Embed(color=0x000000).set_image(url='https://cdn.discordapp.com/attachments/857042462144725005/857970887310180432/Screenshot_2021-06-13_at_3.00.04_PM.png')
        await member.send(embed=embed)
        embed = discord.Embed(title= "Welcome to the MaxCodez ACADEMY!!!", description="Hi! I'm the MaxCodezBot, I'm the official bot for the server!", color=0x000000)

        embed.add_field(name=":cherry_blossom: **Getting help**", value="Please check out <#857042462392582188> to get help for anything coding related", inline=False)
        embed.add_field(name=":cherry_blossom: **Need more information?**", value="Please check out <#857042462144725004>. Also feel free to ask some of our members for more assistance", inline=False)
        embed.set_thumbnail(url="https://media.discordapp.net/attachments/857042462144725005/857970938661830686/Screenshot_2021-06-13_at_2.54.23_PM.png")

        await member.send(embed=embed)


        
def setup(client):
    client.add_cog(welcome(client))
    embed = discord.Embed(color=0x000000).set_image(url="https://media.discordapp.net/attachments/857042462144725005/857970887310180432/Screenshot_2021-06-13_at_3.00.04_PM.png")
        await member.send(embed=embed)
        embed = discord.Embed(title= "Welcome to the MaxCodez ACADEMY!!!", description="Hi! I'm the MaxCodezBot, I'm the official bot for the server!", color=0x000000)
        embed.add_field(name=":cherry_blossom: **Getting help**", value="Please check out <#857042462392582188> to get help for anything coding related", inline=False)
        embed.add_field(name=":cherry_blossom: **Need more information?**", value="Please check out <#857042462144725004>. Also feel free to ask some of our members for more assistance", inline=False)
        embed.set_thumbnail(url="https://media.discordapp.net/attachments/857042462144725005/857970938661830686/Screenshot_2021-06-13_at_2.54.23_PM.png")
        await member.send(embed=embed)
