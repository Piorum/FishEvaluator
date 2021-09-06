# bot.py
import os
import math
import uuid
import shutil
import discord
import requests
import pyautogui
from PIL import Image
from pathlib import Path
from pytesseract import *
from dotenv import load_dotenv
from discord.ext import commands
pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

client = commands.Bot(command_prefix='.', help_command=None)

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="gamergunk_tv .help"))
    
@client.command()
async def leaderboardreset(ctx):
    global owners
    global lbr
    lbr = 0
    owners = ['Piorum#0001', 'gamergunk_tv#3174', 'Seever#1775']
    if str(ctx.author) in owners:
        await ctx.send('Valid user send .CONFRIM to reset')
        lbr = 1
    else: 
        print(str(ctx.author) + ' UNAUTHORIZED USER ATTEMPTING LEADERBOARD RESET')
        await ctx.send('INVALID USER, LOCKDOWN COMMENCING, SENDING NUKES, USER BANNED')

        
@client.command()
async def CONFIRM(ctx):
        global owners
        if str(ctx.author) in owners:
            global lbr
            if lbr == 1:
                await ctx.send('Reset Successful')
                def overwrite(Rarity, Place):
                    file = open("Scores/" + Rarity + '/' + Place + ".txt", "w")
                    file.write('0 Nobody')
                    file.close()
                overwrite('Uncommon', 'First')
                overwrite('Uncommon', 'Second')
                overwrite('Uncommon', 'Third')
                overwrite('Rare', 'First')
                overwrite('Rare', 'Second')
                overwrite('Rare', 'Third')
                overwrite('Legendary', 'First')
                overwrite('Legendary', 'Second')
                overwrite('Legendary', 'Third')
                lbr = 0
            else:
                await ctx.send('Please type .leaderboardreset first')

@client.command()
async def leaderboard(ctx):
    fileu1 = open("Scores/Uncommon/First.txt", "r")
    fileu2 = open("Scores/Uncommon/Second.txt", "r")
    fileu3 = open("Scores/Uncommon/Third.txt", "r")
    filer1 = open("Scores/Rare/First.txt", "r")
    filer2 = open("Scores/Rare/Second.txt", "r")
    filer3 = open("Scores/Rare/Third.txt", "r")
    filel1 = open("Scores/Legendary/First.txt", "r")
    filel2 = open("Scores/Legendary/Second.txt", "r")
    filel3 = open("Scores/Legendary/Third.txt", "r")
    await ctx.send('```diff\n' + '-LEGENDARY-\n' + str(filel1.read()) + '\n' + str(filel2.read()) + '\n' + str(filel3.read()) + '```')
    await ctx.send('```diff\n' + '-RARE-\n' + str(filer1.read()) + '\n' + str(filer2.read()) + '\n' + str(filer3.read()) + '```')
    await ctx.send('```diff\n' + '-UNCOMMON-\n' + str(fileu1.read()) + '\n' + str(fileu2.read()) + '\n' + str(fileu3.read()) + '```')
    fileu1.close
    fileu2.close
    fileu3.close
    filer1.close
    filer2.close
    filer3.close
    filel1.close
    filel2.close
    filel3.close
@client.command()
async def help(ctx):
    await ctx.send(".submit - Send this command with an attachment to submit an image.\n.leaderboard - Shows top 3 competitors in all categories.")
