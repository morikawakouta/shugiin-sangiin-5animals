import requests
from bs4 import BeautifulSoup
import csv
import os
from urllib.parse import urljoin

# URLと出力ファイルパス
list_url = "https://www.sangiin.go.jp/japanese/joho1/kousei/giin/217/giin.htm"
output_dir = "C:/Users/k-mor/Dropbox/code/5animal/VScode/shugiin-sangiin-5animals"
os.makedirs(output_dir, exist_ok=True)
output_csv_path = os.path.join(output_dir, "sangiin_profile_sample.csv")

print("▶ リストページ取得中...")
res = requests.get(list_url)
res.encoding = res.apparent_encoding
soup = BeautifulSoup(res.text, "html.parser")

# 全議員のリンクを取得
link_tags = soup.select("table a[href*='profile']")
print(f"▶ 議員数: {len(link_tags)} 人")

# CSV書き込み準備
with open(output_csv_path, "w", newline="", encoding="utf-8-sig") as f:
    writer = csv.writer(f)
    writer.writerow(["名前", "会派", "選挙区", "役職", "プロフィール文"])

    # 各議員をループ
    for link_tag in link_tags:
        try:
            name = link_tag.text.strip()
            profile_url = urljoin(list_url, link_tag["href"])
            print(f"▶ {name} のページ取得中...")

            res2 = requests.get(profile_url)
            res2.encoding = res2.apparent_encoding
            profile_soup = BeautifulSoup(res2.text, "html.parser")

            # 初期化
            faction = ""
            election_info = ""
            positions = ""

            for dl in profile_soup.select("dl.profile-detail"):
                dt = dl.find("dt")
                dd = dl.find("dd")
                if not dt or not dd:
                    continue
                label = dt.get_text(strip=True)
                value = dd.get_text(separator="\n", strip=True)
                if "所属会派" in label:
                    faction = value
                elif "選挙区" in label:
                    election_info = f"{label}：\n{value}"
                elif "役職等一覧" in label:
                    positions = value

            # プロフィール文抽出
            profile_paragraphs = []
            p1 = profile_soup.find("p", class_="profile2")
            p2 = profile_soup.find("p", class_="ta_l mt10")
            if p1:
                profile_paragraphs.append(p1.get_text(strip=True))
            if p2:
                profile_paragraphs.append(p2.get_text(strip=True))
            profile_text = "\n".join(profile_paragraphs)

            # CSV出力
            writer.writerow([name, faction, election_info, positions, profile_text])
        except Exception as e:
            print(f"❌ エラー: {name} - {e}")

print(f"✅ 完了！出力先: {output_csv_path}")
