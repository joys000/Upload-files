from flask import Flask, render_template, request
import openai
import os

app = Flask(__name__)

# 🔐 환경변수에서 API 키 불러오기
openai.api_key = os.environ.get("OPENAI_API_KEY")

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        name = request.form.get("name")
        hanja_name = request.form.get("hanja_name")
        birth_date = request.form.get("birth_date")
        birth_time = request.form.get("birth_time")

        prompt = f"""
        이름: {name}
        한자 이름: {hanja_name}
        생년월일: {birth_date}
        태어난 시간: {birth_time}

        위 정보를 바탕으로 오늘의 운세를 사주 분석처럼 알려줘.
        """

        try:
            client = openai.OpenAI()  # 1.x 방식 클라이언트 인스턴스
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "당신은 전문적인 운세 분석가입니다."},
                    {"role": "user", "content": prompt}
                ]
            )
            result = response.choices[0].message.content.strip()
        except Exception as e:
            result = f"운세 분석 중 오류 발생: {e}"

        return render_template("result.html", fortune=result)

    return render_template("index.html")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
