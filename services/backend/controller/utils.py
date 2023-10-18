from datetime import datetime
from typing import Any, Tuple

from flask import jsonify, Response
from flask_sqlalchemy import SQLAlchemy
import requests

from .models import Question


def get_used_ids(db: SQLAlchemy) -> set[int]:
    raws_ids: Tuple[int, ] = db.session.query(
        Question.web_id
    ).distinct().all()
    used_ids: set[int] = set(raws_id[0] for raws_id in raws_ids)
    return used_ids


def check_id(id: int, used_ids: set[int]) -> bool:
    if id in used_ids:
        return False
    used_ids.add(id)
    return True


def get_pub_date(date_string: str) -> datetime:
    date_format = "%Y-%m-%dT%H:%M:%S.%fZ"
    return datetime.strptime(date_string, date_format)


def get_question(raw_question: Response) -> Question:
    question: Question = Question(
        web_id=raw_question['id'],
        question_text=raw_question['question'],
        answer=raw_question['answer'],
        publication_date=get_pub_date(raw_question['created_at'])
    )
    return question


def get_raw_data(number: int) -> list[dict[str, Any]]:
    url = f'https://jservice.io/api/random?count={number}'
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            return (
                jsonify({'error': 'Запрос завершился с ошибкой'}),
                response.status_code
            )
    except requests.exceptions.RequestException as e:
        return jsonify({'error': str(e)}), 500


def get_questions(number: int, used_ids: set[int]) -> list[Question]:
    answer: list[Question] = []
    raw_data: list[dict[str, Any]] = get_raw_data(number)
    for raw_question in raw_data:
        if check_id(raw_question['id'], used_ids):
            question: Question = get_question(raw_question)
            answer.append(question)
        else:
            another_raw_question: list[dict[str, Any]] = get_raw_data(1)
            id: int = another_raw_question[0]['id']
            while not check_id(id, used_ids):
                another_raw_question = get_raw_data(1)
            question: Question = get_question(another_raw_question[0])
            answer.append(question)

    return answer


def get_answer(question: Question) -> Response:
    return jsonify({
        'id': question.web_id,
        'question': question.question_text,
        'answer': question.answer,
        'pub_date': question.publication_date,

    })


def get_empty_question() -> Response:
    return jsonify({
        'id': '',
        'question': '',
        'answer': '',
        'pub_date': '',
    })
