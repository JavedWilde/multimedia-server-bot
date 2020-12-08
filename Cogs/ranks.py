from discord.ext import commands
from discord import Embed, Color
import discord
import json
import os
import mysql.connector as sql
import Rank_Image # pylint: disable=F0401

def reconnect():
    global db
    if os.environ.get('IS_HEROKU', None):
        # file is on server side, use heroku/server token 
        db = sql.connect(
            host=os.environ.get('SQL_HOST'),
            port=os.environ.get('SQL_PORT'),
            user=os.environ.get('SQL_USER'),
            passwd=os.environ.get('SQL_PASS'),
            database='javed'
        )
    else:
        # file is on development pc/local, use .env file stored on local
        envJson = json.load(open('.env'))
        db = sql.connect(
            host=envJson['host'],
            port=envJson['port'],
            user=envJson['user'],
            passwd=envJson['passwd'],
            database='javed')
            

def checkTableExists(dbcon, tablename):
    dbcur = dbcon.cursor(buffered=True)
    if not isinstance(tablename, str):
        tb = str(tablename)
    else:
        tb = tablename
    dbcur.execute("""
        SELECT COUNT(*)
        FROM information_schema.tables
        WHERE table_name = '{0}'
        """.format(tb.replace('\'', '\'\'')))
    if dbcur.fetchone()[0] == 1:
        dbcur.close()
        return True

    dbcur.close()
    return False


async def updateData(userid, tablename, message=None):
    cur = db.cursor(buffered=True)
    cur.execute(f"SELECT userid, exp, level FROM {tablename} WHERE userid={userid}")
    if cur.rowcount < 1:
        cur.execute(f"INSERT INTO {tablename} (userid, exp, level) VALUES ({userid}, 0, 1)")
    else:
        user = cur.fetchone()
        tempXP = user[1] + 5
        tempLVL = user[2]
        lvl_end = int(tempXP ** (1 / 4))
        if tempLVL < lvl_end:
            tempLVL = tempLVL + 1
            if message is not None:
                await message.channel.send(f'{message.author.mention} leveled up. New Level : {tempLVL}')

        cur.execute(f"UPDATE {tablename} SET exp = {tempXP}, level = {tempLVL} WHERE userid = {userid}")
    db.commit()

