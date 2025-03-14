import features.initialize.file
import features.exp.count
import discord

async def run(client: discord.Client, tree: discord.app_commands.CommandTree):
    # コマンドの登録
    await tree.sync()
    # ファイル初期化
    await features.initialize.file.run(client)
    # ループタスクの登録
    features.exp.count.experience(client).register_calc_experience.start()
    features.exp.count.experience(client).register_calc_vc_experience.start()