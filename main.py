import os
from telegram import ParseMode
import pymongo
import script
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
from telethon.tl.types import Channel, ChannelFull
from telethon.errors.rpcerrorlist import PeerIdInvalid


def start(update, context):
    # Set the start message with an image
    start_message = "Welcome to 🥭 MANGO UPLOAD BOT!\n\nThis bot can upload files from MongoDB to your Telegram channel."
    start_message += "<a href='https://graph.org/file/e84a8eb7963642ddd2968.jpg'><img src='https://graph.org/file/c88b50dc9274946ad47ca.jpg'></a>"
    context.bot.send_message(chat_id=update.effective_chat.id, text=start_message, parse_mode=ParseMode.HTML)


# Define a function to handle /setdatabase command
def set_database(update: Update, context: CallbackContext) -> None:
    # Get the database URI from the command argument
    database_uri = context.args[0]

    # Check if the URI is valid
    try:
        pymongo.MongoClient(database_uri).server_info()
    except pymongo.errors.ServerSelectionTimeoutError:
        update.message.reply_text("Invalid database URI. Please enter a correct URI.")
        return

    # Set the MONGO_URI environment variable
    os.environ['MONGO_URI'] = database_uri

    # Respond to the user
    update.message.reply_text(f"Database URI updated to {database_uri}")



async def upload(update: Update, context: CallbackContext) -> None:
    await script.upload()
    update.message.reply_text('Latest file uploaded successfully!')


async def set_channel(update, context):
    try:
        channel_id = context.args[0]
        entity = await context.bot.get_entity(channel_id)
        # If the entity is not a channel or supergroup, raise an exception
        if not isinstance(entity, (Channel, ChannelFull)):
            raise ValueError("Provided ID is not a channel or supergroup.")
        # Update the environment variables
        os.environ['CHANNEL_NAME'] = entity.username
        os.environ['CHANNEL_ID'] = str(entity.id)
        # Send a success message to the user
        update.message.reply_text(f"Channel set to @{entity.username}.")
    except IndexError:
        update.message.reply_text("Please provide a channel ID.")
    except (PeerIdInvalid, ValueError):
        update.message.reply_text("Please check the provided channel ID.")


# Set up the Telegram bot and add command handlers
bot_token = os.environ.get('BOT_TOKEN')
updater = Updater(bot_token)
updater.dispatcher.add_handler(CommandHandler('setdatabase', set_database))
updater.dispatcher.add_handler(CommandHandler('upload', upload))
updater.dispatcher.add_handler(commandHandler('setchannel',set_channel))
updater.dispatcher.add_handler(CommandHandler('start', start))
# Start the bot
updater.start_polling()
updater.idle()
