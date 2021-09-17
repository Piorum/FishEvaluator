import os
import cv2
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
from discord.ext.commands import CommandNotFound
pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

client = commands.Bot(command_prefix='.', help_command=None)

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="gamergunk_tv .help"))

global admin

@client.command() 
async def setup(ctx):
    created = False
    serverid = str(ctx.guild.id)
    pathrarities = ['Legendary', 'Rare', 'Uncommon']
    pathplaces = ['First', 'Second', 'Third', 'Backup', 'Overflow']
    for rarity in pathrarities:
        Dirpath = 'Scores/' + serverid + '/' + rarity
        isDir = os.path.isdir(str(Dirpath))
        if isDir == False:
            os.makedirs(Dirpath)
        for place in pathplaces:
            path = 'Scores/' + serverid + '/' + rarity + '/' + place + '.txt.'
            isFile = os.path.isfile(str(path))
            if isFile == False:
                file = open(str(path), 'x')
                file.close()
                file = open(str(path), 'w')
                file.write('0 Nobody')
        path = 'Scores/' + serverid + '/' + 'admins.txt'
        isFile = os.path.isfile(str(path))
        if isFile == False:
            file = open(str(path), 'x')
            created = True
            file.close()
            file = open(str(path), 'w')
            file.write('Piorum#0001')
            file.close()
    if created == True:
        await ctx.send('Setup Complete')
    if created == False:
        await ctx.send('Setup Already Performed')

@client.command()
async def addadmin(ctx, *, msg):
    sendert = ctx.author
    sender = str(sendert).replace(' ', '_')
    global admin
    file = open('Scores/' + str(ctx.guild.id) + '/admins.txt', 'r')
    admin = str(file.read().split())
    adminperm = ctx.author.guild_permissions.administrator
    if adminperm == True:
        dirpath = 'Scores/' + str(ctx.guild.id) + '/admins.txt'
        isDir = os.path.isdir(dirpath)
        if isDir == True:
            file = open(dirpath, 'a')
            file.write(sender + ' ')
    if sender in admin:
        msg = msg.replace('<@!', '')
        msg = msg.replace('>', '')
        try:
            username = await client.fetch_user(msg)
            username = str(username).replace(' ', '_')
            file = open('Scores/' + str(ctx.guild.id) + '/admins.txt', 'a')
            file.write(username + ' ')
            file.close()
            added = True
        except:
            username = msg
            pass
        if added == True:
            await ctx.send('User added.')

@client.command()
async def adminhelp(ctx):
    sendert = ctx.author
    sender = str(sendert).replace(' ', '_')
    global admin
    file = open('Scores/' + str(ctx.guild.id) + '/admins.txt', 'r')
    admin = str(file.read().split())
    adminperm = ctx.author.guild_permissions.administrator
    if adminperm == True:
        dirpath = 'Scores/' + str(ctx.guild.id) + '/admins.txt'
        isDir = os.path.isdir(dirpath)
        if isDir == True:
            file = open(dirpath, 'a')
            file.write(sender + ' ')
    if sender in admin:
        await ctx.send('.leaderboardreset - Usage(.leaderboardreset)\n.addadmin - Usage(.addadmin @User)\n.submit Manual - Usage(.submit Manual Fishname Weight Length @User)\n---[Fishname must be last part of the name if two words EX: use Serpe for Abaia Serpe, Clam for Clam] \n.invalidate - Usage(.invalidate Rarity Placing)')
    else:
        await ctx.send('Not in admin list')
    

