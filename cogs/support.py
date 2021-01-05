import discord
from discord.ext import commands
import urllib.parse
theOwner = 194852876902727680

class Support(commands.Cog):
    """Commands used to give help"""

    def __init__(self,client):
        self.client = client
    
    @commands.group()
    async def support(self, ctx):
        """Commands used to give help"""
        if ctx.invoked_subcommand is None:
            await ctx.send("That's not a valid `support` command")

    @support.command()
    async def root(self,ctx):
        embed=discord.Embed(color=0xeea4f2)
        embed.set_image(url='https://images-ext-1.discordapp.net/external/KUr_9m9wLNNNNIo-9vxcyL36hB9bAhJwGNk8yp0Uhak/https/i.imgur.com/7PIvVjJ.png')
        await ctx.send("",embed=embed)

    @support.command()
    async def writelock(self,ctx):
        embed=discord.Embed(color=0xeea4f2)
        embed.add_field(name="Disable SD Card Write Protection", value="This switch on the SD card should be pushed up, as the image below shows.\n If it is write locked, applications may not work properly")
        embed.set_image(url="https://cdn.discordapp.com/attachments/738767885572505641/743602826919542866/move-lock-switch-to-remove-write-protection.png")
        await ctx.send("",embed=embed)



def setup(client):
    client.add_cog(Support(client))
