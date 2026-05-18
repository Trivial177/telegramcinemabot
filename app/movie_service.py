import aiohttp
from config import KINOPOISK_API_KEY

BASE_URL = "https://kinopoiskapiunofficial.tech/api/v2.2"

HEADERS = {
    "X-API-KEY": KINOPOISK_API_KEY,
    "Content-Type": "application/json"
}

GENRES = {
    "Комедия": 13,
    "Боевик": 11,
    "Триллер": 1,
    "Романтика": 4,
    "Фэнтези": 6,
    "Детектив": 5,
    "Военный": 14,
    "Исторический": 15,
    "Биографический": 22
}


async def search_movie_by_title(title: str):
    url = f"{BASE_URL}/films"
    params = {
        "keyword": title,
        "type": "FILM",
        "page": 1
    }

    async with aiohttp.ClientSession(headers=HEADERS) as session:
        async with session.get(url, params=params) as response:
            data = await response.json()

    return data.get("items", [])


async def get_movies_by_genre(genre_name: str, page: int = 1):
    genre_id = GENRES.get(genre_name)

    if not genre_id:
        return []

    url = f"{BASE_URL}/films"
    params = {
        "genres": genre_id,
        "order": "NUM_VOTE",
        "type": "FILM",
        "ratingFrom": 6,
        "page": page
    }

    async with aiohttp.ClientSession(headers=HEADERS) as session:
        async with session.get(url, params=params) as response:
            data = await response.json()

    return data.get("items", [])


async def get_movie_by_id(movie_id: int):
    url = f"{BASE_URL}/films/{movie_id}"

    async with aiohttp.ClientSession(headers=HEADERS) as session:
        async with session.get(url) as response:
            return await response.json()


def get_movie_title(movie: dict):
    return (
        movie.get("nameRu")
        or movie.get("nameOriginal")
        or movie.get("nameEn")
        or "Без названия"
    )


def get_movie_rating(movie: dict):
    return (
        movie.get("ratingKinopoisk")
        or movie.get("ratingImdb")
        or "Нет рейтинга"
    )


def get_poster_url(movie: dict):
    return movie.get("posterUrl")


def format_movie_info(movie: dict):
    title = get_movie_title(movie)
    rating = get_movie_rating(movie)
    year = movie.get("year", "Неизвестно")
    description = movie.get("description") or movie.get("shortDescription") or "Описание отсутствует."

    genres = ", ".join(
        genre.get("genre", "")
        for genre in movie.get("genres", [])
    )

    return (
        f"🎬 Название: {title}\n"
        f"⭐ Рейтинг: {rating}\n"
        f"📅 Год: {year}\n"
        f"🎭 Жанры: {genres}\n\n"
        f"📝 Описание:\n{description}"
    )