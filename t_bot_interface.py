import asyncio
import configparser
import variables
from aiogram import Bot, Dispatcher, Router, types, F
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage
from bot_commands import set_default_commands
from nim_connect import get_talk

def bot_init(__token):
    bot = Bot(token=__token)
    dp = Dispatcher(storage=MemoryStorage())
    router = Router()
    dp.include_router(router)
    return bot, dp, router

class BotInterface:

    def __init__(self):
        config = configparser.ConfigParser()
        config.read(variables.config_path)
        __token = config['BOT']['token']
        self.bot, self.dp, self.router = bot_init(__token)
        self.callbacks = {}
        self.register_routers()

    def register_routers(self):
        # self.dp.include_router(self.shopping_cart.router)
        pass

    async def handlers(self):

        @self.dp.message(CommandStart())
        async def start(message: types.Message):
            await self.bot.send_message(message.chat.id, "NVIDIA|llama-3_1-nemotron:\nНапиши промпт", reply_markup=types.ReplyKeyboardRemove())

        @self.router.callback_query(lambda c: c.data == 'registration')
        async def callbacks_registration(callback: types.CallbackQuery, state: FSMContext):
            pass

        @self.router.message(F.text)
        async def text(message: types.Message):
            answer = get_talk(message.text, user=message.chat.id)
            await self.bot.send_message(message.chat.id, answer['content'], parse_mode='html')
            pass

        @self.router.message(F.document)
        async def handle_document(message: types.Message):
            await self.bot.send_message(message.chat.id, "Я не знаю что делать с документом")

        async def on_startup(dp):
            await set_default_commands(dp.bot)

        await self.dp.start_polling(self.bot, on_startup=on_startup, skip_updates=True)

    async def send_large_message(self, message, text, **kwargs) -> types.Message:
        pass

    async def send_message(self, message, text, **kwargs) -> types.Message:
        disable_web_page_preview = True if kwargs.get('disable_web_page_preview') else False
        parse_mode = kwargs['parse_mode'] if kwargs.get('parse_mode') else 'html'
        disable_notification = True if kwargs.get('disable_notification') else False
        reply_markup = kwargs['reply_markup'] if kwargs.get('reply_markup') else None
        return await self.bot.send_message(
            message.chat.id, text,
            parse_mode=parse_mode,
            reply_markup=reply_markup,
            disable_notification=disable_notification,
            disable_web_page_preview=disable_web_page_preview
        )

if __name__ == '__main__':
    bot = BotInterface()
    asyncio.run(bot.handlers())
