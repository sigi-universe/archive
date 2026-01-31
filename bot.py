import tweepy
import os

def initial_shot():
    # 登録した合鍵（Secrets）を召喚
    keys = {
        "k": os.environ["API_KEY"],
        "ks": os.environ["API_SECRET"],
        "at": os.environ["ACCESS_TOKEN"],
        "ats": os.environ["ACCESS_TOKEN_SECRET"],
        "bt": os.environ["BEARER_TOKEN"]
    }

    # 認証（v2 APIを使用）
    client = tweepy.Client(
        bearer_token=keys["bt"],
        consumer_key=keys["k"],
        consumer_secret=keys["ks"],
        access_token=keys["at"],
        access_token_secret=keys["ats"]
    )

    # ポスト内容
    tweet_text = "共同創作プラットフォーム「sigi」では、世界観構築（ユニバースビルディング）を共に行う初期メンバーを募集しています。 #sigi #共同創作 #世界観設定"

    try:
        client.create_tweet(text=tweet_text)
        print("ポスト成功")
    except Exception as e:
        print(f"不発（エラー）: {e}")

if __name__ == "__main__":
    initial_shot()
