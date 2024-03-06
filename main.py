import logging
import argparse

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


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--token', type=str, required=True)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    """Start the bot."""
    # Create the Application and pass it your bot's token.
    application = tg_ext.Application.builder().token(args.token).build()

    handlers.setup_handlers(application)

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=tg.Update.ALL_TYPES)


if __name__ == "__main__":
    main()
