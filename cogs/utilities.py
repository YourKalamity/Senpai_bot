import discord
from discord.ext import commands
import traceback
import google_trans_new
import googletrans
import requests
import json
import gpiozero
import os
import time
translator = google_trans_new.google_translator()
import urllib
from cogs.databases import check_blacklist, create_connection, add_command_to_log
import asyncio
database = os.getcwd()+r"/db/database.db"



class Utilities(commands.Cog):
    """Useful Utilities"""

    def __init__(self,client):
        self.client = client
        self.conn = create_connection(database)

    @commands.Cog.listener()
    async def on_ready(self):
        await self.client.change_presence(activity=discord.Game(name='Say yes to bruhRoo'))
        print(f'[LOGS] : {self.client.user} has connected to Discord!')

    @commands.Cog.listener()
    async def on_command(self,ctx):
        add_command_to_log(self.conn, ctx)
    
    @commands.command(help="Returns how long it takes to ping Discord")
    async def ping(self,ctx):
        if check_blacklist(self.conn, ctx.author.id) != None:
            return
        await ctx.send(f'Took `{round(self.client.latency * 1000)}` milliseconds to reach you, sir!')

    @commands.command()
    @commands.has_permissions(add_reactions=True,embed_links=True)
    async def help(self,ctx,*,pageNumber=None):
        if check_blacklist(self.conn, ctx.author.id) != None:
            return


        if isinstance(pageNumber,int) != True:
            if pageNumber in ["convert", "convert unlaunchbg","convert dsmp4","convert video"]:
                pageNumber = 1
            elif pageNumber in ["github","github info","github latest", "github user"]:
                pageNumber = 2
            elif pageNumber in ["ping", "help","translate","google"]:
                pageNumber = 3
            elif pageNumber in ["dsindex","host","removebg"]:
                pageNumber = 4
            elif pageNumber in ["support"]:
                pageNumber = 5
            elif pageNumber in ["ios","ios jailbreak","ios tweak"]:
                pageNumber = 6
        
        if pageNumber == None:
            pageNumber = 1

        pageNumber = int(pageNumber) - 1
        start_time = time.time()
        helpbox = await ctx.send("",embed=help_pages[pageNumber])
        await helpbox.add_reaction("<:back:797052201431334912>")
        await helpbox.add_reaction("<:stop:797089970845515806>")
        await helpbox.add_reaction("<:forward:797052228182867968>")
        escape = False
        while time.time() - start_time < 30 and escape != True:
            helpbox = await ctx.fetch_message(helpbox.id)
            for reaction in helpbox.reactions:
                if reaction.emoji.id == 797089970845515806:
                    async for user in reaction.users():
                        if user.id == ctx.author.id:
                            await reaction.clear()
                            escape = True
                if reaction.emoji.id == 797052201431334912:
                    async for user in reaction.users():
                        if user.id == ctx.author.id:
                            pageNumber = await page_backwards(self,helpbox,pageNumber,reaction,ctx.author)
                            start_time = time.time()
                if reaction.emoji.id == 797052228182867968:
                    async for user in reaction.users():
                        if user.id == ctx.author.id:
                            pageNumber = await page_forwards(self,helpbox,pageNumber,reaction,ctx.author)
                            start_time = time.time()
        for reaction in helpbox.reactions:
            if reaction.me:
                await reaction.remove(self.client.user)

        await helpbox.edit(content="This command has timed out - run s!help again")

            



    @commands.command()
    async def translate(self, ctx, dstLang, *, string):
        """Translate using **Google Translate API**
        
        **Syntax :**
        `senpai translate {destination_language} {string to be translated}`

        **Example :**
        `senpai translate English ありがとう`
        would translate ありがとう to English"""
        
        if check_blacklist(self.conn, ctx.author.id) != None:
            return
        detected_language = (translator.detect(string))[0]

        dstLang = dstLang.lower()

        for key, value in googletrans.LANGUAGES.items():
            if value == dstLang:
                dstLang = key

        translated = translator.translate(string, lang_tgt=dstLang,pronounce=True)

        embed=discord.Embed(title="__Senpai Translate__", color=0xeea4f2 )
        embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/737287669687779428/738337344482050098/language.png")
        embed.add_field(name="Detected Language :", value=(googletrans.LANGUAGES[detected_language]).capitalize(), inline=True)
        embed.add_field(name="Translated Language :", value=(googletrans.LANGUAGES[(dstLang).lower()]).capitalize(), inline=True)
        embed.add_field(name="Original :", value=string, inline=False)
        embed.add_field(name="Translated : ", value=translated[0], inline=True)
        embed.set_footer(text="Powered by Google Translate!")

        if translated[2] != None:
            if string != translated[2]:
                embed.set_footer(text="Pronunciation : " + translated[2])
        await ctx.send("",embed=embed)

    @commands.command()
    async def google(self, ctx, *,string):
        if check_blacklist(self.conn, ctx.author.id) != None:
            return
        await ctx.send("<http://letmegooglethat.com/?q="+urllib.parse.quote(str(string))+">")
        return

    @commands.command()
    async def dsindex(self, ctx, *,category=None):
        if check_blacklist(self.conn, ctx.author.id) != None:
            return
        if category == None:
            embed=discord.Embed(title="__NightScript's DS Modding index__", color=0xeea4f2 )
            embed.set_thumbnail(url="https://nightyoshi370.github.io/assets/images/icon.png")
            text = """ 
            This is a command used to grab information from NightScript's DS Modding index, which can be found [here](https://nightyoshi370.github.io/modding/ds-index)""" 
            embed.add_field(name="Information : ", value=text, inline=False)
            embed.add_field(name="Syntax : ", value=r"""`senpai dsindex {title}`
            Ensure it has been spelt correctly""", inline=False)
            text = """
            • WiFi • Nintendo DS WFC Restoration
            • Homebrew • Development
            • Flashcards • DLDI
            • Time Bomb • ARGV Support
            • Retail ROMs • Anti-Piracy
            • CloneBoot • Thumb instructions
            • Save Files • Card Read DMA
            • Donor ROM  • Action Replay Cheats
            • Nintendo DSi/TWL_FIRM of Nintendo 3DS 
            • Setting-up CFW
            • CPU Speeds • Hardmodding
            • Nintendo DSi System Menu
            • Nintendo DSi Slot-1 Access & Blockout
            • Nintendo DSi Camera • Nintendo DSi Bootstage 2"""
            embed.add_field(name="Valid Titles : ", value=text, inline=False)
            embed.set_footer(text="Credits to NightScript, RocketRobz and DeadSkullzJr for this guide")
            await ctx.send("",embed=embed)
            return

        counter = 0
        firstNumber = None
        source_files = ["dsi-twl-firm.md","hardmod.md","homebrew.md","retail-roms.md","wifi.md"]
        found = False
        link = "https://raw.githubusercontent.com/DS-Homebrew/wiki/main/pages/_en-US/ds-index/"
        while found == False:
            for source in source_files:
                x = requests.get(link+source).content
                with open("downloads/modding_"+source+".txt", "wb") as theFile:
                    theFile.write(x)
                with open("downloads/modding_"+source+".txt","r",errors="ignore") as theFile:
                    data = theFile.readlines()

                if category == (source[:-3]).lower():
                    hashNumber = 4
                    firstNumber = 9
                    found = True
                    break
                else:
                    for string in data:
                        if string.lower().rstrip("\n") ==("### "+category).lower():
                            hashNumber = 3
                            heading = string
                            firstNumber = data.index(string)
                            found = True
                            break
                        elif string.lower().rstrip("\n")==("#### "+category).lower():
                            hashNumber = 4
                            firstNumber = data.index(string)
                            found = True
                            break
                        else:
                            continue
            if found == False and firstNumber == None:
                await ctx.send("Could not find `"+category+"` in NightScript's DS modding index")
                return

        counter = firstNumber + 1
        appended_string = ""
        fullText = ""
        ordered_list_counter = 0
        if hashNumber == 3:
            while True:
                if counter + 1 == len(data) or data[counter].startswith("### ") or data[counter].startswith("#### "):
                    break

                appended_string = data[counter]
                if data[counter].startswith("1. "):
                    ordered_list_counter += 1
                    appended_string = appended_string.replace("1",str(ordered_list_counter),1)
                else:
                    ordered_list_counter = 0

                fullText = fullText + appended_string
                counter = counter + 1
        if hashNumber == 4:
            while True:
                if counter + 1 == len(data) or data[counter].startswith("#### "):
                    break
                appended_string = data[counter]
                if data[counter].startswith("1. "):
                    ordered_list_counter += 1
                    appended_string = appended_string.replace("1",str(ordered_list_counter),1)
                elif data[counter].startswith("### "):
                    ordered_list_counter = 0
                    appended_string = "**" + appended_string[4:] + "**"
                else:
                    ordered_list_counter = 0
                fullText = fullText + appended_string
                counter = counter + 1
                    

        if len(fullText) > 1000:

            fullText1, fullText2 = fullText[:len(fullText)//2], fullText[len(fullText)//2:] 
            embed=discord.Embed(title="**NightScript's DS Modding index**", color=0xeea4f2 )
            embed.set_thumbnail(url="https://nightyoshi370.github.io/assets/images/icon.png")
            embed.add_field(name=data[firstNumber], value=fullText1+" ...", inline=False)
            embed.set_footer(text="""Credits to NightScript, EpicPkmn11, RocketRobz and DeadSkullzJr for this guide
Original Guide : [https://wiki.ds-homebrew.com/ds-index/](https://wiki.ds-homebrew.com/ds-index/)""")
            embed2 = discord.Embed(title="__Continued__", color=0xeea4f2 )
            embed2.set_thumbnail(url="https://nightyoshi370.github.io/assets/images/icon.png")
            embed2.add_field(name=(data[firstNumber]).rstrip("\n")+" (Continued)", value=fullText2, inline=False)
            embed2.set_footer(text="""Credits to NightScript, EpicPkmn11, RocketRobz and DeadSkullzJr for this guide
Original Guide : [https://wiki.ds-homebrew.com/ds-index/](https://wiki.ds-homebrew.com/ds-index/)""")
            await ctx.send("",embed=embed)
            await ctx.send("",embed=embed2)

        else:
            embed=discord.Embed(title="__NightScript's DS Modding index__", color=0xeea4f2 )
            embed.set_thumbnail(url="https://nightyoshi370.github.io/assets/images/icon.png")
            embed.add_field(name=data[firstNumber], value=fullText, inline=False)
            embed.set_footer(text="""Credits to NightScript, EpicPkmn11, RocketRobz and DeadSkullzJr for this guide
Original Guide : [https://wiki.ds-homebrew.com/ds-index/](https://wiki.ds-homebrew.com/ds-index/)""")
            await ctx.send("",embed=embed)

    @commands.command()
    async def host(self, ctx):
        if check_blacklist(self.conn, ctx.author.id) != None:
            return
        """List details about the server I am being hosted on"""
        embed=discord.Embed(title="Senpai's Host Machine Info", color=0xeea4f2)
        embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/737287669687779428/738732946189713469/6edea84dffc69d2c190c427be484143c.png")
        embed.add_field(name="Local Hostname : ", value="KalamPi2B", inline=True)
        embed.add_field(name="Host :", value="Raspberry Pi 2B+", inline=False)
        embed.add_field(name="Processor :", value="ARM v7 BCM2836",inline=True)
        embed.add_field(name="Cores :", value="4@1.1Ghz",inline=False)
        embed.add_field(name="RAM Size :", value="1GB",inline=True)
        embed.add_field(name="Ping :", value=str(round(self.client.latency * 1000)) + "ms",inline=False)
        embed.add_field(name="Current CPU temperature :", value=str(gpiozero.CPUTemperature().temperature) +"°Celsius",inline=True)
        await ctx.send("",embed=embed)
    
    @commands.command()
    async def removebg(self, ctx, image_link=None):

        if check_blacklist(self.conn, ctx.author.id) != None:
            return

        if image_link is None:
            if ctx.message.attachments:
                print(ctx.message.attachments[0])
                image_link = ctx.message.attachments[0].url

        account_details = json.loads(requests.get("https://api.remove.bg/v1.0/account",headers={'X-Api-Key':"WWbJ5BmGBjFk4eqMVpKYrdWH"}).content)


        if account_details["data"]["attributes"]["api"]["free_calls"] > 0:

            response = requests.post(
                'https://api.remove.bg/v1.0/removebg',
            data={
                'image_url': image_link,
                'size': 'auto'
            },
            headers = {'X-Api-Key': 'WWbJ5BmGBjFk4eqMVpKYrdWH'}
                )
            if response.status_code == requests.codes.ok:
                with open("Senpai-BG-removed.png","wb") as out:
                    out.write(response.content)
                await ctx.send(file=discord.File("Senpai-BG-removed.png"))
                os.remove("Senpai-BG-removed.png")
                return
            else:
                await ctx.send("`Error: "+ response.status_code+response.text+"`")
                return
        else:
            await ctx.send("`Error, daily limit reached`")
            return

async def page_backwards(self,message_box,current_page_number,reaction_to_reset,user):
    if current_page_number != 0:
        current_page_number = current_page_number - 1
    await message_box.edit(content=" .",embed=None)
    await message_box.edit(embed=help_pages[current_page_number])
    reaction_emoji = self.client.get_emoji(reaction_to_reset.emoji.id)
    await reaction_to_reset.remove(user)
    await message_box.add_reaction(reaction_emoji)
    return current_page_number

async def page_forwards(self,message_box,current_page_number,reaction_to_reset,user):
    if current_page_number != 5:
        current_page_number = current_page_number + 1
    await message_box.edit(content=" .",embed=None)
    await message_box.edit(embed=help_pages[current_page_number])
    reaction_emoji = self.client.get_emoji(reaction_to_reset.emoji.id)
    await reaction_to_reset.remove(user)
    await message_box.add_reaction(reaction_emoji)
    return current_page_number


help_pages = [None,None,None,None,None,None]

help_pages[0] = discord.Embed(title="Page 1 / 6", description="Convert related commands",color=0xeea4f2 )
help_pages[0].set_author(name="Senpai Help Command")
help_pages[0].add_field(name="convert unlaunchbg", value="`s!convert unlaunchbg {link}` \n Convert an image at `{link}` to an Unlaunch GIF file\nCan also send an attachment instead of link ", inline=False)
help_pages[0].add_field(name="convert (format)", value="`s!convert {jpg|bmp|gif|png} {link}`\n Converts image at `{link}` to `{format}`", inline=False)
help_pages[0].add_field(name="convert boxart", value="`s!convert boxart {console} {link}` \n Consoles : nds, ds, dsi, gba, gb, gbc, fds, nes, gen, md, sfc, ms, gg\n Converts image at `{link}` to `{console}` boxart\n Suitable for use with TWiLight Menu ++", inline=True)
help_pages[0].add_field(name="convert dsmp4", value="`s!convert dsmp4 {link}`\n Converts video at `{link}` to MPEG4 player for use with Gericom's MPEGPLAYER DSi", inline=False)
help_pages[0].add_field(name="convert video", value="`s!convert video {link}`\n Converts video at `{link}` to mp4", inline=False)
help_pages[0].set_footer(text="Use the reactions below to change pages!")

help_pages[1] = discord.Embed(title="Page 2 / 6", description="GitHub related commands",color=0xeea4f2 )
help_pages[1].set_author(name="Senpai Help Command")
help_pages[1].add_field(name="github info", value="`s!github info {Username/Repo}` \n Returns information about a GitHub repo ", inline=False)
help_pages[1].add_field(name="github latest", value="`s!github latest {Username/Repo}`\n Returns link to latest release of repo", inline=False)
help_pages[1].add_field(name="github user", value="`s!github user {Username}` \n Returns information about a GitHub user", inline=True)
help_pages[1].set_footer(text="Use the reactions below to change pages!")

help_pages[2] = discord.Embed(title="Page 3 / 6", description="Utilies Page 1",color=0xeea4f2 )
help_pages[2].set_author(name="Senpai Help Command")
help_pages[2].add_field(name="ping", value="`s!ping` \n Returns how long it takes to ping Discord", inline=False)
help_pages[2].add_field(name="help", value="`s!help`\n Shows this command", inline=False)
help_pages[2].add_field(name="translate", value="`s!translate {destination} {string}` \n Translates string into `{destination}` language", inline=True)
help_pages[2].add_field(name="google", value="`s!google {string}`\n Teach people how to Google a `{string}`", inline=False)
help_pages[2].set_footer(text="Use the reactions below to change pages!")

help_pages[3] = discord.Embed(title="Page 4 / 6", description="Utilies Page 2",color=0xeea4f2 )
help_pages[3].set_author(name="Senpai Help Command")
help_pages[3].add_field(name="dsindex", value="`s!dsindex {search_query}` \n Searches for {search_query} in NightScript's DS Modding index", inline=False)
help_pages[3].add_field(name="host", value="`s!host`\n Shows information about host running me", inline=False)
help_pages[3].add_field(name="removebg BETA", value="`s!removebg {link}` \n Attempts to remove background of image at `{link}`", inline=True)
help_pages[3].set_footer(text="Use the reactions below to change pages!")

help_pages[4] = discord.Embed(title="Page 5 / 6", description="Support related commands",color=0xeea4f2 )
help_pages[4].set_author(name="Senpai Help Command")
help_pages[4].add_field(name="support", value="`s!support {root|writelock}` \n Returns saved support details", inline=False)
help_pages[4].set_footer(text="Use the reactions below to change pages!")

help_pages[5] = discord.Embed(title="Page 6 / 6", description="iOS",color=0xeea4f2 )
help_pages[5].set_author(name="Senpai Help Command")
help_pages[5].add_field(name="ios jailbreak", value="`s!jailbreak {device_model}` \n Returns link to ios.cfw.guide for device", inline=False)
help_pages[5].add_field(name="ios tweak", value="`s!ios tweak {search_query}` \n Searches parcility for `{search_query}`", inline=False)
help_pages[5].set_footer(text="Use the reactions below to change pages!")


def setup(client):
    client.add_cog(Utilities(client))

