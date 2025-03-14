import discord
import features.initialize.main
import features

def register(client: discord.Client, tree: discord.app_commands.CommandTree):
    @client.event
    async def on_ready():
        # 必要に応じてデータを初期化
        await features.initialize.main.run(client, tree)