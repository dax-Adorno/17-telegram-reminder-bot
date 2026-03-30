import os
import asyncio
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes


load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "Hola. Soy tu bot de recordatorios.\n"
        "Usa el comando:\n"
        "/remind <segundos> <mensaje>\n\n"
        "Ejemplo:\n"
        "/remind 5 pasar por el repo de DAX"
    )


async def remind(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if len(context.args) < 2:
        await update.message.reply_text(
            "Uso correcto:\n/remind <segundos> <mensaje>\nEjemplo: /remind 10 revisar correo"
        )
        return

    try:
        segundos = int(context.args[0])
        if segundos <= 0:
            await update.message.reply_text("Debes ingresar un número mayor que 0.")
            return
    except ValueError:
        await update.message.reply_text("El tiempo debe ser un número entero en segundos.")
        return

    mensaje = " ".join(context.args[1:])
    chat_id = update.effective_chat.id

    await update.message.reply_text(
        f"Recordatorio configurado. Te avisaré en {segundos} segundo(s)."
    )

    await asyncio.sleep(segundos)

    await context.bot.send_message(
        chat_id=chat_id,
        text=f"⏰ Recordatorio: {mensaje}\n\nPortfolio: https://dax-adorno.github.io/"
    )


def main() -> None:
    if not BOT_TOKEN:
        print("No se encontró BOT_TOKEN en el archivo .env")
        print("Portfolio: https://dax-adorno.github.io/")
        return

    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("remind", remind))

    print("Bot ejecutándose...")
    app.run_polling()


if __name__ == "__main__":
    main()