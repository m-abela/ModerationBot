from discord.ext import commands
import discord
from pymongo import MongoClient

class embeds(commands.Cog):
    def __init__(self, client):
        self.client = client
       

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def info(self, ctx):
        embed = discord.Embed().set_image(url='https://cdn.discordapp.com/attachments/857042462144725005/857970904059215912/Screenshot_2021-06-13_at_2.58.41_PM.png')
        await ctx.send(embed=embed)

        embed = discord.Embed(title= "MaxCodez Academy Rules:")
        embed.add_field(name=":small_red_triangle:  **Follow the discord TOS**", value="Severe violations will result in a immediate ban. This includes but is not limited to being under the age of 13, Modification of client & Raiding.", inline=False)
        embed.add_field(name='\u200b', value = ':small_blue_diamond:[Discord Terms](https://discordapp.com/terms)')
        embed.add_field(name='\u200b', value = ':small_blue_diamond:[Discord Guidelines](https://discordapp.com/guidelines)')


        embed.add_field(name=":small_red_triangle:  **Be respectful, avoid potentially sensitive or awkward topics.**",value="To keep this community welcoming for anyone; Harassment, Toxicity and Discrimination will not be tolerated. If you have a issue with another user, please handle it in your DMs rather than settling your disputes in our server.", inline=False)
        
        embed.add_field(name=":small_red_triangle:  **Do not post NSFW or unsafe content.**", value="Posting media that contains or heavily alludes to NSFW or NSFL content is forbidden. IP loggers, viruses, and any other file that does not embed into discord should be refrained from being posted in this server.", inline=False)


        embed.add_field(name=":small_red_triangle:  **Do not advertise. Do not post links to other Discord servers or to promote yourself.**",value="This includes asking users to like/subscribe/donate/ect to you or another individual. This rule extends to your DMs with other server members.", inline=False)
       
        embed.add_field(name=":small_red_triangle:  **Do not spam.**", value="Avoid messages that are designed to flood the chat, such as copy-pastas & rapid message sending.", inline=False)

        embed.add_field(name=":small_red_triangle:  **Do not ping Max unless absolutely urgent.**", value="Max will take any actions as he feels, which may include but not only: a warn, mute and potentially a ban",inline=False)

        await ctx.send(embed=embed)
        '''
        embed = discord.Embed().set_image(url='https://cdn.discordapp.com/attachments/847101178940227594/853528870480379934/Screenshot_2021-06-13_at_2.58.50_PM.png')
        await ctx.send(embed=embed)

        embed = discord.Embed(title= "MaxCodez Academy moderation:")
        embed.add_field(name=":small_red_triangle:  **There are no moderators**", value="This server is entirely community moderated, this server can only be a nice place if you want it to be!",inline=False)
        embed.add_field(name=":small_red_triangle:  **React with <:warn:852554763652694077> for moderation**", value="Moderation requires 2 <:warn:852554763652694077> reactions on a harmful message",inline=False)
        embed.add_field(name=":small_red_triangle:  **Punishments given**", value="Moderation works based off a 4 strike basis. 1st: 2hr mute, 2nd: 6h mute, 3rd: 24hr mute, 4th: ban",inline=False)
        embed.add_field(name=":small_red_triangle:  **Misuse of the system results in a ban**", value="If moderation was dealt inappropriately, all users who reacted will be banned!",inline=False)
        embed.set_image(url='https://cdn.discordapp.com/attachments/847004462886158336/852557337670582323/Screenshot_2021-06-10_at_10.38.26_PM.png')
        await ctx.send(embed=embed)'''

        embed = discord.Embed()
        embed.add_field(name="**Enjoy your time in the MaxCodez Academy!**", value="Please read everything above to get to know all the information regarding our server. If you have any questions regarding the server, feel free to chat with one of our members with a high rank",inline=False)
        embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/857042462144725005/857970938661830686/Screenshot_2021-06-13_at_2.54.23_PM.png')
        await ctx.send(embed=embed)

  
    @commands.command()
    async def help(self, ctx):
        try:
            embed = discord.Embed(title= "MaxBot here!", description=f"Hey {ctx.author.name}, here's all the information that I think you might need, for now if there's anything else, please ask another member, I'm still under development!", color=0xFF95CA)
            embed.add_field(name=":cherry_blossom: **?rank**", value="You can check your level and rank in <#857042462392582185>, this level is based off how much you talk in <#857042462392582184>.", inline=False)
            embed.add_field(name=":cherry_blossom: **?leaderboard**", value="You can check the leaderboard for the top 10 people <#857042462392582185>", inline=False)
            embed.add_field(name=":cherry_blossom: **Getting help**", value="Please check out <#857042462392582188> to get help for anything coding related", inline=False)
            embed.add_field(name=":cherry_blossom: **?codeblock**", value="You can use this in a help room to show students how to embed code", inline=False)
            await ctx.author.send(embed=embed)
            embed = discord.Embed(description=f"Hey {ctx.author.mention} I've sent you a DM!", color=0xFF95CA)
            await ctx.send(embed=embed)
            
        except:
            embed = discord.Embed(description=f"Hey {ctx.author.mention} I don't think you have DMs open! I can't send you any information!", color=0xFF95CA)
            await ctx.send(embed=embed)
   @commands.command()
    @commands.has_permissions(administrator=True)
    async def faq(self, ctx):
        embed = discord.Embed().set_image(url='https://cdn.discordapp.com/attachments/857042462144725005/857970921833496576/Screenshot_2021-06-13_at_2.55.37_PM.png')
        await ctx.send(embed=embed)

        embed = discord.Embed(title= ":blue_book: **Pip installation error**", description="You can install modules in the pycharm terminal using “Pip install <module name>”, refer to image below.")
        await ctx.send(embed=embed)
        embed = discord.Embed().set_image(url='https://cdn.discordapp.com/attachments/857042462144725005/857971227464826970/Screenshot_2020-11-14_at_8.58.16_PM.png')
        await ctx.send(embed=embed)

        embed = discord.Embed(title= ":blue_book: **How to run the spam script**", description="Make sure you open up the page you want to spam in, eg. Whatsapp web. And start running the script, you’ll have 5 seconds before the script will start spamming so make sure you click back onto the window to spam in!")
        await ctx.send(embed=embed)

        embed = discord.Embed(title= ":blue_book: **File directory error**", description="You will get an error if you txt file and your script are not in the same directory (which means file), make sure they’re in the same directory!")
        await ctx.send(embed=embed)

        embed = discord.Embed().set_image(url='https://cdn.discordapp.com/attachments/857042462144725005/857971214591721532/Screenshot_2020-11-14_at_9.07.43_PM.png')
        await ctx.send(embed=embed)

        embed = discord.Embed(title= ":blue_book: **How to stop the script**", description="If the spam is too much and you need to stop the file you can hit Command C/Ctrl C to stop the script, this applies to any and all scripts!")
        await ctx.send(embed=embed)

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def gethelp(self, ctx):
        embed = discord.Embed().set_image(url='https://cdn.discordapp.com/attachments/857042462144725005/857970915785834506/Screenshot_2021-06-13_at_2.55.55_PM.png')
        await ctx.send(embed=embed)
        embed = discord.Embed(title= ":blue_book: **Please check FAQ!!!**", description="Make sure you check all the FAQ, if you ask about something in the FAQ, we will kick you!")
        await ctx.send(embed=embed)
        embed = discord.Embed(title= ":blue_book: **To get help**", description="Please react to this message with 🟥 to get started!")
        sent = await ctx.send(embed=embed)
        await sent.add_reaction("🟥")
    
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def sensei(self, ctx, channid: int, *args):
        channel = discord.utils.get(ctx.guild.channels, id=channid)
        speech = ' '.join(args)
        await channel.send(speech)
    
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def maxwellintro(self, ctx):
        embed = discord.Embed(title= "DR. MAXWELL", description="Hi! I'm Dr Maxwell, I'm the principal of the academy but also your programming teacher! I handle anything moderation related and I'll be assisting you with your coding problems. I'm looking forward to seeing you all progress and become top notch coders!", color=0x4DC8E9)
        embed.set_image(url="https://cdn.discordapp.com/attachments/857042462144725005/857970975906594856/Screenshot_2021-06-13_at_2.54.15_PM.png")
        await ctx.send(embed=embed)
    
    '''
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def helpers(self, ctx):
        embed = discord.Embed(color=0x4DC8E9).set_image(url='https://cdn.discordapp.com/attachments/847101178940227594/853530948191518730/Screenshot_2021-06-13_at_3.07.05_PM.png')
        await ctx.send(embed=embed)

        embed = discord.Embed(title= ":blue_book: **New student help**", description="When a new student requests for help, their chat will become visible to you, please assist them!", color=0x4DC8E9)
        await ctx.send(embed=embed)
        embed = discord.Embed(color=0x4DC8E9).set_image(url='https://cdn.discordapp.com/attachments/847101178940227594/853531795139461140/Screenshot_2021-06-13_at_3.10.32_PM.png')
        await ctx.send(embed=embed)

        embed = discord.Embed(title= ":blue_book: **Impolite new students**", description="Using the **?endhelp** command will end the chat and kick the new student out", color=0x4DC8E9)
        await ctx.send(embed=embed)

        embed = discord.Embed(title= ":blue_book: **Opening rooms**", description="When someone needs help, please ask them to open a room by clicking this red button in <#847004807771979776>", color=0x4DC8E9)
        await ctx.send(embed=embed)

        embed = discord.Embed(color=0x4DC8E9).set_image(url='https://cdn.discordapp.com/attachments/847101178940227594/853532276301758492/Screenshot_2021-06-13_at_3.12.27_PM.png')
        await ctx.send(embed=embed)

        embed = discord.Embed(title= ":blue_book: **impolite helpers**", description="You will have to use proper moderation procedures here, 2 helpers will need to react with <:warn:852554763652694077>, don't be scared to ping Max asap. Depending on how users treat helpers in the future, helpers may be given moderation powers.", color=0x4DC8E9)
        await ctx.send(embed=embed)

        embed = discord.Embed(title= ":blue_book: **?codeblock command**", description="You may request a user to display their code in a codeblock and this will show them how", color=0x4DC8E9)
        await ctx.send(embed=embed)
    '''
        

def setup(client):
    client.add_cog(embeds(client))
