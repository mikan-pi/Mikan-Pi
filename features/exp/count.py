from config import GUILD_ID, EXP_RATE, LEVEL_EXP, CYCLE_TIME, VC_EXP_CYCLE_SEC, EXP_IGNORE_ROLES
from features.data import BotData
import asyncio
import discord
from discord.ext import tasks
from features.exp.card import create_image
from public.logging.logger import MainLogger

class experience:
    def __init__(self,client: discord.Client):
        self.client = client
        self.data = BotData(client)
        self.logger = MainLogger()
    @tasks.loop(seconds=CYCLE_TIME)
    async def register_calc_experience(self):
        # メンバー全員を取得
        guild = self.client.get_guild(GUILD_ID)
        members = guild.members

        # 経験値を計算する処理を実行
        for member in members:
            if member.bot: # botの場合はスキップ
                continue
            # memberが持っているロール*LEVEL_RATEを経験値とする(ただし、レベルロールは無効なので、-1にする)
            experience = (len(member.roles) - 1) * (EXP_RATE["role"])
            for igrole in EXP_IGNORE_ROLES:
                if discord.utils.get(member.roles, id=igrole) in member.roles:
                    experience -= EXP_RATE["role"]
            for igrole in self.data.data["level_roles"].values():
                if discord.utils.get(member.roles, id=igrole) in member.roles:
                    experience -= EXP_RATE["role"]
            # もしuserdataにmember.idのキーがなかったら
            if not self.data.data["userdata"].get(str(member.id)):
                await self.data.make_user(member.id)
            self.data.data["userdata"][str(member.id)]["role_experience"] = experience

            # 計算後の経験値に応じてdata.data["level_roles"]のロールを付与
            level = await self.get_level(member.id)
            # levelが前回と違うならロールを処理
            if self.data.data["userdata"][str(member.id)]["level"] != level:
                self.logger.info(f"member:{member.name} level:{self.data.data['userdata'][str(member.id)]['level']} -> {level}")
                # かつ、データ上のlevelが-1でないならDMにメッセージを送る
                # (参加時にDMを即座に飛ばしたくない)
                if self.data.data["userdata"][str(member.id)]["level"] != -1:
                    self.logger.info(f"member:{member.name} send DM")
                    await member.send(f"Miレベルが{level}になりました。", file=discord.File(await create_image(level, self, member), filename="level.png"))
                append = self.data.data["level_roles"].get(str(level))
                append = discord.utils.get(member.guild.roles, id=append)
                if append:
                    # ロールを付与
                    await member.add_roles(append)
                    # 不要になったロールを削除
                    remove = self.data.data["level_roles"].get(str(level - 1))
                    remove = discord.utils.get(member.guild.roles, id=remove)
                    if remove:
                        await member.remove_roles(remove)
                    remove = self.data.data["level_roles"].get(str(level + 1))
                    remove = discord.utils.get(member.guild.roles, id=remove)
                    if remove:
                        await member.remove_roles(remove)
            self.data.data["userdata"][str(member.id)]["level"] = level
        await self.data.set_data()


    @tasks.loop(seconds=VC_EXP_CYCLE_SEC)
    async def register_calc_vc_experience(self):
        # メンバー全員を取得
        guild = self.client.get_guild(GUILD_ID)
        members = guild.members

        # 経験値を計算する処理を実行
        for member in members:
            if member.bot: # botの場合はスキップ
                continue
            # memberがvcに参加していればexpを加算
            if member.voice and member.voice.channel:
                if not self.data.data["userdata"].get(str(member.id)):
                    await self.data.make_user(member.id)
                self.data.data["userdata"][str(member.id)]["vc_experience"] += EXP_RATE["voice"]
        await self.data.set_data()

    async def add_chat_exp(self, member_id):
        if not self.data.data["userdata"].get(str(member_id)):
            await self.data.make_user(member_id)
        self.data.data["userdata"][str(member_id)]["chat_experience"] += EXP_RATE["chat"]

    async def get_level(self,member_id):
        # userdaraキーが無ければ返す
        if not "userdata" in self.data.data:
            return "Disabled"
        if str(member_id) not in self.data.data["userdata"]:
            return 0
        sum_exp = sum(await self.get_exp(member_id))
        # levelxpのどこまで到達しているかのindexを返す
        return len(list(filter(lambda x: x[1] <= sum_exp, LEVEL_EXP.items())))
    
    async def get_exp(self,member_id):
        if str(member_id) not in self.data.data["userdata"]:
            return 0
        return self.data.data["userdata"][str(member_id)]["role_experience"], self.data.data["userdata"][str(member_id)]["vc_experience"], self.data.data["userdata"][str(member_id)]["chat_experience"]
