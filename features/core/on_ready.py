import discord
import features.initialize.main
import features
from public.logging.logger import MainLogger

def register(client: discord.Client, tree: discord.app_commands.CommandTree):
    logger = MainLogger()
    @client.event
    async def on_ready():
        # 必要に応じてデータを初期化
        await features.initialize.main.run(client, tree)
        # ログ出力
        logger.info("OnReady - Ended -")