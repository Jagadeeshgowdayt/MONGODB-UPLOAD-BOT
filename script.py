
import os

import pymongo

import random

import time

from datetime import datetime

from telethon import TelegramClient, errors

# Set up MongoDB

mongo_uri = os.environ.get('MONGODB_URI')

client = pymongo.MongoClient(mongo_uri)

db = client.get_default_database()

collection = db['mycollection']

# Set up Telegram client

bot_token = os.environ.get('BOT_TOKEN')

channel_name = os.environ.get('CHANNEL_NAME')

api_id = os.environ.get('API_ID')

api_hash = os.environ.get('API_HASH')

client = TelegramClient('session_name', api_id, api_hash).start(bot_token=bot_token)

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

                await client.send_message(channel_name, f"Data from MongoDB: {message}")

                sent_messages.add(file_id)

            except errors.FloodWaitError as e:

                print(f"Got FloodWaitError. Sleeping for {e.seconds} seconds.")

                time.sleep(e.seconds)

            except errors.ConnectionError as e:

                print(f"Got ConnectionError: {e}. Retrying in 5 seconds...")

                time.sleep(5)

async def main():

    messages_to_send = []

    for item in collection.find():

        messages_to_send.append(item)

        if len(messages_to_send) >= BATCH_SIZE:

            await send_messages(messages_to_send)

            messages_to_send = []

            await asyncio.sleep(random.randint(3, 6)) # add random delay between batches to avoid flood wait

    # Send any remaining messages

    if messages_to_send:

        await send_messages(messages_to_send)

async def run():

    while True:

        now = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')

        print(f"Running the script. Time: {now}")

        await main()

        # Sleep for 5 minutes

        await asyncio.sleep(5 * 60)

if __name__ == '__main__':

    asyncio.get_event_loop().run_until_complete(run())

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



import asyncio

import os

import pymongo

import random

import time

from datetime import datetime

from telethon import TelegramClient, errors

# Set up MongoDB

mongo_uri = os.environ.get('MONGODB_URI')

client = pymongo.MongoClient(mongo_uri)

db = client.get_default_database()

collection = db['mycollection']

# Set up Telegram client

bot_token = os.environ.get('BOT_TOKEN')

channel_name = os.environ.get('CHANNEL_NAME')

api_id = os.environ.get('API_ID')

api_hash = os.environ.get('API_HASH')

client = TelegramClient('session_name', api_id, api_hash).start(bot_token=bot_token)

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

                await client.send_message(channel_name, f"Data from MongoDB: {message}")

                sent_messages.add(file_id)

            except errors.FloodWaitError as e:

                print(f"Got FloodWaitError. Sleeping for {e.seconds} seconds.")

                time.sleep(e.seconds)

            except errors.ConnectionError as e:

                print(f"Got ConnectionError: {e}. Retrying in 5 seconds...")

                time.sleep(5)

async def main():

    messages_to_send = []

    for item in collection.find():

        messages_to_send.append(item)

        if len(messages_to_send) >= BATCH_SIZE:

            await send_messages(messages_to_send)

            messages_to_send = []

            await asyncio.sleep(random.randint(3, 6)) # add random delay between batches to avoid flood wait

    # Send any remaining messages

    if messages_to_send:

        await send_messages(messages_to_send)

async def run():

    while True:

        now = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')

        print(f"Running the script. Time: {now}")

        await main()

        # Sleep for 5 minutes

        await asyncio.sleep(5 * 60)

if __name__ == '__main__':

    asyncio.get_event_loop().run_until_complete(run())
