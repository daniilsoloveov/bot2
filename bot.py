from aiogram import Bot, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import Dispatcher, FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils import executor
from config import TOKEN

bot = Bot(token=TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


class Games(StatesGroup):
    game = State()
    delivery = State()
    accept = State()
    phone = State()


@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    keyboard = InlineKeyboardMarkup(row_width=1).add(
        InlineKeyboardButton('Action - 2249 RUB', callback_data='Action'),
        InlineKeyboardButton('MMO - 1199 RUB', callback_data='MMO'),
        InlineKeyboardButton('RPG - 2279 RUB', callback_data='RPG')
    )
    await message.answer('Здравствуйте!\nВы находитесь в магазине игр\nВыберите жанр игры:', reply_markup=keyboard)
    await Games.game.set()


@dp.callback_query_handler(state=Games.game)
async def get_games(call: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        data['game'] = call.data
    keyboard = InlineKeyboardMarkup(row_width=1).add(
        InlineKeyboardButton('Доставка курьером - 169 RUB', callback_data='courier'),
        InlineKeyboardButton('Самовывоз', callback_data='pickup')
    )
    await call.message.edit_text(text='Выберите вариант доставки:', reply_markup=keyboard)
    await Games.next()


@dp.callback_query_handler(state=Games.delivery)
async def process_delivery(call: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        data['delivery'] = 'Доставка курьером - 169 RUB' if call.data == 'courier' else 'Самовывоз'
    keyboard = InlineKeyboardMarkup(row_width=1).add(
        InlineKeyboardButton('Оплатить: 2498 RUB', url='https://oplata.qiwi.com/form?invoiceUid=d66b4c7a-85e4-459a-a14e-d5bb28803981', callback_data='pay'),
        InlineKeyboardButton('Отмена', callback_data='cancel')
    )
    await call.message.edit_text(text='Теперь вы можете перейти к <u>Оплате</u> или <u>Отменить заказ</u>', parse_mode='HTML', reply_markup=keyboard)
    await Games.next()



@dp.callback_query_handler(state=Games.accept)
async def process_accept(call: types.CallbackQuery, state: FSMContext):
    if call.data == 'cancel':
        await call.message.edit_text(text='Вы отменили заказ')
        await Games.next()
    else:
        await message.answer('Успешно оплачено')
        await state.finish()



if __name__ == '__main__':
    executor.start_polling(dp)
