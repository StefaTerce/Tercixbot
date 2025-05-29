import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import requests
import os
import logging

# Configura il logging per vedere eventuali errori
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# --- IMPORTANTE ---
# È ALTAMENTE SCONSIGLIATO inserire il token direttamente nel codice.
# Per il deployment, usa una variabile d'ambiente.
# Per ora, uso il token che hai fornito.
TELEGRAM_BOT_TOKEN = "7883497770:AAFRVc8DKBofRkdy6m0EGdpkaoOJz10Qw8E"
# Per il deployment su Render, imposterai questa variabile d'ambiente lì.
# Esempio se usassi una variabile d'ambiente:
# TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
# if not TELEGRAM_BOT_TOKEN:
#     logger.error("TELEGRAM_BOT_TOKEN non trovato! Assicurati di averlo impostato.")
#     exit()

# URL dell'API per le barzellette
JOKE_API_URL = "https://official-joke-api.appspot.com/random_joke"

def start(update, context):
    """Invia un messaggio quando viene eseguito il comando /start."""
    user = update.effective_user
    update.message.reply_html(
        f"Ciao {user.mention_html()}! Sono il tuo bot delle barzellette.\n"
        f"Usa il comando /barzelletta per ricevere una barzelletta!"
    )

def get_joke():
    """Recupera una barzelletta dall'API."""
    try:
        response = requests.get(JOKE_API_URL)
        response.raise_for_status()  # Solleva un errore per risposte HTTP non riuscite (4xx o 5xx)
        joke_data = response.json()
        return f"{joke_data['setup']}\n\n...\n\n{joke_data['punchline']}"
    except requests.exceptions.RequestException as e:
        logger.error(f"Errore nel recuperare la barzelletta dall'API: {e}")
        return "Spiacente, non sono riuscito a trovare una barzelletta al momento. Riprova più tardi!"
    except (KeyError, TypeError) as e:
        logger.error(f"Errore nel formato della risposta dell'API: {e}")
        return "Spiacente, c'è stato un problema con il formato della barzelletta. Riprova più tardi!"


def barzelletta(update, context):
    """Invia una barzelletta all'utente."""
    joke_text = get_joke()
    update.message.reply_text(joke_text)

def unknown(update, context):
    """Risponde a comandi non riconosciuti."""
    update.message.reply_text("Spiacente, non ho capito quel comando. Prova con /barzelletta!")

def error_handler(update, context):
    """Logga gli Errori causati dagli Updates."""
    logger.warning('Update "%s" ha causato l'errore "%s"', update, context.error)

def main():
    """Avvia il bot."""
    if not TELEGRAM_BOT_TOKEN:
        logger.error("TELEGRAM_BOT_TOKEN non è impostato!")
        return

    # Crea l'Updater e passagli il token del tuo bot.
    updater = Updater(TELEGRAM_BOT_TOKEN, use_context=True)

    # Ottieni il dispatcher per registrare gli handler
    dp = updater.dispatcher

    # Comandi
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("barzelletta", barzelletta))
    dp.add_handler(CommandHandler("joke", barzelletta)) # Alias per /barzelletta

    # Messaggi non riconosciuti
    dp.add_handler(MessageHandler(Filters.command, unknown))

    # Logga tutti gli errori
    dp.add_error_handler(error_handler)

    # Avvia il Bot
    updater.start_polling()
    logger.info("Bot avviato e in ascolto...")

    # Mantieni il bot in esecuzione finché non lo interrompi (Ctrl-C)
    updater.idle()

if __name__ == '__main__':
    main()