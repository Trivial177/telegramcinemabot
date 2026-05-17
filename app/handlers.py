from aiogram import F, Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery

import app.keyboards as kb
from app.ai_service import extract_movie_title, make_movie_description
from app.movie_service import search_movie_by_title, get_poster_url, get_movies_by_genre, format_movie_info

router = Router()

waiting_for_title = set()


@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(
"""🎬 Привет! Я Лео — твой гид в мире кино.

Не знаешь, что посмотреть вечером?
Я помогу найти фильм под любое настроение:
от захватывающих триллеров до уютных комедий 🍿

Просто выбери жанр  —
и я подберу для тебя лучшие фильмы! ✨

А ещё можешь нажать «Найти фильм» —
и я найду фильм по названию с помощью ИИ 🤖"""
    , reply_markup=kb.main)


@router.message(F.text == 'Выбрать жанр')
async def choose_jenre(messsage: Message):
    await messsage.answer('Список жанров: ', reply_markup=await kb.inline_films())


@router.callback_query(F.data.startswith('film_'))
async def genre_callback(callback: CallbackQuery):
    await callback.answer('Ищу фильмы по жанру...')

    genre = callback.data.replace('film_', '')

    movies = await get_movies_by_genre(genre)

    if not movies:
        await callback.message.answer('Фильмы по этому жанру не найдены 😔')
        return

    text = f"🎬 Фильмы в жанре «{genre}»:\n\n"

    for index, movie in enumerate(movies[:5], start=1):
        title = movie.get("title", "Без названия")
        rating = movie.get("vote_average", "Нет рейтинга")
        year = movie.get("release_date", "Неизвестно")[:4]

        text += f"{index}. {title} — ⭐ {rating}, 📅 {year}\n"

    text += "\nНапиши название фильма через кнопку «Найти фильм», чтобы получить описание и постер."

    await callback.message.answer(text)

@router.message(F.text == 'Найти фильм')
async def ask_movie_title(message: Message):
    waiting_for_title.add(message.from_user.id)

    await message.answer(
        'Напиши название фильма 🎬\n\n'
        'Можно даже с ошибкой, например:\n'
        'интерстелар\n'
        'зеленая миля\n'
        'titanik'
    )


@router.message()
async def find_movie(message: Message):
    user_id = message.from_user.id

    if user_id not in waiting_for_title:
        return

    waiting_for_title.remove(user_id)

    await message.answer('ИИ анализирует название фильма...')

    ai_title = extract_movie_title(message.text)

    await message.answer(f'Ищу фильм: {ai_title}')

    movies = await search_movie_by_title(ai_title)

    if not movies:
        await message.answer('Фильм не найден 😔 Попробуй написать название по-другому.')
        return

    movie = movies[0]

    text = make_movie_description(movie)
    poster = get_poster_url(movie)

    if poster:
        await message.answer_photo(
            photo=poster,
            caption=text
        )
    else:
        await message.answer(text)