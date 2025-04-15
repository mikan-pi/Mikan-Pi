import discord
import features.vc.voicebox.utils

import io
import asyncio

import features.data

data = features.data.BotData()

async def check(client: discord.Client, message: discord.Message):
    # vcにbot自身が参加しているならその内容を読み上げる
    voice_client = discord.utils.get(client.voice_clients, guild=message.guild)
    if voice_client and voice_client.is_connected():
        return voice_client
    return False

async def read(voice_client: discord.VoiceClient, audio_buffer: discord.Message):
    # ffmpeg に pipe（標準入力）で渡す
    audio_source = discord.FFmpegPCMAudio(
        source=audio_buffer,
        pipe=True,
        before_options="-nostdin",
        options="-f wav"
    )

    if voice_client.is_playing():
        voice_client.stop()

    voice_client.play(audio_source)

    while voice_client.is_playing():
        await asyncio.sleep(1)

async def check_and_read(client: discord.Client, message: discord.Message):
    if not (voice_client := await check(client, message)):
        return
    # user_idから登録されたボイスを再生する
    user_id = str(message.author.id)
    character_id = data.data.get("userdata", {}).get(user_id, {}).get("vc_character", 1)
    content = await features.vc.voicebox.utils.synthesize_voice(message.content, character_id)
    if not content:
        return
    await read(voice_client, content)
