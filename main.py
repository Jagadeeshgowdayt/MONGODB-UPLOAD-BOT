import script

...

async def upload(update: Update, context: CallbackContext) -> None:
    await script.upload()
    update.message.reply_text('Latest file uploaded successfully!')

...
