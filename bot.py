import os
from datetime import time
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

TOKEN = "7978063185:AAFx7VaplhOIONGM_P_M3-lZfaZNADf3q5w"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Включает напоминание на 7:30"""
    chat_id = update.message.chat_id
    
    # Удаляем старые напоминания
    current_jobs = context.job_queue.get_jobs_by_name(f'remind_{chat_id}')
    for job in current_jobs:
        job.schedule_removal()
    
    # Новое напоминание каждый день в 7:30
    context.job_queue.run_daily(
        send_reminder,
        time(7, 30),  # 7:30 утра
        chat_id=chat_id,
        name=f'remind_{chat_id}'
    )
    
    await update.message.reply_text('✅ Напоминание включено! Каждый день в **7:30** будет приходить сообщение о таблетках.')

async def send_reminder(context: ContextTypes.DEFAULT_TYPE):
    """Ежедневное напоминание"""
    job = context.job
    chat_id = job.chat_id
    
    keyboard = [[InlineKeyboardButton("✅ Выпила таблеточку!", callback_data='done')]]
    markup = InlineKeyboardMarkup(keyboard)
    
    await context.bot.send_message(
        chat_id,
        "Котенок, не забудь выпить таблеточку. 💊😘",
        reply_markup=markup
    )

async def done(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Кнопка выполнено"""
    query = update.callback_query
    await query.answer("Молодец, котёнок! 🥰")
    await query.edit_message_text("💕 Таблеточку выпила! До завтра 7:30.")

def main():
    if not TOKEN:
        print("❌ Установи BOT_TOKEN в Bothost!")
        return
    
    app = Application.builder().token(TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(done, pattern='^done$'))
    
    print("🐱 Бот-котёнок запущен! 7:30 ежедневно.")
    app.run_polling()

if __name__ == '__main__':
    main()
