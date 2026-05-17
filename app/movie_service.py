import aiohttp
from config import TMDB_API_KEY

TMDB_BASE_URL = "https://api.themoviedb.org/3"
IMAGE_BASE_URL = "https://image.tmdb.org/t/p/w500"


async def search_movie_by_title(title: str):
    url = f"{TMDB_BASE_URL}/search/movie"

    params = {
        "api_key": TMDB_API_KEY,
        "language": "ru-RU",
        "query": title,
        "include_adult": "false",
        "page": 1,
    }

    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params) as response:
            data = await response.json()

    return data.get("results", [])


def get_poster_url(movie: dict):
    poster_path = movie.get("poster_path")

    if not poster_path:
        return None

    return f"{IMAGE_BASE_URL}{poster_path}"

import random

GENRES = {
    "Комедия": 35,
    "Боевик": 28,
    "Триллер": 53,
    "Романтика": 10749,
    "Фэнтези": 14,
    "Детектив": 9648,
    "Военный": 10752,
    "Исторический": 36,
    "Биографический": 36,
}


async def get_movies_by_genre(genre_name: str):
    genre_id = GENRES.get(genre_name)

    if not genre_id:
        return []

    url = f"{TMDB_BASE_URL}/discover/movie"

    params = {
        "api_key": TMDB_API_KEY,
        "language": "ru-RU",
        "sort_by": "popularity.desc",
        "with_genres": genre_id,
        "vote_count.gte": 100,
        "include_adult": "false",
        "page": random.randint(1, 3),
    }

    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params) as response:
            data = await response.json()

    return data.get("results", [])


def format_movie_info(movie: dict):
    title = movie.get("title", "Неизвестно")
    rating = movie.get("vote_average", "Нет рейтинга")
    release_date = movie.get("release_date", "Неизвестно")
    overview = movie.get("overview", "Описание отсутствует.")

    year = release_date[:4] if release_date else "Неизвестно"

    return (
        f"🎬 Название: {title}\n"
        f"⭐ Рейтинг: {rating}\n"
        f"📅 Год: {year}\n\n"
        f"📝 Описание:\n{overview}"
    )