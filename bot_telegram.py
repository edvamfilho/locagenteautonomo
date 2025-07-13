import os
import traceback
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from telegram import Update
from main import chat  # Importa sua função do agente
from dotenv import load_dotenv

load_dotenv()
TELEGRAM_TOKEN = os.getenv(
    "TELEGRAM_TOKEN") or "7062095518:AAGBZHkzGEG2zstqBavVAWTzOKIiydPccgs"


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Olá! Eu sou o *Lab Onchain*.\n"
        "Pergunte sobre cripto, Web3, NFTs, mercado, preços…\n"
        "Para ajuda: /ajuda",
        parse_mode="Markdown"
    )


async def responder(update: Update, context: ContextTypes.DEFAULT_TYPE):
    pergunta = update.message.text.strip()
    try:
        # Comando personalizado
        if pergunta.lower() in ["/ajuda", "/help"]:
            await update.message.reply_text(
                "🤖 *Como usar o Lab Onchain:*\n"
                "• Pergunte sobre cripto, Web3, NFTs, mercado.\n"
                "• Exemplo: _Qual o preço do BTC agora?_\n"
                "• Para saber mais: /sobre",
                parse_mode="Markdown"
            )
            return
        if pergunta.lower() == "/sobre":
            await update.message.reply_text(
                "🌐 *Lab Onchain* – Agente virtual educativo Web3.\n"
                "Desenvolvido por Edvam e comunidade. Versão Beta 2025 🚀",
                parse_mode="Markdown"
            )
            return
        if pergunta.lower() in ["/quemfez", "/autor", "/dev"]:
            await update.message.reply_text(
                "🤓 Feito por Edvam Filho.\nGitHub: https://github.com/edvamfilho"
            )
            return

        # Resposta padrão
        resposta = chat(pergunta)
        if not resposta or resposta.strip() == "":
            resposta = "😅 Ainda não sei responder isso, tente reformular ou peça /ajuda."

        # Adiciona emoji/contexto na resposta
        if any(p in pergunta.lower() for p in ["preço", "cotação", "quanto vale"]):
            resposta = f"💰 {resposta}"
        elif any(p in pergunta.lower() for p in ["o que é", "defina", "explique"]):
            resposta = f"📚 {resposta}"

        await update.message.reply_text(resposta, parse_mode="Markdown")
    except Exception as e:
        print("ERRO:", e, traceback.format_exc())
        await update.message.reply_text(
            "⚠️ Ops! Tivemos um erro ao buscar sua resposta. Tente de novo em instantes.\n"
            "Se persistir, talvez o saldo da API acabou ou a pergunta não foi reconhecida. Use /ajuda."
        )


def main():
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("ajuda", responder))
    app.add_handler(CommandHandler("sobre", responder))
    app.add_handler(CommandHandler("quemfez", responder))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, responder))
    print("Bot rodando! Pressione Ctrl+C para parar.")
    app.run_polling()


if __name__ == "__main__":
    main()
