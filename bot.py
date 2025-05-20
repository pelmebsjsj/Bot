 import os
from io import BytesIO
from PIL import Image
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

TOKEN = os.environ["7793261549:AAFxPRinGqH1I4juS2yosDNnKX9dUlXfMJQ"]  # Токен брать из переменных окружения!

OVERLAY_PATH = "overlay.png"  # Имя файла с оверлеем

async def add_overlay(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.photo:
        await update.message.reply_text("Пожалуйста, пришлите фото.")
        return

    # Получаем фото наибольшего размера
    photo = update.message.photo[-1]
    file = await context.bot.get_file(photo.file_id)
    img_bytes = BytesIO()
    await file.download_to_memory(out=img_bytes)
    img_bytes.seek(0)

    user_img = Image.open(img_bytes).convert("RGBA")
    overlay = Image.open(OVERLAY_PATH).convert("RGBA")
    overlay = overlay.resize(user_img.size)

    result = Image.alpha_composite(user_img, overlay)
    output = BytesIO()
    result.save(output, format="PNG")
    output.seek(0)

    await update.message.reply_photo(photo=output, caption="Готово!")

if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(MessageHandler(filters.PHOTO, add_overlay))
    print("Бот запущен.")
    app.run_polling()
