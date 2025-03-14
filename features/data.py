from public.json_util import *
import discord
from discord.ext import tasks

# シングルトン
class BotData():
    _instance = None
    # 存在しなければ新しいインスタンスを作る
    def __new__(cls, client: discord.Client):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.client = client
        return cls._instance
    
    def __init__(self,client: discord.Client):
        if hasattr(self, 'initialized'): # 既にインスタンス化済み
            return
        self.initialized = True
        self.client = client
        self.data = {}

    # データの読み出しor作成
    def load(self):
        self.data = load_data()
    # データ全体を返す
    async def get_data(self):
        return self.data

    # データを新しいものに差し替える
    async def set_data(self,data):
        await save_data_and_upload(data, self.client)
        self.data = data
