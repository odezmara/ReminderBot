import os
from datetime import time
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

TOKEN = os.getenv('BOT_TOKEN')

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    current_jobs = context.job_queue.get_jobs_by_name(f'remind_{chat_id}')
    for job in current_jobs:
        job.schedule_removal()
    
    context.job_queue.run_daily(
        send_reminder, time(7, 30), chat_id=chat_id, name=f'remind_{chat_id}'
    )
    await update.message.reply_text('✅ 7:30 ежедневно. Тест: /test')

async def test_reminder(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """СРАЗУ напоминание /test"""
    chat_id = update.effective_chat.id
    keyboard = [[InlineKeyboardButton("✅ Выпила таблеточку!", callback_data='done')]]
    markup = InlineKeyboardMarkup(keyboard)
    await context.bot.send_message(
        chat_id, "🧪 **ТЕСТ 7:30** 🧪\nКотенок, не забудь выпить таблеточку. 💊😘",
        reply_markup=markup, parse_mode='Markdown'
    )

async def send_reminder(context: ContextTypes.DEFAULT_TYPE):
    job = context.job
    chat_id = job.chat_id
    keyboard = [[InlineKeyboardButton("✅ Выпила таблеточку!", callback_data='done')]]
    markup = InlineKeyboardMarkup(keyboard)
    await context.bot.send_message(
        chat_id, "Котенок, не забудь выпить таблеточку. 💊😘", reply_markup=markup
    )

async def done(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer("Молодец, котёнок! 🥰")
    await query.edit_message_text("💕 Таблеточку выпила! До завтра 7:30.")

def main():
    if not TOKEN:
        print("❌ BOT_TOKEN!")
        return
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("test", test_reminder))
    app.add_handler(CallbackQueryHandler(done, pattern='^done$'))
    print("🐱 Бот готов! /start → /test")
    app.run_polling()

if __name__ == '__main__':
    main()
