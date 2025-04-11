
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext
from facebook_creator import create_facebook_account, save_cookies_to_file

TOKEN = '7860410116:AAFpIea3bDqMHw9U0wdLlRNp5KYVZcU9WpE'

def start(update: Update, context: CallbackContext):
    chat_id = update.message.chat.id
    welcome_text = "مرحبا بك في بوت البريد المؤقت + إنشاء حسابات فيسبوك."
    context.bot.send_message(
        chat_id=chat_id,
        text=welcome_text,
        reply_markup=main_menu()
    )

def main_menu():
    markup = InlineKeyboardMarkup([
        [InlineKeyboardButton("قائمة البريد", callback_data='email_list')],
        [InlineKeyboardButton("انشاء بريد", callback_data='generate')],
        [InlineKeyboardButton("بريداتي", callback_data='my_emails')],
        [InlineKeyboardButton("انشاء حساب فيسبوك", callback_data='create_fb_account')]
    ])
    return markup

def handle_create_fb_account(update: Update, context: CallbackContext):
    query = update.callback_query
    chat_id = query.message.chat.id
    query.answer("جاري انشاء حساب فيسبوك...")

    try:
        account = create_facebook_account()
        save_cookies_to_file(account)

        msg = "تم انشاء الحساب بنجاح:\n"
        msg += f"- الاسم: {account['name']}\n"
        msg += f"- البريد: {account['email']}\n"
        msg += f"- الباسورد: {account['password']}\n\n"
        msg += "كوكيز الحساب:\n"
        msg += f"c_user={account['c_user']}; xs={account['xs']};"
        context.bot.send_message(chat_id, msg)
    except Exception as e:
        context.bot.send_message(chat_id, f"فشل في انشاء الحساب:\n{str(e)}")

def handle_callback(update: Update, context: CallbackContext):
    query = update.callback_query
    if query.data == 'create_fb_account':
        handle_create_fb_account(update, context)
    else:
        query.answer("زر غير مفعل حاليا.")

def main():
    updater = Updater(TOKEN)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CallbackQueryHandler(handle_callback))
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
