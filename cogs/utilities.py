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
                            pageNumber = await page_backwards(self,helpbox,pageNumber,reaction,ctx.author,help_pages)
                            start_time = time.time()
                if reaction.emoji.id == 797052228182867968:
                    async for user in reaction.users():
                        if user.id == ctx.author.id:
                            pageNumber = await page_forwards(self,helpbox,pageNumber,reaction,ctx.author,help_pages)
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
        source_files = ["dsi-twl-firm.md","homebrew.md","retail-roms.md","wifi.md"]
        found = False
        link = "https://raw.githubusercontent.com/DS-Homebrew/wiki/main/pages/_en-US/ds-index/"
        search = category.lower()

        while found == False:
            for file_count, source in enumerate(source_files):
                x = requests.get(link+source).content
                with open("downloads/modding_"+source+".txt","wb") as theFile:
                    theFile.write(x)
                with open("downloads/modding_"+source+".txt","r",errors="ignore") as theFile:
                    data = theFile.readlines()
                if search == (source[:-3]).lower():
                    hashNumber = 4
                    firstNumber = 9
                    heading = source[:-3]
                    found = True
                    f_count = file_count
                    break
                else:
                    for count, string in enumerate(data):
                        if string.lower().rstrip("\n") == ("### "+search):
                            hashNumber = 3
                            heading = string
                            firstNumber = count
                            found = True
                            f_count = file_count
                            break
                        elif string.lower().rstrip("\n")==("#### "+search):
                            hashNumber = 4
                            heading = string
                            firstNumber = count
                            found = True
                            f_count = file_count
                            break
                        else:
                            continue
            if found == False and firstNumber == None:
                print("Couldn't find that!")
                return

        counter = firstNumber + 1
        appended_string = ""
        fullText = ""
        ordered_list_counter = 0
        end = False

        with open("downloads/modding_"+source_files[f_count]+".txt","r",errors="ignore") as theFile:
            data = theFile.readlines()
        
        if hashNumber == 3:
            while end == False:
                if counter + 1 == len(data) or data[counter].startswith("### ") or data[counter].startswith("#### "):
                    end = True
                else:
                    appended_string = data[counter]
                    if data[counter].startswith("1. "):
                        ordered_list_counter += 1
                        appended_string = appended_string.replace("1",str(ordered_list_counter),1)
                    else:
                        ordered_list_counter = 0
                    fullText = fullText + appended_string
                    counter += 1
        if hashNumber == 4:
            while end == False:
                if counter + 1 == len(data) or data[counter].startswith("#### "):
                    end = True
                else:
                    appended_string = data[counter]
                    if data[counter].startswith("1. "):
                        ordered_list_counter += 1
                        appended_string = appended_string.replace("1",str(ordered_list_counter),1)
                    else:
                        ordered_list_counter = 0

                    fullText = fullText + appended_string
                    counter += 1

        embed_list = dsindex_embed_generator(fullText,heading,link+source_files[f_count])
        pageNumber = 0
        start_time = time.time()
        dsindexbox = await ctx.send("",embed=embed_list[pageNumber])
        if len(embed_list) != 1:
            await dsindexbox.add_reaction("<:back:797052201431334912>")
            await dsindexbox.add_reaction("<:stop:797089970845515806>")
            await dsindexbox.add_reaction("<:forward:797052228182867968>")
            escape = False
            while time.time() - start_time < 30 and escape != True:
                dsindexbox = await ctx.fetch_message(dsindexbox.id)
                for reaction in dsindexbox.reactions:
                    if reaction.emoji.id == 797089970845515806:
                        async for user in reaction.users():
                            if user.id == ctx.author.id:
                                await reaction.clear()
                                escape = True
                    if reaction.emoji.id == 797052201431334912:
                        async for user in reaction.users():
                            if user.id == ctx.author.id:
                                pageNumber = await page_backwards(self,dsindexbox,pageNumber,reaction,ctx.author,embed_list)
                                start_time = time.time()
                    if reaction.emoji.id == 797052228182867968:
                        async for user in reaction.users():
                            if user.id == ctx.author.id:
                                pageNumber = await page_forwards(self,dsindexbox,pageNumber,reaction,ctx.author,embed_list)
                                start_time = time.time()
            for reaction in dsindexbox.reactions:
                if reaction.me:
                    await reaction.remove(self.client.user)


        

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

async def page_backwards(self,message_box,current_page_number,reaction_to_reset,user,list_of_embeds):
    if current_page_number != 0:
        current_page_number = current_page_number - 1
    await message_box.edit(content=" .",embed=None)
    await message_box.edit(embed=list_of_embeds[current_page_number])
    reaction_emoji = self.client.get_emoji(reaction_to_reset.emoji.id)
    await reaction_to_reset.remove(user)
    await message_box.add_reaction(reaction_emoji)
    return current_page_number

async def page_forwards(self,message_box,current_page_number,reaction_to_reset,user,list_of_embeds):
    if current_page_number != len(list_of_embeds)-1:
        current_page_number = current_page_number + 1
    await message_box.edit(content=" .",embed=None)
    await message_box.edit(embed=list_of_embeds[current_page_number])
    reaction_emoji = self.client.get_emoji(reaction_to_reset.emoji.id)
    await reaction_to_reset.remove(user)
    await message_box.add_reaction(reaction_emoji)
    return current_page_number

def splitter(n, s):
    pieces = s.split(" ")
    return (" ".join(pieces[i:i+n]) for i in range(0, len(pieces), n))

