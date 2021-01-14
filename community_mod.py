import discord
from discord.ext import commands

class community_mod(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    

def setup(client):
    client.add_cog(community_mod(client))