@client.command()
async def leaderboardreset(ctx):
    sendert = ctx.author
    sender = str(sendert).replace(' ', '_')
    global admin
    file = open('Scores/' + str(ctx.guild.id) + '/admins.txt', 'r')
    admin = str(file.read().split())
    adminperm = ctx.author.guild_permissions.administrator
    if adminperm == True:
        dirpath = 'Scores/' + str(ctx.guild.id) + '/admins.txt'
        isDir = os.path.isdir(dirpath)
        if isDir == True:
            file = open(dirpath, 'a')
            file.write(sender + ' ')
    global lbr
    lbr = 0
    if sender in admin:
        await ctx.send('Valid user send .CONFRIM to reset')
        lbr = 1
    else: 
        print(sender + ' UNAUTHORIZED USER ATTEMPTING LEADERBOARD RESET')
        await ctx.send('INVALID USER, LOCKDOWN COMMENCING, SENDING NUKES, USER BANNED')

        
@client.command()
async def CONFIRM(ctx):
    sendert = ctx.author
    sender = str(sendert).replace(' ', '_')
    global admin
    file = open('Scores/' + str(ctx.guild.id) + '/admins.txt', 'r')
    admin = str(file.read().split())
    adminperm = ctx.author.guild_permissions.administrator
    if adminperm == True:
        dirpath = 'Scores/' + str(ctx.guild.id) + '/admins.txt'
        isDir = os.path.isdir(dirpath)
        if isDir == True:
            file = open(dirpath, 'a')
            file.write(sender + ' ')
    if str(ctx.author) in admin:
        global lbr
        if lbr == 1:
            await ctx.send('Reset Successful')
            def overwrite(Rarity, Place):
                file = open("Scores/" + str(ctx.guild.id) + '/' + Rarity + '/' + Place + ".txt", "w")
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
    fileu1 = open("Scores/" + str(ctx.guild.id) + "/Uncommon/First.txt", "r")
    fileu2 = open("Scores/" + str(ctx.guild.id) + "/Uncommon/Second.txt", "r")
    fileu3 = open("Scores/" + str(ctx.guild.id) + "/Uncommon/Third.txt", "r")
    filer1 = open("Scores/" + str(ctx.guild.id) + "/Rare/First.txt", "r")
    filer2 = open("Scores/" + str(ctx.guild.id) + "/Rare/Second.txt", "r")
    filer3 = open("Scores/" + str(ctx.guild.id) + "/Rare/Third.txt", "r")
    filel1 = open("Scores/" + str(ctx.guild.id) + "/Legendary/First.txt", "r")
    filel2 = open("Scores/" + str(ctx.guild.id) + "/Legendary/Second.txt", "r")
    filel3 = open("Scores/" + str(ctx.guild.id) + "/Legendary/Third.txt", "r")
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
    await ctx.send(".submit - Send this command with an attachment to submit an image.\n.leaderboard - Shows top 3 competitors in all categories.\n.setup - Run this command to setup files for saving scores.\n.adminhelp - Help command for commands only usable by admins.")
