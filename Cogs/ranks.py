from discord.ext import commands
# from discord import Embed
# import json
# import operator
# import os
import mysql.connector as sql

db = sql.connect(
    host='pass.mrcow.xyz',
    port='33069',
    user='javedUser',
    passwd='nnBmkRLFjeKRR9JrzdrTzLi123!',
    database='javed'
)


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


class Test(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_member_join(self, member):
        dbcursor = db.cursor(buffered=True)
        if checkTableExists(db, f'{member.guild.id}_ranks'):
            await updateData(member.id, f'{member.guild.id}_ranks')
        else:
            dbcursor.execute(f'CREATE TABLE {member.guild.id}_ranks (userid bigint PRIMARY KEY, exp int UNSIGNED, level'
                             f' int UNSIGNED)')
            await updateData(member.id, f'{member.guild.id}_ranks')

    @commands.Cog.listener()
    async def on_message(self, message):
        dbcursor = db.cursor(buffered=True)
        if message.author.id == self.client.user.id:
            return

        if checkTableExists(db, f'{message.guild.id}_ranks'):
            await updateData(message.author.id, f'{message.guild.id}_ranks', message)
        else:
            dbcursor.execute(f'CREATE TABLE {message.guild.id}_ranks (userid bigint PRIMARY KEY, exp int UNSIGNED,'
                             f' level int UNSIGNED)')
            await updateData(message.author.id, f'{message.guild.id}_ranks', message)

    @commands.command(aliases=['sqlx'])
    async def sql(self, ctx):
        dbcursor = db.cursor(buffered=True)
        dbcursor.execute(f"SELECT * FROM {ctx.guild.id}_ranks")
        for x in dbcursor.fetchall():
            await ctx.send(x)


def setup(client):
    client.add_cog(Test(client))
