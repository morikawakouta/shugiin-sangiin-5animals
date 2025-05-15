import os
import re

# フォルダのパスを指定（修正版）
directory = r"C:\Users\k-mor\Dropbox\code\5animal\VScode\shugiin-sangiin-5animals\docs"

# 動物名の対応リスト
animal_dict = {
    "hitsuji": "ひつじ",
    "koara": "子守熊",
    "kojika": "こじか",
    "kurohyou": "くろひょう",
    "ookami": "狼",
    "pegasasu": "ペガサス",
    "raion": "ライオン",
    "saru": "猿",
    "tanuki": "たぬき",
    "ti-ta-": "チーター",
    "tora": "虎",
    "zou": "ゾウ"
}

# HTMLを書き換える関数
def modify_html(content):
    # H2を置換（「動物占い結果」を変更）
    content = re.sub(
        r'<h2>動物占い結果</h2>',
        '<h2>個性心理学 / 動物占い結果</h2>',
        content
    )

    # 動物の画像タグに動物名を追加
    def add_animal_name(match):
        img_tag = match.group(0)
        animal_file = re.search(r'animal_aicon/(.+?)\.png', img_tag).group(1)
        animal_name = animal_dict.get(animal_file, "")
        return f'{img_tag}\n<div class="animal-name">{animal_name}</div>'

    # 動物名がまだ追加されていない画像タグのみを処理
    content = re.sub(
        r'(<img src="image/animal_aicon/.+?\.png"\s*/?>)(?!\s*<div class="animal-name">)',
        add_animal_name,
        content
    )

    return content

# 全ファイルの一括処理を実行
for filename in os.listdir(directory):
    if filename.endswith(".html"):
        file_path = os.path.join(directory, filename)
        
        with open(file_path, "r", encoding="utf-8") as file:
            html_content = file.read()
        
        modified_content = modify_html(html_content)
        
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(modified_content)

print("✅ すべてのページに変更を反映しました。")
