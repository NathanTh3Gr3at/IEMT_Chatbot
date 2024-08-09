from telegram.ext import Updater, MessageHandler, CommandHandler,filters,ContextTypes
from telegram.ext import Application,CallbackContext,ConversationHandler
from telegram import ForceReply,Update
import logging

# Game States
START,FIRST_CHOICE,SECOND_CHOICE,THIRD_CHOICE=range(4)

# Game Start function
def start(update:Update,context:CallbackContext)->int:
    update.message.reply_text("Welcome To The Text Adventure Game?\n""You find yourself in a room with only 2 exits. one to the North and the other to the south""Do you want to go North (N) or South (S)?")
    return FIRST_CHOICE

# handle first choice
def first_choice(update:Update,context:CallbackContext)->int:
    choice=update.message.text.lower()
    if choice == 'n':
        update.message.reply_text(
            '''You  head to the door to the north.
            Upon reaching the door you notice that the door is unlocked do you want to enter (y or n)?''' 
        )
        return SECOND_CHOICE
    elif choice == 'south':
        update.message.reply_text(
            '''You head south and reach a wall that has the number 42 etched deeply into it.
            You can head north only'''
        )
        return FIRST_CHOICE
    else:
        update.message.reply_text("Invalid choice. Please choose North or South.")
        return FIRST_CHOICE

# Second room that has 3 doors
def second_choice(update:Update,context:CallbackContext)->int:
    choice=update.message.text.lower()
    if choice =='y':
        update.message.reply_text(
            '''You enter the room. 
            The room is dark but illuminated by candles
            There are 3 doors, at the far end of the room.
            The doors are numbered 1-3 starting from the left
            Pick a door (1-3)'''
        )
        return THIRD_CHOICE
    elif choice=='n':
        update.message.reply_text(
            '''You retrace your steps and have the option to go to the wall or the door you just came through
            Do you want to go through the door(y or n)?'''
        )
        return FIRST_CHOICE
    else:
        update.message.reply_text("Invalid, please choose y or n")
        return SECOND_CHOICE

def third_choice(update:Update,context:CallbackContext)->int:
    choice= update.message.text.lower()
    if choice=="1":
        update.message.reply_text(
            '''You are enter the first door
            You are greeted by repetition'''
        )
        return FIRST_CHOICE
    elif choice=="2":
        update.message.reply_text(
            '''You are enter the first door
            You are greeted by Victory'''
        )
        return ConversationHandler.END
    elif choice=="2":
        update.message.reply_text(
            '''You are enter the Third door
            You are greeted by repetition'''
        )
        return FIRST_CHOICE
    else:
        update.message.reply_text("Invalid, choose either door 1,2 or 3")
        return THIRD_CHOICE

# handle cancel
def cancel(update:Update,context:CallbackContext)->int:
    update.message.reply_text("Adventure cancelled")
    return ConversationHandler.END

def main()->None:
    Token="7453996986:AAGSyvVzDgLehyO_cF1Ejzyeclu1E0779MM"
    updater=Updater(Token,use_context=True)
    dp=updater.dispatcher
    conv_handler=ConversationHandler(
        entry_points=[CommandHandler('start',start)],
        states={FIRST_CHOICE:[MessageHandler(filters.text & ~filters.command,first_choice)],
                SECOND_CHOICE:[MessageHandler(filters.text & ~filters.command,second_choice)],
                THIRD_CHOICE:[MessageHandler(filters.text & ~filters.command,third_choice)],
                },
        fallbacks=[CommandHandler('cancel',cancel)]
    )
    dp.add_handler(conv_handler)
    updater.start_polling()
    updater.idle()
    

if __name__ == "__main__":
    main()