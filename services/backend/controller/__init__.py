from flask import Flask, request, jsonify, Response
from flask_sqlalchemy import SQLAlchemy
from typing import Dict, Any, List

from .utils import get_answer, get_empty_question, get_used_ids, get_questions
from .models import db, Question


app = Flask(__name__)
app.config.from_object('controller.config.Config')
db.init_app(app)


@app.route('/', methods=['POST'])
def process_questions() -> tuple[Response, int]:
    try:
        data: Dict[str, Any] = request.get_json()
        questions_num: int | None = data.get('questions_num')

        if questions_num is not None and isinstance(questions_num, int):
            used_ids: set[int] = get_used_ids(db)
            questions: List[Question] = get_questions(questions_num, used_ids)
            db.session.add_all(questions)
            db.session.commit()
            if questions_num:
                answer: Response = get_answer(questions[-1])
            else:
                answer: Response = get_empty_question()

            return answer, 200

        else:
            return jsonify({'error': 'Неверный формат запроса'}), 400

    except Exception as e:
        return jsonify({'error': str(e)}), 500
