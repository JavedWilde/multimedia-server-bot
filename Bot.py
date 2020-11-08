import discord
import random

TOKEN = 'Nzc0NjY1MTAzMzA3NDQwMTc5.X6bFGQ.yGZlmMkGnF2kVes4bTIXPEJi5-8'

client = discord.Client()

# command Prefix
prefix = '.'
# Gaali
slur = ['madherchod', 'randwa', 'randi', 'betichod', 'vinoth ki jhaant', 'raand ki gand', 'chutiya', 'gandu', 'muthela',
        'bhayrand', 'napunsak']
# slur = ['sahil ka papa','sahil ki gaand leta','sahil se chooswata']
# roles that must be excluded from being Given by the bot
excludedRoles = ['@everyone', 'bots', 'Groovy', 'Rythm', 'Admins', 'SulagtiGaand', 'Moderator']

# important Channel IDs
ROLES_CHANNEL_ID = 774708133150588980
INTRO_CHANNEL_ID = 774619692550586369


@client.event
async def on_member_join(member):
    channel = discord.utils.get(client.guild.channels, id=INTRO_CHANNEL_ID)


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    # check server speed
    if message.content.startswith(prefix + 'ping'):
        mes = await message.channel.send('meh')
        pingDelay = mes.created_at - message.created_at
        pingDelay_DIGITSONLY = ''
        for x in str(pingDelay):
            if x != ':' and x != '.' and x != '0':
                pingDelay_DIGITSONLY += x

        await message.channel.send(pingDelay_DIGITSONLY + 'ms')
        await mes.delete()

    # help
    if message.content.startswith(prefix + 'help'):
        strng = '**List of available commands:** \n'
        strng += '*' + prefix + 'provoke <name>* to provoke\n'
        strng += '*' + prefix + 'iam <role name>* to assign self roles (Case Sensitive)\n'
        strng += '*' + prefix + 'iamnot <role name>* to remove self roles (Case Sensitive)\n'
        strng += '*' + prefix + 'roles* to see available roles\n\n'
        strng += '**Admin Commands:**\n'
        strng += '*' + prefix + 'clear <number of messages>* to delete messages (only accessed by a Mod)\n'
        await message.channel.send(strng)

    # Gaali Galouj
    if message.content.startswith(prefix + 'provoke'):
        mes = message.content.split()
        if 1 < len(mes) < 3:
            output = ''
            for word in mes[1:2]:
                output += word
                output += ' '
            x = random.randint(0, len(slur))
            await message.channel.send(output + slur[x] + ' h')
        else:
            await message.channel.send("Please give just a single word name")

    # list of avaible roles command
    if message.content.startswith(prefix + 'roles'):
        strng = '**List of available Roles:**'
        for r in message.guild.roles:
            roleOK = True  # same as role public but different name for the scope of this loop
            for rr in excludedRoles:
                if str(r) == rr:
                    roleOK = False
                    break
            if roleOK:
                strng += '\n'
                strng += str(r)
        await message.channel.send(strng)

    # role un assign command
    if message.content.startswith(prefix + 'iamnot'):
        if message.channel.id == ROLES_CHANNEL_ID or 'Moderator' in [y.name for y in message.author.roles]:
            mes = message.content.split()
            output = ''  # temp Rolename
            for word in mes[1:]:
                output += word
                output += ' '

            roleName = ''  # actual Rolename
            for x in output[0:len(output) - 1]:
                roleName += x
            role = discord.utils.get(message.guild.roles, name=roleName)  # roleHolder

            if str(role) in [y.name for y in message.author.roles]:
                await message.author.remove_roles(role)
                await message.channel.send('**' + str(role) + '** role has been removed')
            else:
                await message.channel.send('You dont have **' + roleName + '** role or it doesnt exist')

    # role assign command
    elif message.content.startswith(prefix + 'iam'):
        if message.channel.id == ROLES_CHANNEL_ID or 'Moderator' in [y.name for y in message.author.roles]:
            mes = message.content.split()
            output = ''  # temp Rolename
            for word in mes[1:]:
                output += word
                output += ' '

            roleName = ''  # actual Rolename
            for x in output[0:len(output) - 1]:
                roleName += x
            role = discord.utils.get(message.guild.roles, name=roleName)  # roleHolder

            # if role typed in the message does not exist in the server or is a non public role
            if role is None or str(role) in [a for a in excludedRoles]:
                await message.channel.send('Please type in the proper role name. **NOTE- Names are Case Sensitive**')
                await message.channel.send('Type **' + prefix + 'roles** to see available roles')
            else:
                await message.author.add_roles(role)
                await message.channel.send('**' + str(role) + '** ' + 'Role has been added')
        else:
            await message.channel.send('Wrong Channel')

    # Clear Messages (For Admin)
    if message.content.startswith(prefix + 'clear'):
        if 'Moderator' in [y.name for y in message.author.roles]:
            number = ''
            for x in message.content[len(prefix) + 6:]:
                number += x
            print(number.isdigit())

            if number.isdigit():
                if int(number) < 101:
                    mgs = []  # Empty list to put all the messages in the log
                    async for x in message.channel.history(limit=int(number)):
                        mgs.append(x)
                    await message.channel.delete_messages(mgs)
                else:
                    await message.channel.send('Can only bulk delete messages up to 100 messages')

            else:
                await message.channel.send('Please use a number to clear Chat')
        else:
            await message.channel.send('You dont have enough permissions')


@client.event
async def on_ready():
    print("Bot on")


client.run(TOKEN)
