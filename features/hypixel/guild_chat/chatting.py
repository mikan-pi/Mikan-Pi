"""
ループ実行
webhookチャンネルに送信されたデータをすべて読む
すべて消す
exp処理を行う
設定した適当なチャンネルに成型後のチャットを送信
"""
import discord
import features.exp.count
from config import HYPIXEL_GUILD_CHAT_SEND_CHANNEL_ID, HYPIXEL_GUILD_CHAT_WEBHOOK_CHANNEL_ID, HYPIXEL_FETCH_CYCLE
import public.embed
from features.hypixel.guild_chat.utils import parse_msg, get_mcid, mcid_to_discord
from discord.ext import tasks
from hypixel_token import HYPIXEL_TOKEN
import requests
from public.logging.logger import MainLogger


before_time_stamp = None
logger = MainLogger()


@tasks.loop(seconds=HYPIXEL_FETCH_CYCLE)
async def fetch_hypixel_guild_chat():
    # 定期的にAPIを送る
    url = f"https://api.hypixel.net/v2/skyblock/news?key={HYPIXEL_TOKEN}"
    r = requests.get(url)
    logger.info(f"fetch hypixel : {r.status_code}")
    

async def read_and_write(client: discord.Client, tree: discord.app_commands.CommandTree, message: discord.Message):
    exp = features.exp.count.experience(client)
    # データがwebhookによるものでなければkick
    # if message.webhook_id is None:
    #     return
    # channelがwebhookチャンネルでなければkick
    if message.channel.id != HYPIXEL_GUILD_CHAT_WEBHOOK_CHANNEL_ID:
        return
    names,msgs = parse_msg(message.content)
    
    for name, msg in zip(names, msgs):
        embed = public.embed.Embed.Default(description="\n".join(msg).replace("_", "\\_").replace("*", "\\*"))
        embed.set_thumbnail(url=None)
        mcid = get_mcid(name)
        discord_id = None
        if mcid is not None:
            discord_id = await mcid_to_discord(client, mcid)
        if discord_id is not None:
            #discord_idからアイコン・名前を取得
            user = discord.utils.get(message.guild.members, name=discord_id)
            if user is not None:
                user_name = user.name + f"({name})"
                user_icon = user.avatar.url if user.avatar else user.default_avatar.url
                # 誰か分かっていればexpを加算
                await exp.add_chat_exp(user.id)
            else:
                user_name = name + "(hypixelに登録されているdiscordリンク/IDが不正です)"
                user_icon = None
            embed.set_author(name = user_name, icon_url=user_icon)
        else:
            embed.set_author(name = name)
        await client.get_channel(HYPIXEL_GUILD_CHAT_SEND_CHANNEL_ID).send(embed=embed)
    await message.delete()
    