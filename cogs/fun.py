

import discord
import discord.ext
from discord.ext import commands
import os
from cogs.databases import check_blacklist, create_connection
import requests
import json
database = os.getcwd()+r"/db/database.db"
member_converter = discord.ext.commands.MemberConverter()
from zalgo_text import zalgo

class Fun(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.conn = create_connection(database)

    @commands.command()
    async def slap(self,ctx,*,member):
        if check_blacklist(self.conn, ctx.author.id) != None:
            return
        
        try:
            m = await member_converter.convert(ctx=ctx,argument=member)
        except discord.ext.commands.BadArgument:
            await ctx.send("You can't slap `"+member+"` if they're not here...")
            return
        
        image = (json.loads(requests.get("https://nekos.life/api/v2/img/slap").content))["url"]
        title = ctx.author.name + " slapped " + m.name
        embed = discord.Embed(title=title,color=0xeea4f2)
        embed.add_field(name="*ouch that looks like it hurts...*",value="maybe you should s!slap them back?",inline=False)
        embed.set_image(url=image)
        await ctx.send(embed=embed)
    
    @commands.command()
    async def hug(self,ctx,*,member):
        if check_blacklist(self.conn, ctx.author.id) != None:
            return
        
        try:
            m = await member_converter.convert(ctx=ctx,argument=member)
        except discord.ext.commands.BadArgument:
            await ctx.send("You can't hug `"+member+"` if they're not here...")
            return
        
        image = (json.loads(requests.get("https://nekos.life/api/v2/img/hug").content))["url"]
        title = ctx.author.name + " hugged " + m.name
        embed = discord.Embed(title=title,color=0xeea4f2)
        embed.add_field(name="*aww how wholesome...*",value="maybe you should s!hug them back?",inline=False)
        embed.set_image(url=image)
        await ctx.send(embed=embed)
    
    @commands.command(aliases=["headpat"])
    async def pat(self,ctx,*,member):
        if check_blacklist(self.conn, ctx.author.id) != None:
            return
        
        try:
            m = await member_converter.convert(ctx=ctx,argument=member)
        except discord.ext.commands.BadArgument:
            await ctx.send("You can't headpat `"+member+"` if they're not here...")
            return
        
        image = (json.loads(requests.get("https://nekos.life/api/v2/img/pat").content))["url"]
        title = ctx.author.name + " patted " + m.name
        embed = discord.Embed(title=title,color=0xeea4f2)
        embed.add_field(name="*you slowly feel more happy...*",value="maybe you should s!pat them back?",inline=False)
        embed.set_image(url=image)
        await ctx.send(embed=embed)
    
    @commands.command()
    async def tickle(self,ctx,*,member):
        if check_blacklist(self.conn, ctx.author.id) != None:
            return
        
        try:
            m = await member_converter.convert(ctx=ctx,argument=member)
        except discord.ext.commands.BadArgument:
            await ctx.send("You can't tickle `"+member+"` if they're not here...")
            return
        
        image = (json.loads(requests.get("https://nekos.life/api/v2/img/tickle").content))["url"]
        title = ctx.author.name + " tickled " + m.name
        embed = discord.Embed(title=title,color=0xeea4f2)
        embed.add_field(name="*you can't control your laughter...*",value="maybe you should s!tickle them back?",inline=False)
        embed.set_image(url=image)
        await ctx.send(embed=embed)

    @commands.command()
    async def notice(self,ctx,*,member):
        if check_blacklist(self.conn, ctx.author.id) != None:
            return
        if member == "me":
            m = ctx.author
        else:
            try:
                m = await member_converter.convert(ctx=ctx,argument=member)
            except discord.ext.commands.BadArgument:
                await ctx.send("I can't notice `"+member+"` if they're not here...")
                return
        
        title = "Senpai has finally noticed " + m.name +"!"
        embed = discord.Embed(title=title,color=0xeea4f2)
        embed.add_field(name="*you can't control your joy...*",value="maybe you should s!notice someone else?",inline=False)
        await ctx.send(embed=embed)
        
    @commands.command()
    async def zalgofy(self,ctx,*,string):
        if check_blacklist(self.conn, ctx.author.id) != None:
            return
        if string != None:
            await ctx.send(content=zalgo.zalgo().zalgofy(string))
            return
        
        
        
        


def setup(client):
    client.add_cog(Fun(client))