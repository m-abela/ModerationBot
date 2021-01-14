import json
import discord
from discord.ext import commands
from replit import db

with open("data.json", "r") as datab:
    config = json.load(datab)
    python_help_channel = config["python_help_channel"]


class python_help(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.has_any_role("Python helper", "Moderator", "MaxCodez")
    async def docs(self, ctx, module):
        room = False
        try: 
            if db["*" + str(ctx.channel.id)] == "yes":
                room = True
        except:
            pass
        if (room == True) or (ctx.channel.id in python_help_channel):
            if module == "pyautogui":
                response = "https://pyautogui.readthedocs.io/en/latest/"
            elif module == "discord":
                response = "https://discordpy.readthedocs.io/en/latest/"
            elif module == "selenium":
                response = "https://selenium-python.readthedocs.io"
            elif module == "python":
                response = "https://docs.python.org/3/"
            else:
                response = f'I made a link to the documentation but I do not know if it works. \"http://{module}.readthedocs.io\"'
            embed = discord.Embed(description=response, color=0x397882)
            await ctx.send(embed=embed)

    @commands.command()
    @commands.has_any_role("Python helper", "Moderator", "MaxCodez")
    async def error(self, ctx, *args):
        room = False
        try: 
            if db["*" + str(ctx.channel.id)] == "yes":
                room = True
        except:
            pass
        if (room == True) or (ctx.channel.id in python_help_channel):
            if "pyautogui" in args:
                embed = discord.Embed(description=f"Ah so i guess you got a pyautogui error? Well! You need to import pyautogui in the terminal! You can do this by going over to the terminal and typing in \"pip install pyautogui\", Good luck!", color=0x397882)
                embed.set_image(url='https://media.discordapp.net/attachments/719103243459756052/777160606221598730/Screenshot_2020-11-14_at_8.58.16_PM.png?width=2160&height=588')
                await ctx.send(embed=embed)

            if "nofile" in args:
                embed = discord.Embed(description=f"Ah so you don't have your file in the same directory? You need to make sure your text file and your python file are in the same directory!", color=0x397882)
                embed.set_image(url='https://cdn.discordapp.com/attachments/719103243459756052/777160600425594890/Screenshot_2020-11-14_at_9.07.43_PM.png')
                await ctx.send(embed=embed)

            if "syntax" in args:
                embed = discord.Embed(description=f"Ah well it appears you have a syntax error in your code! Make sure you check through each line carefully and master the basics of python! Ping a code helper if you still need help!", color=0x397882)
                await ctx.send(embed=embed)

    @commands.command()
    @commands.has_any_role("Python helper", "Moderator", "MaxCodez")
    async def comply(self, ctx, *args):
        room = False
        try: 
            if db["*" + str(ctx.channel.id)] == "yes":
                room = True
        except:
            pass
        if (room == True) or (ctx.channel.id in python_help_channel):
            embed = discord.Embed(description=f'''
```
Hi there! If you're reading this, a helper is probably a little frustrated. Here are some of the following things you need to do for us:
----------------------
Have you sent all of the code? (Please use a pasting website if your code is too long, please don't send a .txt files)
----------------------
Have you sent all of your errors? (Copy and paste all of the errors, use ?codeblock for reference)
----------------------
Are you patient? (All of the helpers here are using their own time, please be patient, we will get to you!)
----------------------
Have you thanked the helper? (Sometimes all helpers need is a simple thank you you can do this by typing ?givestar @user)
----------------------
```
            ''', color=0x397882)
            await ctx.channel.send(embed=embed)
      
    @commands.command()
    @commands.has_any_role("Python helper", "Moderator", "MaxCodez")
    async def codeblock(self, ctx):
      room = False
      try: 
          if db["*" + str(ctx.channel.id)] == "yes":
              room = True
      except:
          pass
      if (room == True) or (ctx.channel.id in python_help_channel):
        embed = discord.Embed(description=f"It is much easier for code helpers to read if you embed your code! You can do it like this!", color=0x397882)
        embed.set_image(url='https://media.discordapp.net/attachments/719103243459756052/777160604892528650/Screenshot_2020-11-14_at_9.14.59_PM.png')
        await ctx.send(embed=embed)


    @commands.command()
    @commands.has_any_role("Python helper", "Moderator", "MaxCodez")
    async def spamscript(self, ctx):
        room = False
        try: 
            if db["*" + str(ctx.channel.id)] == "yes":
                room = True
        except:
            pass
        script='''
```python
import pyautogui
from time import sleep
sleep(5)
f = open('beemovie.txt', 'r')
for word in f:
  pyautogui.typewrite(word)
  pyautogui.press("enter")
f.close()```'''
        if (room == True) or (ctx.channel.id in python_help_channel):
            embed = discord.Embed(title='Spam script:', description=script)
            await ctx.send(embed=embed)
    
    
def setup(client):
    client.add_cog(python_help(client))