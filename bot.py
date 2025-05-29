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
# Per il deployment, usa una variabile d'ambiente.
# Il token che avevi fornito era: "7883497770:AAFRVc8DKBofRkdy6m0EGdpkaoOJz10Qw8E"
# Assicurati che TELEGRAM_BOT_TOKEN sia impostato come variabile d'ambiente su Render.
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")

if not TELEGRAM_BOT_TOKEN:
    logger.error("TELEGRAM_BOT_TOKEN non trovato! Assicurati di averlo impostato come variabile d'ambiente.")
    # In un ambiente di produzione, potresti voler far uscire il programma se il token non è presente.
    # exit(1) # Scommenta se vuoi che il bot si fermi se il token non è trovato.
    # Per ora, lo lascio continuare ma stamperà l'errore.

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
    # Linea originale che causava SyntaxError su Render:
    # logger.warning('Update "%s" ha causato l'errore "%s"', update, context.error)
    
    # Linea corretta usando f-string per maggiore compatibilità e chiarezza:
    try:
        update_representation = str(update) if update else "Nessun update"
        error_representation = str(context.error) if context and context.error else "Nessun errore specifico"
        
        # Se possibile, rendi la rappresentazione dell'update più concisa
        if update and hasattr(update, 'update_id'):
            update_representation = f"Update (ID: {update.update_id})"

        logger.warning(f"L'update \"{update_representation}\" ha causato l'errore \"{error_representation}\"")
    except Exception as log_formatting_error:
        # Fallback nel caso la formattazione stessa dell'errore causi un problema
        logger.error(f"Errore critico durante la formattazione del messaggio di log per un errore precedente: {log_formatting_error}")
        # Logga l'errore originale in modo grezzo se possibile
        if context and context.error:
            logger.error(f"Errore originale non formattato: {context.error}")
        else:
            logger.error("Errore originale non disponibile o non formattabile.")


def main():
    """Avvia il bot."""
    if not TELEGRAM_BOT_TOKEN:
        logger.critical("TOKEN DEL BOT NON IMPOSTATO. Il bot non può avviarsi.")
        return # Esce dalla funzione main se il token non è disponibile.

    # Crea l'Updater e passagli il token del tuo bot.
    updater = Updater(TELEGRAM_BOT_TOKEN, use_context=True)

    # Ottieni il dispatcher per registrare gli handler
    dp = updater.dispatcher

    # Comandi
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("barzelletta", barzelletta))
    dp.add_handler(CommandHandler("joke", barzelletta)) # Alias per /barzelletta

    # Messaggi non riconosciuti (assicurati che questo sia dopo i CommandHandler)
    dp.add_handler(MessageHandler(Filters.command & (~Filters.update.edited_message), unknown))

    # Logga tutti gli errori
    dp.add_error_handler(error_handler)

    # Avvia il Bot
    logger.info("Avvio del bot in modalità polling...")
    updater.start_polling()
    logger.info("Bot avviato e in ascolto.")

    # Mantieni il bot in esecuzione finché non lo interrompi (Ctrl-C)
    updater.idle()

if __name__ == '__main__':
    main()