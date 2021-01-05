import discord
from discord.ext import commands
import traceback
import requests
import json

class GitHub(commands.Cog):
    """Useful Commands for use with GitHub API"""

    def __init__(self,client):
        self.client = client
    
    @commands.group()
    async def github(self, ctx):
        """Collection of commands used for GitHub"""
        if ctx.invoked_subcommand is None:
            await ctx.send("That's not a valid `github` command")

    @github.command()
    async def info(self, ctx, repo):
        try:

            if repo[0][:1] == "/":
                repo = repo[1:]
            if repo[-1] == "/":
                repo = repo[:-1]

            string = "https://api.github.com/repos/"+repo
            release = json.loads(requests.get(string).content)

            embed=discord.Embed(title="Created by "+release["owner"]["login"] , color=0xeea4f2)
            embed.set_thumbnail(url=release["owner"]["avatar_url"])
            embed.set_author(name=release["name"] , url=release["html_url"])
            embed.add_field(name="**Description :**" , value=release["description"], inline=False)
            embed.add_field(name="**Created on :**" , value=release["created_at"], inline=True)
            embed.add_field(name="**Last Push :**" , value=release["pushed_at"] , inline=True)
            embed.add_field(name="**Language :**" , value=release["language"] , inline=False)
            embed.add_field(name="**Release Downloads : **" , value="https://github.com/"+repo+"/releases", inline=False)
            await ctx.send("",embed=embed)
        except commands.CommandInvokeError:
            await ctx.send("The GitHub repository `"+repo+"` could not be found")
    
    @github.command()
    async def latest(self, ctx, repo):
        try:
            if repo[0][:1] == "/":
                repo = repo[1:]
            if repo[-1] == "/":
                repo = repo[:-1]

            string = "https://api.github.com/repos/"+repo
            release = json.loads(requests.get(string).content)
            embed=discord.Embed(title=release["name"], color=0xeea4f2)
            embed.set_thumbnail(url=release["owner"]["avatar_url"])
            embed.add_field(name="**Latest Release : **", value="https://github.com/"+repo+"/releases/latest",inline=False)
            await ctx.send("",embed=embed)
        except commands.CommandInvokeError:
            await ctx.send("The GitHub repository `"+repo+"` could not be found")

    @github.command()
    async def user(self, ctx, username):
        try:
            

            string = "https://api.github.com/users/"+username
            release = json.loads(requests.get(string).content)
            embed=discord.Embed(title=release["login"], color=0xeea4f2)
            embed.set_thumbnail(url=release["avatar_url"])
            embed.add_field(name="**Link to Profile : **", value=release["html_url"],inline=False)
            embed.add_field(name="**Followers : **", value=release["followers"], inline=True)
            embed.add_field(name="**Following : **", value=release["following"], inline=True)
            embed.add_field(name="**Account created on : **", value=release["created_at"], inline=False)
            embed.add_field(name="**Public Repositories : **", value=release["public_repos"], inline=False)
            await ctx.send("",embed=embed)
        except commands.CommandInvokeError:
            await ctx.send("The GitHub user, `"+username+"`, could not be found")

            
            


def setup(client):
    client.add_cog(GitHub(client))