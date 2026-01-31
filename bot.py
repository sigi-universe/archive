import tweepy
import os
import random

def get_tweet_variations():
    """投稿内容のバリエーション（20種類）"""
    return [
        "共同創作プラットフォーム「sigi」では、世界観構築を共に行う初期メンバーを募集しています。 #sigi #共同創作",
        "【メンバー募集】sigiで新しいユニバースを構築しませんか？議論から始まる物語制作。 #sigi #世界観設定",
        "設定の議論を核とした創作サイト「sigi」。現在、基盤作りに携わる初期メンバーを募集中です。#共同創作",
        "一人の想像力を、コミュニティの創造力へ。sigiはユニバースビルディングのためのプラットフォームです。#共同創作 #sigi",
        "「sigi」では、特定の作法に縛られず、純粋に世界観を育てる仲間を探しています。 #共同創作 #sigi",
        "あなたのアイデアが世界の礎になる。共同創作サイト「sigi」で初期メンバーとして活動しませんか？#共同創作",
        "【募集】ユニバースビルディングに特化したサイト「sigi」。新しい物語の形を共に模索しましょう。 #sigi",
        "sigiは「議論」で世界を創る場所。設定を練り上げるのが好きな初期メンバーを募集しています。#共同創作",
        "物語の「種」を共有し、みんなで大樹に育てる。そんな共同創作をsigiで始めませんか？ #sigi #世界観構築",
        "【sigi】初期メンバー募集中。世界観構築のプロセスそのものを楽しむプラットフォームです。 #共同創作",
        "ゼロから世界を構築する。共同創作プラットフォーム「sigi」であなたの設定を共有してください。#共同創作",
        "sigiでは、相互のフィードバックを通じて深まる世界観を目指しています。初期メンバー募集中。#共同創作 #sigi",
        "文字数や書式よりも「設定の整合性と広がり」を重視する。そんな創作をsigiで。 #世界観設定 #sigi",
        "共同創作サイト「sigi」始動。世界観を共に作り上げる、熱意ある初期メンバーを募集しています。#共同創作",
        "あなたの考える「最強の世界観」をsigiで形にしませんか？構築メンバー募集中。 #sigi #共同創作",
        "議論が物語を加速させる。ユニバースビルディングサイト「sigi」の初期メンバー募集。",
        "sigiは創作の「過程」を重視します。設定構築の議論に参加してくれるメンバーを募集中。#共同創作 #sigi",
        "【急募】sigiのユニバースを共に広げる初期メンバー。詳細はサイトを確認してください。 #共同創作",
        "一人では到達できない設定の深みへ。共同創作プラットフォーム「sigi」で世界を創りましょう。#共同創作",
        "共同創作の新しい形。sigiで世界観構築のパイオニアになりませんか？初期メンバー募集中。#共同創作 #sigi"
    ]

def initial_shot():
    keys = {
        "k": os.environ["API_KEY"],
        "ks": os.environ["API_SECRET"],
        "at": os.environ["ACCESS_TOKEN"],
        "ats": os.environ["ACCESS_TOKEN_SECRET"],
        "bt": os.environ["BEARER_TOKEN"]
    }

    client = tweepy.Client(
        bearer_token=keys["bt"],
        consumer_key=keys["k"],
        consumer_secret=keys["ks"],
        access_token=keys["at"],
        access_token_secret=keys["ats"]
    )

    # ランダムに1つ選択
    tweet_text = random.choice(get_tweet_variations())

    try:
        client.create_tweet(text=tweet_text)
        print(f"ポスト成功: {tweet_text}")
    except Exception as e:
        print(f"不発（エラー）: {e}")

if __name__ == "__main__":
    initial_shot()
