from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


main = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='Выбрать жанр')],
        [KeyboardButton(text='Найти фильм')]
    ],
    resize_keyboard=True,
    input_field_placeholder='Выберите пункт меню'
)


films = [
    'Комедия',
    'Боевик',
    'Триллер',
    'Романтика',
    'Фэнтези',
    'Детектив'
]


async def inline_films():
    keyboard = InlineKeyboardBuilder()

    for film in films:
        keyboard.add(
            InlineKeyboardButton(
                text=film,
                callback_data=f'film_{film}'
            )
        )

    return keyboard.adjust(1).as_markup()