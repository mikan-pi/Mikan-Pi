from public.json_util import init_data
import discord
import config
import logging
from features.data import BotData
import os

async def run(client: discord.Client):
    # ファイルがないなら新しいデータを作る
    if not os.path.exists('./data.json'):
        # 現在の人数を取得
        guild = config.GUILD_ID
        guild = client.get_guild(guild)
        member_count = len(guild.members)
        init_data({
            "userdata": {}, # ユーザが持つ経験値などの情報
            "join_order": member_count # 何人目の参加者かの情報
        })
    # データインスタンスの作成
    data = BotData(client)
    data.load()