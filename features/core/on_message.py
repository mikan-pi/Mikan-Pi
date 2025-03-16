import discord
import features.exp.count
import features.hypixel.guild_chat.chatting
import config
from public.logging.logger import MainLogger

logger = MainLogger()
# メッセージ受信時、呼び出す処理
def register(client: discord.Client, tree: discord.app_commands.CommandTree):
    exp = features.exp.count.experience(client)
    @client.event
    async def on_message(message: discord.Message):
        if message.author.bot and message.webhook_id is None: # botの場合はスキップ
            return
        # データが正常にロードされる前なら無視
        if not exp.data.isloaded:
            logger.info("exp data is not loaded")
            return
        # 経験値処理
        # もし、指定したguildでなければ無視する
        if message.guild is None:
            return
        if message.guild.id == config.GUILD_ID:
            if message.webhook_id is None: 
                await exp.add_chat_exp(message.author.id)# ユーザーによるチャットなら経験値を1加算
            await features.hypixel.guild_chat.chatting.read_and_write(client, tree, message)