@client.command()
async def submit(ctx, *, msg=''):
    global F
    global BMI
    sendert = ctx.author
    sender = str(sendert).replace(' ', '_')
    global admin
    file = open('Scores/' + str(ctx.guild.id) + '/admins.txt', 'r')
    admin = str(file.read().split())
    adminperm = ctx.author.guild_permissions.administrator
    if adminperm == True:
        dirpath = 'Scores/' + str(ctx.guild.id) + '/admins.txt'
        isDir = os.path.isdir(dirpath)
        if isDir == True:
            file = open(dirpath, 'a')
            file.write(sender + ' ')
    global output
    def extractdata(a, b, c):
        global F
        global BMI
        global output
        print(output)
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
    if msg != '':
        sendert = ctx.author
        sender = str(sendert).replace(' ', '_')
        if sender in admin:
            if msg.split()[0] == 'Manual':
                wn = len(msg.split())
                if wn == 5:
                    F = msg.split()[1]
                    W = msg.split()[2]
                    H = msg.split()[3]
                    sender = str(msg.split()[4])
                    sender = sender.replace('<@!', '')
                    sender = sender.replace('>', '')
                    sender = await client.fetch_user(sender)
                    output = (F + ' ' + W + 'lb ' + H + 'in')
                    extractdata(0, 1, 2)
                else:
                    await ctx.send('Expected 5 Variables, Got ' + str(wn))
        else:
            await ctx.send('Submit with no message')
    else:
        sendert = ctx.author
        sender = str(sendert).replace(' ', '_')
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
            output = pytesseract.image_to_string(img)
            wn = len(output.split())
            if wn == 3:
                extractdata(0, 1, 2)
            elif wn == 4:
                extractdata(1, 2, 3)
            elif wn == 5:
                extractdata(2, 3, 4)
            else:
                print('seen output: ' + output)
                BMI = 'Weight/Height Not Found'
                Rarity = 'Rarity Not Found'
                F = 'Fish Name Not Found'
                
    common = ['Bass', 'Bluefish', 'Flounder', 'Hake', 'Mackerel', 'Snapper', 'Salmon', 'Perch', 'Pike', 'Trout', 'Sunfish']
    uncommon = ['Snail', 'Catfish', 'Clam', 'Cod', 'Halibut', 'Squid', 'Sturgeon', 'Tadpole', 'Glam']
    rare = ['Fish', 'Eel', 'Frogfish', 'Madtom', 'Oyster', 'Paddlefish', 'Piranha', 'Sculpin', 'Shark', 'Stringray', 'Starfish', 'Swordfish']
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
    await ctx.send('BMI: ' + str(BMI) + '\nRarity: ' + str(Rarity))
    
    def checkscore(filescore, Rarity):
        global placing
        if filescore == 0 and Rarity == 'Trash':
            placing = 0
        else:
            file1 = open('Scores/' + str(ctx.guild.id) + '/' + Rarity + '/First.txt')
            file2 = open('Scores/' + str(ctx.guild.id) + '/' + Rarity + '/Second.txt')
            file3 = open('Scores/' + str(ctx.guild.id) + '/' + Rarity + '/Third.txt')
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
                        file1 = open('Scores/' + str(ctx.guild.id) + '/' + Rarity + '/First.txt', 'w')
                        file1.write(str(filescore) + ' ' + str(sender))
                        placing = 1
                    elif str(sender) != str(file1name):
                        file1 = open('Scores/' + str(ctx.guild.id) + '/' + Rarity + '/First.txt', 'w')
                        file1.write(str(filescore) + ' ' + str(sender))
                        placing = 1
                        file2 = open('Scores/' + str(ctx.guild.id) + '/' + Rarity + '/Second.txt', 'w')
                        file2.write(str(file1score) + ' ' + str(file1name))
                        if str(sender) != str(file2name):
                            file3 = open('Scores/' + str(ctx.guild.id) + '/' + Rarity + '/Third.txt', 'w')
                            file3.write(str(file2score) + ' ' + str(file2name))
                            fileb = open('Scores/' + str(ctx.guild.id) + '/' + Rarity + '/Backup.txt', 'a')
                            fileb.write('\n' + str(file3str))
                            fileb.close()
                elif float(file2score) < float(filescore):
                    if str(sender) == str(file2name):
                        file1 = open('Scores/' + str(ctx.guild.id) + '/' + Rarity + '/Second.txt', 'w')
                        file1.write(str(filescore) + ' ' + str(sender))
                        placing = 2
                    elif str(sender) != str(file2name):
                        file2 = open('Scores/' + str(ctx.guild.id) + '/' + Rarity + '/Second.txt', 'w')
                        file2.write(str(filescore) + ' ' + str(sender))
                        placing = 2
                        file3 = open('Scores/' + str(ctx.guild.id) + '/' + Rarity + '/Third.txt', 'w')
                        file3.write(str(file2score) + ' ' + str(file2name))
                        fileb = open('Scores/' + str(ctx.guild.id) + '/' + Rarity + '/Backup.txt', 'a')
                        fileb.write('\n' + str(file3str))
                        fileb.close()
                elif float(file3score) < float(filescore):
                    file3 = open('Scores/' + str(ctx.guild.id) + '/' + Rarity + '/Third.txt', 'w')
                    file3.write(str(filescore) + ' ' + str(sender))
                    placing = 3
                    fileb = open('Scores/' + str(ctx.guild.id) + '/' + Rarity + '/Backup.txt', 'a')
                    fileb.write('\n' + str(file3str))
                    fileb.close()
                elif float(file3score) == float(filescore):
                    file4 = open('Scores/' + str(ctx.guild.id) + '/' + Rarity + '/Overflow.txt', 'a')
                    file4.write(str(filescore) + ' ' + str(sender) + '\n')
                    placing = 5
                    file4.close()
            else:
                if float(file1score) < float(filescore):
                    file1 = open('Scores/' + str(ctx.guild.id) + '/' + Rarity + '/First.txt', 'w')
                    file1.write(str(filescore) + ' ' + str(sender))
                    placing = 1
                    file2 = open('Scores/' + str(ctx.guild.id) + '/' + Rarity + '/Second.txt', 'w')
                    file2.write(str(file1score) + ' ' + str(file1name))
                    file3 = open('Scores/' + str(ctx.guild.id) + '/' + Rarity + '/Third.txt', 'w')
                    file3.write(str(file2score) + ' ' + str(file2name))
                    fileb = open('Scores/' + str(ctx.guild.id) + '/' + Rarity + '/Backup.txt', 'a')
                    fileb.write('\n' + str(file3str))
                    fileb.close()
                elif float(file2score) < float(filescore):
                    file2 = open('Scores/' + str(ctx.guild.id) + '/' + Rarity + '/Second.txt', 'w')
                    file2.write(str(filescore) + ' ' + str(sender))
                    placing = 2
                    file3 = open('Scores/' + str(ctx.guild.id) + '/' + Rarity + '/Third.txt', 'w')
                    file3.write(str(file2score) + ' ' + str(file2name))
                    fileb = open('Scores/' + str(ctx.guild.id) + '/' + Rarity + '/Backup.txt', 'a')
                    fileb.write('\n' + str(file3str))
                    fileb.close()
                elif float(file3score) < float(filescore):
                    file3 = open('Scores/' + str(ctx.guild.id) + '/' + Rarity + '/Third.txt', 'w')
                    file3.write(str(filescore) + ' ' + str(sender))
                    placing = 3
                    fileb = open('Scores/' + str(ctx.guild.id) + '/' + Rarity + '/Backup.txt', 'a')
                    fileb.write('\n' + str(file3str))
                    fileb.close()
                elif float(file3score) == float(filescore):
                    file4 = open('Scores/' + str(ctx.guild.id) + '/' + Rarity + '/Overflow.txt', 'a')
                    file4.write(str(filescore) + ' ' + str(sender) + '\n')
                    placing = 5
                    file4.close()
                else:
                    placing = 4
                
    if Rarity == 'Legendary':
        path_to_file = 'Scores/' + str(ctx.guild.id) + '/Legendary/' + str(sender)
        path = Path(path_to_file)

        if path.is_file():
            file = open(str('Scores/' + str(ctx.guild.id) + '/Legendary/') + str(sender), "r")
            scoret = file.read()
            scoret = int(scoret) + 1
            file.close()
            file = open(str('Scores/' + str(ctx.guild.id) + '/Legendary/') + str(sender), "w")
            score = str(scoret)
            file.write(score)
            file.close()
        else:
            file = open(str('Scores/' + str(ctx.guild.id) + '/Legendary/') + str(sender), "x")
            file.close()
            file = open(str('Scores/' + str(ctx.guild.id) + '/Legendary/') + str(sender), "w")
            file.write('1')
            file.close()

        file = open(str('Scores/' + str(ctx.guild.id) + '/Legendary/') + str(sender), "r")
        score = str(file.read())
        checkscore(score, 'Legendary')
    
    elif Rarity == 'Rare':
        checkscore(BMI, 'Rare')

    elif Rarity == 'Uncommon':
        checkscore(BMI, 'Uncommon')

    elif Rarity == 'Trash' or 'Common':
        checkscore(0, 'Trash')


    if placing == 5:
        await ctx.send("Tied for 3rd added to overflow")
    elif placing == 4:
        await ctx.send("Didn't place, if you think this is an error apply for human verification")
    elif placing == 3:
        await ctx.send('Third place!')
    elif placing == 2:
        await ctx.send('Second place!')
    elif placing == 1:
        await ctx.send('First place! This spot is eligible for prizes!')
    elif placing == 0:
        await ctx.send('Rarity not elligible for prizes, if you think this is an eror apply for human verification')

