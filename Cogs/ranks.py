from discord.ext import commands


class Test(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def testcommand(self, ctx):
        await ctx.send('negro')


def setup(client):
    client.add_cog(Test(client))
