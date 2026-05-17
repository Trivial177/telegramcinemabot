from openai import OpenAI
from config import OPENAI_API_KEY

client = OpenAI(api_key=OPENAI_API_KEY)


def extract_movie_title(user_text: str) -> str:
    response = client.responses.create(
        model="gpt-4.1-mini",
        input=f"""
Ты ИИ для Telegram-бота по фильмам.

Пользователь написал:
{user_text}

Твоя задача:
выделить или исправить название фильма.

Примеры:
"интерстелар" -> "Интерстеллар"
"найди мне зеленую милю" -> "Зеленая миля"
"аватар 2009" -> "Аватар"
"titanik" -> "Titanic"

Ответь ТОЛЬКО названием фильма.
Без пояснений.
"""
    )

    return response.output_text.strip()


def make_movie_description(movie: dict) -> str:
    title = movie.get("title", "Неизвестно")
    original_title = movie.get("original_title", "Неизвестно")
    rating = movie.get("vote_average", "Нет рейтинга")
    release_date = movie.get("release_date", "Неизвестно")
    overview = movie.get("overview", "Описание отсутствует.")

    response = client.responses.create(
        model="gpt-4.1-mini",
        input=f"""
Сделай красивое описание фильма для Telegram.

Данные фильма:
Название: {title}
Оригинальное название: {original_title}
Рейтинг: {rating}
Дата выхода: {release_date}
Описание: {overview}

Ответь на русском языке.

Формат:
🎬 Название:
🌍 Оригинальное название:
⭐ Рейтинг:
📅 Дата выхода:
📝 Описание:
"""
    )

    return response.output_text