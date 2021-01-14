import discord
from discord.ext import commands
from replit import db

class helproom(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        try:
            if (db["*" + str(payload.channel_id)] == "yes") and (payload.user_id != 771103336207220756):
                if payload.emoji.name == "🟥":
                    await self.client.get_channel(payload.channel_id).delete()
                    del db["*" + str(payload.channel_id)]
        except:
            pass
      
    @commands.command()
    @commands.has_any_role("Python helper", "Moderator", "MaxCodez")
    async def room(self, ctx, member: discord.Member):
        channel = await ctx.guild.create_text_channel(f"🟥 {member.name} room", category=ctx.channel.category)
        db["*" + str(channel.id)] = "yes"
        await channel.set_permissions(ctx.guild.default_role, read_messages=False, read_message_history=False)
        await channel.set_permissions(ctx.guild.get_role(735360869059526686), overwrite=discord.PermissionOverwrite(send_messages=True, read_message_history=True, read_messages=True))
        await channel.set_permissions(member, overwrite=discord.PermissionOverwrite(send_messages=True, read_message_history=True, read_messages=True))
        await channel.set_permissions(ctx.guild.get_role(781751214907064330), overwrite=discord.PermissionOverwrite(send_messages=False))
        await ctx.send(f"Room created: {channel.mention}")
        embed = discord.Embed(description=f'''
        {member.mention} will receive help in here from {ctx.author.mention}!
        when finished react with 🟥 to delete the channel!
        ''', color=0xb91919)
        sent = await channel.send(embed=embed)
        await sent.add_reaction("🟥")

    @commands.command()
    @commands.has_any_role("Moderator", "MaxCodez")
    async def privtalk(self, ctx, member: discord.Member):
        channel = await ctx.guild.create_text_channel(f"🟦 {member.name} room", category=ctx.channel.category)
        db["*" + str(channel.id)] = "yes"
        await channel.set_permissions(ctx.guild.default_role, read_messages=False, read_message_history=False)
        await channel.set_permissions(ctx.author, overwrite=discord.PermissionOverwrite(send_messages=True, read_message_history=True, read_messages=True))
        await channel.set_permissions(member, overwrite=discord.PermissionOverwrite(send_messages=True, read_message_history=True, read_messages=True))
        await channel.set_permissions(ctx.guild.get_role(781751214907064330), overwrite=discord.PermissionOverwrite(send_messages=False))
        await ctx.send(f"Room created: {channel.mention}")
        embed = discord.Embed(description=f'''
        {member.mention} private room made by {ctx.author.mention}!
        when finished react with 🟥 to delete the channel!
        ''', color=0xb91919)
        sent = await channel.send(embed=embed)
        await sent.add_reaction("🟥")

    @commands.command()
    @commands.has_any_role("MaxCodez", "Moderator", "Python helper")
    async def endroom(self, ctx):
        if db["*" + str(ctx.channel.id)] == "yes":
            await ctx.channel.delete()
            

def setup(client):
    client.add_cog(helproom(client))
