__author__   =   "Ben Kowalski"

#this code is a shell for a discord bot, it allows for the bot to be updated remotely using github gists

#imports
import discordBotCode.discordBot as discordBot
#import GitHub

 
#main loop
print("Beginning Discord bot service")

#discord bot section - must be executed as separate python code
discordBot.start()

#integrated ability to leave bot status to update code
# this is handled in discordBot as the $$close command from discord

#update discordBotCode/ 



#jump back to discord bot status