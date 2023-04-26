import threading
import telegram
from rasa.core.agent import Agent
from telegram import ext
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext, ConversationHandler
import asyncio
from datetime import datetime
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict
import requests
from rasa_sdk.events import BotUttered
from rasa.core.agent import Agent
from rasa.core.utils import EndpointConfig
from telegram import Bot
import requests
import os

TOKEN = '6042767853:AAERCZHMBwaSiSY8Moamt6CHIwhMppjKFWU'
BOT_USERNAME = '@YORO_TECBLIC_BOT'
action_endpoint = EndpointConfig(url="http://localhost:5055/webhook")
rasa_agent = Agent.load("models/20230418-123556-impulsive-term.tar.gz", action_endpoint=action_endpoint)
telegram_bot = telegram.Bot(token=TOKEN)
bot = Bot(token=TOKEN)

# from telegram import TelegramDispatcher

async def handle_conversation(update: telegram.Update, context: telegram.ext.CallbackContext) -> None:
    print("Handling conversation...")
    # get the user message
    user_message = update.message.text
    # process the user message with the Rasa agent
    bot_response = await rasa_agent.handle_text(user_message)
    print("Bot response:", bot_response)
    # check if the Rasa agent generated a response
    if bot_response and len(bot_response) > 0:
        # loop over all the response messages
        for response in bot_response:
            # check if the response is a text message
            if response.get("text"):
                # send the text message to the user
                telegram_bot.send_message(chat_id=update.effective_chat.id, text=response["text"])
                
            # check if the response is an image message
            elif response.get("attachment"):
                 # get the image filename from the response message
                image_filename = response["attachment"]
                print("image file name is ",image_filename)
                # read the image file from the local directory
                with open(image_filename, "rb") as f:
                    # send the image file to the user as a document
                    telegram_bot.send_document(chat_id=update.effective_chat.id, document=f, filename=image_filename)
                os.remove(image_filename)
    else:
        # if the Rasa agent didn't generate a response, send a default message to the user
        default_response = "Sorry, I'm having trouble understanding you right now. Please try again later."
        telegram_bot.send_message(chat_id=update.effective_chat.id, text=default_response)

def start_conversation(chat_id, user_message):
    print("Starting conversation...")
    message = telegram.Message(message_id=1, chat=telegram.Chat(id=chat_id, type='private'), date=datetime.now(), text=user_message)
    update = telegram.Update(update_id=1, message=message)
    asyncio.run(handle_conversation(update, None))
 
def handle_telegram_message(update: telegram.Update, context: telegram.ext.CallbackContext):
    print("Handling telegram message...")
    chat_id = update.message.chat_id
    user_message = update.message.text
    
    threading.Thread(target=start_conversation, args=(chat_id, user_message)).start()

def main():
    updater = telegram.ext.Updater(token=TOKEN, use_context=True)
    updater.dispatcher.add_handler(telegram.ext.MessageHandler(telegram.ext.Filters.text, handle_telegram_message))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
