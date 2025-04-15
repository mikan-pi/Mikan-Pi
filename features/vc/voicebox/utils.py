import aiohttp
from io import BytesIO

async def synthesize_voice(text, speaker=1):
    async with aiohttp.ClientSession() as session:
        # 1. クエリ作成
        query_url = 'http://localhost:50021/audio_query'
        async with session.post(query_url, params={'text': text, 'speaker': speaker}) as resp:
            if resp.status != 200:
                print(f"Error in audio_query: {await resp.text()}")
                return
            query = await resp.json()
        # 2. 音声合成
        synthesis_url = 'http://localhost:50021/synthesis'
        async with session.post(synthesis_url, params={'speaker': speaker}, json=query) as resp:
            if resp.status == 200:
                data = await resp.read()
                with open("output.wav", "wb") as f:
                    f.write(data)
                return BytesIO(data)
            else:
                print(f"Error in synthesis: {await resp.text()}")