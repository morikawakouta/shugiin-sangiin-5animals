import pandas as pd
import os
import re

# CSVと写真ディレクトリのパス
csv_path = "C:/Users/k-mor/Dropbox/code/5animal/VScode/shugiin-sangiin-5animals/sangiin_list.csv"
photo_dir = "C:/Users/k-mor/Dropbox/code/5animal/VScode/shugiin-sangiin-5animals/docs/image/profile_sangiin"

df = pd.read_csv(csv_path, encoding="utf-8-sig")

for idx, row in df.iterrows():
    number = f"{idx+1:03d}"

    # 名前列の最初の行（改行前だけ）を取得
    raw_name = str(row["名前"]).splitlines()[0].strip()
    safe_name = re.sub(r'\s+', '', raw_name)  # スペース削除

    new_filename = f"{number}_{safe_name}.jpg"
    new_path = os.path.join(photo_dir, new_filename)

    # 現在のファイル（連番一致）を探す
    pattern = re.compile(rf"^{number}_.+\.jpg$")
    matched_files = [f for f in os.listdir(photo_dir) if pattern.match(f)]

    if not matched_files:
        print(f"❌ 見つからない: {number} → {raw_name}")
        continue

    old_filename = matched_files[0]
    old_path = os.path.join(photo_dir, old_filename)

    if old_filename != new_filename:
        try:
            os.rename(old_path, new_path)
            print(f"✅ リネーム: {old_filename} → {new_filename}")
        except Exception as e:
            print(f"❌ リネーム失敗: {old_filename} → {new_filename} - {e}")
    else:
        print(f"✔️ 変更不要: {old_filename}")
