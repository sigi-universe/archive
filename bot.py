import tweepy
import os
import json
import random
from pathlib import Path

TWEETS_FILE  = "tweets.json"
POSTED_FILE  = "posted_titles.txt"
SITE_URL     = "https://sigi-universe.com/"


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


def pick_tweet(tweets: dict) -> tuple[str, str] | None:
    """未投稿からランダムに1件選んで (title, text) を返す"""
    posted = load_posted()
    candidates = [(t, v) for t, v in tweets.items() if t not in posted]

    if not candidates:
        # 全件投稿済み → リセット
        print("全件投稿済み → ローテーション再開")
        candidates = list(tweets.items())

    return random.choice(candidates)


def post_with_reply(tweet_text: str, reply_url: str):
    """メイン投稿 → リプライでURL挿入"""
    client = tweepy.Client(
        bearer_token=os.environ["BEARER_TOKEN"],
        consumer_key=os.environ["API_KEY"],
        consumer_secret=os.environ["API_SECRET"],
        access_token=os.environ["ACCESS_TOKEN"],
        access_token_secret=os.environ["ACCESS_TOKEN_SECRET"],
    )

    main = client.create_tweet(text=tweet_text)
    tweet_id = main.data["id"]
    print(f"投稿成功: https://x.com/i/web/status/{tweet_id}")

    client.create_tweet(text=reply_url, in_reply_to_tweet_id=tweet_id)
    print("リプライ（URL）添付完了")


if __name__ == "__main__":
    tweets = load_tweets()
    title, text = pick_tweet(tweets)

    print(f"選択: {title}")
    print(f"投稿文: {text}  ({len(text)}字)")

    post_with_reply(text, SITE_URL)
    save_posted(title)

