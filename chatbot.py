from telegram.ext import Updater, MessageHandler, CommandHandler,filters
from telegram.ext import CallbackContext,ConversationHandler,Application,ContextTypes
from telegram import Update,ReplyKeyboardMarkup,ReplyKeyboardRemove
import spacy
import requests
from bs4 import BeautifulSoup

# Load spaCy model
nlp=spacy.load("en_core_web_sm")

# Define States the the Conversation handler
# 
#
FIRST_CHOICE, SECOND_CHOICE,TREASURE,DEAD_END,LOST,MAZE,MAIN_MENU,SUMMARIZE,URL,TEXT = range(10)
# Define the Keyboards 
main_menu_keyboard=[['Maze Game','Content Summarizer']]
main_menu_markup=ReplyKeyboardMarkup(main_menu_keyboard,one_time_keyboard=True)

start_keyboard=[['Left','Right']]
start_markup = ReplyKeyboardMarkup(start_keyboard, one_time_keyboard=True)

first_choice_keyboard=[['Left','Straight']]
first_choice_markup = ReplyKeyboardMarkup(first_choice_keyboard, one_time_keyboard=True)

second_choice_keyboard=[['Left','Right']]
second_choice_markup = ReplyKeyboardMarkup(second_choice_keyboard, one_time_keyboard=True)




# Define the start function
async def start(update: Update, context: CallbackContext) -> int:
    await update.message.reply_text(
        "Welcome to the Multi-Use Bot!\n"
        "You can choose to play the Maze Game or use the Content summarizer.\n"
        "Please choose an option.",
        reply_markup=main_menu_markup
    )
    return MAIN_MENU

# Handles the Main menu
async def main_menu(update:Update,context:CallbackContext)->int:
    choice=update.message.text
    if choice=="Maze Game":
        await update.message.reply_text(
            "Welcome to the Leafy Maze of Adventure!\n"
            "You find yourself at the entrance of a leafy maze. The paths look confusing and contain various twists and turns\n"
            "Do you want to go 'left' or 'right'.",
            reply_markup=start_markup
        )
        return FIRST_CHOICE
    elif choice =='Content Summarizer':
        await update.message.reply_text(
            "Send the text you want summarized or send the URL",
            
        )
        return SUMMARIZE
    else:
        await update.message.reply_text(
            "Invalid choice. Please choose Maze game or Content Summarizer.",
            reply_markup=main_menu_markup
        )
        return MAIN_MENU

# Handle the first choice
async def first_choice(update: Update, context: CallbackContext) -> int:
    choice = update.message.text.lower()
    if choice == 'left':
        await update.message.reply_text(
            "You take the left path and soon reach another fork in the path.\n",
            "Do you want to go 'left' or 'straight'?",
            reply_markup=first_choice_markup
        )
        return SECOND_CHOICE
    elif choice == 'right':
        await update.message.reply_text(
            "You take the right path and soon reach a dead end. You turn back to the start.\n",
            "Do you want to go 'left' or 'right'?",
            reply_markup=start_markup
        )
        return FIRST_CHOICE
    else:
        await update.message.reply_text(
            "Invalid choice. Please type 'left' or 'right'.",
            reply_markup=start_markup
        )
        return FIRST_CHOICE

# Handle the second choice
async def second_choice(update: Update, context: CallbackContext) -> int:
    choice = update.message.text.lower()
    if choice == 'left':
        await update.message.reply_text(
            "You take the left path and find yourself at another fork.\n"
            "Do you want to go 'left' or 'right'?",
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
            "Invalid choice. Please type 'left' or 'straight'.",
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
            "Do you want to go 'left' or 'right'?",
            reply_markup=second_choice_markup
        )
        return SECOND_CHOICE
    else:
        await update.message.reply_text(
            "Invalid choice. Please type 'left' or 'right'.",
            reply_markup=second_choice_markup
        )
        return TREASURE

async def dead_end(update:Update,context:CallbackContext)->int:
    await update.message.reply_text(
        "You reach a dead end and have to turn back. Do you want to go left or right?",
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

# Content Summarizer
def summarize(update:Update,context:CallbackContext)->int:
    text=update.message.text
    if text.startswith("http"):
        return handle_url(update,context)
    else:
        return handle_text(update,context)
async def handle_url(update:Update,content:CallbackContext)->int:
    url=update.message.text
    try:
        response=requests.get(url)
        soup=BeautifulSoup(response.content,'html.parser')
        paragraphs=soup.find_all('p')
        text=' '.join([para.text for para in paragraphs])
        summary=summarize_text(text)
        await update.message.reply_text(f"Summary:\n{summary}")
    except Exception as e:
        await update.message.reply_text("An error occurred while processing the URL. Please try again.")
    return ConversationHandler.END

async def handle_text(update:Update,context:CallbackContext)->int:
    text=update.message.text
    summary=summarize_text(text)
    await update.message.reply_text(f"Summary:\n{summary}")
    return ConversationHandler.END

async def summarize_text(text:str)-> str:
    doc=nlp(text)
    sentences=[sent.text for sent in doc.sents]
    if len(sentences)>5:
        summary=' '.join(sentences[:5])
    else:
        summary=text
    return summary

def main()->None:
    Token="7453996986:AAGSyvVzDgLehyO_cF1Ejzyeclu1E0779MM"
    application=Application.builder().token(Token).build()
    
    
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            MAIN_MENU: [MessageHandler(filters.TEXT & ~filters.COMMAND, main_menu)],
            FIRST_CHOICE: [MessageHandler(filters.TEXT & ~filters.COMMAND, first_choice)],
            SECOND_CHOICE: [MessageHandler(filters.TEXT & ~filters.COMMAND, second_choice)],
            TREASURE: [MessageHandler(filters.TEXT & ~filters.COMMAND, treasure)],
            DEAD_END: [MessageHandler(filters.TEXT & ~filters.COMMAND, dead_end)],
            LOST: [MessageHandler(filters.TEXT & ~filters.COMMAND, lost)],
            URL: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_url)],
            TEXT: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text)],
            SUMMARIZE: [MessageHandler(filters.TEXT & ~filters.COMMAND, summarize)],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )

    application.add_handler(conv_handler)
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()