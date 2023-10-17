from flask import Flask, request, jsonify, Response
from flask_sqlalchemy import SQLAlchemy
from typing import Dict, Any

app = Flask(__name__)
app.config.from_object("controller.config.Config")
db = SQLAlchemy(app)


class Question(db.Model):
    __tablename__ = "questions"
    id = db.Column(db.Integer, primary_key=True)
    web_id = db.Column(db.Integer)
    question_text = db.Column(db.String(1023))
    answer = db.Column(db.String(255))
    publication_date = db.Column(db.Date)


@app.route('/', methods=['POST'])
def process_questions() -> tuple[Response, int]:
    try:
        data: Dict[str, Any] = request.get_json()
        questions_num: int | None = data.get("questions_num")

        if questions_num is not None and isinstance(questions_num, int):
            result: Dict[str, str] = {"message": f"{questions_num}"}
            return jsonify(result), 200

        else:
            return jsonify({"error": "Неверный формат запроса"}), 400

    except Exception as e:
        return jsonify({"error": str(e)}), 500
