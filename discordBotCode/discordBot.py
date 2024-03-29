#imports
import discord
from discord.ext import commands
import discordBotCode.databaseManagement as databaseManagement
import sqlite3
from sqlite3 import Error
import sys
import datetime
import re

#consts
database = r"C:\Users\bkowa\Documents\Python Code\OhioBot\discordBotCode\csgamerpings.db"
cryingEmoji =  r"C:\Users\bkowa\Documents\Python Code\OhioBot\discordBotCode\crying-emoji-dies.gif"
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='$', intents=intents)

client = discord.Client(intents=intents)

# Converts messages with EST to PST
def convert_to_pst(text):
    text = text.replace(":", "")
    match = re.search(r'\d+ est', text)
    number = match.group(0)[0:-4]
    if len(number) == 4:
        value = str(((9 + int(number[0:2]))%12))+":" + (number[2:4]) 
    elif len(number) == 3:
        value = str(((9 + int(number[0:1]))%12))+":" + (number[1:3])
    elif len(number) == 2:
        value = str((9 + int(number))%12)+ ":00"
    else:
        value = str((9 + int(number)))+ ":00" 
    return(value)

def get_messages_count():
        conn = databaseManagement.create_connection(database)
        
        with conn:
            table = databaseManagement.print_pings_messages(conn)
            count = ''
            for row in table:
                count = count + str(row[0]) + ' has sent '+ str(row[1]) + ' messages' + '\n'
        return count

def get_pings_count():
        conn = databaseManagement.create_connection(database)
        with conn:
            table = databaseManagement.print_pings(conn)
            count = ''
            for row in table:
                count = count + str(row[0]) + ' has pinged @CSGamer '+ str(row[1]) + ' times\n'
        return count

# Sends message to alert Discord that there was an error
async def error_occurred():
    await discord.message.channel.send("Something went horribly wrong")

# commands require new invite to server to allow for commands to be listed as a part of the bot
@bot.command()
async def howManySends(ctx, content: get_pings_count):
    count = get_pings_count()
    await ctx.send(count)



@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')



@client.event
async def on_message(message):
    
    # could add line to check message for other states besides Ohio and Cali to respond *state name* who???

    if message.author == client.user:
        return

    text = message.content.lower()
    
    conn = databaseManagement.create_connection(database)
    with conn:
        user = message.author.name
        user = user.replace('\'', '')
        user = user.replace('\"', '')
        databaseManagement.insertOrUpdateUserMessages(conn,user)
        

    if 'ohio' in text:
        await message.channel.send('I love Ohio! 🎉')
    
    if 'california' in text:
        await message.channel.send('Fuck California. 😠')

    if '$$updateCode' in text:
        #end this python command to jump up to updater section
        return
    
    if '$$member' in text:
        await message.channel.send(type(message.author.display_name))
        return

    if '$count' in text:        

            count = get_pings_count()
            await message.channel.send(count)


    if '$messages' in message.content.lower():        

            count = get_messages_count()
            await message.channel.send(count)

    if ' est' in message.content.lower():
        text = message.content.lower()
        # does not check if " est" occurs with non-numeric entries and will try to convert them
        value = convert_to_pst(text)
        await message.channel.send("That's " + str(value) + " PST")
        

    if ' pst' in message.content.lower():
        with open(cryingEmoji, 'rb') as f:
            picture = discord.File(f)
            await message.channel.send(file=picture)

    if ' cst' in message.content.lower():
        
        await message.channel.send("Shuddup")

    if len(message.role_mentions) > 0:
        for role in message.role_mentions:
            if 'csgamer' in role.name.lower():                    

                conn = databaseManagement.create_connection(database)
                with conn:
                    user = message.author.name
                    databaseManagement.insertOrUpdateUser(conn,user)
                
    
    if '$help' in text:
        await message.channel.send('''**$count** will tell you how many times we've pinged csgamer\n **$messages** will tell you how many messages everyone has sent
        ''')
    
    if '$$close' in text:
        await client.close() 
        sys.exit()



def start():
    key = '' 
    reader = open(r"C:\Users\bkowa\Documents\Python Code\OhioBot\discordBotCode\SecretKey.txt", "r")
    key = reader.readline()

    client.run(key)
