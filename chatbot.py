from telegram.ext import Updater, MessageHandler, CommandHandler,filters
from telegram.ext import CallbackContext,ConversationHandler,Application,ContextTypes
from telegram import Update,ReplyKeyboardMarkup,ReplyKeyboardRemove
import logging

# Define game states
START, FIRST_CHOICE, SECOND_CHOICE,TREASURE,DEAD_END,LOST = range(6)
# Define the Keyboards
start_keyboard=[['Left','Right']]
start_markup = ReplyKeyboardMarkup(start_keyboard, one_time_keyboard=True)

first_choice_keyboard=[['Left','Straight']]
first_choice_markup = ReplyKeyboardMarkup(first_choice_keyboard, one_time_keyboard=True)

second_choice_keyboard=[['Left','Right']]
second_choice_markup = ReplyKeyboardMarkup(second_choice_keyboard, one_time_keyboard=True)

# Define the start function
async def start(update: Update, context: CallbackContext) -> int:
    await update.message.reply_text(
        "Welcome to the Leafy Maze Adventure!\n"
        "You find yourself at the entrance of a large, leafy maze. The paths look confusing and twist in various directions.\n"
        "Do you want to go 'left' or 'right'?"
        reply_markup=start_markup
    )
    return FIRST_CHOICE

# Handle the first choice
async def first_choice(update: Update, context: CallbackContext) -> int:
    choice = update.message.text.lower()
    if choice == 'left':
        await update.message.reply_text(
            "You take the left path and soon reach another fork in the path.\n"
            "Do you want to go 'left' or 'straight'?"
            reply_markup=first_choice_markup
        )
        return SECOND_CHOICE
    elif choice == 'right':
        await update.message.reply_text(
            "You take the right path and soon reach a dead end. You turn back to the start.\n"
            "Do you want to go 'left' or 'right'?"
            reply_markup=start_markup
        )
        return FIRST_CHOICE
    else:
        await update.message.reply_text(
            "Invalid choice. Please type 'left' or 'right'."
            reply_markup=start_markup
        )
        return FIRST_CHOICE

# Handle the second choice
async def second_choice(update: Update, context: CallbackContext) -> int:
    choice = update.message.text.lower()
    if choice == 'left':
        await update.message.reply_text(
            "You take the left path and find yourself at another fork.\n"
            "Do you want to go 'left' or 'right'?"
            reply_markup=second_choice_markup
        )
        return TREASURE
    elif choice == 'straight':
        await update.message.reply_text(
            "You walk straight and find a hidden treasure chest! Congratulations, you have found the treasure and completed the adventure!"

        )
        return ConversationHandler.END
    else:
        await update.message.reply_text(
            "Invalid choice. Please type 'left' or 'straight'."
            reply_markup=first_choice_markup
        )
        return SECOND_CHOICE

async def treasure(update: Update, context: CallbackContext) -> int:
    choice = update.message.text.lower()
    if choice == 'left':
        await update.message.reply_text(
            "You take the left path and find yourself lost in the maze. You wander around but can't find your way back. You are lost."
        )
        return LOST
    elif choice == 'right':
        await update.message.reply_text(
            "You take the right path and find yourself at a dead end. You turn back to the previous fork.\n"
            "Do you want to go 'left' or 'right'?"
            reply_markup=second_choice_markup
        )
        return SECOND_CHOICE
    else:
        await update.message.reply_text(
            "Invalid choice. Please type 'left' or 'right'."
            reply_markup=second_choice_markup
        )
        return TREASURE

async def dead_end(update:Update,context:CallbackContext)->int:
    await update.message.reply_text(
        "You reach a dead end and have to turn back. Do you want to go left or right?"
        reply_markup=start_markup
    )
    return FIRST_CHOICE
async def lost(update:Update,context:CallbackContext)->int:
    await update.message.reply_text(
        "You wander aimlessly and realize you are hopelessly lost.The Adventure ends here"
    )
    return ConversationHandler.END
# Handle the cancel command
async def cancel(update: Update, context: CallbackContext) -> int:
    await update.message.reply_text(
        "Adventure canceled. See you next time!"
    )
    return ConversationHandler.END

def main()->None:
    Token="7453996986:AAGSyvVzDgLehyO_cF1Ejzyeclu1E0779MM"
    application=Application.builder().token(Token).build()
    
    
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            FIRST_CHOICE: [MessageHandler(filters.TEXT & ~filters.COMMAND, first_choice)],
            SECOND_CHOICE: [MessageHandler(filters.TEXT & ~filters.COMMAND, second_choice)],
            TREASURE: [MessageHandler(filters.TEXT & ~filters.COMMAND, treasure)],
            DEAD_END: [MessageHandler(filters.TEXT & ~filters.COMMAND, dead_end)],
            LOST: [MessageHandler(filters.TEXT & ~filters.COMMAND, lost)],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )

    application.add_handler(conv_handler)
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()