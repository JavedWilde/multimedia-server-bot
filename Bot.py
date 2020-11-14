import discord
from discord.ext.commands import Bot
import random
import UrbanFunc
import os
import json

prefix = '.'
intent = discord.Intents.all()
client = Bot(command_prefix=prefix, intents=intent)
client.remove_command('help')

help_text = {
    'provoke <name>': 'provoke the name typed in the command',
    'urban <search term>': 'search a word on urban dictionary',
    'iamnot <role name>': 'to remove self roles',
    'roles': 'see available roles\n\u200b\n\u200b',

    'Admin Commands': '__________________',
    'clear <number of messages>': 'delete messages',
    'spam <number of spams> <spam message>': 'spam messages',
    'rolemanager help': 'manage roles assignable by the bot'
}  # dictionary

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
    for filename in os.listdir('./Cogs'):
        if filename.endswith('.py'):
            client.load_extension(f'Cogs.{filename[:-3]}')


@client.event
async def on_command_error(ctx, error):
    if not isinstance(error, discord.ext.commands.CommandNotFound):
        daddy = client.get_user(id=DADDYS_ID)
        channel = await daddy.create_dm()
        await channel.send(f' error occured when user `{ctx.author}`, id - `{ctx.author.id}` accessed the command '
                           f'`{ctx.message.content}`, error details: \n```py\n#{error}\n```')


@client.command()
async def loadcog(ctx, arg):
    if ctx.message.author.guild_permissions.administrator:
        try:
            client.load_extension(f'Cogs.{arg}')
        except discord.ext.commands.ExtensionAlreadyLoaded:
            await ctx.send('Cog already loaded')
        except discord.ext.commands.ExtensionNotFound:
            await ctx.send('Cog not found')


@client.command()
async def unloadcog(ctx, arg):
    if ctx.message.author.guild_permissions.administrator:
        try:
            client.unload_extension(f'Cogs.{arg}')
        except discord.ext.commands.ExtensionNotLoaded:
            await ctx.send('Cog not loaded or not found')


@client.command()
async def spam(ctx, arg1, *, arg2):
    if ctx.message.author.guild_permissions.administrator:
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
    embeded = discord.Embed(title='List of Available commands', description='__________________',
                            color=discord.Color.red())
    embeded.set_footer(text='__________________________\n' + prefix + 'helpadmin for all registered commands under '
                                                                      'Client.Commands. Info For Devs')
    for key in help_text:
        if key == 'Admin Commands':
            embeded.add_field(name=key, value=str(help_text.get(key)), inline=False)
        else:
            embeded.add_field(name=prefix + key, value=str(help_text.get(key)), inline=False)
    await ctx.send(embed=embeded)


@client.command()
async def helpadmin(ctx):
    if ctx.message.author.guild_permissions.administrator:
        helptext = "```asciidoc\n"
        for command in client.commands:
            helptext += f"{command}\n"
        helptext += "___________\n All available commands in Client.commands. Info For developers```"
        await ctx.send(helptext)


@client.command()
async def urban(ctx, *, arg):
    try:
        await ctx.send(embed=UrbanFunc.runUrbanEmbed(arg))
    except discord.HTTPException:
        embed = UrbanFunc.runUrbanEmbed(arg)
        embed.set_footer(text=f'{embed.footer.__getattribute__("text")}\n\nPrevious attempt returned an '
                              f'HTTPException error,\nthis is a second attempt')
        await ctx.send(embed=embed)


@urban.error
async def urban_error(ctx, error):
    await ctx.send('Command threw an error, if the error is an HTTPException error, all previous attempts have failed')
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
    if ctx.channel.id == ROLES_CHANNEL_ID or ctx.message.author.guild_permissions.administrator:
        guild_roles = dict()
        for r in ctx.guild.roles:
            guild_roles[str(r.name).lower()] = r.id

        role_id = guild_roles.get(str(roleName).lower())
        role = discord.utils.get(ctx.guild.roles, id=role_id)
        if role is None or str(role).lower() in [a.lower() for a in excludedRoles]:
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
    if ctx.channel.id == ROLES_CHANNEL_ID or ctx.message.author.guild_permissions.administrator:
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
async def clear(ctx, number=0):
    if ctx.message.author.guild_permissions.administrator:
        if number > 0:
            await ctx.channel.purge(limit=number + 1)
        else:
            await ctx.send('Please specify the number of messsages to delete')
    else:
        await ctx.channel.send('You dont have enough permissions')


@client.command()
async def rolemanager(ctx, *arg):
    if ctx.message.author.guild_permissions.administrator:
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


envJson = json.load(open('env'))
client.run(envJson['token'])
