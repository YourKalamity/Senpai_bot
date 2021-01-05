import discord
from discord.ext import commands

class Moderation(commands.Cog):
    """Tools for moderation"""

    def __init__(self,client):
        self.client = client

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, amount=2):
        await ctx.channel.purge(limit=amount)
    
    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member=None):
        if not member:
            await ctx.send("I looked everywhere, but couldn't find that user, sir")
            return
        await member.ban()
        await ctx.send(f'{member.mention} had witnessed the ban hammer')

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member=None):
        if not member:
            await ctx.send("I looked everywhere, but I couldn't find that user, sir")
            return
        await member.kick()
        await ctx.send(f'{member.mention} got booted')

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def unban(self, ctx, *, member):
        banned_users = await ctx.guild.bans()
        member_name, member_discriminator = member.split('#')
        for ban_entry in banned_users:
            user = ban_entry.user

            if (user.name, user.discriminator) == (member_name, member_discriminator):
                await ctx.guild.unban(user)
                await ctx.send(f"Ban hammer reversed on {user.name}#{user.discriminator}")   

def setup(client):
    client.add_cog(Moderation(client))
