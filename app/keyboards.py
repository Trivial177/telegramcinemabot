from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton,
                           InlineKeyboardMarkup, InlineKeyboardButton)
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

main = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text = 'Выбрать жанр')],
],                          resize_keyboard=True,
                            input_field_placeholder='Выберите пункт меню.')


settings = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text= 'smth', url='')]
])



# jenres = InlineKeyboardMarkup(inline_keyboard=[
    # [InlineKeyboardButton(text= 'Комедия', callback_data='comedy')]
# ])


films= ['Комедия', 'Боевик', 'Триллер', 'Романтика', 'Фэнтези', 'Детектив', 'Семейный', 'Документальный', 'Спорт', 'Биографический', 'Военный', 'Исторический']

async def inline_films():
    keyboard = InlineKeyboardBuilder()
    for film in films:
        keyboard.add(InlineKeyboardButton(text=film, callback_data=f'film{film}'))
    return keyboard.adjust(1).as_markup()