import discord
import features.vc.voicebox.define
import features.data
from discord import app_commands

import public.embed

async def get_characters_choice_format(interaction: discord.Interaction, current: str):
    return [
        app_commands.Choice(name=value, value=key) for key, value in features.vc.voicebox.define.voicebox_id_to_name.items() if value.startswith(current)
    ][:25]


def register(client: discord.Client, tree: discord.app_commands.CommandTree):
    vc_command_group = discord.app_commands.Group(name="vc", description="vcに関するコマンド")
    data = features.data.BotData()
    @vc_command_group.command(name="join", description="vcに参加します")
    async def vc(interaction: discord.Interaction):
        if interaction.user.voice is None:
            await interaction.response.send_message("vcに参加していません", ephemeral=True)
            return
        await interaction.user.voice.channel.connect()
        await interaction.response.send_message("vcに参加しました", ephemeral=True)
    @vc_command_group.command(name="autojoin", description="現在あなたがいるvcに今後メンバーがいる場合、自動で読み上げを開始します。この設定は最後に設定した1つのチャンネルで有効です。")
    async def autojoin(interaction: discord.Interaction):
        pass
    @vc_command_group.command(name="set-voice", description="現在あなたがいるvcに今後メンバーがいる場合、自動で読み上げを開始します。この設定は最後に設定した1つのチャンネルで有効です。")
    @app_commands.autocomplete(
        character = get_characters_choice_format
    )
    async def set_voice(interaction: discord.Interaction, character: int):
        embed = public.embed.Embed.Default()
        user_id = str(interaction.user.id)
        if "userdata" not in data.data:
            data.make_user(user_id)
        if user_id not in data.data["userdata"]:
            data.data[user_id] = {}
        data.data["userdata"][user_id]["vc_character"] = character
        # データを保存する
        await data.set_data()
        embed.add_field(name="Success", value=f"読み上げを{features.vc.voicebox.define.voicebox_id_to_name[character]}に変更しました。", inline=False)
        await interaction.response.send_message(embed=embed, ephemeral=True)

    tree.add_command(vc_command_group)
    pass