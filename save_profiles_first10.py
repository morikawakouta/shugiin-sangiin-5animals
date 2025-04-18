import requests
from bs4 import BeautifulSoup
import pandas as pd
import os

# 出力ファイル（スクリプトと同じ場所に保存）
script_dir = os.path.dirname(os.path.abspath(__file__))
output_path = os.path.join(script_dir, "profiles.csv")

# URLリスト（001〜010）
base_url = "https://www.shugiin.go.jp/internet/itdb_giinprof.nsf/html/profile/"
profile_urls = [f"{base_url}{str(i).zfill(3)}.html" for i in range(1, 11)]

def get_name_and_profile(url):
    try:
        res = requests.get(url, timeout=10)
        res.encoding = "shift_jis"  # ← これが重要！
        soup = BeautifulSoup(res.text, "html.parser")
        contents = soup.find("div", id="contents")
        if not contents:
            return ("名前取得失敗", "本文取得失敗")

        # 氏名は h2 タグ、「（」の前だけ
        h2 = contents.find("h2")
        name = h2.get_text(strip=True).split("（")[0] if h2 else "名前取得失敗"

        profile_text = contents.get_text(separator="\n", strip=True)
        return (name, profile_text)

    except Exception as e:
        return ("取得エラー", f"エラー内容: {e}")

# データ取得と保存
records = []
for url in profile_urls:
    print(f"取得中: {url}")
    name, profile = get_name_and_profile(url)
    records.append({"氏名": name, "プロフィール": profile})

df = pd.DataFrame(records)
df.to_csv(output_path, index=False, encoding="utf-8-sig", lineterminator="\r\n")
print(f"✅ 保存完了: {output_path}")
