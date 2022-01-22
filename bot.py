import discord
from discord.ext import commands

import os, re
from webserver import keep_alive

client = commands.Bot(command_prefix='.')

scam_list = []
with open("bot/scammers.txt") as file:
    for line in file:
        scam_list += re.sub("[^\w]", " ", line).split()
print(scam_list)


@client.event
async def on_ready():
    print('Bot is ready')

@client.event
async def on_message(message):
    # print(message)
    # print(message.content)

    message_list = []
    counter = 0

    # before iterating through the message, check if there is a phone number or a discord link and ban+delete the message
    invite_regex = re.compile("(?:https?://)?discord(?:(?:app)?\.com/invite|\.gg)/?[a-zA-Z0-9]+/?")
    result = invite_regex.findall(message.content)
    if (len(result) > 0):
        await message.channel.send(
            f'No spamming links you knew the rule, sorry {message.author.name} but you\'re banned!', delete_after=10)
        await message.author.ban(reason="spammer")

    regexList = ['\d\d\d-\d\d\d-\d\d\d\d', '\d\d\d \d\d\d-\d\d\d\d', '\d\d\d \d\d\d \d\d\d\d',
                  '\(\d\d\d\) \d\d\d-\d\d\d\d', '\(\d\d\d\) \d\d\d \d\d\d\d']
    result_phone_list = []
    for x in regexList:
        result_phone_list += re.findall(x, message.content)

    if (len(result_phone_list) > 0):
        await message.channel.send(
            f'No spamming phone, you knew the rule, sorry {message.author.name} but you\'re banned!', delete_after=10)
        await message.author.ban(reason="spammer")

        # function to iterate over message's words and strip each word and then put each word in the message_list list
    message_list = re.sub('[:/!,*)\'@#%(&$_?.^]', ' ', message.content).split()
    message_list = [each_word.lower() for each_word in message_list]

    # scammers test
    # if all(word in stock_scam_list. for word in message.content.lower()):
    #     #     await message.channel.send('catched stock scammer')

    for word in scam_list:
        if word.lower() in message_list:
            counter += 1
    print(counter)
    if counter >= 3:
        await message.channel.send(f'Catched you, you idiot scammer: {message.author.name} you\'re banned!',
                                   delete_after=10)
        print(message.author.id)
        print(message.author.name)
        await message.author.ban(reason="Scammer")


# @client.command()
# async def ping(ctx):
#     await ctx.send('Pong!')

# # @client.command()
# # async def clear(ctx, amount=5):
# #     await ctx.channel.purge(limit=amount)

# # @client.command()
# # async def ban(ctx, member: discord.Member, *, reason=None):
# #     await member.ban(reason=reason)
keep_alive()

client.run(os.environ.get("api_token"))