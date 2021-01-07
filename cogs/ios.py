import discord
from discord.ext import commands
import requests
import urllib.parse
import os
import json
from cogs.databases import check_blacklist, create_connection
database = os.getcwd()+r"/db/database.db"

class Ios(commands.Cog):
    """iOS related commands"""

    def __init__(self, client):
        self.client = client
        self.conn = create_connection(database)

    @commands.group()
    async def ios(self, ctx):
        """iOS related commands!"""
        if check_blacklist(self.conn, ctx.author.id) != None:
            return

    @ios.command()
    async def jailbreak(self, ctx, *, phone_model):
        if check_blacklist(self.conn, ctx.author.id) != None:
            return
        phone_model = phone_model.replace(" ","-")
        return await ctx.send("https://iOS.cfw.guide/firmware-selection-("+phone_model+")")

    @ios.command()
    async def tweak(self,ctx,*,tweak_name):
        if check_blacklist(self.conn, ctx.author.id) != None:
            return
        search_term = urllib.parse.quote(tweak_name)
        string = "https://api.parcility.co/db/search?q="+search_term
        info = json.loads(requests.get(string).content)

        embed=discord.Embed(title="Maintained by "+info["data"][0]["Maintainer"], color=0xeea4f2)
        embed.set_thumbnail(url=info["data"][0]["Icon"])
        embed.set_author(name=info["data"][0]["Name"],url="https://parcility.co/package/"+info["data"][0]["Package"])
        embed.add_field(name="**Description :**" , value=info["data"][0]["Description"], inline=False)
        embed.add_field(name="**Version :**" , value=info["data"][0]["Version"], inline=True)
        embed.add_field(name="**More Info :**" , value="[View on Parcility](https://parcility.co/package/"+info["data"][0]["Package"]+")", inline=False)
        return await ctx.send("",embed=embed)
        

def setup(client):
    client.add_cog(Ios(client))
