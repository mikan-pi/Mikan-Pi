import discord

def make_intent():
    intents = discord.Intents.default()
    intents.members = True  # メンバーの入退出イベントを有効化
    client = discord.Client(intents=intents)
    return client