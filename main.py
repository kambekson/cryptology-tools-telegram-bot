import asyncio
from aiogram import Bot, Dispatcher
from config import API_TOKEN, API_SERVER

# Initialize bot with base URL to handle potential DNS issues
bot = Bot(token=API_TOKEN, base_url=API_SERVER)
dp = Dispatcher()

# Import handlers after bot initialization to avoid circular imports
from handlers import register_all_handlers

# Регистрация всех обработчиков
dp = register_all_handlers(dp)

# Запуск бота
async def main():
    print("Bot is running...")
    print("Connecting to Telegram servers...")
    try:
        # Удаляем webhook перед использованием polling
        await bot.delete_webhook(drop_pending_updates=True)
        print("Webhook deleted successfully")
        await dp.start_polling(bot)
    except Exception as e:
        print(f"Error starting bot: {e}")
        print("If you're experiencing network issues, consider:")
        print("1. Check your internet connection")
        print("2. Verify your firewall settings")
        print("3. Try using a VPN or proxy")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Bot stopped by user.")
