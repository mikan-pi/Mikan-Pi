from public.json_util import *
import discord
from discord.ext import tasks

# シングルトン
class BotData():
    _instance = None
    # 存在しなければ新しいインスタンスを作る
    def __new__(cls, client: discord.Client = None):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.client = client
            cls._instance.data = cls._instance.load()
            cls._instance.isloaded = False
        return cls._instance
    
    def __init__(self,client: discord.Client = None):
        pass

    def set_client(self, client: discord.Client):
        self.client = client

    # データの読み出しor作成
    def load(self):
        self.data = load_data()
        self.isloaded = True
        return self.data
    # データ全体を返す
    async def get_data(self):
        return self.data

    # データを新しいものに差し替える
    async def set_data(self,data = None):
        if data is None:
            data = self.data
        if not self.isloaded:
            data |= self.load()
        if self.client is None:
            save_data(data)
        else:
            await save_data_and_upload(data, self.client)
        self.data = data

    async def make_user(self, member_id: int) -> None:
        if not self.data["userdata"].get(str(member_id)):
            self.data["userdata"][str(member_id)] = {
                "role_experience": 0,
                "vc_experience": 0,
                "chat_experience": 0,
                "level": -1,
            }
            await self.set_data(self.data)