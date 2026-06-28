import os
import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton

# Токен берется из переменных окружения сервера (для безопасности на Render)
# Для теста на ПК можешь временно заменить os.getenv(...) на 'ТВОЙ_ТОКЕН_ИЗ_BOTFATHER'
TOKEN = os.getenv("BOT_TOKEN", "ТВОЙ_ТОКЕН_ИЗ_BOTFATHER")
# ID твоего Telegram-аккаунта, куда бот будет пересылать заявки от клиентов
ADMIN_ID = os.getenv("ADMIN_ID", "ТВОЙ_ТЕЛЕГРАМ_ID")

bot = Bot(token=TOKEN)
dp = Dispatcher()

# Главное меню (кнопки внизу экрана)
def get_main_keyboard():
    buttons = [
        [KeyboardButton(text="ℹ️ О нас"), KeyboardButton(text="💰 Услуги и Цены")],
        [KeyboardButton(text="✍️ Оставить заявку / Связаться")]
    ]
    return ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)

# Команда /start
@dp.message(F.text == "/start")
async def cmd_start(message: Message):
    welcome_text = (
        "👋 Здравствуйте!\n\n"
        "Приветствуем вас в нашем боте-ассистенте. "
        "Здесь вы можете узнать актуальные цены, информацию о нас и оставить заявку.\n\n"
        "👇 Выберите интересующий раздел меню ниже:"
    )
    await message.answer(welcome_text, reply_markup=get_main_keyboard())

# Раздел "О нас"
@dp.message(F.text == "ℹ️ О нас")
async def about_us(message: Message):
    about_text = (
        "🏢 **О нашей компании:**\n\n"
        "Мы помогаем нашим клиентам получать лучший сервис быстро и удобно. "
        "Работаем ежедневно, индивидуальный подход к каждому!\n\n"
        "📍 Наш адрес: ул. Примерная, д. 10\n"
        "📞 Телефон: +7 (999) 123-45-67"
    )
    await message.answer(about_text, parse_mode="Markdown")

# Раздел "Услуги и Цены"
@dp.message(F.text == "💰 Услуги и Цены")
async def services_and_prices(message: Message):
    prices_text = (
        "📋 **Наш прайс-лист:**\n\n"
        "🔹 Вариант 1 — 1 500 руб.\n"
        "🔹 Вариант 2 — 3 000 руб.\n"
        "🔹 Вариант 3 — 5 500 руб.\n\n"
        " Нажмите кнопку ниже, чтобы забронировать или задать вопрос!"
    )
    await message.answer(prices_text, parse_mode="Markdown")

# Раздел "Оставить заявку"
@dp.message(F.text == "✍️ Оставить заявку / Связаться")
async def Order_request(message: Message):
    await message.answer(
        "Напишите ваш вопрос или желаемую услугу/товар в ответном сообщении. "
        "Администратор свяжется с вами в ближайшее время!"
    )

# Пересылка любого другого сообщения админу (сбор заявок)
@dp.message()
async def forward_to_admin(message: Message):
    # Если пишет обычный пользователь, пересылаем админу
    if str(message.from_user.id) != str(ADMIN_ID):
        user_info = f"🔔 **Новая заявка!**\n\n👤 От: @{message.from_user.username or 'без_username'}\nID: {message.from_user.id}\n\n💬 Текст:"
        
        # Уведомляем админа
        await bot.send_message(chat_id=ADMIN_ID, text=user_info, parse_mode="Markdown")
        # Пересылаем само сообщение (чтобы админ мог ответить пользователю)
        await message.forward(chat_id=ADMIN_ID)
        
        # Отвечаем пользователю
        await message.answer("✅ Ваша заявка принята! Администратор уже уведомлен и скоро вам напишет.")

async def main():
    print("Бот успешно запущен!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
