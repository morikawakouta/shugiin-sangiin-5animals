import requests
from bs4 import BeautifulSoup
import os
from urllib.parse import urljoin
import re

# リストページ（第217回）
list_url = "https://www.sangiin.go.jp/japanese/joho1/kousei/giin/217/giin.htm"

# 保存先
save_dir = "C:/Users/k-mor/Dropbox/code/5animal/VScode/shugiin-sangiin-5animals/docs/image/profile_sangiin"
os.makedirs(save_dir, exist_ok=True)

# 議員リスト取得
res = requests.get(list_url)
res.encoding = res.apparent_encoding
soup = BeautifulSoup(res.text, "html.parser")

link_tags = soup.select("table a[href*='profile']")

for idx, link_tag in enumerate(link_tags, start=1):
    try:
        name_raw = link_tag.text.strip()
        name = re.sub(r'[\\/:*?"<>|]', '', name_raw)  # ファイル名から危険文字除去

        profile_url = urljoin(list_url, link_tag["href"])
        res2 = requests.get(profile_url)
        res2.encoding = res2.apparent_encoding
        profile_soup = BeautifulSoup(res2.text, "html.parser")

        # <div id="profile-photo"> 内の <img src="...">
        photo_div = profile_soup.find("div", id="profile-photo")
        img_tag = photo_div.find("img") if photo_div else None
        if not img_tag or not img_tag.get("src"):
            print(f"❌ 写真なし: {name}")
            continue

        photo_url = urljoin(profile_url, img_tag["src"])  # ../photo/ を補完して完全URLに
        print(f"▶ {name} の写真URL: {photo_url}")

        # 写真ダウンロード
        img_data = requests.get(photo_url).content
        filename = f"{idx:03d}_{name}.jpg"
        filepath = os.path.join(save_dir, filename)

        with open(filepath, "wb") as f:
            f.write(img_data)

        print(f"✅ 保存完了: {filename}")
    except Exception as e:
        print(f"❌ エラー: {name_raw} - {e}")
