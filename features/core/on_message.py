import discord
import features.exp.count
import config

# メッセージ受信時、呼び出す処理
def register(client: discord.Client, tree: discord.app_commands.CommandTree):
    exp = features.exp.count.experience(client)
    @client.event
    async def on_message(message: discord.Message):
        if message.author.bot: # botの場合はスキップ
            return
        # 経験値処理
        # もし、指定したguildでなければ無視する
        if message.guild is None:
            return
        if message.guild.id == config.GUILD_ID:
            await exp.add_chat_exp(message.author.id)