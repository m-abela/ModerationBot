from discord.ext import commands
import discord
from pymongo import MongoClient
''':cherry_blossom::hibiscus: :rose::tulip:'''
class welcome(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.cluster = MongoClient("mongodb+srv://maxcodez:zbndxaPz1BNseBgl@cluster0.hqubn.mongodb.net/<dbname>?retryWrites=true&w=majority")
        self.db = self.cluster["discord"]
        self.levelling = self.db["levelling"]
        self.info = self.db["info"]
        self.rooms = self.db["rooms"]
        self.noranks = self.info.find_one({"name":"bots"})["value"]
  
    @commands.Cog.listener()
    async def on_member_join(self, member):
        category = self.client.get_channel(857042462392582186)
        guild = self.client.get_guild(857042462132404234)
        channel = await guild.create_text_channel(f"🌸 Joined: {member.name}", category=category)
        await channel.set_permissions(guild.default_role, read_messages=False, read_message_history=False)
        await channel.set_permissions(member, overwrite=discord.PermissionOverwrite(send_messages=True,read_message_history=True, read_messages=True))

        embed = discord.Embed(color=0xFF95CA).set_image(url='https://cdn.discordapp.com/attachments/857042462144725005/857970887310180432/Screenshot_2021-06-13_at_3.00.04_PM.png')
        await channel.send(embed=embed)
        embed = discord.Embed(title= "Welcome to the MaxCodez ACADEMY!!!", color=0xFF95CA)
        embed.add_field(name=":cherry_blossom: **To get help:**",value="Please click :rose:",inline=False)
        embed.add_field(name=":cherry_blossom: **To join the community:**",value="Please click :tulip:",inline=False)
        embed.add_field(name=":cherry_blossom: **If you choose help**",value="You can still join later no worries!!!",inline=False)
        sent = await channel.send(embed=embed)
        await sent.add_reaction("🌹")
        await sent.add_reaction("🌷")
        await sent.pin()

        self.rooms.insert_one({"name" : "*" +str(channel.id), "id": str(member.id)})
    
    @commands.command()
    async def endhelp(self, ctx):
        room = self.rooms.find_one({"name" : "*" + str(ctx.channel.id)})
        if (room != None):
            person = discord.utils.find(lambda m : m.id == int(room["id"]), ctx.guild.members)
            await person.kick()
            await ctx.channel.delete()
            self.rooms.delete_one({"name": "*" + str(ctx.channel.id)})
      
    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        guild = discord.utils.find(lambda g : g.id == payload.guild_id, self.client.guilds)
        channelsend = discord.utils.get(guild.channels, id=payload.channel_id)
        room = self.rooms.find_one({"name" : "*" +str(payload.channel_id)})
        author = discord.utils.find(lambda m : m.id == int(room["id"]), guild.members)
        if (room != None) and (payload.user_id not in self.noranks):
            if payload.emoji.name == "🌷":
                await author.add_roles(discord.utils.get(guild.roles, name="Student"))
                await self.client.get_channel(payload.channel_id).delete()
                self.rooms.delete_one({"name":"*" + str(payload.channel_id)})
                embed = discord.Embed(title="Welcome to the MaxCodez Academy!",
                          description=f"{author.mention} please check out the rules and info <#847146274251472936>, We hope you enjoy your stay in our server!")
                embed.set_image(url='https://cdn.discordapp.com/attachments/857042462144725005/857970887310180432/Screenshot_2021-06-13_at_3.00.04_PM.png')
                embed.set_footer(text=f"Member count: {author.guild.member_count}")
                welcome_channel = discord.utils.get(author.guild.channels, id=847101178940227594)
                sent = await welcome_channel.send(embed=embed)

            if payload.emoji.name == "🌹":
                await channelsend.set_permissions(guild.get_role(857042462132404238), overwrite=discord.PermissionOverwrite(send_messages=True,read_message_history=True, read_messages=True))
                embed = discord.Embed(title="For optimum help please do the following", color=0xFF95CA)
                embed.add_field(name="🌸 Describe the problem in full detail", value=
                "Make sure you send all the bugs and problems with your code",inline=False)
                embed.add_field(name="🌸 Send all the code",value= "Please use a pasting website if your code is too long, do not send a .txt file", inline=False)
                embed.add_field(name="🌸 After getting help:",value= "use **?endhelp** to end the service or press :tulip: (on pinned message) to join the community", inline=False)
                embed.add_field(name="🌸 Finally, thank your helper!", value="please be aware that the helper is taking time out of their day to help you", inline=False)
                sent = await channelsend.send(embed=embed)

        
def setup(client):
    client.add_cog(welcome(client))
