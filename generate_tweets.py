"""
generate_tweets.py
LoA_Data_Omega_V8.yaml を読み込み、全エントリーの投稿文を
Claude APIで事前生成して tweets.json に保存する。

使い方:
  ANTHROPIC_API_KEY=xxx python generate_tweets.py
"""

import os
import json
import yaml
import time
import anthropic
from pathlib import Path

YAML_PATH   = "LoA_Data_Omega_V8.yaml"
OUTPUT_PATH = "tweets.json"
HASHTAG     = "#sigi"


def load_entries(path: str) -> list[dict]:
    with open(path, "r", encoding="utf-8-sig") as f:
        raw = f.read().replace("\\'", "'")   # YAML内の不正エスケープを修正
    data = yaml.safe_load(raw)
    return data.get("Entries", [])


def build_context(entry: dict) -> str:
    """エントリーからClaudeに渡すコンテキスト文字列を構築"""
    lines = [f"タイトル: {entry.get('Title', '')}"]

    # core_concept
    cc = entry.get("core_concept", {})
    if isinstance(cc, dict):
        for v in cc.values():
            if isinstance(v, dict):
                attr = v.get("attribute", "")
                fact = v.get("fact_value", "")
                if attr and fact:
                    lines.append(f"- {attr}: {fact}")

    # constraints
    rc = entry.get("the_rule_constraints", {})
    if isinstance(rc, dict):
        for v in rc.values():
            if isinstance(v, dict):
                subj = v.get("subject", "")
                desc = v.get("description", "")
                if desc:
                    lines.append(f"制約/{subj}: {desc}")
    elif isinstance(rc, str) and rc.strip():
        lines.append(f"制約: {rc.strip()}")

    # Content
    content = (entry.get("Content") or "").strip()
    if content:
        lines.append(f"補足: {content[:300]}")

    # 関連エントリー名（雰囲気の補強）
    rels = entry.get("Semantic_Relations", [])
    related = [r.get("Target_Title", "") for r in rels if r.get("Target_Title")]
    if related:
        lines.append(f"関連: {', '.join(related[:4])}")

    return "\n".join(lines)


def generate_tweet(client: anthropic.Anthropic, entry: dict) -> str:
    context = build_context(entry)

    prompt = f"""あなたはSF×ファンタジー創作プラットフォーム「Sigi Universe」の公式X担当です。
以下はこの世界のLore Architecture（設定資料）の1エントリーです。
これをもとにX（旧Twitter）の投稿文を1つ作成してください。

{context}

ルール:
- {HASHTAG} を必ず含める
- URLは含めない
- 120字以内（厳守）
- 世界観・物語の魅力が伝わる、詩的または知的な文体
- 投稿文のみ返す（説明・前置き・引用符なし）
"""

    msg = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=300,
        messages=[{"role": "user", "content": prompt}]
    )
    return msg.content[0].text.strip()


def main():
    entries = load_entries(YAML_PATH)
    print(f"{len(entries)} エントリー読み込み完了")

    # テスト用エントリーを除外
    entries = [e for e in entries if e.get("Title", "").startswith("テスト") is False
               and e.get("Title") != "テスト　Eclipsed"]

    client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

    # 既存の生成済みデータを読み込んで差分だけ生成
    existing: dict = {}
    if Path(OUTPUT_PATH).exists():
        with open(OUTPUT_PATH, "r", encoding="utf-8") as f:
            existing = json.load(f)
        print(f"既存: {len(existing)} 件 → 残り {len(entries) - len(existing)} 件を生成")

    tweets = dict(existing)

    for i, entry in enumerate(entries):
        title = entry.get("Title", f"entry_{i}")
        if title in tweets:
            continue  # 生成済みはスキップ

        print(f"[{i+1}/{len(entries)}] {title} ... ", end="", flush=True)
        try:
            tweet = generate_tweet(client, entry)
            tweets[title] = tweet
            print(f"OK ({len(tweet)}字)")
        except Exception as e:
            print(f"エラー: {e}")
            tweets[title] = f"【{title}】{HASHTAG}"  # フォールバック

        # 中間保存（APIエラーで途中停止しても安全）
        with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
            json.dump(tweets, f, ensure_ascii=False, indent=2)

        time.sleep(0.5)  # レート制限対策

    print(f"\n完了: {len(tweets)} 件 → {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
