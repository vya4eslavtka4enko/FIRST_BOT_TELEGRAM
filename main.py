from typing import Final
import os
from telegram import Update
from telegram.ext import Application,CommandHandler,MessageHandler,filters,ContextTypes

TOKEN = os.environ['API_BOT']
BOT_USERNAME:Final = "@ask_price_bot"
print(TOKEN)


async def start_command(update: Update,context:ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello! I'm crypto bot")
    
    
async def help_command(update:Update,context:ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Please type something so I can respond")
    
    
async def custom_command(update:Update,context:ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hi! This is custom command")
    
#Responses


def handle_response(text:str) -> str:
    processed: str = text.lower()
    if "hello" in processed:
        return "Hey there"
    if "how are you" in processed:
        return "I am good"
    if "I love python" in processed:
        return "nice"
    else:
        return 'I did not get you'  
    
async def handle_message(update: Update ,context:ContextTypes.DEFAULT_TYPE):
    message_type: str = update.message.chat.type
    text:str = update.message.text  
    print(f"User ({update.message.chat.id}) in {message_type}")
    
    if message_type == "group":
        if BOT_USERNAME in text:
            new_text:str = text.replace(BOT_USERNAME,'').strip()
            response:str = handle_response(new_text)
        else:
            return 
    else:
        response:str = handle_response(text)
    
    print("Bot:",response)
    await update.message.reply_text(response)
    

async def error(update:Update, context: ContextTypes.DEFAULT_TYPE):
    print(f"Update {update} caused error {context.error}")
    
    
if __name__ == "__main__":
    print("Starting bot...")
    app = Application.builder().token(TOKEN).build()
    
    # Command
    app.add_handler(CommandHandler('start',start_command))
    app.add_handler(CommandHandler('help',help_command))
    app.add_handler(CommandHandler('custom',custom_command))
    #Message
    app.add_handler(MessageHandler(filters.TEXT, handle_message))
    # Errors
    app.add_error_handler(error)
    
    #Polls the bot
    print("Polling...")
    app.run_polling(poll_interval = 3)
    