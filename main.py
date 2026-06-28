import os
import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiohttp import web

TOKEN = os.getenv("BOT_TOKEN", "ТВОЙ_ТОКЕН_ИЗ_BOTFATHER")
ADMIN_ID = os.getenv("ADMIN_ID", "ТВОЙ_ТЕЛЕГРАМ_ID")

bot = Bot(token=TOKEN)
dp = Dispatcher()

# Микро веб-сервер для "успокоения" Render
async def handle_ping(request):
    return web.Response(text="Бот работает!")

def get_main_keyboard():
    buttons = [
        [KeyboardButton(text="ℹ️ О нас"), KeyboardButton(text="💰 Услуги и Цены")],
        [KeyboardButton(text="✍️ Оставить заявку / Связаться")]
    ]
    return ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)

@dp.message(F.text == "/start")
async def cmd_start(message: Message):
    welcome_text = (
        "👋 Здравствуйте!\n\n"
        "Приветствуем вас в нашем боте-ассистенте. "
        "Здесь вы можете узнать актуальные цены, информацию о нас и оставить заявку.\n\n"
        "👇 Выберите интересующий раздел меню ниже:"
    )
    await message.answer(welcome_text, reply_markup=get_main_keyboard())

@dp.message(F.text == "ℹ️ О нас")
async def about_us(message: Message):
    about_text = (
        "🏢 **О нашей компании:**\n\n"
        "Мы помогаем нашим клиентам получать лучший сервис быстро и удобно. "
        "📍 Наш адрес: ул. Примерная, д. 10\n"
        "📞 Телефон: +7 (999) 123-45-67"
    )
    await message.answer(about_text, parse_mode="Markdown")

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

@dp.message(F.text == "✍️ Оставить заявку / Связаться")
async def order_request(message: Message):
    await message.answer(
        "Напишите ваш вопрос или желаемую услугу/товар в ответном сообщении. "
        "Администратор свяжется с вами в ближайшее время!"
    )

@dp.message()
async def forward_to_admin(message: Message):
    if str(message.from_user.id) != str(ADMIN_ID):
        user_info = f"🔔 **Новая заявка!**\n\n👤 От: @{message.from_user.username or 'без_username'}\nID: {message.from_user.id}\n\n💬 Текст:"
        await bot.send_message(chat_id=ADMIN_ID, text=user_info, parse_mode="Markdown")
        await message.forward(chat_id=ADMIN_ID)
        await message.answer("✅ Ваша заявка принята! Администратор уже уведомлен и скоро вам напишет.")

async def main():
    # Запускаем веб-сервер на порту, который требует Render (обычно 10000)
    app = web.Application()
    app.router.add_get("/", handle_ping)
    
    port = int(os.getenv("PORT", 10000))
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", port)
    
    # Запускаем веб-сервер в фоне
    asyncio.create_task(site.start())
    
    print("Бот и веб-сервер успешно запущены!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
