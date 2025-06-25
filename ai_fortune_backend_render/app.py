from flask import Flask, request, jsonify
import openai
import os

app = Flask(__name__)

openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route("/fortune", methods=["POST"])
def get_fortune():
    try:
        data = request.json
        name = data.get("name", "")
        hanja_name = data.get("hanja_name", "")
        birth_date = data.get("birth_date", "")
        birth_time = data.get("birth_time", "")

        prompt = f"{name}({hanja_name})님은 {birth_date} {birth_time}에 태어났습니다. 오늘의 운세를 자세히 알려주세요."

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "당신은 운세를 알려주는 전문가입니다."},
                {"role": "user", "content": prompt}
            ]
        )

        result = response.choices[0].message["content"].strip()
        return jsonify({"fortune": result})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/", methods=["GET"])
def home():
    return "AI Fortune Flask API is running."
