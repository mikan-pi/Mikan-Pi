import discord
import features.initialize.main
import features
from public.logging.logger import MainLogger

is_ready = False

def register(client: discord.Client, tree: discord.app_commands.CommandTree):
    logger = MainLogger()
    @client.event
    async def on_ready():
        global is_ready
        if is_ready: return
        is_ready = True
        # 必要に応じてデータを初期化
        await features.initialize.main.run(client, tree)
        # ログ出力
        logger.info("OnReady - Ended -")