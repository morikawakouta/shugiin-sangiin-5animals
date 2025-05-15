import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
import re
# 画像を収集


def safe_filename(name):
    name = re.sub(r'[\\/:*?"<>|]', '', name)
    name = re.sub(r'[・、。]', '', name)
    name = re.sub(r'君$', '', name)
    name = re.sub(r'\s+', ' ', name).strip()
    return name

spreadsheet_csv_url = "https://docs.google.com/spreadsheets/d/1XvMAzd4jQ-YLDVs3ZKEk2mt7sp8j3qVbXJk3lg0vtRg/export?format=csv"
save_dir = r"C:\Users\k-mor\Dropbox\code\5animal\image\profilephoto"
os.makedirs(save_dir, exist_ok=True)

df = pd.read_csv(spreadsheet_csv_url)
download_logs = []

headers = {"User-Agent": "Mozilla/5.0"}

# ✅ 11人目以降を対象にする
for i, row in df.iloc[10:].iterrows():  # 0-based index: 10 から = 11人目～
    cell = str(row[2])
    if 'http' not in cell:
        download_logs.append((cell, 'リンクなしまたは無効', ''))
        continue

    try:
        idx = int(row[0])  # A列：通し番号（ユニークなIDに使える）
        name, url = cell.split('(')
        name = name.strip()
        url = url.replace(')', '').strip()
        safe_name = f"{idx:03d}_{safe_filename(name)}"
        filename = safe_name + ".jpg"
        save_path = os.path.join(save_dir, filename)

        # ✅ 既に保存済みならスキップ
        if os.path.exists(save_path):
            download_logs.append((safe_name, 'スキップ（既存）', ''))
            continue

        res = requests.get(url, timeout=10, headers=headers)
        res.encoding = 'shift_jis'
        soup = BeautifulSoup(res.text, 'html.parser')

        img_tag = soup.select_one('div#photo img')
        if not img_tag or 'src' not in img_tag.attrs:
            download_logs.append((safe_name, '画像タグなし', url))
            continue

        src = img_tag['src']
        img_filename = os.path.basename(src)
        img_url = f"https://www.shugiin.go.jp/internet/itdb_giinprof.nsf/html/profile/{img_filename}/$File/{img_filename}"

        img_res = requests.get(img_url, headers=headers)
        if img_res.status_code == 200 and img_res.content:
            with open(save_path, 'wb') as f:
                f.write(img_res.content)
            download_logs.append((safe_name, '成功', img_url))
        else:
            download_logs.append((safe_name, f'取得失敗（status: {img_res.status_code}）', img_url))

    except Exception as e:
        download_logs.append((cell, f'エラー: {e}', ''))

log_path = os.path.join(save_dir, "download_log_rest.csv")
log_df = pd.DataFrame(download_logs, columns=["氏名", "結果", "画像URLまたはページ"])
log_df.to_csv(log_path, index=False, encoding="utf-8-sig")

print(f"✅ ダウンロード完了！（11人目以降）ログ: {log_path}")
