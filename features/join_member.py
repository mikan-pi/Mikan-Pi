from config import SYS_CHANNEL_ID
import discord
from features.data import BotData
from public.embed import Embed

def setup(client):
    data = BotData(client)
    @client.event
    async def on_member_join(member):
        channel_id = SYS_CHANNEL_ID  # 送信するチャンネルのIDに置き換える
        channel = client.get_channel(channel_id)
        
        if channel:
            # 人数を加算
            items = await data.get_data()
            items["join_order"] += 1
            await data.set_data(items)
            embed = Embed.Default(
                title=f"Join #{items.get('join_order')}", # 現在の人数を送信
                description=f"Mi Server へようこそ！"
            )
            embed.set_author(name=member.name, icon_url=member.avatar.url if member.avatar else member.default_avatar.url)
            await channel.send(embed=embed)
