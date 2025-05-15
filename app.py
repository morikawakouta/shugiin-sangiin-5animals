from flask import Flask, render_template, request, redirect, url_for, session
from get_five_animals import get_5animals

app = Flask(__name__)
app.secret_key = "any-random-string-you-like"

def build_result_with_image(result):
    filename_map = {
        'ひつじ': 'hitsuji.png', 'ヒツジ': 'hitsuji.png', '羊': 'hitsuji.png',
        'ペガサス': 'pegasasu.png', 'ぺがさす': 'pegasasu.png',
        '黒ひょう': 'kurohyou.png', 'クロヒョウ': 'kurohyou.png', 'くろひょう': 'kurohyou.png',
        'チータ': 'ti-ta-.png', 'チーター': 'ti-ta-.png', 'ちーたー': 'ti-ta-.png',
        'トラ': 'tora.png', '虎': 'tora.png', 'とら': 'tora.png',
        'コアラ': 'koara.png', '子守熊': 'koara.png', 'こあら': 'koara.png',
        'ライオン': 'raion.png', 'らいおん': 'raion.png', '獅子': 'raion.png',
        'サル': 'saru.png', '猿': 'saru.png', 'さる': 'saru.png',
        'ゾウ': 'zou.png', '象': 'zou.png', 'ぞう': 'zou.png',
        'タヌキ': 'tanuki.png', '狸': 'tanuki.png', 'たぬき': 'tanuki.png',
        'コジカ': 'kojika.png', '小鹿': 'kojika.png', 'こじか': 'kojika.png',
        'オオカミ': 'ookami.png', '狼': 'ookami.png', 'おおかみ': 'ookami.png'
    }

    return {
        k: {
            'name': v,
            'img': f"/static/image/animal_aicon/{filename_map.get(v, 'default.png')}"
        }
        for k, v in result.items()
    }

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    name = ""
    selected_year = 1980
    selected_month = 1
    selected_day = 1

    if request.method == 'POST':
        name = request.form.get('name', '').strip() or 'ゲスト'
        selected_year = int(request.form['year'])
        selected_month = int(request.form['month'])
        selected_day = int(request.form['day'])

        birthdate = f"{selected_year:04}/{selected_month:02}/{selected_day:02}"
        result = get_5animals(birthdate)

        if result:
            session['result'] = build_result_with_image(result)
            session['name'] = name
            session['selected_year'] = selected_year
            session['selected_month'] = selected_month
            session['selected_day'] = selected_day

        return redirect(url_for('index'))

    # GETで表示（セッションから取得）
    result = session.get('result', None)
    name = session.get('name', "")
    selected_year = session.get('selected_year', 1980)
    selected_month = session.get('selected_month', 1)
    selected_day = session.get('selected_day', 1)

    return render_template(
        "form.html",
        name=name,
        result=result,
        year_range=range(1930, 2026),
        month_range=range(1, 13),
        day_range=range(1, 32),
        selected_year=selected_year,
        selected_month=selected_month,
        selected_day=selected_day
    )

@app.route('/reset')
def reset():
    session.clear()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
