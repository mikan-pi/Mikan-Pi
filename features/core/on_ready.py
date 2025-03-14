import discord
import features.initialize.main
import features

def register(client: discord.Client):
    @client.event
    async def on_ready():
        # 必要に応じてデータを初期化
        await features.initialize.main.run(client)