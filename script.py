import asyncio

import os

import pymongo

import time

import random

from telethon import TelegramClient, errors

# Connect to MongoDB

client = pymongo.MongoClient("mongodb://localhost:27017/")

db = client["mydatabase"]

collection = db["mycollection"]

# Set up Telegram client

bot_token = os.environ['BOT_TOKEN']

channel_name = '@YOUR_TELEGRAM_CHANNEL_NAME'

client = TelegramClient('session_name', 12345, 'YOUR_API_HASH').start(bot_token=bot_token)

# Define batch size and message sending function

BATCH_SIZE = 100  # Number of messages to send in each batch

sent_messages = set()  # Keep track of file_ids that have been sent

async def send_messages(messages_to_send):

    global sent_messages

    for message in messages_to_send:

        # Extract the file ID from the message's media

        media = message.get('media', None)

        if media:

            file_id = media.get('file_id', None)

        else:

            file_id = None

        

        # Use the file ID to check for duplicates

        if file_id and file_id not in sent_messages:

            try:

                await client.send_message('@YOUR_TELEGRAM_CHANNEL_NAME', f"Data from MongoDB: {message}")

                sent_messages.add(file_id)

            except errors.FloodWaitError as e:

                print(f"Got FloodWaitError. Sleeping for {e.seconds} seconds.")

                time.sleep(e.seconds)

            except errors.ConnectionError as e:

                print(f"Got ConnectionError: {e}. Retrying in 5 seconds...")

                time.sleep(5)

# Send messages in batches

messages_to_send = []

for item in collection.find():

    messages_to_send.append(item)

    if len(messages_to_send) >= BATCH_SIZE:

        asyncio.run(send_messages(messages_to_send))

        messages_to_send = []

        await asyncio.sleep(random.randint(3,6)) # add random delay between batches to avoid flood wait

# Send any remaining messages

if messages_to_send:

    asyncio.run(send_messages(messages_to_send))

# Disconnect the client

client.disconnect()

