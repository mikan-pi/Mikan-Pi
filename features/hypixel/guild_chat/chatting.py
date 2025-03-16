"""
ループ実行
webhookチャンネルに送信されたデータをすべて読む
すべて消す
exp処理を行う
設定した適当なチャンネルに成型後のチャットを送信
"""
import discord
import features.exp.count
from config import HYPIXEL_GUILD_CHAT_SEND_CHANNEL_ID, HYPIXEL_GUILD_CHAT_WEBHOOK_CHANNEL_ID
import public.embed
from features.hypixel.guild_chat.utils import parse_msg, get_mcid, mcid_to_discord

before_time_stamp = None

async def read_and_write(client: discord.Client, tree: discord.app_commands.CommandTree, message: discord.Message):
    exp = features.exp.count.experience(client)
    # データがwebhookによるものでなければkick
    if message.webhook_id is None:
        return
    # channelがwebhookチャンネルでなければkick
    if message.channel.id != HYPIXEL_GUILD_CHAT_WEBHOOK_CHANNEL_ID:
        return
    name,msg = parse_msg(message.content)
    
    embed = public.embed.Embed.Default(title=name, description="\n".join(msg))
    mcid = get_mcid(name)
    discord_id = None
    if mcid is not None:
        discord_id = await mcid_to_discord(client, mcid)
    if discord_id is not None:
        #discord_idからアイコン・名前を取得
        user = discord.utils.get(message.guild.members, name=discord_id)
        user_name = user.name
        user_icon = user.avatar.url if user.avatar else user.default_avatar.url
        embed.set_author(name = user_name, icon_url=user_icon)
        # 誰か分かっていればexpを加算
        await exp.add_chat_exp(user.id)
    else:
        embed.set_author(name = name)
    await message.delete()
    await client.get_channel(HYPIXEL_GUILD_CHAT_SEND_CHANNEL_ID).send(embed=embed)
    