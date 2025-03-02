import asyncio
import logging
import sys
from aiogram.fsm.context import FSMContext
from config import TOKEN
from aiogram.types import FSInputFile
from aiogram import Bot, Dispatcher, F, html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from aiogram.fsm.state import State, StatesGroup
from aiogram.handlers import CallbackQueryHandler
from keyboard import Keyboards
from data import db


dp = Dispatcher()
bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))


class MyState(StatesGroup):
    default = State()
    rating = State()
    description = State()
    add_photo = State()
    delete_photo = State()
    update_info = State()



async def response_answer_to_creator(photo, serial_id, text, user_id, username):
    creator = db.Database.get_creator_id(serial_id)
    if creator ==  user_id:
        await bot.send_photo(photo=photo, chat_id=1856040379, caption=f'{text}\n{username}')
    else:
        await bot.send_photo(photo=photo, chat_id=creator, caption=f'{text}\n{username}')

@dp.message(Command('стоп'))
async def start_handler(message: Message, state: FSMContext) -> None:
    await state.set_state(MyState.default)
    await message.answer('вы вышли из цикла бесконечного счастья(')



@dp.message(Command('отложенное'))
async def skip_queue(message: Message, state: FSMContext):
    await state.set_data({'from_aside': True})
    # await message.answer(text = 'вы вошли в отложенную очередь, чтобы выйти: /вернуться')
    info = db.Database.get_aside_photo(message.from_user.id)
    print(info.id)
    await state.update_data({'id': info.number, 'photo': info.photo})
    await message.answer_photo(photo=info.photo, caption=f'что вы думаете об этой тянке теперь?({info.number})',reply_markup=Keyboards.skip_photo())
    await state.set_state(MyState.rating)

@dp.message(MyState.rating)
async def rating_handler(message: Message, state: FSMContext) -> None:
    massive = message.text.split('\n', 1)
    id = await state.get_value('id')
    if len(massive) > 1:
        rating, description = massive

        if rating.isnumeric():
            if int(rating) in range(1, 11):
                db.Database.save_result(
                    id=id,photo = await state.get_value('photo'), rating=rating, description=description, user_id=message.from_user.id, from_aside=await state.get_value('from_aside'))
                await response_answer_to_creator(photo=await state.get_value('photo'), serial_id=id, text=message.text, user_id=message.from_user.id, username=message.from_user.username)
                await state.set_data({'from_aside': await state.get_value('from_aside')})
                if await state.get_value('from_aside') == False:
                    await answer_photo(message, state)
                else:
                    await skip_queue(message,state)
            else:
                await message.answer('рейтинг должен быть от 1 до 10')

    else:
        if message.text.isnumeric() and int(message.text) in range(1, 11):
            await state.update_data({'rating': int(message.text)})
            await state.set_state(MyState.description)
            await message.answer('теперь напишите любой коментарий, иначе отправьте skip')
        else:
            await message.answer('поставьте ей циферку пожалуйста от 1 до 10')


@dp.message(MyState.description)
async def description_handler(message: Message, state: FSMContext):
    id = await state.get_value('id')
    photo = await state.get_value('photo')
    rating = await state.get_value('rating')

    await response_answer_to_creator(photo=photo, serial_id=id, text=f'{rating}\n{message.text}', user_id=message.from_user.id, username=message.from_user.username)
    db.Database.save_result(id=id, rating=rating,photo = await state.get_value('photo'), description=message.text, user_id=message.from_user.id)
    await state.set_data({'from_aside':await state.get_value('from_aside')})
    await message.answer('ответ сохранён в вашу личную историю')
    await answer_photo(message, state)


@dp.message(F.photo)
async def add_photo_handler(message: Message, state: FSMContext) -> None:
    for i in message.photo[-1]:  # i[1] уникальный ключ из тг
        db.Database.add_photo(photo=i[1], creator=message.from_user.id)
        await message.answer('Аригато за тян!')
        break


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer(f"Hello, {html.bold(message.from_user.full_name)}!", reply_markup=Keyboards.main_menu())
    await message.answer('запуск ленты по команде /оценка')

    print(message.from_user.id)
    # await bot.send_photo(chat_id=message.chat.id, photo=photo)
    db.Database.create_history(message.from_user.id)


@dp.message(Command('оценка', 'Оценка'))
async def answer_photo(message: Message, state: FSMContext, id=None) -> None:
    await state.set_state(MyState.rating)
    await state.set_data({'from_aside':False})

    if id is None:
        n = db.Database.get_next_photo(user_id=message.from_user.id)
    else:
        n = db.Database.get_next_photo(user_id=id)

    if n == None:
        await message.answer(f'вы всё оценили!!! Извините, больше нет тянок, вы увидели всю красоту мира')
        return
    if n[1] == None:
        photo = FSInputFile(f'data/photos/{n[0]}.jpg')
    else:
        photo = n[1]  # unique telegram id

    await state.update_data({'id': n[0], 'photo': photo})
    await bot.send_photo(chat_id=message.chat.id,
                        photo=photo,
                        caption=f'господин, посвятите оценочку по десятибальной для такой няшки (id = {n[0]})\n(можно сразу c комментарием, но через enter только)',
                        reply_markup=Keyboards.inline_skip())


@dp.message(Command('добавить'))
async def install_state_add_photo(message: Message):
    await message.answer('пожалуйста, господин, отправьте фотографию няшечки')



@dp.message()
async def echo_handler(message: Message) -> None:
    try:
        await message.send_copy(chat_id=message.chat.id)
    except TypeError:
        await message.answer("Nice try!")


async def main() -> None:

    await dp.start_polling(bot)


@dp.callback_query()
class MyHundler(CallbackQueryHandler):
    async def handle(self):# я без понятия кто делал это, но я даже документацию не вижу
        data = self.callback_data
        match data:
            case 'skip':
                # print(self.data.keys())
                # print(self.data['handler'])
                for info in self.message.photo[-1]:

                    ID = self.message.caption.split('\n')[0].split('id = ')[1][:-1]
                    print(ID)
                    print(f"{db.Database.set_aside_photo(photo_id= info[1], user_id=self.from_user.id, number= ID)} успешно добавлено")
                    break
                
                # await bot.send_message(self.from_user.id, text = 'на стадии "пофиг"')
            case 'repeat':
                ID = self.message.caption.split('\n')[0].split('id = ')[1][:-1]
                if db.Database.delete_replic(ID):
                    print(f'{ID} deleted')
                else:
                    print(f'{ID} notdeleted')

            case 'back':
                for info in self.message.photo[-1]:
                    photo = info[1] 
                    ID = self.message.caption.split('(')[:-1]
                    db.Database.set_aside_photo(photo,self.from_user.id,ID)
                    await self.message.answer(text = 'вы вернулись покинули скип очередь', reply_markup=Keyboards.main_menu())
                    break

        await self.data['state'].set_state(MyState.rating)
        await answer_photo(self.message,state = self.data['state'], id = self.from_user.id)
        
            
    
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
