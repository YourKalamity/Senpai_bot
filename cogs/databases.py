
import discord
from discord.ext import commands
import sqlite3

class Database(commands.Cog):
    """Used to store data in to SQL databases using SQLLite3"""
    def __init__(self,client):
        self.client = client
    
def setup(client):
    client.add_cog(Database(client))
