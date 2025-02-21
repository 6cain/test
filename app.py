from flask import Flask, request, render_template

app = Flask(__name__)

# 判别逻辑的系数和阈值
coefficients = {
    '嗳气': 3.11,
    '腹胀': 9.63,
    '心烦': 10.73,
    '嗓子有痰': 1.85,
    '咽喉不利': 8.07,
    '神疲乏力': 11.47,
    '入睡困难': 9.94,
    '胆小': 5.05,
    '多愁善感': 8.17,
    '症状随情绪波动': 16.28,
    '舌红': 6.87,
    '脉弦': 8.83
}
threshold = 81.63

# 将症状名称映射到表单中的输入字段名
symptom_to_input = {
    '嗳气': 'a',
    '腹胀': 'b',
    '心烦': 'c',
    '嗓子有痰': 'd',
    '咽喉不利': 'e',
    '神疲乏力': 'f',
    '入睡困难': 'g',
    '胆小': 'h',
    '多愁善感': 'i',
    '症状随情绪波动': 'j',
    '舌红': 'k',
    '脉弦': 'l'
}

# 症状对应的分数
score_mapping = {
    '无': 0,
    '偶尔': 1,
    '经常': 2,
    '总是': 3,
    '有': 1  # 特别注意：'舌红'和'脉弦'只有'有'和'无'两种选项，'有'对应1分
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/diagnose', methods=['POST'])
def diagnose():
    total_score = 0
    for symptom, input_field in symptom_to_input.items():
        if symptom in ['舌红', '脉弦']:
            # 特殊处理'舌红'和'脉弦'，它们只有'有'和'无'两个选项
            if request.form.get(input_field) == '有':
                total_score += coefficients[symptom]
        else:
            # 其他症状根据用户选择的频率计算分数
            score = score_mapping[request.form.get(input_field)]
            total_score += score * coefficients[symptom]

    diagnosis = '气郁风动证' if total_score > threshold else '非气郁风动证'

    return render_template('result.html', diagnosis=diagnosis, total_score=total_score)

if __name__ == '__main__':
    app.run(debug=True)