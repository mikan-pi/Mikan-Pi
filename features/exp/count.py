from config import GUILD_ID, EXP_RATE, LEVEL_EXP, CYCLE_TIME, VC_EXP_CYCLE_SEC, EXP_IGNORE_ROLES
from features.data import BotData
import asyncio
import discord
from discord.ext import tasks
from features.exp.card import create_image
from public.logging.logger import MainLogger
import time

class experience:
    def __init__(self,client: discord.Client):
        self.client = client
        self.data = BotData(client)
        self.logger = MainLogger()

        self.sort_objs = {"time-stamp": 0, "data": {}}
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
                    await member.send(f"Miレベルが{level}になりました。サーバーで報告してみましょう！", file=discord.File(await create_image(level, self, member), filename="level.png"))
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

    async def sort(self, cache_time):
        # 順位順(経験値)にソート
        # ただし、前回のソートから10分経過していない場合にはソートせず、前回の順位表を返す
        # データが存在しないなら
        if not self.data.data["userdata"]:
            return {}
        # time-stampとの差がcache_time以上なら
        if int(time.time()) - self.sort_objs["time-stamp"] > cache_time:
            self.sort_objs["time-stamp"] = int(time.time())
            self.data.data["userdata"] = dict(sorted(self.data.data["userdata"].items(), key=lambda x: x[1]["chat_experience"] + x[1]["vc_experience"] + x[1]["role_experience"], reverse=True))
            self.sort_objs["data"] = self.data.data["userdata"]
        return self.sort_objs["data"]

    async def get_rank(self,member_id):
        """
        サーバー内順位を返す(1-index)

        """
        member_id = str(member_id)
        # ソートして自身のキーがいくつ目かを返す
        sorted_keys = list((await self.sort(cache_time=10 * 60)).keys())
        for rank, key in enumerate(sorted_keys, start=1):
            if key == member_id:
                return rank

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

    def __len__(self):
        return len(self.data.data["userdata"])