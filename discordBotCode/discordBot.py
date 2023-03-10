#imports
import discord
import discordBotCode.databaseManagement as databaseManagement
import sqlite3
from sqlite3 import Error
import sys
import datetime
import re

#consts
database = r"C:\Users\bkowa\Documents\Python Code\OhioBot\discordBotCode\csgamerpings.db"
intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

def convert_to_pst(text):
    match = re.search(r'\d+ est', text)
    number = match.group(0)[0:-4]
    if len(number) == 4:
        number = ((9 + int(number[0:2]))%12)*100 + int(number[2:4])
        value =  int(number) 
    elif len(number) == 3:
        number = ((9 + int(number[0:1]))%12)*100 + int(number[1:3])
        value =  int(number)
    elif len(number) == 2:
        number = number[0]
        value = (9 + int(number))%12 
    else:
        value = (9 + int(number))%12  
    return(value)

# Sends message to alert Discord that there was an error
async def error_occurred():
    await discord.message.channel.send("Something went horribly wrong")


@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

#def time_converter() - should take any line containing ' EST' and respond with PST and CST 


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
    
    elif 'california' in text:
        await message.channel.send('Fuck California. 😠')

    if '$$updateCode' in text:
        #end this python command to jump up to updater section
        return
    
    if '$$member' in text:
        await message.channel.send(type(message.author.display_name))
        return

    if '$count' in text:        

        conn = databaseManagement.create_connection(database)
        with conn:
            table = databaseManagement.print_pings(conn)
            count = ''
            for row in table:
                count = count + str(row[0]) + ' has pinged @CSGamer '+ str(row[1]) + ' times\n'
            await message.channel.send(count)


    if '$messages' in message.content.lower():        

        conn = databaseManagement.create_connection(database)
        with conn:
            table = databaseManagement.print_pings_messages(conn)
            count = ''
            for row in table:
                count = count + str(row[0]) + ' has sent '+ str(row[1]) + ' messages' + '\n'
            await message.channel.send(count)

    if ' est' in message.content.lower():
        text = message.content.lower()
        # only checks first character currently
        if text[0].isnumeric():
            value = convert_to_pst(text)
            await message.channel.send("That's " + str(value) + " PST")

    if ' pst' in message.content.lower():
        
        await message.channel.send("That's " + message.content.lower())


    if len(message.role_mentions) > 0:
        for role in message.role_mentions:
            if 'csgamer' in role.name.lower():                    

                conn = databaseManagement.create_connection(database)
                with conn:
                    user = message.author.name
                    databaseManagement.insertOrUpdateUser(conn,user)
                return
    
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
