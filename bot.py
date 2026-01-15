import os
from datetime import time
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

TOKEN = "7978063185:AAFx7VaplhOIONGM_P_M3-lZfaZNADf3q5w"
PHOTO_URL = "https://avatars.mds.yandex.net/i?id=c503a23ec48b8aeef2f1f3bd00f031d124b59d7e-8497453-images-thumbs&n=13"  # Милый котёнок 💕

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    current_jobs = context.job_queue.get_jobs_by_name(f'remind_{chat_id}')
    for job in current_jobs:
        job.schedule_removal()
    
    context.job_queue.run_daily(send_reminder, time(7, 30), chat_id=chat_id, name=f'remind_{chat_id}')
    await update.message.reply_text('✅ 7:30 ежедневно 📸 с картинкой. Тест: /test')

async def test_reminder(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton("✅ Таблеточку выпила!", callback_data='done')]]
    markup = InlineKeyboardMarkup(keyboard)
    await context.bot.send_photo(
        update.effective_chat.id,
        photo=PHOTO_URL,
        caption="🧪 **ТЕСТ 7:30** 🧪\nКотенок, не забудь выпить таблеточку.",
        reply_markup=markup,
        parse_mode='Markdown'
    )

async def send_reminder(context: ContextTypes.DEFAULT_TYPE):
    job = context.job
    keyboard = [[InlineKeyboardButton("✅ Таблеточку выпила!", callback_data='done')]]
    markup = InlineKeyboardMarkup(keyboard)
    await context.bot.send_photo(
        job.chat_id,
        photo=PHOTO_URL,
        caption="Котенок, не забудь выпить таблеточку.",
        reply_markup=markup,
        parse_mode='Markdown'
    )

async def done(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer("Умница! 🥰")
    await query.edit_message_caption("Обожаю тебя!")

def main():
    if not TOKEN:
        print("❌ BOT_TOKEN!")
        return
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("test", test_reminder))
    app.add_handler(CallbackQueryHandler(done, pattern='^done$'))
    print("🐱 Бот с картинкой готов!")
    app.run_polling()

if __name__ == '__main__':
    main()
