

import os
import asyncio
import logging

from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from TikTokLive import TikTokLiveClient
from TikTokLive.events import ConnectEvent

TOKEN = os.environ["BOT_TOKEN"]
GROUP_ID = -5461828369
TIKTOK_USER = "@santobelen_"

logging.basicConfig(level=logging.INFO)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "❤️ ¡Bienvenida a Alerta LIVE Belu!\n"
        "Estamos preparando las alertas. 🔔"
    )

async def ayuda(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Alerta LIVE Belu 🔔")

async def id_grupo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        f"ID de este grupo: {update.effective_chat.id}"
    )

async def vigilar_directo(app):
    client = TikTokLiveClient(unique_id=TIKTOK_USER)

    @client.on(ConnectEvent)
    async def al_conectar(event: ConnectEvent):
        await app.bot.send_message(
            chat_id=GROUP_ID,
            text=(
                "🔴❤️ ¡BELÉN ESTÁ EN DIRECTO!\n\n"
                "Entra aquí para verla:\n"
                "https://www.tiktok.com/@santobelen_/live"
            )
        )

    while True:
        try:
            if await client.is_live():
                await client.connect()

            await asyncio.sleep(60)

        except Exception:
            logging.exception("Error comprobando el directo")
            await asyncio.sleep(60)

async def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("ayuda", ayuda))
    app.add_handler(CommandHandler("id", id_grupo))

    await app.initialize()
    await app.start()
    await app.updater.start_polling()

    asyncio.create_task(vigilar_directo(app))

    logging.info("Alerta LIVE Belu está funcionando")
    await asyncio.Event().wait()

if __name__ == "__main__":
    asyncio.run(main())
