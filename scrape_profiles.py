import requests
from bs4 import BeautifulSoup
import os
import csv
import time
import re

# === 対象範囲 ===
start_index = 1
end_index = 10

# === 設定 ===
base_url = "https://www.shugiin.go.jp/internet/itdb_giinprof.nsf/html/profile/"
image_base_direct = "https://www.shugiin.go.jp/internet/itdb_giinprof.nsf/html/profile/"
save_dir = r"C:\Users\k-mor\Dropbox\code\5animal\image\profilephoto"
output_csv = r"C:\Users\k-mor\Dropbox\code\5animal\VScode\shugiin-sangiin-5animals\profiles_1_10.csv"

os.makedirs(save_dir, exist_ok=True)
records = [["氏名", "ふりがな", "プロフィール文"]]

for i in range(start_index, end_index + 1):
    profile_id = str(i).zfill(3)
    profile_url = f"{base_url}{profile_id}.html"
    try:
        res = requests.get(profile_url)
        res.encoding = "shift_jis"
        soup = BeautifulSoup(res.text, "html.parser")

        # 氏名・ふりがな
        h2 = soup.find("h2", id="TopContents")
        name_full = h2.text.strip() if h2 else ""
        name_only = name_full.split("（")[0].strip()
        kana = name_full.split("（")[1].replace("）", "").strip() if "（" in name_full else ""

        # プロフィール文
        contents_div = soup.find("div", id="contents")
        profile_text = contents_div.get_text(separator="\n", strip=True) if contents_div else ""
        match = re.search(r"○.*当選.*（.*?）", profile_text)
        profile = match.group(0).strip() if match else profile_text

        records.append([name_only, kana, profile])
        print(f"🟩 プロフィール取得成功: {name_full}")

        # === 画像取得（直接リンクへ）===
        img_tag = soup.find("div", id="photo").find("img")
        if img_tag and "src" in img_tag.attrs and "$File/" in img_tag["src"]:
            image_url = image_base_direct + img_tag["src"]
            try:
                img_res = requests.get(image_url, stream=True)
                if img_res.status_code == 200:
                    img_path = os.path.join(save_dir, f"{name_only}.jpg")
                    with open(img_path, "wb") as f:
                        for chunk in img_res.iter_content(1024):
                            f.write(chunk)
                    print(f"🟩 画像保存成功: {name_only}")
                else:
                    print(f"❌ 画像DL失敗: {name_only} - {img_res.status_code}")
            except Exception as e:
                print(f"❌ 画像保存エラー: {name_only} - {e}")
        else:
            print(f"❌ 画像タグ見つからず: {name_only}")

        time.sleep(0.3)

    except Exception as e:
        print(f"❌ ページ取得失敗: {profile_url} - {e}")

# === CSV出力（UTF-8 BOMで文字化け防止）===
try:
    with open(output_csv, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f)
        writer.writerows(records)
    print(f"\n✅ CSV出力完了：{output_csv}")
except PermissionError:
    print(f"\n❌ CSV書き込み失敗: ファイルが開かれていないか確認して！\n{output_csv}")
