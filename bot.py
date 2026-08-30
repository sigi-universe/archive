import os
import json
import random
from pathlib import Path
import tweepy

TWEETS_FILE = "tweets.json"
POSTED_FILE = "posted_titles.txt"


def load_tweets() -> dict:
    """事前生成済みの投稿文を読み込む"""
    if not Path(TWEETS_FILE).exists():
        raise FileNotFoundError(
            f"{TWEETS_FILE} が見つかりません。先に generate_tweets.py を実行してください。"
        )
    with open(TWEETS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def load_posted() -> set:
    p = Path(POSTED_FILE)
    if p.exists():
        return set(p.read_text(encoding="utf-8").splitlines())
    return set()


def save_posted(title: str):
    posted = load_posted()
    posted.add(title)
    Path(POSTED_FILE).write_text("\n".join(sorted(posted)), encoding="utf-8")


def pick_tweet(tweets: dict) -> tuple[str, dict | str]:
    """未投稿からランダムに1件選んで (title, payload) を返す"""
    posted = load_posted()
    candidates = [(t, v) for t, v in tweets.items() if t not in posted]

    if not candidates:
        # 全件投稿済み → リセット
        print("全件投稿済み → ローテーション再開")
        candidates = list(tweets.items())

    return random.choice(candidates)


def post_tweet(tweet_text: str, image_path: str | None = None):
    """メイン投稿のみ実行（画像があれば添付）"""
    # v1.1 API（画像アップロード用）
    auth = tweepy.OAuth1UserHandler(
        os.environ["API_KEY"],
        os.environ["API_SECRET"],
        os.environ["ACCESS_TOKEN"],
        os.environ["ACCESS_TOKEN_SECRET"]
    )
    api_v1 = tweepy.API(auth)

    # v2 API（ポスト送信用）
    client_v2 = tweepy.Client(
        bearer_token=os.environ["BEARER_TOKEN"],
        consumer_key=os.environ["API_KEY"],
        consumer_secret=os.environ["API_SECRET"],
        access_token=os.environ["ACCESS_TOKEN"],
        access_token_secret=os.environ["ACCESS_TOKEN_SECRET"],
    )

    media_ids = []

    # 画像が存在する場合はアップロードを実行
    if image_path and Path(image_path).exists():
        print(f"画像をアップロード中: {image_path}")
        media = api_v1.media_upload(filename=image_path)
        media_ids.append(media.media_id)
    elif image_path:
        print(f"警告: 画像ファイルが存在しません ({image_path})。テキストのみで投稿します。")

    # ポスト送信
    if media_ids:
        main = client_v2.create_tweet(text=tweet_text, media_ids=media_ids)
    else:
        main = client_v2.create_tweet(text=tweet_text)

    tweet_id = main.data["id"]
    print(f"投稿成功: https://x.com/i/web/status/{tweet_id}")


if __name__ == "__main__":
    tweets = load_tweets()
    title, payload = pick_tweet(tweets)

    # 旧形式（文字列のみ）と新形式（辞書型）の両方に対応
    if isinstance(payload, dict):
        text = payload.get("text", "")
        image_path = payload.get("image", None)
    else:
        text = payload
        image_path = None

    print(f"選択: {title}")
    print(f"投稿文: {text}  ({len(text)}字)")
    if image_path:
        print(f"画像: {image_path}")

    post_tweet(text, image_path)
    save_posted(title)
