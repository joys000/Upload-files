from flask import Flask, render_template, request
import openai
import os

app = Flask(__name__)

# OpenAI API 키는 환경변수에서 불러옵니다 (Render Dashboard에서 설정)
openai.api_key = os.environ.get("OPENAI_API_KEY")

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        name = request.form.get("name")
        hanja_name = request.form.get("hanja_name")
        birth_date = request.form.get("birth_date")
        birth_time = request.form.get("birth_time")

        prompt = f"""
이름: {name} ({hanja_name})
생년월일: {birth_date}
태어난 시간: {birth_time}

위 정보를 바탕으로 사주 운세를 분석해줘.
간단한 오늘의 운세, 성격, 직업적 성향도 함께 알려줘.
"""

        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "당신은 전문가 사주 운세 분석가입니다."},
                    {"role": "user", "content": prompt}
                ]
            )
            result = response.choices[0].message.content.strip()
        except Exception as e:
            result = f"운세 분석 중 오류 발생: {str(e)}"

        return render_template("result.html", fortune=result)

    return render_template("index.html")

# ⬇️ 이 부분이 Render에서 포트를 열 수 있게 하는 핵심입니다
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
