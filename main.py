import logging
import asyncio
from aiogram import Bot, Dispatcher
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram.filters import Command
from os import getenv
from dotenv import load_dotenv

load_dotenv()

API_TOKEN = getenv("BOT_TOKEN")

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

inline_markup = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text=' 1 ', callback_data='1'), InlineKeyboardButton(text=' 2 ', callback_data='2'), InlineKeyboardButton(text=' 3 ', callback_data='3')],
    [InlineKeyboardButton(text=' 4 ', callback_data='4'), InlineKeyboardButton(text=' 5 ', callback_data='5'), InlineKeyboardButton(text=' 6 ', callback_data='6')],
    [InlineKeyboardButton(text=' 7 ', callback_data='7'), InlineKeyboardButton(text=' 8 ', callback_data='8'), InlineKeyboardButton(text=' 9 ', callback_data='9')],
    [InlineKeyboardButton(text=' 0 ', callback_data='0'), InlineKeyboardButton(text=' + ', callback_data='+'), InlineKeyboardButton(text=' - ', callback_data='-')],
    [InlineKeyboardButton(text=' * ', callback_data='*'), InlineKeyboardButton(text=' / ', callback_data='/'), InlineKeyboardButton(text=' C ', callback_data='C')],
    [InlineKeyboardButton(text=' = ', callback_data='=')]
])

user_input = ""

@dp.message(Command("start"))
async def start(message: Message):
    await message.answer("Kalkulyator botiga xush kelibsiz!", reply_markup=inline_markup)

@dp.callback_query(lambda c: c.data in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '+', '-', '*', '/'])
async def calculate(callback: CallbackQuery):
    global user_input
    user_input += callback.data
    await callback.message.edit_text(user_input, reply_markup=inline_markup)

@dp.callback_query(lambda c: c.data == 'C')
async def clear(callback: CallbackQuery):
    global user_input
    user_input = ""
    await callback.message.edit_text("Tozalandi", reply_markup=inline_markup)

@dp.callback_query(lambda c: c.data == '=')
async def equals(callback: CallbackQuery):
    global user_input
    try:
        result = eval(user_input)
        await callback.message.edit_text(f"Natija: {result}", reply_markup=inline_markup)
        user_input = str(result)
    except Exception:
        await callback.message.edit_text("Xatolik!", reply_markup=inline_markup)
        user_input = ""

async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
