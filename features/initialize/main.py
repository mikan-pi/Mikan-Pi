import features.initialize.file
import discord

async def run(client: discord.Client):
    # ファイル初期化
    await features.initialize.file.run(client)
