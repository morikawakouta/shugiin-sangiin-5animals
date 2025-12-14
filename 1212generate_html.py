# -*- coding: utf-8 -*-
import os
import re
import html
from pathlib import Path

import pandas as pd

# =========================
# 設定
# =========================
CSV_PATH = r"C:\Users\k-mor\Dropbox\code\5animal\VScode\shugiin-sangiin-5animals\docs\1214sangiinlist_with_5animals.csv"
OUTPUT_DIR = r"C:\Users\k-mor\Dropbox\code\5animal\VScode\shugiin-sangiin-5animals\docs"

PHOTO_DIR_REL = "image/profile_sangiin"      # HTMLから見た相対パス
ANIMAL_DIR_REL = "image/animal_aicon"       # HTMLから見た相対パス

# 連番（写真ファイルがCSVに無い場合だけ使う）
START_NO = 241  # 必要なら 240 に変えろ

# 生成するHTMLファイル名
# 例: member_241.html
HTML_NAME_FORMAT = "member_{no:03d}.html"

# CSV列名（あなたのCSVに合わせる）
COL_NAME = "氏名"
COL_FURIGANA = "ふりがな"  # 無ければ空でOK
COL_BIRTH = "生年月日"

# 公式から取った列（あなたが前段で作った想定）
COL_KAIHA = "所属会派"
COL_ELECT = "選挙区・比例区／当選年／当選回数"
COL_ROLES = "参議院における役職等一覧"
COL_PROFILE_TEXT = "プロフィール文"

# 動物占い列
COL_SURFACE = "表面キャラ"
COL_ESSENCE = "本質キャラ"
COL_DECIDE = "意思決定キャラ"
COL_HIDDEN = "隠れキャラ"
COL_HOPE = "希望キャラ"

# 写真ファイル列（あれば最優先）
COL_PHOTO_FILE = "顔写真ファイル"  # 例: 241_青木愛.jpg

# =========================
# 動物名 → アイコンファイル対応（表記ゆれ吸収）
# =========================
animal_map = {
    # ひらがな
    "たぬき": "tanuki.png",
    "くろひょう": "kurohyou.png",
    "こじか": "kojika.png",
    "ひつじ": "hitsuji.png",
    "おおかみ": "ookami.png",
    "さる": "saru.png",
    "らいおん": "raion.png",
    "ぞう": "zou.png",
    "こあら": "koara.png",
    "とら": "tora.png",

    # カタカナ
    "タヌキ": "tanuki.png",
    "クロヒョウ": "kurohyou.png",
    "コジカ": "kojika.png",
    "ヒツジ": "hitsuji.png",
    "オオカミ": "ookami.png",
    "サル": "saru.png",
    "ライオン": "raion.png",
    "ゾウ": "zou.png",
    "コアラ": "koara.png",
    "トラ": "tora.png",
    "チーター": "ti-ta-.png",
    "ペガサス": "pegasasu.png",

    # 漢字混在
    "虎": "tora.png",
    "猿": "saru.png",
    "狼": "ookami.png",
    "ゾウ": "zou.png",
    "子守熊": "koara.png",
}

# =========================
# ユーティリティ
# =========================
def read_csv_smart(path: str) -> pd.DataFrame:
    for enc in ("utf-8-sig", "utf-8", "cp932", "shift_jis"):
        try:
            return pd.read_csv(path, encoding=enc)
        except UnicodeDecodeError:
            continue
    return pd.read_csv(path, encoding="cp932", errors="replace")


def safe_filename(name: str) -> str:
    # Windows禁止文字: \ / : * ? " < > |
    name = re.sub(r'[\\/:*?"<>|]', "_", str(name))
    name = name.replace("　", " ").strip()
    return name


def nl2br(s: str) -> str:
    """改行を <br> に。Noneやnanも吸収。"""
    if s is None:
        return ""
    s = str(s)
    if s.lower() == "nan":
        return ""
    s = html.escape(s)
    s = s.replace("\r\n", "\n").replace("\r", "\n")
    # 空行が多い場合を軽く圧縮
    s = re.sub(r"\n{3,}", "\n\n", s)
    return s.replace("\n", "<br>\n")


def get_str(row, col: str) -> str:
    if col in row and pd.notna(row[col]):
        return str(row[col]).strip()
    return ""


def extract_leading_no(filename: str) -> int | None:
    """ '241_青木愛.jpg' -> 241 """
    m = re.match(r"^(\d+)[_-]", str(filename).strip())
    if m:
        return int(m.group(1))
    return None


def animal_icon(animal_name: str) -> str:
    a = (animal_name or "").strip()
    return animal_map.get(a, "")


