import requests
from bs4 import BeautifulSoup
import re

def get_5animals(birthdate):
    y, m, d = birthdate.split('/')

    # POSTデータはリスト形式のタプルで順序保証＆複数key対応
    data = [
        ('nickname', 'ゲスト'),
        ('gender', 'F'),
        ('birth_array[]', str(int(y))),
        ('birth_array[]', str(int(m)).zfill(2)),
        ('birth_array[]', str(int(d)).zfill(2)),
        ('method', 'input')
    ]

    headers = {
        'User-Agent': 'Mozilla/5.0'
    }

    res = requests.post(
        "https://www.doubutsu-uranai.com/uranai_chara_5animals.php",
        data=data,
        headers=headers
    )

    with open("debug.html", "wb") as f:
        f.write(res.content)

    soup = BeautifulSoup(res.content, "html.parser")
    result = {}
    img_tags = soup.select('#animal5 img')
    for img in img_tags:
        alt_text = img.get('alt', '')
        match = re.match(r'(本質|意思決定|表面|隠れ|希望)キャラ：(.+)', alt_text)
        if match:
            category, animal = match.groups()
            result[category] = animal

    return result

if __name__ == '__main__':
    print(get_5animals("1986/10/08"))