reconnect()
class Ranks(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_member_join(self, member):
        if member.bot:
            return
        
        try:
            dbcursor = db.cursor(buffered=True)
        except sql.OperationalError:
            reconnect()
            dbcursor = db.cursor(buffered=True)
        
        if checkTableExists(db, f'{member.guild.id}_ranks'):
            await updateData(member.id, f'{member.guild.id}_ranks')
        else:
            dbcursor.execute(f'CREATE TABLE {member.guild.id}_ranks (userid bigint PRIMARY KEY, exp int UNSIGNED, level'
                             f' int UNSIGNED)')
            await updateData(member.id, f'{member.guild.id}_ranks')

    @commands.Cog.listener()
    async def on_message(self, message):
        try:
            dbcursor = db.cursor(buffered=True)
        except sql.OperationalError:
            reconnect()
            dbcursor = db.cursor(buffered=True)
        
        if message.author.bot:
            return

        if checkTableExists(db, f'{message.guild.id}_ranks'):
            await updateData(message.author.id, f'{message.guild.id}_ranks', message)
        else:
            dbcursor.execute(f'CREATE TABLE {message.guild.id}_ranks (userid bigint PRIMARY KEY, exp int UNSIGNED,'
                             f' level int UNSIGNED)')
            await updateData(message.author.id, f'{message.guild.id}_ranks', message)

    @commands.command(aliases=['lb'])
    async def leaderboard(self, ctx):
        try:
            dbcursor = db.cursor(buffered=True)
        except sql.OperationalError:
            reconnect()
            dbcursor = db.cursor(buffered=True)
        
        if checkTableExists(db, f'{ctx.guild.id}_ranks'):
            dbcursor.execute(f"SELECT userid, exp, level FROM {ctx.guild.id}_ranks ORDER BY exp DESC LIMIT 10")
            embeded = Embed(title='**LeaderBoard**', color=Color.red())
            embeded.set_thumbnail(url=ctx.guild.icon_url)
            embeded.set_author(name=ctx.guild.name)
            for iteration, row in enumerate(dbcursor.fetchall()):
                member_name = ctx.guild.get_member(row[0])
                embeded.add_field(name=f'{iteration+1}. {str(member_name)[:-5]}',
                                    value=f'```cs\nLevel : {row[2]}              Exp : {str(row[1])}              ```',
                                    inline=False)

            await ctx.send(embed=embeded)
            
        else:
            await ctx.send(f'Database : {ctx.guild.id}_ranks not Found')

    @commands.command()
    async def rank(self, ctx):
        if ctx.message.mentions[0].bot:
            await ctx.send('Bot plebs dont get ranks :slight_smile:')
            return

        try:
            dbcursor = db.cursor(buffered=True)
        except sql.OperationalError:
            reconnect()
            dbcursor = db.cursor(buffered=True)
        
        if checkTableExists(db, f'{ctx.guild.id}_ranks'):
            try:
                member_obj = ctx.message.mentions[0]
            except IndexError:
                member_obj = ctx.author
            dbcursor.execute(f"SELECT userid, exp, level FROM {ctx.guild.id}_ranks ORDER BY exp DESC")
            for iteration, row in enumerate(dbcursor.fetchall()):
                if row[0] == member_obj.id:
                    await ctx.send('Generating Card, Please Wait...')
                    await member_obj.avatar_url.save('./Images/pfp.jpg')
                    try:
                        await ctx.guild.icon_url.save('./Images/server.jpg')
                    except discord.DiscordException:
                        await member_obj.avatar_url.save('./Images/server.jpg')

                    Rank_Image.generate_rank_img('./Images/pfp.jpg', './Images/server.jpg',
                                                str(member_obj),iteration + 1, 
                                                str(member_obj.roles[len(member_obj.roles) - 1]),
                                                row[1])
                                                
                    f = discord.File('./Images/rank.png', filename='rank.png')
                    await ctx.channel.purge(limit=1)
                    await ctx.send(file=f)
                    return
        else:
            await ctx.send(f'Database : {ctx.guild.id}_ranks not Found')     


    # admin Commands
    @commands.command()
    async def ranktest(self, ctx):
        if ctx.author.guild_permissions.administrator:
            try:
                dbcursor = db.cursor(buffered=True)
            except sql.OperationalError:
                reconnect()
                dbcursor = db.cursor(buffered=True)
        
            if checkTableExists(db, f'{ctx.guild.id}_ranks'):
                try:
                    member_obj = ctx.message.mentions[0]
                except IndexError:
                    member_obj = ctx.author
                dbcursor.execute(f"SELECT userid, exp, level FROM {ctx.guild.id}_ranks ORDER BY exp DESC")
                for iteration, row in enumerate(dbcursor.fetchall()):
                    if row[0] == member_obj.id:
                        embeded = Embed(title=f'**{member_obj.name}**', 
                                        description=f'```cs\nLevel : {row[2]}              Exp : {str(row[1])}              ```')
                        embeded.set_author(name=f'Rank : {iteration + 1}')
                        embeded.set_thumbnail(url=member_obj.avatar_url)
                        if member_obj.nick is not None:
                            embeded.set_footer(text=f'Nickname : {member_obj.nick}')
                        await ctx.send(embed=embeded)
                        return
            else:
                await ctx.send(f'Database : {ctx.guild.id}_ranks not Found')     

    @commands.command()
    async def update_db(self, ctx):
        if ctx.author.guild_permissions.administrator:
            try:
                dbcursor = db.cursor(buffered=True)
            except sql.OperationalError:
                reconnect()
                dbcursor = db.cursor(buffered=True)
                
            for member in ctx.guild.members:
                if not member.bot:
                    if checkTableExists(db, f'{ctx.guild.id}_ranks'):
                        await updateData(member.id, f'{ctx.guild.id}_ranks')
                    else:
                        dbcursor.execute(f'CREATE TABLE {ctx.guild.id}_ranks (userid bigint PRIMARY KEY, exp int UNSIGNED,'
                                    f' level int UNSIGNED)')
                        await updateData(member.id, f'{ctx.guild.id}_ranks')
            await ctx.send('Database Updated')


def setup(client):
    client.add_cog(Ranks(client))
