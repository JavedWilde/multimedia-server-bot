import discord
from discord.ext.commands import Bot
import random
import UrbanFunc

TOKEN = 'Nzc0NjY1MTAzMzA3NDQwMTc5.X6bFGQ.yGZlmMkGnF2kVes4bTIXPEJi5-8'

prefix = '.'
intent = discord.Intents.all()
client = Bot(command_prefix=prefix, intents=intent)
client.remove_command('help')

help_text = '''
__List of available commands:__
**$prefixprovoke <name>** to provoke
**$prefixurban <search term>** to search a word on urban dictionary
**$prefixiam <role name>** to assign self roles (Case Sensitive)
**$prefixiamnot <role name>** to remove self roles (Case Sensitive)
**$prefixroles** to see available roles

__Admin Commands:__
**$prefixclear <number of messages>** to delete messages
**$prefixspam <number of spams> <spam message>** to spam messages
**$prefixrolemanager help** to manage roles assignable by the bot
```asciidoc
__________
Type $prefixhelpadmin for all registered commands under Client.Commands. For Devs
```
'''

# Gaali
slur = ['madherchod', 'randwa', 'randi', 'betichod', 'vinoth ki jhaant', 'raand ki gand', 'chutiya', 'gandu', 'muthela',
        'bhayrand', 'napunsak']

# roles that must be excluded from being Given by the bot
excludedRoles = ['@everyone', 'bots', 'Groovy', 'Rythm', 'Admins', 'SulagtiGaand', 'Moderator', 'NotSoBot',
                 'Professional', 'Dank Memer']

# names excluded from provoke
provoke_exclusions = ['saksham', 'javed', 'sonu', 'sexa']

# important Channel IDs
ROLES_CHANNEL_ID = 774708133150588980
RULES_CHANNEL_ID = 774619660037390339
INTRO_CHANNEL_ID = 774619692550586369

# user IDs
DADDYS_ID = 389432819056771072


@client.event
async def on_ready():
    print('Bot On')


@client.command()
async def spam(ctx, arg1, *, arg2):
    if 'Moderator' in [y.name for y in ctx.message.author.roles]:
        for x in range(0, int(arg1)):
            await ctx.message.channel.send(arg2)


@spam.error
async def spam_error(ctx, error):
    await ctx.send(f'Invalid arguments, check **{prefix}help** for usage')
    await ctx.send(f'```py\n# {error}```')


@client.command()
async def ping(ctx):
    delay = str(round(client.latency, 3) * 1000)
    await ctx.send(delay[:-2] + 'ms')


@client.command()
async def help(ctx):
    global help_text
    help_text = help_text.replace('$prefix', prefix)
    await ctx.send(help_text)


@client.command()
async def helpadmin(ctx):
    if 'Moderator' in [str(y.name) for y in ctx.author.roles]:
        helptext = "```asciidoc\n"
        for command in client.commands:
            helptext += f"{command}\n"
        helptext += "___________\n All available commands in Client.commands. Info For developers```"
        await ctx.send(helptext)


@client.command()
async def urban(ctx, *, arg):
    await ctx.send(UrbanFunc.runUrban(arg))


@urban.error
async def urban_error(ctx, error):
    await ctx.send('Type a keyword to search after the command')
    await ctx.send(f'```py\n# {error}```')


@client.command()
async def provoke(ctx, *, arg='ye command likhne wala'):
    for x in provoke_exclusions:
        if str(arg).lower().find(x) > -1:
            await ctx.send(f'{ctx.author.mention} {random.choice(slur)} h')
            return
    await ctx.send(arg + ' ' + random.choice(slur) + ' h')


@client.command()
async def roles(ctx):
    strng = '**List of available Roles:**'
    for r in ctx.guild.roles:
        if str(r).lower() not in [y.lower() for y in excludedRoles]:
            strng += '\n'
            strng += str(r)
    await ctx.send(strng)


@client.command()
async def iam(ctx, *, roleName=None):
    if ctx.channel.id == ROLES_CHANNEL_ID or 'Moderator' in [y.name for y in ctx.author.roles]:
        guild_roles = dict()
        for r in ctx.guild.roles:
            guild_roles[str(r.name).lower()] = r.id

        role_id = guild_roles.get(str(roleName).lower())
        role = discord.utils.get(ctx.guild.roles, id=role_id)
        if role is None or str(role) in [a.lower() for a in excludedRoles]:
            if ctx.author.id == DADDYS_ID:
                await ctx.send('Yes Daddy :weary: Harder Please')
            else:
                await ctx.send(
                    'Please type in the proper role name.')
                await ctx.channel.send('Type **' + prefix + 'roles** to see available roles')
        else:
            await ctx.author.add_roles(role)
            await ctx.send('**' + str(role) + '** ' + 'Role has been added')


