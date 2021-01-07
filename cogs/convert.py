import subprocess
from subprocess import Popen
import discord
from discord.ext import commands
import requests
import os
import traceback
import time
from cogs.databases import check_blacklist, create_connection
database = os.getcwd()+r"/db/database.db"
supportedImage = [".bmp", ".gif", ".gif87", ".ico",
    ".icon", ".jpe", ".jpeg", ".jpg", ".jps", ".png"]


class Convert(commands.Cog):
    """Used to convert things"""

    def __init__(self, client):
        self.client = client
        self.conn = create_connection(database)

    @commands.group()
    async def convert(self, ctx):
        """Groud of comamands that convert something to another
        
        __Unlaunch Background__

        `senpai convert unlaunchbg {link}`

        Convert an image at `{link}` to an Unlaunch GIF file
        Can also send an attachment instead of link
        
        __Image Converter__

        `senpai convert {format} {link}`

        Formats : JPG, BMP, GIF, PNG

        Converts image at {link} to {format}
        Can also send an attachment instead of link

        __Boxart Converter__

        `senpai convert boxart {console} {link}`

        Consoles : nds, ds, dsi, gba, gb, gbc, fds, nes, gen, md, sfc, ms, gg

        Converts image at {link} to {console} boxart suitable for use with TWiLight Menu++

        
        """
        if check_blacklist(self.conn, ctx.author.id) != None:
            return
        if ctx.invoked_subcommand is None:
            await ctx.send("That's not a valid `convert` command, sir")
            await ctx.send("Maybe you meant `senpai convert unlaunchbg` ?")

    @convert.command()
    async def unlaunchbg(self, ctx, filelink=None):
        if check_blacklist(self.conn, ctx.author.id) != None:
            return
        supported = False
        if filelink is None:
            if ctx.message.attachments:
                f = ctx.message.attachments[0]
                
                for extension in supportedImage:
                    if f.filename.lower().endswith(extension):
                        supported = True
                        r = requests.get(f.url, allow_redirects=True)
                        fileName = "downloads/" + f.filename
        
        else:
            for extension in supportedImage:
                if filelink.lower().endswith(extension):
                    r = requests.get(filelink, allow_redirects=True)
                    if filelink.find('/'):
                        fileName = "downloads/" + filelink.rsplit('/', 1)[1]
                    supported = True
        
        
        if supported == True:
            start_time = time.time()
            async with ctx.typing():
                oldFileExists = False
            
                outputtext = await ctx.send("`Downloading image...`")

                try:
                    open(fileName, 'wb').write(r.content)
                except Exception:
                    await outputtext.edit(content="`Failed to download image`")
                    return
                await outputtext.edit(content="`Image downloaded...`")


                if (fileName.lower()).endswith('.gif') == False:

                    oldFileName = fileName
                    fileName = "downloads/senpai_converted_" + fileName[10:] + "_.gif"
                    print(oldFileName)
                    print(fileName)
                    oldFileExists = True
                

                    await outputtext.edit(content="`Converting to GIF...`")
                    try:
                        proc = Popen(["magick","convert", oldFileName, fileName],stdout=subprocess.PIPE)
                        ret_val = proc.wait()
                    except Exception:
                        error_message = traceback.format_exc()
                        print(exc)
                        await outputtext.edit(content="`Failed to convert to GIF`")
                        return
                    
                    await outputtext.edit(content="`Converted to GIF...`")


                if fileName.endswith('.gif'):
                    
                    await outputtext.edit(content="`Colour Mapping GIF...`")

                    proc = Popen(["gifsicle",fileName,"-O3", "--no-extensions", "-k", "31" , "#0", "-o", fileName])
                    ret_val = proc.wait()
                    await outputtext.edit(content="`GIF colour mapped...`")

                    await outputtext.edit(content="`Resizing GIF...`")            
                    proc = Popen(["magick", fileName, "-resize", "256x192^","-gravity","center","-extent","256x192", fileName])
                    ret_val = proc.wait()    
                    await outputtext.edit(contents="`GIF resized`")
                    

                    await outputtext.edit(contents="`Optimising GIF size...`")
                    warning = False

                    if os.stat(fileName).st_size > 15000 :
                        while True:
                            x = 0
                            while x < 10:
                                if os.stat(fileName).st_size > 15000 :
                                    proc = Popen(["gifsicle", fileName, "-O3" ,"--no-extensions" ,"--lossy=100" ,"-o", fileName])
                                    ret_val = proc.wait()
                                    x = x + 1
                                else:
                                    break
                                if x == 5:
                                    warning = True
                            break
                    await outputtext.edit(contents="`GIF size optimised`")    


                            
                    await outputtext.edit(contents="`Uploading GIF...`")
                    await ctx.send(file=discord.File(fileName))
                    os.remove(fileName)
                    if oldFileExists:
                        os.remove(oldFileName)
                    await outputtext.edit(content="`All done! Completed in "+str(round(time.time()-start_time,2))+" seconds`")
                    if warning:
                        await ctx.send("`[Warning] : File size was not reduced to less than 15KiB.\n[Warning] : Converted GIF won't work with Unlaunch (try something less complicated)`")
                    return
        else:
            await ctx.send("Unsupported image format, or URL does not end in "+supportedImage)    
        
    
    @convert.command()
    async def bmp(self, ctx, filelink=None):
        if check_blacklist(self.conn, ctx.author.id) != None:
            return
        supported = False
        if filelink is None:
            if ctx.message.attachments:
                f = ctx.message.attachments[0]
                
                for extension in supportedImage:
                    if f.filename.lower().endswith(extension):
                        supported = True
                        r = requests.get(f.url, allow_redirects=True)
                        fileName = "downloads/" + f.filename
        
        else:
            for extension in supportedImage:
                if filelink.lower().endswith(extension):
                    r = requests.get(filelink, allow_redirects=True)
                    if filelink.find('/'):
                        fileName = "downloads/" + filelink.rsplit('/', 1)[1]
                    supported = True


        if supported == True:
            start_time = time.time()
            async with ctx.typing():
                outputtext = await ctx.send("`Downloading image...`")
                try:
                    open(fileName, 'wb').write(r.content)
                except Exception:
                    await outputtext.edit(content="`Failed to download image `")
                    return
                await outputtext.edit(content="`Image downloaded...`")
                if fileName.endswith('.bmp') == False:
                    await outputtext.edit(content="`Converting to BMP...`")
                    newFileName = "senpai_converted_" + fileName + "_.bmp"
                    try:
                        proc = Popen(["magick", "convert", fileName, newFileName])
                        ret_val = proc.wait()
                        proc = Popen(["magick", "convert", newFileName, "-define", "bmp:subtype=RGB565", newFileName])
                        ret_val = proc.wait()
                    except Exception:
                        await outputtext.edit(content="`Failed to convert to BMP`")
                        return
                    await outputtext.edit(content="`Converted to BMP`")
                    await outputtext.edit(content="`Uploading BMP...`")
                    await ctx.send(file=discord.File(newFileName))
                    await outputtext.edit(content="`All done! Completed in "+str(round(time.time()-start_time,2))+" seconds`")
                    os.remove(fileName)
                    os.remove(newFileName)
                    return
                else:
                    await outputtext.edit(content="`You asked me to convert a BMP into a ... BMP`")
                    return
        else:
            await ctx.send("`Unsupported image format, or URL does not end in "+supportedImage+"`")


    @convert.command()
    async def png(self, ctx, filelink=None):
        if check_blacklist(self.conn, ctx.author.id) != None:
            return
        supported = False
        if filelink is None:
            if ctx.message.attachments:
                f = ctx.message.attachments[0]
                
                for extension in supportedImage:
                    if f.filename.lower().endswith(extension):
                        supported = True
                        r = requests.get(f.url, allow_redirects=True)
                        fileName = "downloads/" + f.filename
        
        else:
            for extension in supportedImage:
                if filelink.lower().endswith(extension):
                    r = requests.get(filelink, allow_redirects=True)
                    if filelink.find('/'):
                        fileName = "downloads/" + filelink.rsplit('/', 1)[1]
                    supported = True


        if supported == True:
            start_time = time.time()
            async with ctx.typing():
                outputtext = await ctx.send("`Downloading image...`")
                try:
                    open(fileName, 'wb').write(r.content)
                except Exception:
                    await outputtext.edit(content="`Failed to download image `")
                    return
                await outputtext.edit(content="`Image downloaded...`")
                if fileName.endswith('.png') == False:
                    await outputtext.edit(content="`Converting to PNG...`")
                    newFileName = "senpai_converted_" + fileName + "_.png"
                    try:
                        proc = Popen(["magick", "convert", fileName, newFileName])
                        ret_val = proc.wait()
                    except Exception:
                        await outputtext.edit(content="`Failed to convert to PNG`")
                        return
                    await outputtext.edit(content="`Converted to PNG`")
                    await outputtext.edit(content="`Uploading PNG...`")
                    await ctx.send(file=discord.File(newFileName))
                    await outputtext.edit(content="`All done! Completed in "+str(round(time.time()-start_time,2))+" seconds`")
                    os.remove(fileName)
                    os.remove(newFileName)
                    return
                else:
                    await outputtext.edit(content="`You asked me to convert a PNG into a ... PNG`")
                    return
        else:
            await ctx.send("`Unsupported image format, or URL does not end in "+supportedImage+"`")  

    @convert.command()
    async def gif(self, ctx, filelink=None):
        if check_blacklist(self.conn, ctx.author.id) != None:
            return
        supported = False
        if filelink is None:
            if ctx.message.attachments:
                f = ctx.message.attachments[0]
                
                for extension in supportedImage:
                    if f.filename.lower().endswith(extension):
                        supported = True
                        r = requests.get(f.url, allow_redirects=True)
                        fileName = "downloads/" + f.filename
        
        else:
            for extension in supportedImage:
                if filelink.lower().endswith(extension):
                    r = requests.get(filelink, allow_redirects=True)
                    if filelink.find('/'):
                        fileName = "downloads/" + filelink.rsplit('/', 1)[1]
                    supported = True


        if supported == True:
            start_time = time.time()
            async with ctx.typing():
                outputtext = await ctx.send("`Downloading image...`")
                try:
                    open(fileName, 'wb').write(r.content)
                except Exception:
                    await outputtext.edit(content="`Failed to download image `")
                    return
                await outputtext.edit(content="`Image downloaded...`")
                if fileName.endswith('.gif') == False:
                    await outputtext.edit(content="`Converting to GIF...`")
                    newFileName = "senpai_converted_" + fileName + "_.gif"
                    try:
                        proc = Popen(["magick", "convert", fileName, newFileName])
                        ret_val = proc.wait()
                    except Exception:
                        await outputtext.edit(content="`Failed to convert to GIF`")
                        return
                    await outputtext.edit(content="`Converted to GIF`")
                    await outputtext.edit(content="`Uploading GIF...`")
                    await ctx.send(file=discord.File(newFileName))
                    await outputtext.edit(content="`All done! Completed in "+str(round(time.time()-start_time,2))+" seconds`")
                    os.remove(fileName)
                    os.remove(newFileName)
                    return
                else:
                    await outputtext.edit(content="`You asked me to convert a GIF into a ... GIF`")
                    return
        else:
            await ctx.send("`Unsupported image format, or URL does not end in "+supportedImage+"`")

    @convert.command()
    async def jpeg(self, ctx, filelink=None):
        if check_blacklist(self.conn, ctx.author.id) != None:
            return
        supported = False
        if filelink is None:
            if ctx.message.attachments:
                f = ctx.message.attachments[0]
                
                for extension in supportedImage:
                    if f.filename.lower().endswith(extension):
                        supported = True
                        r = requests.get(f.url, allow_redirects=True)
                        fileName = "downloads/" + f.filename
        
        else:
            for extension in supportedImage:
                if filelink.lower().endswith(extension):
                    r = requests.get(filelink, allow_redirects=True)
                    if filelink.find('/'):
                        fileName = "downloads/" + filelink.rsplit('/', 1)[1]
                    supported = True


        if supported == True:
            start_time = time.time()
            async with ctx.typing():
                outputtext = await ctx.send("`Downloading image...`")
                try:
                    open(fileName, 'wb').write(r.content)
                except Exception:
                    await outputtext.edit(content="`Failed to download image `")
                    return
                await outputtext.edit(content="`Image downloaded...`")
                if fileName.endswith('.jpeg') == False and fileName.endswith('.jpg') == False:
                    await outputtext.edit(content="`Converting to JPEG...`")
                    newFileName = "senpai_converted_" + fileName + "_.jpeg"
                    try:
                        proc = Popen(["magick", "convert", fileName, newFileName])
                        ret_val = proc.wait()
                    except Exception:
                        await outputtext.edit(content="`Failed to convert to JPEG`")
                        return
                    await outputtext.edit(content="`Converted to JPEG`")
                    await outputtext.edit(content="`Uploading JPEG...`")
                    await ctx.send(file=discord.File(newFileName))
                    await outputtext.edit(content="`All done! Completed in "+str(round(time.time()-start_time,2))+" seconds`")
                    os.remove(fileName)
                    os.remove(newFileName)
                    return
                else:
                    await outputtext.edit(content="`You asked me to convert a JPEG into a ... JPEG`")
                    return
        else:
            await ctx.send("`Unsupported image format, or URL does not end in "+supportedImage+"`")        
    
    @convert.group()
    async def boxart(self, ctx):
        if check_blacklist(self.conn, ctx.author.id) != None:
            return
        if ctx.invoked_subcommand is None:
            await ctx.send("That's not a valid `convert boxart` command, sir")

    @boxart.command(aliases=["nds","dsi"])
    async def ds(self, ctx, filelink=None):
        if check_blacklist(self.conn, ctx.author.id) != None:
            return
        supported = False
        if filelink is None:
            if ctx.message.attachments:
                f = ctx.message.attachments[0]
                
                for extension in supportedImage:
                    if f.filename.lower().endswith(extension):
                        supported = True
                        r = requests.get(f.url, allow_redirects=True)
                        fileName = "downloads/" + f.filename
        
        else:
            for extension in supportedImage:
                if filelink.lower().endswith(extension):
                    r = requests.get(filelink, allow_redirects=True)
                    if filelink.find('/'):
                        fileName = "downloads/" + filelink.rsplit('/', 1)[1]
                    supported = True


        if supported == True:
            start_time = time.time()
            async with ctx.typing():
                
                outputtext = await ctx.send("`Downloading image...`")
                try:
                    open(fileName, 'wb').write(r.content)
                except Exception:
                    await outputtext.edit(content="`Failed to download image `")
                    return

                await outputtext.edit(content="`Image downloaded...`")    
                if fileName.endswith('.png') == False:
                    await outputtext.edit(content="`Converting to PNG...`")
                    oldFileName = fileName
                    fileName = "downloads/senpai_converted_" + fileName[10:] + "_.png"
                    proc = Popen(["convert", oldFileName, fileName])
                    ret_val = proc.wait()
                    os.remove(oldFileName)
                    await outputtext.edit(content="`Converted to PNG`")
                
                try:
                    proc = Popen(["magick", fileName,"-resize","128x115\!", fileName])
                    ret_val = proc.wait()
                except Exception:
                    await outputtext.edit(content="`Failed to convert to PNG`")
                    return
                await outputtext.edit(content="`Uploading boxart...`")
                await ctx.send(file=discord.File(fileName))
                await outputtext.edit(content="`All done! Completed in "+str(round(time.time()-start_time,2))+" seconds`")
                os.remove(fileName)
                return

        else:
            await ctx.send("`Unsupported image format, or URL does not end in "+supportedImage+"`")
    

    @boxart.command(aliases=["fds","gbc","gb"])
    async def gba(self, ctx, filelink=None):
        if check_blacklist(self.conn, ctx.author.id) != None:
            return
        supported = False
        if filelink is None:
            if ctx.message.attachments:
                f = ctx.message.attachments[0]
                
                for extension in supportedImage:
                    if f.filename.lower().endswith(extension):
                        supported = True
                        r = requests.get(f.url, allow_redirects=True)
                        fileName = "downloads/" + f.filename
        
        else:
            for extension in supportedImage:
                if filelink.lower().endswith(extension):
                    r = requests.get(filelink, allow_redirects=True)
                    if filelink.find('/'):
                        fileName = "downloads/" + filelink.rsplit('/', 1)[1]
                    supported = True


        if supported == True:
            start_time = time.time()
            async with ctx.typing():
                outputtext = await ctx.send("`Downloading image...`")
                try:
                    open(fileName, 'wb').write(r.content)
                except Exception:
                    await outputtext.edit(content="`Failed to download image `")
                    return

                await outputtext.edit(content="`Image downloaded...`")    
                if fileName.endswith('.png') == False:
                    await outputtext.edit(content="`Converting to PNG...`")
                    oldFileName = fileName
                    fileName = "downloads/senpai_converted_" + fileName[10:] + "_.png"
                    proc = Popen(["convert", oldFileName, fileName])
                    ret_val = proc.wait()
                    os.remove(oldFileName)
                    await outputtext.edit(content="`Converted to PNG`")
                
                try:
                    proc = Popen(["magick", fileName,"-resize","115x115\!", fileName])
                    ret_val = proc.wait()
                except Exception:
                    await outputtext.edit(content="`Failed to convert to PNG`")
                    return
                await outputtext.edit(content="`Uploading boxart...`")
                await ctx.send(file=discord.File(fileName))
                await outputtext.edit(content="`All done! Completed in "+str(round(time.time()-start_time,2))+" seconds`")
                os.remove(fileName)
                return

        else:
            await ctx.send("`Unsupported image format, or URL does not end in "+supportedImage+"`")

    @boxart.command(aliases=["gen","md","sfc","ms","gg"])
    async def nes(self, ctx, filelink=None):
        if check_blacklist(self.conn, ctx.author.id) != None:
            return
        supported = False
        if filelink is None:
            if ctx.message.attachments:
                f = ctx.message.attachments[0]
                
                for extension in supportedImage:
                    if f.filename.lower().endswith(extension):
                        supported = True
                        r = requests.get(f.url, allow_redirects=True)
                        fileName = "downloads/" + f.filename
        
        else:
            for extension in supportedImage:
                if filelink.lower().endswith(extension):
                    r = requests.get(filelink, allow_redirects=True)
                    if filelink.find('/'):
                        fileName = "downloads/" + filelink.rsplit('/', 1)[1]
                    supported = True


        if supported == True:
            start_time = time.time()
            async with ctx.typing():
                    
                outputtext = await ctx.send("`Downloading image...`")
                try:
                    open(fileName, 'wb').write(r.content)
                except Exception:
                    await outputtext.edit(content="`Failed to download image `")
                    return

                await outputtext.edit(content="`Image downloaded...`")    
                if fileName.endswith('.png') == False:
                    await outputtext.edit(content="`Converting to PNG...`")
                    oldFileName = fileName
                    fileName = "downloads/senpai_converted_" + fileName[10:] + "_.png"
                    proc = Popen(["convert", oldFileName, fileName])
                    ret_val = proc.wait()
                    os.remove(oldFileName)
                    await outputtext.edit(content="`Converted to PNG`")
                
                try:
                    proc = Popen(["magick", fileName,"-resize","84x115\!", fileName])
                    ret_val = proc.wait()
                except Exception:
                    await outputtext.edit(content="`Failed to convert to PNG`")
                    return
                await outputtext.edit(content="`Uploading boxart...`")
                await ctx.send(file=discord.File(fileName))
                await outputtext.edit(content="`All done! Completed in "+str(round(time.time()-start_time,2))+" seconds`")
                os.remove(fileName)
                return

        else:
            await ctx.send("`Unsupported image format, or URL does not end in "+supportedImage+"`")
    
    @boxart.command()
    async def snes(self, ctx, filelink=None):
        if check_blacklist(self.conn, ctx.author.id) != None:
            return
        supported = False
        if filelink is None:
            if ctx.message.attachments:
                f = ctx.message.attachments[0]
                
                for extension in supportedImage:
                    if f.filename.lower().endswith(extension):
                        supported = True
                        r = requests.get(f.url, allow_redirects=True)
                        fileName = "downloads/" + f.filename
        
        else:
            for extension in supportedImage:
                if filelink.lower().endswith(extension):
                    r = requests.get(filelink, allow_redirects=True)
                    if filelink.find('/'):
                        fileName = "downloads/" + filelink.rsplit('/', 1)[1]
                    supported = True


        if supported == True:
            start_time = time.time()
            async with ctx.typing():
                    
                outputtext = await ctx.send("`Downloading image...`")
                try:
                    open(fileName, 'wb').write(r.content)
                except Exception:
                    await outputtext.edit(content="`Failed to download image `")
                    return

                await outputtext.edit(content="`Image downloaded...`")    
                if fileName.endswith('.png') == False:
                    await outputtext.edit(content="`Converting to PNG...`")
                    oldFileName = fileName
                    fileName = "downloads/senpai_converted_" + fileName[10:] + "_.png"
                    proc = Popen(["convert", oldFileName, fileName])
                    ret_val = proc.wait()
                    os.remove(oldFileName)
                    await outputtext.edit(content="`Converted to PNG`")
                
                try:
                    proc = Popen(["magick", fileName,"-resize","158x115\!", fileName])
                    ret_val = proc.wait()
                except Exception:
                    await outputtext.edit(content="`Failed to convert to PNG`")
                    return
                await outputtext.edit(content="`Uploading boxart...`")
                await ctx.send(file=discord.File(fileName))
                await outputtext.edit(content="`All done! Completed in "+str(round(time.time()-start_time,2))+" seconds`")
                os.remove(fileName)
                return

        else:
            await ctx.send("`Unsupported image format, or URL does not end in "+supportedImage+"`")
    
    @convert.command()
    async def dsimenu(self,ctx,filelink=None):
        if check_blacklist(self.conn, ctx.author.id) != None:
            return
        supported = False
        if filelink is None:
            if ctx.message.attachments:
                f = ctx.message.attachments[0]
                
                for extension in supportedImage:
                    if f.filename.lower().endswith(extension):
                        supported = True
                        r = requests.get(f.url, allow_redirects=True)
                        fileName = "downloads/" + f.filename
        
        else:
            for extension in supportedImage:
                if filelink.lower().endswith(extension):
                    r = requests.get(filelink, allow_redirects=True)
                    if filelink.find('/'):
                        fileName = "downloads/" + filelink.rsplit('/', 1)[1]
                    supported = True


        if supported == True:
            start_time = time.time()
            async with ctx.typing():
                outputtext = await ctx.send("`Downloading image...`")
                try:
                    open(fileName, 'wb').write(r.content)
                except Exception:
                    await outputtext.edit(content="`Failed to download image `")
                    return
                await outputtext.edit(content="`Image downloaded...`")
                if fileName.endswith('.png') == False:
                    await outputtext.edit(content="`Converting to PNG...`")
                    newFileName = "senpai_converted_" + fileName + "_.png"
                    try:
                        proc = Popen(["magick", "convert", fileName, newFileName])
                        ret_val = proc.wait()
                        oldFileName = fileName
                        fileName = newFileName
                        os.remove(oldFileName)
                        
                    except Exception:
                        await outputtext.edit(content="`Failed to convert to PNG`")
                        return
                    await outputtext.edit(content="`Converted to PNG`")

                process = Popen(["identify", fileName], stdout=subprocess.PIPE)
                stdout = process.communicate()[0]
                identification = ((stdout.decode("utf-8").split())[2]).split("x")
                if int(identification[0]) > 208 or int(identification[1]) > 156:
                    await outputtext.edit(content="`Resizing image...`")
                    try:
                        proc = Popen(["magick", fileName,"-resize","208x156\!", fileName])
                        ret_val = proc.wait()
                    except Exception:
                        await outputtext.edit(content="`Failed to resize`")
                        return
                
                await outputtext.edit(content="`Uploading DSi Menu image...`")
                await ctx.send(file=discord.File(fileName))
                await outputtext.edit(content="`All done! Completed in "+str(round(time.time()-start_time,2))+" seconds`")
                os.remove(fileName)
                return
        else:
            await ctx.send("`Unsupported image format, or URL does not end in "+supportedImage+"`")
        
    @convert.command()
    async def dsmp4(self,ctx,filelink=None):
        if check_blacklist(self.conn, ctx.author.id) != None:
            return
        supported = False
        if filelink is None:
            if ctx.message.attachments:
                f = ctx.message.attachments[0]
                
                for extension in [".mp4",".mov",".wmv",".flv",".avi",".mkv"]:
                    if f.filename.lower().endswith(extension):
                        supported = True
                        r = requests.get(f.url, allow_redirects=True)
                        fileName = "downloads/"+f.filename
        else:
            for extension in [".mp4",".mov",".wmv",".flv",".avi",".mkv"]:
                if filelink.lower().endswith(extension):
                    r = requests.get(filelink, allow_redirects=True)
                    if filelink.find('/'):
                        fileName = "downloads/"+filelink.rsplit('/', 1)[1]
                    supported = True                
        if supported:

            async with ctx.typing():
                start_time = time.time()
                outputtext = await ctx.send("`Downloading video...`")
                print(outputtext)
                try:
                    open(fileName, 'wb').write(r.content)
                except Exception:
                    await outputtext.edit(content="`Failed to download video`")
                    return
                await outputtext.edit(content="`Converting video...`")
                with open(os.devnull, "w") as devnull:
                    output = subprocess.run(['ffmpeg','-y', '-i', fileName, '-f', 'mp4', '-s', '256x144', '-vf', 'colorspace=space=ycgco:primaries=bt709:trc=bt709:range=pc:iprimaries=bt709:iall=bt709', '-dst_range', "1", '-color_range', "2", '-vcodec', 'mpeg4', '-profile:v', "0", '-level', "8", '-b:v', "500000", '-acodec', 'aac', '-ar', "32000", '-b:a', "128000", '-ac', "1", '-slices', "1", '-g', "50", 'downloads/senpai_converted.mp4'],stdout=devnull)
                params = (
                    ('d', 'upload-tool'),
                )

                files = {
                    'file': ('senpai_converted.mp4', open("downloads/senpai_converted.mp4", 'rb')),
                }
                response = requests.post('https://tmp.ninja/api.php', params=params, files=files)
                await ctx.send("""Converted video link {hosted by `tmp.ninja`}
                """+response.content.decode("utf-8"))
                os.remove("downloads/senpai_converted.mp4")
                os.remove(fileName)
                await outputtext.edit(content="`Done! Completed in "+str(round(time.time()-start_time,2))+" seconds`")
        else:
            return
            










def setup(client):
    client.add_cog(Convert(client))
