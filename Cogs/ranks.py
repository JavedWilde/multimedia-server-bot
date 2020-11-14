from discord.ext import commands
from discord import Embed
import json
import operator
import os


def update_data(users_data, user):
    if str(user.id) not in users_data:
        users_data[str(user.id)] = {}
        users_data[str(user.id)]['exp'] = 0
        users_data[str(user.id)]['lvl'] = 1


def add_exp(users_data, user, amount):
    users_data[str(user.id)]['exp'] += amount


async def level_up(users_data, user, channel):
    exp = users_data[str(user.id)]['exp']
    lvl_start = users_data[str(user.id)]['lvl']
    lvl_end = int(exp ** (1 / 4))

    if lvl_start < lvl_end:
        users_data[str(user.id)]['lvl'] += 1
        await channel.send(f'{user.mention} leveled up. New Level - {users_data[str(user.id)]["lvl"]}')


class Test(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_member_join(self, member):
        try:
            open(f'.//Cogs//rank_data//{member.guild.id}_ranks.json', 'r')
        except FileNotFoundError:
            try:
                os.mkdir(f'.//Cogs//rank_data//')
            except FileExistsError:
                with open(f'.//Cogs//rank_data//{member.guild.id}_ranks.json', 'w+') as f:
                    f.write('{}')
            else:
                with open(f'.//Cogs//rank_data//{member.guild.id}_ranks.json', 'w+') as f:
                    f.write('{}')
        finally:
            with open(f'.//Cogs//rank_data//{member.guild.id}_ranks.json', 'r') as f:
                users = json.load(f)

        update_data(users, member)

        with open(f'.//Cogs//rank_data//{member.guild.id}_ranks.json', 'w') as f:
            json.dump(users, f, indent=4)

    @commands.Cog.listener()
    async def on_message(self, message):
        try:
            open(f'.//Cogs//rank_data//{message.guild.id}_ranks.json', 'r')
        except FileNotFoundError:
            try:
                os.mkdir(f'.//Cogs//rank_data//')
            except FileExistsError:
                with open(f'.//Cogs//rank_data//{message.guild.id}_ranks.json', 'w+') as f:
                    f.write('{}')
            else:
                with open(f'.//Cogs//rank_data//{message.guild.id}_ranks.json', 'w+') as f:
                    f.write('{}')
        finally:
            with open(f'.//Cogs//rank_data//{message.guild.id}_ranks.json', 'r') as f:
                users = json.load(f)

        update_data(users, message.author)
        add_exp(users, message.author, 5)
        await level_up(users, message.author, message.channel)

        with open(f'.//Cogs//rank_data//{message.guild.id}_ranks.json', 'w') as f:
            json.dump(users, f, indent=4)

    @commands.command(aliases=['lb'])
    async def leaderboard(self, ctx):
        try:
            open(f'.//Cogs//rank_data//{ctx.guild.id}_ranks.json', 'r')
        except FileNotFoundError:
            try:
                os.mkdir(f'.//Cogs//rank_data//')
            except FileExistsError:
                with open(f'.//Cogs//rank_data//{ctx.guild.id}_ranks.json', 'w+') as f:
                    f.write('{}')
            else:
                with open(f'.//Cogs//rank_data//{ctx.guild.id}_ranks.json', 'w+') as f:
                    f.write('{}')
        finally:
            with open(f'.//Cogs//rank_data//{ctx.guild.id}_ranks.json', 'r') as f:
                users = json.load(f)

        temp_dict = dict()
        for key in users:
            temp_dict[key] = users[key]['exp']
        sorted_d = dict(sorted(temp_dict.items(), key=operator.itemgetter(1), reverse=True))

        embeded = Embed(title='**LeaderBoard**')
        embeded.set_thumbnail(url=ctx.guild.icon_url)
        embeded.set_author(name=ctx.guild.name)
        for iteration, key in enumerate(sorted_d):
            member_name = ctx.guild.get_member(int(key))
            embeded.add_field(name=f'{iteration + 1}. {str(member_name)[:-5]}',
                              value=f'```cs\nLevel : {int(sorted_d.get(key) ** (1 / 4))}'
                                    f'              Exp : {str(sorted_d.get(key))}              ```',
                              inline=False)

        await ctx.send(embed=embeded)


def setup(client):
    client.add_cog(Test(client))
