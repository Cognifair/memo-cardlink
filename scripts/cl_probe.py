# -*- coding: utf-8 -*-
"""卡跳跳辅助：只读解析官方 OpenAPI 的牌组/章节/卡片，取出 root_id。不写入。"""
import json, os, sys, time
import requests

BASE = "https://open.maimemo.com/open/api/v1"
TOKEN = os.environ.get("MAIMEMO_TOKEN", "").strip()
if not TOKEN:
    print("MAIMEMO_TOKEN missing"); sys.exit(2)
H = {"Authorization": f"Bearer {TOKEN}", "Accept": "application/json"}


def get(path, **params):
    for attempt in range(4):
        r = requests.get(BASE + path, headers=H, params=params or None, timeout=30)
        if r.status_code == 429:
            time.sleep(2 + attempt * 2); continue
        body = r.json()
        if body.get("success") is not True:
            raise RuntimeError(f"{r.status_code} {body.get('errors')}")
        return body["data"]
    raise RuntimeError("rate limited")


def paged(path, key):
    out, offset = [], 0
    while True:
        d = get(path, offset=offset, limit=100)
        items = d.get(key, [])
        out.extend(items)
        total = int(d.get("total", len(out)))
        if not items or len(out) >= total:
            break
        offset += len(items)
        time.sleep(0.15)
    return out


cmd = sys.argv[1] if len(sys.argv) > 1 else "decks"
if cmd == "decks":
    for d in paged("/markji/decks", "decks"):
        print(d.get("id"), "|", d.get("name"), "| cards", d.get("card_count"),
              "| chapters", d.get("chapter_count"))
elif cmd == "chapters":
    deck = sys.argv[2]
    for c in paged(f"/markji/decks/{deck}/chapters", "chapters"):
        print(c.get("id"), "|", c.get("name"), "| cards", c.get("card_count"))
elif cmd == "probe":
    deck, card = sys.argv[2], sys.argv[3]
    d = get(f"/markji/decks/{deck}/cards/{card}")
    c = d.get("card", d)
    print(json.dumps({k: v for k, v in c.items() if k != "content"}, ensure_ascii=False, indent=1))
elif cmd == "dumptree":
    deck = sys.argv[2]
    tree = []
    for ch in paged(f"/markji/decks/{deck}/chapters", "chapters"):
        cid = ch.get("id")
        detail = get(f"/markji/decks/{deck}/chapters/{cid}")
        chd = detail.get("chapter", detail)
        tree.append({"chapter_id": cid, "name": ch.get("name"),
                     "cards": chd.get("cards", [])})
        time.sleep(0.15)
    print(json.dumps(tree, ensure_ascii=False, indent=1))
