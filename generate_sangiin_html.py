import pandas as pd
import os
import re

# --- 設定 ---

csv_path = "C:/Users/k-mor/Dropbox/code/5animal/VScode/shugiin-sangiin-5animals/sangiin_list.csv"
output_dir = "C:/Users/k-mor/Dropbox/code/5animal/VScode/shugiin-sangiin-5animals/docs"
photo_dir = "image/profile_sangiin"
animal_dir = "image/animal_aicon"

animal_map = {
    "たぬき": "tanuki.png",
    "くろひょう": "kurohyou.png",
    "こじか": "kojika.png",
    "ひつじ": "hitsuji.png",
    "虎": "tora.png",
    "子守熊": "koara.png",
    "狼": "ookami.png",
    "猿": "saru.png",
    "ペガサス": "pegasasu.png",
    "ライオン": "raion.png",
    "ゾウ": "zou.png",
    "チーター": "ti-ta-.png"
}

df = pd.read_csv(csv_path, encoding="utf-8-sig")

for idx, row in df.iterrows():
    try:
        name = row["名前"]
        furigana = row["ふりがな"]
        birth = row["生年月日"]
        party = row["会派"]
        area = row["選挙区"]
        role = row["役職"]
        term = row["任期満了"]
        profile = row["プロフィール文"]

        animal_surface = animal_map.get(row["表面"], "")
        animal_hope = animal_map.get(row["希望"], "")
        animal_core = animal_map.get(row["本質"], "")
        animal_decision = animal_map.get(row["意思決定"], "")
        animal_hidden = animal_map.get(row["隠れ"], "")

        first_line_name = str(name).splitlines()[0].strip()
        safe_name = re.sub(r'\s+', '', first_line_name)
        photo_filename = f"{idx+1:03d}_{safe_name}.jpg"

        html_filename = f"sangiin_{idx+1:03d}.html"
        html_path = os.path.join(output_dir, html_filename)

        html = f"""<!DOCTYPE html>
<html lang="ja">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{name}君｜議員プロフィール</title> 
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
    <img src="{photo_dir}/{photo_filename}" class="profile-photo" alt="{name}君">
    <h2>{name}君（「{furigana}」）</h2> 
    <p>生年月日：{birth}<br>会派：{party}<br>{area}<br>役職：{role}<br>任期：{term}</p> 

    <h2>プロフィール</h2>
    <p>{profile}</p> 

    <h2>動物占い結果</h2>
    <div class="animal-grid">
      <div></div>
      <div><div>表面</div><img src="{animal_dir}/{animal_surface}" /></div> 
      <div></div>

      <div><div>希望</div><img src="{animal_dir}/{animal_hope}" /></div>
      <div><div>本質</div><img src="{animal_dir}/{animal_core}" /></div>
      <div><div>意思決定</div><img src="{animal_dir}/{animal_decision}" /></div>

      <div></div>
      <div><div>隠れ</div><img src="{animal_dir}/{animal_hidden}" /></div>
      <div></div>
    </div>
  </div>
</body>
</html>"""

        with open(html_path, "w", encoding="utf-8") as f:
            f.write(html)

        print(f"✅ {html_filename} を生成しました")

    except Exception as e:
        print(f"❌ エラー at row {idx+1}: {e}")