@client.command()
async def invalidate(ctx, *, msg):
    sendert = ctx.author
    sender = str(sendert).replace(' ', '_')
    global admin
    file = open('Scores/' + str(ctx.guild.id) + '/admins.txt', 'r')
    admin = str(file.read().split())
    adminperm = ctx.author.guild_permissions.administrator
    if adminperm == True:
        dirpath = 'Scores/' + str(ctx.guild.id) + '/admins.txt'
        isDir = os.path.isdir(dirpath)
        if isDir == True:
            file = open(dirpath, 'a')
            file.write(sender + ' ')
    if str(ctx.author) in admin:
        Rarity = str(msg.split()[0])
        Place = str(msg.split()[1])
        Rarities = ['Uncommon', 'Rare', 'Legendary']
        if Rarity in Rarities:
            file1 = open('Scores/' + str(ctx.guild.id) + '/' + Rarity + '/First.txt', 'r')
            file2 = open('Scores/' + str(ctx.guild.id) + '/' + Rarity + '/Second.txt', 'r')
            file3 = open('Scores/' + str(ctx.guild.id) + '/' + Rarity + '/Third.txt', 'r')
            file1str = file1.read()
            file2str = file2.read()
            file3str = file3.read()
            file1.close
            file2.close
            file3.close
            file1 = open('Scores/' + str(ctx.guild.id) + '/' + Rarity + '/First.txt', 'w')
            file2 = open('Scores/' + str(ctx.guild.id) + '/' + Rarity + '/Second.txt', 'w')
            file3 = open('Scores/' + str(ctx.guild.id) + '/' + Rarity + '/Third.txt', 'w')
            if Place == 'First':
                file1.write(file2str)
                file2.write(file3str)
                file3.write('0 Nobody')
                await ctx.send('Invalidated ' + Rarity + ' First Place.')
            elif Place == 'Second':
                file1.write(file1str)
                file2.write(file3str)
                file3.write('0 Nobody')
                await ctx.send('Invalidated ' + Rarity + ' Second Place.')
            elif Place == 'Third':
                file1.write(file1str)
                file2.write(file2str)
                file3.write('0 Nobody')
                await ctx.send('Invalidated ' + Rarity + ' Third Place.')
            else:
                await ctx.send('Invalid Place')
            file1.close
            file2.close
            file3.close
        else:
         await ctx.send('Invalid Rarity')
        
    else:
        await ctx.send('INVALID USER, LOCKDOWN COMMENCING, SENDING NUKES, USER BANNED')

@client.command()
async def overflowleaderboard(ctx, *, msg):
        Rarity = str(msg.split()[0])
        Rarities = ['Uncommon', 'Rare', 'Legendary']
        if Rarity in Rarities:
            file = open('Scores/' + str(ctx.guild.id) + Rarity + '/Overflow.txt', 'r')
            filestr = str(file.read())
            if filestr != '':
                await ctx.send('```diff\n- ' + Rarity + ' -\n' + filestr + '```')
            else:
                await ctx.send('Overflow file empty.')
            file.close()
        else:
            await ctx.send('Invalid Rarity')
            
@client.event
async def on_command_error(ctx, error):
    if isinstance(error, CommandNotFound):
        return
    raise error

client.run(TOKEN)