@client.command()
async def submit(ctx):
    try:
        url = ctx.message.attachments[0].url
    except IndexError:
        print("Error: No attachments")
        await ctx.send("No attachments detected!")
    else:
        if url[0:26] == "https://cdn.discordapp.com":
            r = requests.get(url, stream=True)
            imageName = '1.png'
            with open(imageName, 'wb') as out_file:
                shutil.copyfileobj(r.raw, out_file)
                
        imgt = Image.open('1.png')
        width, height = imgt.size
        aspect = width / float(height)
        ideal_width = 1920
        ideal_height = 1080
        ideal_aspect = ideal_width / float(ideal_height)
        if aspect > ideal_aspect:
            new_width = int(ideal_aspect * height)
            offset = (width - new_width) / 2
            resize = (offset, 0, width - offset, height)
            imgt = imgt.crop(resize).resize((ideal_width, ideal_height), Image.ANTIALIAS)
            imgt.show()
        elif aspect < ideal_aspect:
            new_height = int(width / ideal_aspect)
            offset = (height - new_height) / 2
            resize = (0, offset, width, height - offset)
            imgt = imgt.crop(resize).resize((ideal_width, ideal_height), Image.ANTIALIAS)
        width, height = imgt.size
        left = width * float(0.592)
        top = height * float(0.595)
        right = width * float(0.844)
        bottom = height * float(0.628)
        img = imgt.crop((left, top, right, bottom))
        new_size=tuple(8*x for x in img.size)
        img = img.resize(new_size, Image.ANTIALIAS)
        

        global F
        global BMI
        global output
        output = pytesseract.image_to_string(img)
        wn = len(output.split())
        def extractdata(a, b, c):
            global F
            global BMI
            global output
            F = output.split()[a]
            wt = output.split()[b]
            wt = wt.rsplit('!')[0]
            wt = wt.rsplit('i')[0]
            wt = wt.rsplit('I')[0]
            wt = wt.rsplit('l')[0]
            W = wt.rsplit('|')[0]
            W = W.replace(')', '.')
            W = W.replace(',', '.')
            ht = output.split()[c]
            H = ht.rsplit('i')[0]
            H = H.replace(')', '.')
            H = H.replace(',', '.')
            bmit = 42*float(W)/float(H)
            bmit = bmit*100
            bmit = math.trunc(bmit)
            BMI = bmit/100
        if wn == 3:
            extractdata(0, 1, 2)
        elif wn == 4:
            extractdata(1, 2, 3)
        elif wn == 5:
            extractdata(2, 3, 4)
        else:
            BMI = 'Weight/Height Not Found'
            Rarity = 'Rarity Not Found'
            F = 'Fish Name Not Found'
            
        common = ['Bass', 'Bluefish', 'Flounder', 'Hake', 'Mackerel', 'Snapper', 'Salmon', 'Perch', 'Pike', 'Trout', 'Sunfish']
        uncommon = ['Snail', 'Catfish', 'Clam', 'Cod', 'Halibut', 'Squid', 'Sturgeon', 'Tadpole', 'Glam']
        rare = ['Fish', 'Eel', 'Frogfish', 'Madtom', 'Oysters', 'Paddlefish', 'Piranha', 'Sculpin', 'Shark', 'Stringray', 'Starfish', 'Swordfish']
        legendary = ['Serpe', 'Albenaja', 'Aquanaja', 'Barb', 'Daemonaja', 'Guardfish', 'Gnufish', 'Mandje']
        if F in common:
            Rarity = 'Common'
        elif F in uncommon:
            Rarity = 'Uncommon'
        elif F in rare:
            Rarity = 'Rare'
        elif F in legendary:
            Rarity = 'Legendary'
        elif F == 'Fish Name Not Found':
            Rarity = 'Fish Name Not Found'
        else:
            Rarity = 'Trash'
        await ctx.send('BMI: ' + str(BMI))
        await ctx.send('Rarity: ' + str(Rarity))
        sendert = ctx.author
        sender = str(sendert).replace(' ', '_')
        
        def checkscore(filescore, Rarity):
            global placing
            if filescore == 0 and Rarity == 'Trash':
                placing = 0
            else:
                file1 = open('Scores/' + Rarity + '/First.txt')
                file2 = open('Scores/' + Rarity + '/Second.txt')
                file3 = open('Scores/' + Rarity + '/Third.txt')
                file1str = file1.read()
                file2str = file2.read()
                file3str = file3.read()
                file1score = file1str.split()[0]
                file1name = file1str.split()[1]
                file2score = file2str.split()[0]
                file2name = file2str.split()[1]
                file3score = file3str.split()[0]
                file3name = file3str.split()[1]
                scoreholders = [file1name, file2name, file3name]
                if str(sender) in str(scoreholders):
                    if float(file1score) < float(filescore):
                        if str(sender) == str(file1name):
                            file1 = open('Scores/' + Rarity + '/First.txt', 'w')
                            file1.write(str(filescore) + ' ' + str(sender))
                            placing = 1
                        elif str(sender) != str(file1name):
                            file1 = open('Scores/' + Rarity + '/First.txt', 'w')
                            file1.write(str(filescore) + ' ' + str(sender))
                            placing = 1
                            file2 = open('Scores/' + Rarity + '/Second.txt', 'w')
                            file2.write(str(file1score) + ' ' + str(file1name))
                            if str(sender) != str(file2name):
                                file3 = open('Scores/' + Rarity + '/Third.txt', 'w')
                                file3.write(str(file2score) + ' ' + str(file2name))
                                fileb = open('Scores/' + Rarity + '/Backup.txt', 'a')
                                fileb.write('\n' + str(file3str))
                                fileb.close()
                    elif float(file2score) < float(filescore):
                        if str(sender) == str(file2name):
                            file1 = open('Scores/' + Rarity + '/Second.txt', 'w')
                            file1.write(str(filescore) + ' ' + str(sender))
                            placing = 2
                        elif str(sender) != str(file2name):
                            file2 = open('Scores/' + Rarity + '/Second.txt', 'w')
                            file2.write(str(filescore) + ' ' + str(sender))
                            placing = 2
                            file3 = open('Scores/' + Rarity + '/Third.txt', 'w')
                            file3.write(str(file2score) + ' ' + str(file2name))
                            fileb = open('Scores/' + Rarity + '/Backup.txt', 'a')
                            fileb.write('\n' + str(file3str))
                            fileb.close()
                    elif float(file3score) < float(filescore):
                        file3 = open('Scores/' + Rarity + '/Third.txt', 'w')
                        file3.write(str(filescore) + ' ' + str(sender))
                        placing = 3
                        fileb = open('Scores/' + Rarity + '/Backup.txt', 'a')
                        fileb.write('\n' + str(file3str))
                        fileb.close()
                else:
                    if float(file1score) < float(filescore):
                        file1 = open('Scores/' + Rarity + '/First.txt', 'w')
                        file1.write(str(filescore) + ' ' + str(sender))
                        placing = 1
                        file2 = open('Scores/' + Rarity + '/Second.txt', 'w')
                        file2.write(str(file1score) + ' ' + str(file1name))
                        file3 = open('Scores/' + Rarity + '/Third.txt', 'w')
                        file3.write(str(file2score) + ' ' + str(file2name))
                        fileb = open('Scores/' + Rarity + '/Backup.txt', 'a')
                        fileb.write('\n' + str(file3str))
                        fileb.close()
                    elif float(file2score) < float(filescore):
                        file2 = open('Scores/' + Rarity + '/Second.txt', 'w')
                        file2.write(str(filescore) + ' ' + str(sender))
                        placing = 2
                        file3 = open('Scores/' + Rarity + '/Third.txt', 'w')
                        file3.write(str(file2score) + ' ' + str(file2name))
                        fileb = open('Scores/' + Rarity + '/Backup.txt', 'a')
                        fileb.write('\n' + str(file3str))
                        fileb.close()
                    elif float(file3score) < float(filescore):
                        file3 = open('Scores/' + Rarity + '/Third.txt', 'w')
                        file3.write(str(filescore) + ' ' + str(sender))
                        placing = 3
                        fileb = open('Scores/' + Rarity + '/Backup.txt', 'a')
                        fileb.write('\n' + str(file3str))
                        fileb.close()
                    else:
                        placing = 4
                    
        if Rarity == 'Legendary':
            path_to_file = 'Scores/Legendary/' + str(sender)
            path = Path(path_to_file)

            if path.is_file():
                file = open(str('Scores/Legendary/') + str(sender), "r")
                scoret = file.read()
                scoret = int(scoret) + 1
                file.close()
                file = open(str('Scores/Legendary/') + str(sender), "w")
                score = str(scoret)
                file.write(score)
                file.close()
            else:
                file = open(str('Scores/Legendary/') + str(sender), "x")
                file.close()
                file = open(str('Scores/Legendary/') + str(sender), "w")
                file.write('1')
                file.close()

            file = open(str('Scores/Legendary/') + str(sender), "r")
            score = str(file.read())
            checkscore(score, 'Legendary')
        
        elif Rarity == 'Rare':
            checkscore(BMI, 'Rare')

        elif Rarity == 'Uncommon':
            checkscore(BMI, 'Uncommon')

        elif Rarity == 'Trash' or 'Common':
            checkscore(0, 'Trash')

    
        if placing == 4:
            await ctx.send("Didn't place, if you think this is an error apply for human verification")
        elif placing == 3:
            await ctx.send('Third place!')
        elif placing == 2:
            await ctx.send('Second place!')
        elif placing == 1:
            await ctx.send('First place! This spot is eligible for prizes!')
        elif placing == 0:
            await ctx.send('Rarity not elligible for prizes, if you think this is an eror apply for human verification')

client.run(TOKEN)
