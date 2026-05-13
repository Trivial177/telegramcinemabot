from aiogram import F, Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery

import app.keyboards as kb

router = Router()

@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(
"""🎬 Привет! Я Лео — твой гид в мире кино.

Не знаешь, что посмотреть вечером?
Я помогу найти фильм под любое настроение:
от захватывающих триллеров до уютных комедий 🍿

Просто выбери жанр  —
и я подберу для тебя лучшие фильмы! ✨"""
    , reply_markup=kb.main)  # Ответ на команду "start"


@router.message(F.text == 'Выбрать жанр')
async def choose_jenre(messsage: Message):
    await messsage.answer('Список жанров: ', reply_markup=await kb.inline_films())


@router.callback_query(F.data == 'comedy')
async def comedy(callback: CallbackQuery):
    await callback.answer('')
    await callback.message.answer('Hello')