# =========================
# HTMLテンプレ生成
# =========================
def build_html(
    name: str,
    furigana: str,
    photo_src: str,
    birth: str,
    kaiha: str,
    elect: str,
    roles: str,
    profile_text: str,
    animal_surface: str,
    animal_hope: str,
    animal_core: str,
    animal_decide: str,
    animal_hidden: str,
):
    # 表示用：ふりがなが無いなら括弧ごと消す
    if furigana:
        name_line = f"{html.escape(name)}君（「{html.escape(furigana)}」）"
    else:
        name_line = f"{html.escape(name)}君"

    # 情報ブロック（改行保持）
    elect_html = nl2br(elect)
    roles_html = nl2br(roles)
    profile_html = nl2br(profile_text)

    # 動物（ファイル名 + 表示名）
    def animal_block(label: str, icon_file: str, animal_label: str) -> str:
        if not icon_file:
            # 未取得でも崩れないようにする（空のまま表示）
            return f"""<div><div>{html.escape(label)}</div><div class="animal-name">{html.escape(animal_label)}</div></div>"""
        return f"""<div>
  <div>{html.escape(label)}</div>
  <img src="{html.escape(ANIMAL_DIR_REL)}/{html.escape(icon_file)}" alt="{html.escape(animal_label)}">
  <div class="animal-name">{html.escape(animal_label)}</div>
</div>"""

    # それぞれ
    surface_icon = animal_icon(animal_surface)
    hope_icon = animal_icon(animal_hope)
    core_icon = animal_icon(animal_core)
    decide_icon = animal_icon(animal_decide)
    hidden_icon = animal_icon(animal_hidden)

    # 文章内は <br> があるので <p> は1つにまとめる
    info_html = (
        f"生年月日：{html.escape(birth)}<br>"
        f"会派：{html.escape(kaiha)}<br>"
        f"選挙区・比例区／当選年／当選回数：<br>{elect_html}<br>"
        f"役職：<br>{roles_html}"
    )

    html_text = f"""<!DOCTYPE html>
<html lang="ja">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{html.escape(name)}君｜議員プロフィール</title>
  <style>
    body {{ font-family: sans-serif; background:#f9f9f9; color:#333; margin:0; padding:0; }}
    .container {{ max-width:800px; margin:2em auto; padding:1em; background:#fff;
                  border-radius:8px; box-shadow:0 0 10px rgba(0,0,0,0.05); }}
    h1 {{ background:#005b9a; color:#fff; padding:1em; margin:0 0 1em; text-align:center; }}
    h2 {{ color:#005b9a; margin-top:1em; }}
    .profile-photo {{ width:160px; border-radius:8px; margin:1em auto; display:block; }}
    .animal-grid {{ display:grid; grid-template-columns:1fr 1fr 1fr; gap:1em; text-align:center; margin-top:1em; }}
    .animal-grid img {{ width:80px; height:80px; }}
    .animal-name {{ margin-top:0.4em; font-size:0.95em; }}
  </style>
</head>
<body>
  <div class="container">
    <h1>議員プロフィール</h1>
    <img src="{html.escape(photo_src)}" class="profile-photo" alt="{html.escape(name)}君">
    <h2>{name_line}</h2>

    <p>{info_html}</p>

    <h2>プロフィール</h2>
    <p>{profile_html}</p>

    <h2>個性心理学 / 動物占い結果</h2>
    <div class="animal-grid">
      <div></div>
      {animal_block("表面", surface_icon, animal_surface)}
      <div></div>

      {animal_block("希望", hope_icon, animal_hope)}
      {animal_block("本質", core_icon, animal_core)}
      {animal_block("意思決定", decide_icon, animal_decide)}

      <div></div>
      {animal_block("隠れ", hidden_icon, animal_hidden)}
      <div></div>
    </div>
  </div>
</body>
</html>
"""
    return html_text


# =========================
# メイン
# =========================
def main():
    df = read_csv_smart(CSV_PATH)

    if COL_NAME not in df.columns:
        raise RuntimeError(f"CSVに '{COL_NAME}' 列が無い。columns={df.columns.tolist()}")

    # 氏名が空の行は除外
    df[COL_NAME] = df[COL_NAME].astype(str)
    df = df[df[COL_NAME].str.strip().ne("")].copy()

    # 72人を強制したいなら有効化（事故防止）
    df = df.head(72).copy()

    out_dir = Path(OUTPUT_DIR)
    out_dir.mkdir(parents=True, exist_ok=True)

    created = 0

    for idx, (_, row) in enumerate(df.iterrows()):
        name = get_str(row, COL_NAME)
        furigana = get_str(row, COL_FURIGANA)
        birth = get_str(row, COL_BIRTH)

        kaiha = get_str(row, COL_KAIHA)
        elect = get_str(row, COL_ELECT)
        roles = get_str(row, COL_ROLES)
        profile_text = get_str(row, COL_PROFILE_TEXT)

        # 動物
        animal_surface = get_str(row, COL_SURFACE)
        animal_hope = get_str(row, COL_HOPE)
        animal_core = get_str(row, COL_ESSENCE)
        animal_decide = get_str(row, COL_DECIDE)
        animal_hidden = get_str(row, COL_HIDDEN)

        # 写真ファイル名の決定
        photo_file = get_str(row, COL_PHOTO_FILE)
        if photo_file:
            no = extract_leading_no(photo_file)
            if no is None:
                # 先頭数字が無いなら fallback
                no = START_NO + idx
        else:
            # CSVに無いなら生成
            no = START_NO + idx
            photo_file = f"{no}_{safe_filename(name).replace(' ', '')}.jpg"

        photo_src = f"{PHOTO_DIR_REL}/{photo_file}"

        # HTMLファイル名（写真番号と一致させる）
        html_filename = HTML_NAME_FORMAT.format(no=no)
        html_path = out_dir / html_filename

        html_text = build_html(
            name=name,
            furigana=furigana,
            photo_src=photo_src,
            birth=birth,
            kaiha=kaiha,
            elect=elect,
            roles=roles,
            profile_text=profile_text,
            animal_surface=animal_surface,
            animal_hope=animal_hope,
            animal_core=animal_core,
            animal_decide=animal_decide,
            animal_hidden=animal_hidden,
        )

        with open(html_path, "w", encoding="utf-8") as f:
            f.write(html_text)

        created += 1
        print(f"OK: {html_filename}")

    print("-----")
    print(f"DONE: {created} files")
    print(f"OUT : {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
