import os
import re

# 顔写真の保存ディレクトリ
photo_dir = "C:/Users/k-mor/Dropbox/code/5animal/VScode/shugiin-sangiin-5animals/docs/image/profile_sangiin"

# 対象ファイルの拡張子（.jpg に限定）
for filename in os.listdir(photo_dir):
    if not filename.endswith(".jpg"):
        continue

    # 例: 001_阿達　　雅志.jpg
    base, ext = os.path.splitext(filename)

    # 分割して「連番」「名前」を分ける
    if "_" not in base:
        print(f"❌ スキップ（形式不一致）: {filename}")
        continue

    number, name_part = base.split("_", 1)

    # 名前からスペース（全角・半角）を除去
    name_clean = re.sub(r"\s+", "", name_part.strip())

    # 新しいファイル名作成
    new_filename = f"{number}_{name_clean}{ext}"
    old_path = os.path.join(photo_dir, filename)
    new_path = os.path.join(photo_dir, new_filename)

    # 実行（重複防止）
    if old_path != new_path and not os.path.exists(new_path):
        os.rename(old_path, new_path)
        print(f"✅ リネーム: {filename} → {new_filename}")
    else:
        print(f"⚠️ スキップ（同名 or 既に変換済）: {filename}")
