from telegram.ext import Updater, CommandHandler

...

def start(update, context):
    ...

def help(update, context):
    ...

def upload_file(update, context):
    # Your file upload logic goes here
    ...

def main():
    ...
    
    # Add the command handler for the /upload command
    dp.add_handler(CommandHandler("upload", upload_file))

    ...
    
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
