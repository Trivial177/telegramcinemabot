from aiogram import F, Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton

import app.keyboards as kb
from app.ai_service import extract_movie_title, make_movie_description
from app.movie_service import (
    search_movie_by_title,
    get_poster_url,
    get_movies_by_genre,
    format_movie_info,
    get_movie_title,
    get_movie_rating,
    get_movie_by_id
)

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
    movies = await get_movies_by_genre(genre, page=1)

    if not movies:
        await callback.message.answer('Фильмы по этому жанру не найдены 😔')
        return

    text = f"🎬 Фильмы в жанре «{genre}»:\n\n"
    buttons = []

    for movie in movies[:8]:
        movie_id = movie.get("kinopoiskId")
        title = get_movie_title(movie)
        rating = get_movie_rating(movie)
        year = movie.get("year", "Неизвестно")

        text += f"• {title} — ⭐ {rating}, 📅 {year}\n"

        if movie_id:
            buttons.append([
                InlineKeyboardButton(
                    text=title,
                    callback_data=f"movie_{movie_id}"
                )
            ])

    buttons.append([
        InlineKeyboardButton(
            text="➡️ Ещё фильмы",
            callback_data=f"more_{genre}_2"
        )
    ])

    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    await callback.message.answer(text, reply_markup=keyboard)


@router.callback_query(F.data.startswith('more_'))
async def more_movies(callback: CallbackQuery):
    await callback.answer('Загружаю ещё фильмы...')

    data = callback.data.replace('more_', '')
    genre, page = data.rsplit('_', 1)
    page = int(page)

    movies = await get_movies_by_genre(genre, page=page)

    if not movies:
        await callback.message.answer('Больше фильмов не нашёл 😔')
        return

    text = f"🎬 Ещё фильмы в жанре «{genre}»:\n\n"
    buttons = []

    for movie in movies[:8]:
        movie_id = movie.get("kinopoiskId")
        title = get_movie_title(movie)
        rating = get_movie_rating(movie)
        year = movie.get("year", "Неизвестно")

        text += f"• {title} — ⭐ {rating}, 📅 {year}\n"

        if movie_id:
            buttons.append([
                InlineKeyboardButton(
                    text=title,
                    callback_data=f"movie_{movie_id}"
                )
            ])

    buttons.append([
        InlineKeyboardButton(
            text="➡️ Ещё фильмы",
            callback_data=f"more_{genre}_{page + 1}"
        )
    ])

    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    await callback.message.answer(text, reply_markup=keyboard)


@router.callback_query(F.data.startswith('movie_'))
async def movie_details(callback: CallbackQuery):
    await callback.answer('Открываю фильм...')

    movie_id = int(callback.data.replace('movie_', ''))
    movie = await get_movie_by_id(movie_id)

    text = format_movie_info(movie)
    poster = get_poster_url(movie)

    if poster:
        await callback.message.answer_photo(
            photo=poster,
            caption=text
        )
    else:
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