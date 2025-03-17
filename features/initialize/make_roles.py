import discord
from features.data import BotData
import config

async def run(client: discord.client):
    data = BotData(client)
    # ロールを作成
    # 記録されているロールを削除
    for role_id in data.data.get("level_roles", {}).values():
        for guild in client.guilds:
            role = guild.get_role(role_id)
            if role:  # ロールが存在するなら削除
                await role.delete()

    # データを削除
    data.data["level_roles"] = {}
    # 新たに10個準備する
    for i in range(config.MAX_LEVEL + 1):
        for guild in client.guilds:
            role = await guild.create_role(name=f"level{i}", color = discord.Color.from_str(config.LEVEL_ROLES_COLOR[i]))
            # ロールidを追加
            data.data["level_roles"][str(i)] = role.id


    await data.set_data()
