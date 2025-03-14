import features.join_member
from features.core.make_intent import make_intent
from features.core.run import run
from bot_token import BOT_TOKEN
import features.core.on_ready

if __name__ == "__main__":
    client = make_intent()
    # bot起動時実行関数の登録
    features.core.on_ready.register(client)
    # メンバー参加時アクションの登録
    features.join_member.setup(client)
    run(client, BOT_TOKEN)