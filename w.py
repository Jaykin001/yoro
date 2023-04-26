from typing import Final

# pip install python-telegram-bot
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from telegram import InputFile

print('Starting up bot...')

TOKEN: Final = '6042767853:AAERCZHMBwaSiSY8Moamt6CHIwhMppjKFWU'
BOT_USERNAME: Final = '@YORO_TECBLIC_BOT'


# Import the InputFile class from the telegram module

# Define the image path
image_path = 'https://www.google.com/url?sa=i&url=https%3A%2F%2Funsplash.com%2Fs%2Fphotos%2Fhuman&psig=AOvVaw1enG6Xob49CM9Z7wWue3j0&ust=1680163220622000&source=images&cd=vfe&ved=0CA8QjRxqFwoTCOiz7fDVgP4CFQAAAAAdAAAAABAE'

# Define the start_command function
from telegram import Update, InputMediaPhoto

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Send a message with an image
    with open('inventory_value.png', 'rb') as f:
        photo_bytes = f.read()
        await update.message.reply_photo(photo_bytes, caption='Hello there!')

    # Alternatively, you can use the InputMediaPhoto class to send multiple images at once
    # with open('path/to/image2.jpg', 'rb') as f2:
    #     photo_bytes2 = f2.read()
    #     media_group = [InputMediaPhoto(photo_bytes), InputMediaPhoto(photo_bytes2)]
    #     update.message.reply_media_group(media_group)


# Lets us use the /help command
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Try typing anything and I will do my best to respond!')


# Lets us use the /custom command
async def custom_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('This is a custom command, you can add whatever text you want here.')


def handle_response(text: str) -> str:
    # Create your own response logic
    processed: str = text.lower()

    if 'hello' in processed:
        return 'Hey there!'

    if 'how are you' in processed:
        return 'I\'m good!'

    if 'i love python' in processed:
        return 'Remember to subscribe!'

    return 'I don\'t understand'


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Get basic info of the incoming message
    message_type: str = update.message.chat.type
    text: str = update.message.text

    # Print a log for debugging
    print(f'User ({update.message.chat.id}) in {message_type}: "{text}"')

    # React to group messages only if users mention the bot directly
    if message_type == 'group':
        # Replace with your bot username
        if BOT_USERNAME in text:
            new_text: str = text.replace(BOT_USERNAME, '').strip()
            response: str = handle_response(new_text)
        else:
            return  # We don't want the bot respond if it's not mentioned in the group
    else:
        response: str = handle_response(text)

    # Reply normal if the message is in private
    print('Bot:', response)
    await update.message.reply_text(response)


# Log errors
async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'Update {update} caused error {context.error}')


# Run the program
if __name__ == '__main__':
    app = Application.builder().token(TOKEN).build()

    # Commands
    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('help', help_command))
    app.add_handler(CommandHandler('custom', custom_command))

    # Messages
    app.add_handler(MessageHandler(filters.TEXT, handle_message))

    # Log all errors
    app.add_error_handler(error)

    print('Polling...')
    # Run the bot
    app.run_polling(poll_interval=5)
