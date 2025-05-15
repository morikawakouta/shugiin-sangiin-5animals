import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
# プロフィール文の収集


# 出力ファイルのパス（この.pyと同じ場所にあるCSV）
script_dir = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(script_dir, "profiles.csv")

# 現在の最大IDを取得（今回は11～475まで想定）
START_ID = 11
END_ID = 475

# URLリスト作成
base_url = "https://www.shugiin.go.jp/internet/itdb_giinprof.nsf/html/profile/"
profile_urls = [f"{base_url}{str(i).zfill(3)}.html" for i in range(START_ID, END_ID + 1)]

# 既存CSV読み込み（なければ空で）
if os.path.exists(csv_path):
    df_existing = pd.read_csv(csv_path, encoding="utf-8-sig")
    existing_names = set(df_existing["氏名"].tolist())
else:
    df_existing = pd.DataFrame(columns=["氏名", "プロフィール"])
    existing_names = set()

def get_name_and_profile(url):
    try:
        res = requests.get(url, timeout=10)
        res.encoding = "shift_jis"
        soup = BeautifulSoup(res.text, "html.parser")
        contents = soup.find("div", id="contents")
        if not contents:
            return ("名前取得失敗", "本文取得失敗")

        h2 = contents.find("h2")
        name = h2.get_text(strip=True).split("（")[0] if h2 else "名前取得失敗"

        profile_text = contents.get_text(separator="\n", strip=True)
        return (name, profile_text)

    except Exception as e:
        return ("取得エラー", f"エラー内容: {e}")

# 追加取得ループ
new_records = []
for url in profile_urls:
    print(f"確認中: {url}")
    name, profile = get_name_and_profile(url)

    if name in existing_names or "取得エラー" in name:
        print(f"スキップ: {name}")
        continue

    new_records.append({"氏名": name, "プロフィール": profile})

# 追記して保存
if new_records:
    df_new = pd.DataFrame(new_records)
    df_combined = pd.concat([df_existing, df_new], ignore_index=True)
    df_combined.to_csv(csv_path, index=False, encoding="utf-8-sig", lineterminator="\r\n")
    print(f"✅ {len(new_records)} 件を追記しました → {csv_path}")
else:
    print("🔁 新規データなし。スキップしました。")
