import abc

import telegram as tg
import telegram.ext as tg_ext
import typing as tp
from bot import messages


# Define a few command handlers. These usually take the two arguments update and
# context.

class BaseHandler(abc.ABC):
    def __init__(self) -> None:
        self.user: tp.Optional[tg.User] = None

    async def __call__(self, update: tg.Update, context: tg_ext.ContextTypes.DEFAULT_TYPE) -> None:
        self.user = update.effective_user
        self.messages = messages.get_message(self.user)
        await self.handle(update, context)

    @abc.abstractmethod
    async def handle(self, update: tg.Update, context: tg_ext.ContextTypes.DEFAULT_TYPE) -> None:
        raise NotImplemented


class StartHandler(BaseHandler):
    async def handle(self, update: tg.Update, context: tg_ext.ContextTypes.DEFAULT_TYPE) -> None:
        await update.message.reply_text(self.messages.start())


class HelpHandler(BaseHandler):
    async def handle(self, update: tg.Update, context: tg_ext.ContextTypes.DEFAULT_TYPE) -> None:
        await update.message.reply_text(self.messages.help())


class WeatherHandler(BaseHandler):
    async def handle(self, update: tg.Update, context: tg_ext.ContextTypes.DEFAULT_TYPE) -> None:
        await update.message.reply_text(self.messages.weather(update.message.text)[0])
        await update.message.reply_text(self.messages.weather(update.message.text)[1])


def setup_handlers(application: tg_ext.Application) -> None:
    application.add_handler(tg_ext.CommandHandler('start', StartHandler()))
    application.add_handler(tg_ext.CommandHandler('help', HelpHandler()))
    application.add_handler(tg_ext.MessageHandler(tg_ext.filters.TEXT & ~tg_ext.filters.COMMAND, WeatherHandler()))
    # on non command i.e. message - echo the message on Telegram
