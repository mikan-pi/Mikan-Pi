import discord

# treeの作成
def run(client: discord.Client):
    tree = discord.app_commands.CommandTree(client)
    return tree