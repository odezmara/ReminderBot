import logging
import os
from datetime import time
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

TOKEN = os.getenv('7978063185:AAFx7VaplhOIONGM_P_M3-lZfaZNADf3q5w')

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton("✅ Настроить напоминание о таблетках", callback_data='set_reminder')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        '👋 Привет! Я бот-напоминалка о таблетках.\n'
        'Нажми кнопку ниже, чтобы настроить ежедневное напоминание в 10:00.',
        reply_markup=reply_markup
    )

async def set_reminder(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    chat_id = query.message.chat_id

    current_jobs = context.job_queue.get_jobs_by_name(f'reminder_{chat_id}')
    for job in current_jobs:
        job.schedule_removal()

    context.job_queue.run_daily(
        reminder_callback,
        time(10, 0),
        chat_id=chat_id,
        name=f'reminder_{chat_id}',
        data={'user_id': chat_id}
    )

    await query.edit_message_text(
        '✅ Напоминание настроено!\n'
        '💊 Каждый день в 10:00 бот пришлёт уведомление "Выпей таблетки!"\n'
        'с кнопкой подтверждения.\n\n'
        'Для отмены: /stop',
        parse_mode='Markdown'
    )

async def reminder_callback(context: ContextTypes.DEFAULT_TYPE):
    job = context.job
    chat_id = job.chat_id

    keyboard = [[InlineKeyboardButton("✅ Выпил(а) таблетки!", callback_data='done')]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await context.bot.send_message(
        chat_id=chat_id,
        text='⏰ *Напоминание: время пить таблетки!* 💊\n\n'
             'Не забудьте принять лекарство! 👇',
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )

async def done(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer('Отлично! Запись сохранена ✅')

    await query.edit_message_text(
        '🎉 *Отлично! Таблетки приняты!*\n\n'
        'До завтра в 10:00! 😊\n'
        '_Если нужно изменить время — /start_',
        parse_mode='Markdown'
    )

async def stop(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    current_jobs = context.job_queue.get_jobs_by_name(f'reminder_{chat_id}')
    for job in current_jobs:
        job.schedule_removal()

    await update.message.reply_text('🛑 Напоминания отменены!')

def main():
    if not TOKEN:
        print("❌ Переменная BOT_TOKEN не задана!")
        return

    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("stop", stop))
    application.add_handler(CallbackQueryHandler(set_reminder, pattern='^set_reminder$'))
    application.add_handler(CallbackQueryHandler(done, pattern='^done$'))

    print("🚀 Бот запущен на Bothost!")
    application.run_polling()

if __name__ == '__main__':
    main()
