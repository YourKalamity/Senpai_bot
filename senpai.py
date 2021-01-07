import os
import discord
from discord.ext import commands
import sys


theOwner = 194852876902727680
client = commands.AutoShardedBot(command_prefix = ['senpai ','Senpai ','s!'])
token = "NDI4MjcxNzc5MzA4NjM0MTMy.WrqZLQ.8On8oZ9QXjJEek8wXnoOK-jPqHA"
important_directories = ["ns-ds-index","cogs","downloads"]

client.remove_command('help')

@client.command()
async def goodbye(ctx):
    """Shutdown bot"""
    if ctx.author.id == theOwner:
        await ctx.send("See you later!")
        sys.exit()

@client.command(hidden=True)
async def load(ctx, extension):
    if ctx.author.id == theOwner:
        if extension == "all":
            for filename in os.listdir('./cogs'):
                if filename.endswith('.py'):
                    print("[COGS] : Loading cogs."+filename[:-3])
                    message = await ctx.send("Loading `cogs."+filename[:-3]+"`")
                    try:
                        client.load_extension(f'cogs.{filename[:-3]}')
                        await message.edit(content="Loaded `cogs."+filename[:-3]+"`")
                    except Exception:
                        pass
            await ctx.message.add_reaction('👍')
        else:
            message = await ctx.send("Loading `cogs."+extension+"`")
            client.load_extension(f'cogs.{extension}')
            await ctx.message.add_reaction('👍')
            await message.edit(content="Loaded `cogs."+extension+"`")

@client.command(hidden=True)
async def unload(ctx, extension):
    if ctx.author.id == theOwner:
        if extension == "all":
            for filename in os.listdir('./cogs'):
                if filename.endswith('.py'):
                    print("[COGS] : Unloading cogs."+filename[:-3]) 
                    message = await ctx.send("Unloading `cogs."+filename[:-3]+"`")
                    try:
                        client.unload_extension(f'cogs.{filename[:-3]}')
                        await message.edit(content="Unloaded `cogs."+filename[:-3]+"`")
                    except Exception:
                        pass
            await ctx.message.add_reaction('👍')
        
        else:
            message = await ctx.send("Unloading `cogs."+extension+"`")
            client.unload_extension(f'cogs.{extension}')
            await ctx.message.add_reaction('👍')
            await message.edit(content="Unloaded `cogs."+extension+"`")

@client.command(hidden=True)
async def reload(ctx, extension):
    if ctx.author.id == theOwner:
        if extension == "all":
            for filename in os.listdir('./cogs'):
                if filename.endswith('.py'):
                    print("[COGS] : Reloading cogs."+filename[:-3]) 
                    message = await ctx.send("Reloading `cogs."+filename[:-3]+"`")
                    try:
                        client.unload_extension(f'cogs.{filename[:-3]}')
                        await message.edit(content="Unloaded `cogs."+filename[:-3]+"`")
                        client.load_extension(f'cogs.{filename[:-3]}')
                        await message.edit(content="Loaded `cogs."+filename[:-3]+"`")
                    except commands.ExtensionNotFound:
                        await ctx.send("That command was not found")
            await ctx.message.add_reaction('👍')

        else:
            message = await ctx.send("Reloading `cogs."+extension+"`")
            try:
                client.unload_extension(f'cogs.{extension}')
            except Exception:
                pass
            client.load_extension(f'cogs.{extension}')
            await ctx.message.add_reaction('👍')
            await message.edit(content="Reloaded `cogs."+extension+"`")

        

print("")
print("Welcome to YourKalamity's Discord Bot!")
print("")
os.chdir(os.path.dirname(os.path.abspath(sys.argv[0])))
print("")
print("[LOGS] : Checking for folders...")
for x in important_directories:
    if os.path.exists(x) != True:
        print("[LOGS] : Creating folder `"+x+"`")
        os.mkdir(x)
print("[LOGS] : Connecting to Discord...")
for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        print("[COGS] : Loading cogs." + filename[:-3])
        client.load_extension('cogs.'+filename[:-3])

client.load_extension("jishaku")

client.run(token, reconnect=True)

