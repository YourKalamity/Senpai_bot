import discord
from discord.ext import commands
import traceback
import google_trans_new
import googletrans
import requests
import json
import gpiozero
import os
translator = google_trans_new.google_translator()
import urllib
class Utilities(commands.Cog):
    """Useful Utilities"""

    def __init__(self,client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        await self.client.change_presence(activity=discord.Game(name='Say yes to bruhRoo'))
        print(f'[LOGS] : {self.client.user} has connected to Discord!')
    
    @commands.command(help="Returns how long it takes to ping Discord")
    async def ping(self,ctx):
        await ctx.send(f'Took `{round(self.client.latency * 1000)}` milliseconds to reach you, sir!')

    @commands.command(pass_context=True)
    @commands.has_permissions(add_reactions=True,embed_links=True)
    async def help(self,ctx,*cog):
        """Gets all cogs and commands of mine."""
        try:
            if not cog:
                """Cog listing.  What more?"""
                halp=discord.Embed(title='Senpai Help Command',
                                description='Use `senpai help *category*` to find out more about them!\n')
                cogs_desc = ''
                for x in self.client.cogs:
                    cogs_desc += ('{} - {}'.format(x,self.client.cogs[x].__doc__)+'\n')
                halp.add_field(name='Categories',value=cogs_desc[0:len(cogs_desc)-1],inline=False)
                cmds_desc = ''
                for y in self.client.walk_commands():
                    if not y.cog_name and not y.hidden:
                        cmds_desc += ('{} - {}'.format(y.name,y.help)+'\n')
                halp.add_field(name='Uncatergorized Commands',value=cmds_desc[0:len(cmds_desc)-1],inline=False)
                await ctx.send('',embed=halp)
            else:
                """Helps me remind you if you pass too many args."""
                if len(cog) > 1:
                    halp = discord.Embed(title='Error!',description="You passed in too many parameters",color=discord.Color.red())
                    await ctx.send('',embed=halp)
                else:
                    """Command listing within a cog."""
                    found = False
                    for x in self.client.cogs:
                        for y in cog:
                            x = (x.lower()).capitalize()
                            y = (y.lower()).capitalize()
                            if x == y:
                                
                                halp=discord.Embed(title=(cog[0].lower()).capitalize()+' Command Listing',description=self.client.cogs[(cog[0].lower()).capitalize()].__doc__)
                                for c in self.client.get_cog(y).get_commands():
                                    if not c.hidden:
                                        halp.add_field(name=c.name,value=c.help,inline=False)
                                found = True
                    if not found:
                        """Reminds you if that cog doesn't exist."""
                        halp = discord.Embed(title='Error!',description='That category does not exist',color=discord.Color.red())
                    else:
                        await ctx.send('',embed=halp)
        except OSError:
            print("how")
    
    @commands.command()
    async def translate(self, ctx, dstLang, *, string):
        """Translate using **Google Translate API**
        
        **Syntax :**
        `senpai translate {destination_language} {string to be translated}`

        **Example :**
        `senpai translate English ありがとう`
        would translate ありがとう to English"""
        
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

        if translated[2] != None:
            if string != translated[2]:
                embed.set_footer(text="Pronunciation : " + translated[2])
        await ctx.send("",embed=embed)

    @commands.command()
    async def google(self, ctx, *,string):
        await ctx.send("<http://letmegooglethat.com/?q="+urllib.parse.quote(str(string))+">")
        return

    @commands.command()
    async def dsindex(self, ctx, *,category=None):
        if category == None:
            embed=discord.Embed(title="__NightScript's DS Modding index__", color=0xeea4f2 )
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
        x = requests.get("https://raw.githubusercontent.com/NightYoshi370/nightyoshi370.github.io/master/pages/modding/ds-index.md").content
        
        with open("modding.txt", "wb") as theFile:
            theFile.write(x)
        with open("modding.txt","r",errors="ignore") as theFile:
            data = theFile.readlines()

        for string in data:
            if string.lower().rstrip("\n") ==("### "+category).lower():
                hashNumber = 3
                firstNumber = data.index(string)
                break
            elif string.lower().rstrip("\n")==("#### "+category).lower():
                hashNumber = 4
                firstNumber = data.index(string)
                break
            else:
                continue
        if firstNumber == None:
            await ctx.send("Could not find `"+category+"` in NightScript's DS Modding index")
            return   
        counter = firstNumber + 1
        
        fullText = ""
        if hashNumber == 3:
            while True:
                if data[counter].startswith("### "):
                    break
                fullText = fullText + data[counter]
                counter = counter + 1
        if hashNumber == 4:
            while True:
                if data[counter].startswith("### ") or data[counter].startswith("#### "):
                    break
                fullText = fullText + data[counter]
                counter = counter + 1
        if len(fullText) > 1000:

            fullText1, fullText2 = fullText[:len(fullText)//2], fullText[len(fullText)//2:] 
            embed=discord.Embed(title="__NightScript's DS Modding index__", color=0xeea4f2 )
            embed.add_field(name=data[firstNumber], value=fullText1+" ...", inline=False)
            embed.set_footer(text="""Credits to NightScript, RocketRobz and DeadSkullzJr for this guide
Original Guide : https://nightyoshi370.github.io/modding/ds-index""")
            embed2 = discord.Embed(title="__Continued__", color=0xeea4f2 )
            embed2.add_field(name=(data[firstNumber]).rstrip("\n")+" (Continued)", value=fullText2, inline=False)
            embed2.set_footer(text="""Credits to NightScript, RocketRobz and DeadSkullzJr for this guide
Original Guide : https://nightyoshi370.github.io/modding/ds-index""")
            await ctx.send("",embed=embed)
            await ctx.send("",embed=embed2)

        else:
            embed=discord.Embed(title="__NightScript's DS Modding index__", color=0xeea4f2 )
            embed.add_field(name=data[firstNumber], value=fullText, inline=False)
            embed.set_footer(text="""Credits to NightScript, RocketRobz and DeadSkullzJr for this guide
Original Guide : https://nightyoshi370.github.io/modding/ds-index""")
            await ctx.send("",embed=embed)

    @commands.command()
    async def host(self, ctx):
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

      
def setup(client):
    client.add_cog(Utilities(client))
