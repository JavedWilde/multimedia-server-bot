import discord
import random

TOKEN = 'Nzc0NjY1MTAzMzA3NDQwMTc5.X6bFGQ.yGZlmMkGnF2kVes4bTIXPEJi5-8'

intent = discord.Intents.all()
client = discord.Client(intents=intent)

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
RULES_CHANNEL_ID = 774619660037390339
INTRO_CHANNEL_ID = 774619692550586369


@client.event
async def on_member_join(member):
    channel = client.get_channel(id=INTRO_CHANNEL_ID)
    myid = '<@' + str(member.id) + '>'
    await channel.send(
        'Hey ' + myid + ', welcome to ' + client.get_guild(774541979085438978).name +
        ' Server! enjoy your stay in the server make sure to read the ' + client.get_channel(
            id=RULES_CHANNEL_ID).mention + ' and assign '
        + client.get_channel(id=ROLES_CHANNEL_ID).mention + ' to yourself')
    # await client.send_message(channel, ' : %s is the best ' % myid)

    # await channel.send('meh')


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith(prefix + 'spam') and 'Moderator' in [y.name for y in message.author.roles]:
        mes = message.content.split()
        if 1 < len(mes) < 3:
            output = ''
            for word in mes[1:2]:
                output += word
                output += ' '
            for x in range(0, 10):
                await message.channel.send(output)

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

            testing = output.lower()
            x = random.randint(0, len(slur))
            if not testing.find('javed'):
                await message.channel.send(output + slur[x] + ' h')
            else:
                await message.channel.send(message.author.mention + ' ' + slur[x] + ' h')
        else:
            await message.channel.send("Please give just a single word name")


# list of available roles command
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
                if message.author.id == 389432819056771072:
                    await message.channel.send('Yes Daddy :weary: Harder Please')
                else:
                    await message.channel.send(
                        'Please type in the proper role name. **NOTE- Names are Case Sensitive**')
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
