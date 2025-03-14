import json
from config import BACKUP_CHANNEL_ID, BACKUP_CYCLE_SEC, BACKUP_CHANNEL_ID
import asyncio
import os

is_register_uploaded = False

def init_data(Data  = {
        "userdata": {}, # ユーザが持つ経験値などの情報
        "join_order": 1 # 何人目の参加者かの情報
    }) -> dict:
    
    # ./data.json
    with open('./data.json', 'w') as f:
        json.dump(Data, f)
    return Data

# discordに送る
def send_data(data, client, channel = BACKUP_CHANNEL_ID) -> None:
    channel = client.get_channel(channel)
    if channel:
        channel.send(json.dumps(data))

def save_data(data) -> None:
    with open('./data.json', 'w') as f:
        json.dump(data, f)

async def save_data_and_upload(data, client) -> None:
    with open('./data.json', 'w') as f:
        json.dump(data, f)
    await upload_data(client, data)


def load_data() -> dict:
    if not os.path.exists('./data.json'):
        init_data()
    with open('./data.json', 'r') as f:
        return json.load(f)

async def upload_data(client, data) -> None:
    channel = client.get_channel(BACKUP_CHANNEL_ID)
    data = "```json\n" + json.dumps(data) + "\n```"
    if channel:
        await channel.send(data)