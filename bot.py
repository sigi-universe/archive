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

    # 記念すべき初弾のポスト内容
    # 資料「ネタ」の管理会社「蛇」っぽいトーンだ
    tweet_text = "管理会社『蛇』より。スカイマンション（空中開発タカラ）の観測を開始しました。入居者の皆さんは、実存の漏洩と配管の歪みに十分注意してください。イキスギィ！ #スカイマンション #蛇"

    try:
        client.create_tweet(text=tweet_text)
        print("初弾発射成功。ネットの海が孕んだぜ。")
    except Exception as e:
        print(f"不発（エラー）: {e}")

if __name__ == "__main__":
    initial_shot()