def dsindex_embed_generator(text,title,link):
    split_data = splitter(100,text)
    embeds = []

    for count, section in enumerate(split_data):
        embed = discord.Embed(title="__DS-Homebrew Nintendo DS index__", description=title,color=0xeea4f2,url=link)
        embed.add_field(name=title,value=section,inline=False)
        embed.add_field(name="Credits to:",value="NightScript, EpicPkmn11, RocketRobz and DeadSkullzJr",inline=False)
        embed.set_footer(text="Use the reactions below to change pages!")
        embeds.append(embed)
    return embeds

help_pages = [None,None,None,None,None,None,None]
help_pages[0] = discord.Embed(title="Page 1 / 7", description="Convert related commands",color=0xeea4f2 )
help_pages[0].set_author(name="Senpai Help Command")
help_pages[0].add_field(name="convert unlaunchbg", value="`s!convert unlaunchbg {link}` \n Convert an image at `{link}` to an Unlaunch GIF file\nCan also send an attachment instead of link ", inline=False)
help_pages[0].add_field(name="convert (format)", value="`s!convert {jpg|bmp|gif|png} {link}`\n Converts image at `{link}` to `{format}`", inline=False)
help_pages[0].add_field(name="convert boxart", value="`s!convert boxart {console} {link}` \n Consoles : nds, ds, dsi, gba, gb, gbc, fds, nes, gen, md, sfc, ms, gg\n Converts image at `{link}` to `{console}` boxart\n Suitable for use with TWiLight Menu ++", inline=True)
help_pages[0].add_field(name="convert dsmp4", value="`s!convert dsmp4 {link}`\n Converts video at `{link}` to MPEG4 player for use with Gericom's MPEGPLAYER DSi", inline=False)
help_pages[0].add_field(name="convert video", value="`s!convert video {link}`\n Converts video at `{link}` to mp4", inline=False)
help_pages[0].set_footer(text="Use the reactions below to change pages!")

help_pages[1] = discord.Embed(title="Page 2 / 7", description="GitHub related commands",color=0xeea4f2 )
help_pages[1].set_author(name="Senpai Help Command")
help_pages[1].add_field(name="github info", value="`s!github info {Username/Repo}` \n Returns information about a GitHub repo ", inline=False)
help_pages[1].add_field(name="github latest", value="`s!github latest {Username/Repo}`\n Returns link to latest release of repo", inline=False)
help_pages[1].add_field(name="github user", value="`s!github user {Username}` \n Returns information about a GitHub user", inline=True)
help_pages[1].set_footer(text="Use the reactions below to change pages!")

help_pages[2] = discord.Embed(title="Page 3 / 7", description="Fun commands",color=0xeea4f2 )
help_pages[2].set_author(name="Senpai Help Command")
help_pages[2].add_field(name="slap", value="`s!slap {someone}` \n Slap someone! ", inline=True)
help_pages[2].add_field(name="hug", value="`s!hug {someone}`\n Hug someone!", inline=True)
help_pages[2].add_field(name="pat", value="`s!pat {someone}` \n Give someone a headpat!", inline=True)
help_pages[2].add_field(name="notice", value="`s!notice {someone}` \n Get senpai to finally notice you or someone else!", inline=True)
help_pages[2].add_field(name="zalgofy", value="`s!zalgofy {string}` \n Turns strings into s̰̈́͟t̪̉͘r̯̳͝i̮̅́n̻ͣ̅ģ̼͢ş̙̂", inline=True)
help_pages[2].set_footer(text="Use the reactions below to change pages!")

help_pages[3] = discord.Embed(title="Page 4 / 7", description="Utilies Page 1",color=0xeea4f2 )
help_pages[3].set_author(name="Senpai Help Command")
help_pages[3].add_field(name="ping", value="`s!ping` \n Returns how long it takes to ping Discord", inline=False)
help_pages[3].add_field(name="help", value="`s!help`\n Shows this command", inline=False)
help_pages[3].add_field(name="translate", value="`s!translate {destination} {string}` \n Translates string into `{destination}` language", inline=True)
help_pages[3].add_field(name="google", value="`s!google {string}`\n Teach people how to Google a `{string}`", inline=False)
help_pages[3].set_footer(text="Use the reactions below to change pages!")

help_pages[4] = discord.Embed(title="Page 5 / 7", description="Utilies Page 2",color=0xeea4f2 )
help_pages[4].set_author(name="Senpai Help Command")
help_pages[4].add_field(name="dsindex", value="`s!dsindex {search_query}` \n Searches for {search_query} in NightScript's DS Modding index", inline=False)
help_pages[4].add_field(name="host", value="`s!host`\n Shows information about host running me", inline=False)
help_pages[4].add_field(name="removebg BETA", value="`s!removebg {link}` \n Attempts to remove background of image at `{link}`", inline=True)
help_pages[4].set_footer(text="Use the reactions below to change pages!")

help_pages[5] = discord.Embed(title="Page 6 / 7", description="Support related commands",color=0xeea4f2 )
help_pages[5].set_author(name="Senpai Help Command")
help_pages[5].add_field(name="support", value="`s!support {root|writelock}` \n Returns saved support details", inline=False)
help_pages[5].set_footer(text="Use the reactions below to change pages!")

help_pages[6] = discord.Embed(title="Page 7 / 7", description="iOS",color=0xeea4f2 )
help_pages[6].set_author(name="Senpai Help Command")
help_pages[6].add_field(name="ios jailbreak", value="`s!jailbreak {device_model}` \n Returns link to ios.cfw.guide for device", inline=False)
help_pages[6].add_field(name="ios tweak", value="`s!ios tweak {search_query}` \n Searches parcility for `{search_query}`", inline=False)
help_pages[6].set_footer(text="Use the reactions below to change pages!")


def setup(client):
    client.add_cog(Utilities(client))