@client.command()
async def iamnot(ctx, *, roleName='None'):
    if ctx.channel.id == ROLES_CHANNEL_ID or 'Moderator' in [y.name for y in ctx.author.roles]:
        guild_roles = dict()
        for r in ctx.guild.roles:
            guild_roles[str(r.name).lower()] = r.id

        role_id = guild_roles.get(str(roleName).lower())
        role = discord.utils.get(ctx.guild.roles, id=role_id)
        if str(role) in [y.name for y in ctx.author.roles]:
            await ctx.author.remove_roles(role)
            await ctx.channel.send('**' + str(role) + '** role has been removed')
        else:
            await ctx.channel.send('You dont have **' + roleName + '** role or it doesnt exist')


@client.command()
async def clear(ctx, *, number):
    if 'Moderator' in [y.name for y in ctx.author.roles]:
        if number.isdigit():
            if int(number) < 101:
                mgs = []  # Empty list to put all the messages in the log
                async for x in ctx.channel.history(limit=int(number) + 1):
                    mgs.append(x)
                await ctx.channel.delete_messages(mgs)
            else:
                await ctx.channel.send('Can only bulk delete messages up to 100 messages')
        else:
            await ctx.channel.send('Please use a number to clear Chat')
    else:
        await ctx.channel.send('You dont have enough permissions')


@client.command()
async def rolemanager(ctx, *arg):
    if 'Moderator' in [y.name for y in ctx.author.roles]:
        if arg[0].lower() == 'exclude':
            if arg[1].lower() in [y.lower() for y in excludedRoles]:
                await ctx.channel.send(arg[1] + ' is already excluded')
            elif arg[1] in [str(y.name) for y in ctx.guild.roles]:
                excludedRoles.append(arg[1])
                await ctx.channel.send(arg[1] + ' added to exclusions, it is not assignable by '
                                                'command now')
            else:
                await ctx.channel.send(arg[1] + ' doesnt exist. Role names are Caps sensitive')
        elif arg[0].lower() == 'include':
            if arg[1] in excludedRoles:
                excludedRoles.remove(arg[1])
                await ctx.channel.send(arg[1] + ' removed from exclusions, role is now '
                                                'assignable by command')
            elif arg[1].lower() in [str(y.name).lower() for y in ctx.guild.roles]:
                await ctx.channel.send(arg[1] + ' role is not in the exclusions')
            else:
                await ctx.channel.send(arg[1] + ' doesnt exist. Role names are Caps sensitive')
        elif arg[0].lower() == 'roles':
            temp = ''
            for x in excludedRoles:
                if x != '@everyone':
                    temp += x
                    temp += '\n'
            await ctx.channel.send('Excluded Roles: \n' + temp)
        elif arg[0].lower() == 'help':
            temp = 'Available Commands. **Rolenames are Caps sensitive**\n\n'
            temp += '*' + prefix + 'rolemanager exclude <rolename>* to block a rolename from being assigned ' \
                                   'by the bot\n'
            temp += '*' + prefix + 'rolemanager include <rolename>* to allow a rolename to be assigned by ' \
                                   'the bot\n'
            temp += '*' + prefix + 'rolemanager roles* to show list of excluded roles\n'
            await ctx.channel.send(temp)
        else:
            await ctx.channel.send('Wrong usage, use **' + prefix + 'rolemanager help** for usage guide')


@rolemanager.error
async def rolemanager_error(ctx, error):
    await ctx.channel.send('Wrong usage, use **' + prefix + 'rolemanager help** for usage guide')
    await ctx.send(f'```py\n# {error}```')


@client.event
async def on_member_join(member):
    channel = client.get_channel(id=INTRO_CHANNEL_ID)
    myid = '<@' + str(member.id) + '>'
    await channel.send(
        'Hey ' + myid + ', welcome to ' + client.get_guild(774541979085438978).name +
        ' Server! enjoy your stay in the server make sure to read the ' + client.get_channel(
            id=RULES_CHANNEL_ID).mention + ' and assign '
        + client.get_channel(id=ROLES_CHANNEL_ID).mention + ' to yourself')


client.run('Nzc0NjY1MTAzMzA3NDQwMTc5.X6bFGQ.yGZlmMkGnF2kVes4bTIXPEJi5-8')
