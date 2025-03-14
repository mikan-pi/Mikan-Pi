DEV_MODE = True

GUILD_ID = 864093335123001374 if DEV_MODE else 807264600718442516
SYS_CHANNEL_ID = 1349749883506003979 if DEV_MODE else 1327223543548870678
BACKUP_CHANNEL_ID = 1349752769434878033 if DEV_MODE else 1349752853111242794


EXP_ROLE = {
    "role": 250,    # 持っているロール1つ辺りの経験値
    "chat": 1,      # メッセージ1つ辺りの経験値
    "voice": 3      # vc接続10分毎の経験値
}


# レベルアップに必要な総経験値
LEVEL_EXP = {
    1: 250,
    2: 500,
    3: 1000,
    4: 1500,
    5: 2500,
    6: 5000,
    7: 10000,
    8: 20000,
    9: 50000,
    10: 100000
}

# 1cycleの時間(秒)
CYCLE_TIME = 60 * 10

# discordにデータファイルをアップロード(バックアップ)する周期
BACKUP_CYCLE_SEC = 60


