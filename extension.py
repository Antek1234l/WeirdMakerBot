import discord, random
from discord.ext import commands

hlink = ""

class Test(commands.Cog):


    def __init__(self, client):
        self.client = client

    # Właściwy kod
    @commands.Cog.listener()
    async def on_message(self, message):
        global hlink
        if message.content.startswith('wm!'):
            try:
                hlink = (message.attachments[0].url)
            except Exception:
                print('Log message')
            if hlink == "":
                pass
            else:
                with open ("hlink.txt", "w") as f:
                    f.write(hlink)


    @commands.command()
    async def example(self, ctx):
        if "example" in ctx.message.content:
            await ctx.send("example jest w wiadomości")

def setup(client):
    client.add_cog(Test(client))