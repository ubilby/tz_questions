# tz_questions
Настройки .env добавил в репозиторий

Для запуска из корневой дирректории введите
docker-compose up --build

Отправьте post-запрос по адресу http://127.0.0.1:5000/ вида
{
    "questions_num": 1
}
Вместо единицы может быть любое число до 100 (можно ввести и больше, но я так понял, service.io/api/random?count=1 принимает все, что больше ста, за сто)

В задании столкнулся с формулировкой 
"В случае, если в БД имеется такой же вопрос, к публичному API с викторинами должны выполняться дополнительные запросы до тех пор, пока не будет получен уникальный вопрос для викторины.
Ответом на запрос из п.2.a должен быть предыдущей сохранённый вопрос для викторины. В случае его отсутствия - пустой объект."
я так понял, что единственный случай, когда объекта не будет - это если передать count=0
