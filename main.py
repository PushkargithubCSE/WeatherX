from telegram import Update, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler
from telegram.ext import CallbackContext
from weather import get_forecast

async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text(
        text="Hello! how can i assist you today , please share your location "
    )

async def echo(update: Update, context: CallbackContext) -> None:
    # Check if there is a message associated with the update
    if update.message is None:
        return

    # Check if the message contains location data
    if update.message.location:
        await handle_location(update, context)
        return

    # Check if the message is a command
    if update.message.text.startswith('/'):
        return  # Ignore command messages

    # If not a command or location, echo the message
    message_text = update.message.text
    await context.bot.send_message(chat_id=update.effective_chat.id, text=message_text)

async def button(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()

    # Handle button presses
    if query.data == "option1":
        await query.message.reply_text(f"You pressed Option 1!")
    elif query.data == "option2":
        await query.message.reply_text(f"You pressed Option 2!")

async def handle_location_command(update: Update, context: CallbackContext) -> None:
    # Check if the command is /location
    if update.message.text.lower() == '/location':
        button = [[KeyboardButton("Share Location", request_location=True)]]  # Set request_location to True
        reply_markup = ReplyKeyboardMarkup(button)
        await update.message.reply_text(
            text="Please share your location:",
            reply_markup=reply_markup
        )

async def handle_location(update: Update, context: CallbackContext) -> None:
    # Check if the message contains location data
    if update.message.location:
        location = update.message.location
        latitude = location.latitude
        longitude = location.longitude
        forecast = get_forecast(latitude,longitude)
        await update.message.reply_text(
            text=forecast

        )
    else:
        # Ignore non-location messages
        return

def main() -> None:
    application = Application.builder().token("7193704850:AAEsd6Az6KqWQvYfO0ItO0daSs-uyJfs0aY").build()

    start_handler = CommandHandler('start', start)
    echo_handler = MessageHandler(None, echo)  # Echo all non-command messages
    button_handler = CallbackQueryHandler(button)
    location_command_handler = CommandHandler('location', handle_location_command)

    application.add_handler(start_handler)
    application.add_handler(echo_handler)
    application.add_handler(button_handler)
    application.add_handler(location_command_handler)

    application.run_polling()

if __name__ == '__main__':
    main()
