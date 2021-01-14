from discord.ext import commands
import discord
import random
from textblob import TextBlob


class misc(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print('MaxBot is ready.')

    @commands.command()
    async def repeat(self, ctx, *, args):
        if (("@everyone") in args) or (("@here") in args):
            return None
        else:
            await ctx.send('You said {}'.format(args))

    @commands.command()
    async def angry(self, ctx, *args):
        if (("@everyone") in args) or (("@here") in args):
            return None
        else:
            await ctx.send('angry tone: {}'.format((' '.join(args)).upper()))
    
    @commands.command()
    @commands.has_any_role("Senior Mods", "Moderator", "MaxCodez")
    async def staffintro(self, ctx, *args):
        embed = discord.Embed(color=0x397882)
        embed.add_field(name=ctx.author.name, value=(' '.join(args)), inline=False)
        embed.set_thumbnail(url=ctx.author.avatar_url)
        await ctx.send(embed=embed)
        await ctx.delete()

    @commands.command()
    async def sad(self, ctx, *args):
        if (("@everyone") in args)or (("@here") in args):
            return None
        else:
            await ctx.send('{}... :((((((((((((('.format((' '.join(args)).lower()))

    @commands.command()
    async def headpat(self, ctx, member: discord.User):
        responses = ['https://i.pinimg.com/originals/2e/27/d5/2e27d5d124bc2a62ddeb5dc9e7a73dd8.gif',
                 'https://i.imgur.com/EItM5ht.gif',
                 'https://archive-media-0.nyafuu.org/c/image/1536/38/1536381393938.gif']
        embed = discord.Embed(description=f"{ctx.author.mention} headpatted {member.mention}!", color=0x397882)
        embed.set_image(url=f'{random.choice(responses)}')
        await ctx.send(embed=embed)


    @commands.command()
    async def slap(self, ctx, member: discord.User):
        responses = ['https://tenor.com/view/gap-slapped-knock-out-punch-gif-5122019', 'https://images-ext-2.discordapp.net/external/oKgP-4HbUB8182mIqILMV1uYmLyazXo2FHytDNTLeQ4/%3Fcid%3Decf05e475bwu3q8xsji33efrpq2e213l3stlqfyfkfhrocmp%26rid%3Dgiphy.gif/https/media4.giphy.com/media/uqSU9IEYEKAbS/giphy.gif', 'https://cdn.discordapp.com/attachments/724530865585258516/762576928531939328/tenor.gif']
        embed = discord.Embed(description=f"{ctx.author.mention} slapped {member.mention}!", color=0x397882)
        embed.set_image(url=f'{random.choice(responses)}')
        await ctx.send(embed=embed)
    
    @commands.command()
    async def translate(self, ctx, *, args):
        blob = TextBlob(args)
        translation = blob.translate(to='en')
        if (("@everyone") in translation) or (("@here") in translation):
            await ctx.author.guild.ban(ctx.author, reason="Trying to ping everyone")
            embed = discord.Embed(
                description="{0} banned for trying to ping everyone".format(ctx.author.name),
                color=0xdddd1e)
            await ctx.channel.send(embed=embed)
        else:
            await ctx.channel.send(translation)
                

    


def setup(client):
    client.add_cog(misc(client))