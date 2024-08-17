#!/usr/bin/env python3
import logging
from telegram import Update
from telegram.ext import Application,CommandHandler, MessageHandler, filters, CallbackContext, ConversationHandler
import spacy

# Initialize SpaCy
nlp = spacy.load('en_core_web_sm')

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# States for the conversation
ASKING_NAME, ASKING_AGE, ASKING_OCCUPATION, COMPILING_INFO,ASKING_EMAIL,ASKING_PHONENUMBER,ASKING_SCHOOL = range(7)

# User data dictionary
user_data = {}

async def start(update: Update, context: CallbackContext) -> int:
    logger.info('USER STARTED CONVERSATION: %s',update.effective_user)
    await update.message.reply_text('Hi! I am your info bot. What is your name?')
    return ASKING_NAME

async def ask_age(update: Update, context: CallbackContext) -> int:
    user_data['name'] = update.message.text
    logger.info('RECEVEIVED NAME: %s',user_data['name'])
    await update.message.reply_text('Nice to meet you! How old are you?')
    return ASKING_AGE

async def ask_email(update:Update,context:CallbackContext)->int:
    user_data['age']=update.message.text
    logger.info('RECEIVED AGE: %s',user_data['age'])
    await update.message.reply_text('Please enter your email address?')
    return ASKING_EMAIL

async def ask_phonenumber(update:Update,context:CallbackContext)->int:
    user_data['email']=update.message.text
    logger.info('RECEIVED EMAIL: %s',user_data['email'])
    await update.message.reply_text('Please enter your Phone number?')
    return ASKING_PHONENUMBER

async def ask_occupation(update: Update, context: CallbackContext) -> int:
    user_data['phonenumber'] = update.message.text
    logger.info('RECEIVED PHONENUMBER: %s',user_data['phonenumber'])
    await update.message.reply_text('Great! What is your occupation?')
    return ASKING_OCCUPATION

async def ask_school(update: Update, context: CallbackContext) -> int:
    user_data['occupation'] = update.message.text
    logger.info('RECEIVED OCCUPATION: %s', user_data['occupation'])
    if user_data['occupation'].lower() == 'student':
        await update.message.reply_text('Which school or university do you attend?')
        return ASKING_SCHOOL
    else:
        return compile_info(update, context)

async def compile_info(update: Update, context: CallbackContext) -> int:
    if user_data['occupation'].lower()=='student':
        user_data['school']=update.message.text
        logger.info('RECEIVED SCHOOL: %s',user_data['school'])
    user_data['occupation'] = update.message.text
    name_doc = nlp(user_data['name'])
    age_doc = nlp(user_data['age'])
    occupation_doc = nlp(user_data['occupation'])
    email_doc=nlp(user_data['email'])
    phonenumber_doc=nlp(user_data['phonenumber'])
    
    name = " ".join([ent.text for ent in name_doc.ents if ent.label_ == "PERSON"]) or user_data['name']
    age = " ".join([ent.text for ent in age_doc.ents if ent.label_ == "DATE"]) or user_data['age']
    occupation = " ".join([ent.text for ent in occupation_doc.ents if ent.label_ == "WORK_OF_ART"]) or user_data['occupation']
    email=" ".join([ent.text for ent in email_doc.ents if ent.label=="PERSON"])or user_data['email']
    phonenumber=" ".join([ent.text for ent in phonenumber_doc.ents if ent.label=="PERSON"])or user_data['phonenumber']
    info_card = (
        f"Information Card:\n\n"
        f"Name: {name}\n"
        f"Age: {age}\n"
        f"Email: {email}\n"
        f"Phone number: {phonenumber}\n"
        f"Occupation: {occupation}"
    )
    if 'school' in user_data:
        info_card+= f"\nSchool/University: {user_data['school']}"
    await update.message.reply_text(info_card)
    logger.info('INFORMATON CARD SENT: %s',{'name':name,'age':age,'occupation':occupation,'school':user_data.get('school')})
    return ConversationHandler.END

async def cancel(update: Update, context: CallbackContext) -> int:
    logger.info('CONVERSATION CANCELED BY USER: %s',update.effective_user)
    await update.message.reply_text('Goodbye! If you need to start again, just type /start.')
    return ConversationHandler.END

def main():
    
    Token="7453996986:AAGSyvVzDgLehyO_cF1Ejzyeclu1E0779MM"
    application=Application.builder().token(Token).build()
    
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            ASKING_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_age)],
            ASKING_AGE: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_email)],
            ASKING_EMAIL:[MessageHandler(filters.TEXT & ~filters.COMMAND,ask_phonenumber)],
            ASKING_PHONENUMBER:[MessageHandler(filters.TEXT & ~filters.COMMAND,ask_occupation)],
            ASKING_OCCUPATION: [MessageHandler(filters.TEXT & ~filters.COMMAND, compile_info)],
            
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )

    application.add_handler(conv_handler)
    application.run_polling(allowed_updates=Update.ALL_TYPES)



if __name__ == '__main__':
    main()