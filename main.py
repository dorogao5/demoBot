import logging
import argparse
import secrets

from bot import handlers

import telegram as tg
import telegram.ext as tg_ext

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

tg_token = open('C:/Users/ilasn/PycharmProjects/demoBot/secrets/tg_token').readline()


def main() -> None:
    """Start the bot."""
    # Create the Application and pass it your bot's token.
    application = tg_ext.Application.builder().token(tg_token).build()

    handlers.setup_handlers(application)

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=tg.Update.ALL_TYPES)


if __name__ == "__main__":
    main()
