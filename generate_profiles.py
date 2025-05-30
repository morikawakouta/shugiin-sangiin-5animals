import pandas as pd
import os
import re
# 完成シートから個人ページHTMLを生成


def safe_filename(name):
    # Windows 禁則文字・記号・末尾「君」を除去
    name = re.sub(r'[\\/:*?"<>|]', '', name)
    name = re.sub(r'[・、。]', '', name)
    name = re.sub(r'君$', '', name)
    name = re.sub(r'\s+', ' ', name).strip()
    return name

# ▼ 動物名 → アイコンファイル名 対応表
animal_filename_map = {
    "たぬき": "tanuki.png",
    "くろひょう": "kurohyou.png",
    "こじか": "kojika.png",
    "ひつじ": "hitsuji.png",
    "虎": "tora.png",
    "子守熊": "koara.png",
    "狼": "ookami.png",
    "猿": "saru.png",      # 後で差し替え
    "ペガサス": "pegasasu.png",
    "ライオン": "raion.png",
    "ゾウ": "zou.png",
    "チーター": "ti-ta-.png"
}

# CSV と出力先ディレクトリ
csv_path    = r"C:\Users\k-mor\Dropbox\code\5animal\VScode\shugiin-sangiin-5animals\shuugiinlist.csv"
output_dir  = r"C:\Users\k-mor\Dropbox\code\5animal\VScode\shugiin-sangiin-5animals\docs"
os.makedirs(output_dir, exist_ok=True)

# CSV 読み込み
df = pd.read_csv(csv_path, encoding="utf-8-sig")

for _, row in df.iterrows():
    member_id = int(row['No'])
    name      = row['氏名']
    furigana  = row['ふりがな']
    birthday  = row['生年月日']
    party     = row['会派']
    district  = row['選挙区']
    terms     = row['当選回数']
    profile   = row['プロフィール']

    # プロフィール画像パス（docs から見て image/...）
    profile_filename = f"{member_id:03d}_{safe_filename(name)}.jpg"
    profile_img_path = f"image/profilephoto/{profile_filename}"

    # 動物アイコンパス（同じく image/...）
    animal_icons = {
        "表面":     f"image/animal_aicon/{animal_filename_map.get(row['表面'], 'notfound.png')}",
        "希望":     f"image/animal_aicon/{animal_filename_map.get(row['希望'], 'notfound.png')}",
        "本質":     f"image/animal_aicon/{animal_filename_map.get(row['本質'], 'notfound.png')}",
        "意思決定": f"image/animal_aicon/{animal_filename_map.get(row['意思決定'], 'notfound.png')}",
        "隠れ":     f"image/animal_aicon/{animal_filename_map.get(row['隠れ'], 'notfound.png')}"
    }

    # HTML テンプレート（クロス型レイアウト＋h1 見出し）
    html = f"""<!DOCTYPE html>
<html lang="ja">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{name}｜議員プロフィール</title>
  <style>
    body {{ font-family: sans-serif; background:#f9f9f9; color:#333; margin:0; padding:0; }}
    .container {{ max-width:800px; margin:2em auto; padding:1em; background:#fff;
                  border-radius:8px; box-shadow:0 0 10px rgba(0,0,0,0.05); }}
    h1 {{ background:#005b9a; color:#fff; padding:1em; margin:0 0 1em; text-align:center; }}
    h2 {{ color:#005b9a; margin-top:1em; }}
    .profile-photo {{ width:160px; border-radius:8px; margin:1em auto; display:block; }}
    .animal-grid {{ display:grid; grid-template-columns:1fr 1fr 1fr; gap:1em; text-align:center; margin-top:1em; }}
    .animal-grid img {{ width:80px; height:80px; }}
  </style>
</head>
<body>
  <div class="container">
    <h1>議員プロフィール</h1>
    <img src="{profile_img_path}" class="profile-photo" alt="{name}">
    <h2>{name}（{furigana}）</h2>
    <p>生年月日：{birthday}<br>会派：{party}<br>選挙区：{district}<br>当選回数：{terms}</p>

    <h2>プロフィール</h2>
    <p>{profile}</p>

    <h2>動物占い結果</h2>
    <div class="animal-grid">
      <div></div>
      <div><div>表面</div><img src="{animal_icons['表面']}" /></div>
      <div></div>

      <div><div>希望</div><img src="{animal_icons['希望']}" /></div>
      <div><div>本質</div><img src="{animal_icons['本質']}" /></div>
      <div><div>意思決定</div><img src="{animal_icons['意思決定']}" /></div>

      <div></div>
      <div><div>隠れ</div><img src="{animal_icons['隠れ']}" /></div>
      <div></div>
    </div>
  </div>
</body>
</html>
"""

    # ファイルを書き出し
    filename = f"member_{member_id:03d}.html"
    filepath = os.path.join(output_dir, filename)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(html)

print(f"✅ 全議員ページを `{output_dir}` に生成しました。")
