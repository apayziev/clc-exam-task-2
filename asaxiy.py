import logging
import requests
from telegram import Update, ForceReply
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    CallbackContext,
)

from bs4 import BeautifulSoup
from settings import TOKEN

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

logger = logging.getLogger(__name__)


def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    update.message.reply_markdown_v2(f"Enter the product name:")


def help_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    update.message.reply_text("Help!")


def url(update: Update, context: CallbackContext) -> None:
    """Echo the user message."""
    query = update.message.text.lower()
    URL = f"https://asaxiy.uz/product?key={query}"
    response = requests.get(URL, timeout=10)
    soup = BeautifulSoup(response.text, "html.parser")

    # get the first ten products

    products = soup.find_all(
        "div", attrs={"class": "col-6 col-xl-3 col-md-4"}, limit=10
    )
    # print(products)

    for product in products:
        product_title = product.find(
            "h5", attrs={"class": "product__item__info-title"}
        ).text
        product_price = product.find(
            "span", attrs={"class": "product__item-price"}
        ).text
        product_image_link = product.find(
            "div", attrs={"class": "product__item-img"}
        ).find("img")["data-src"]

        if image_link[-5:] == ".webp":
            image_link = product.find("div", attrs={"class": "product__item-img"}).find(
                "img"
            )["data-src"][0:-5]

        context.bot.send_photo(
            update.effective_user.id,
            product_image_link,
            f"{product_title}\n" f"Mahsulot narxi: {product_price}\n",
        )


def main() -> None:
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    updater = Updater(TOKEN, use_context=True)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("start", start))

    # on non command i.e message - echo the message on Telegram
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, url))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == "__main__":
    main()
