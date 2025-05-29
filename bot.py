import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import requests
import logging
import os # Ancora utile per la variabile PORT fornita da Render
from flask import Flask, request
import sys

# --- Configurazione Logging (in cima) ---
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# --- Costanti e Token ---
TELEGRAM_BOT_TOKEN = "7883497770:AAFRVc8DKBofRkdy6m0EGdpkaoOJz10Qw8E" # Hardcoded come richiesto
JOKE_API_URL = "https://official-joke-api.appspot.com/random_joke"
RENDER_APP_URL_BASE = "https://jokebot-47zu.onrender.com" # Il tuo URL base di Render

# --- Inizializzazione Flask App ---
app = Flask(__name__)

# --- Inizializzazione Bot e Dispatcher (globali per essere usati da Flask e funzioni di setup) ---
bot_instance = telegram.Bot(token=TELEGRAM_BOT_TOKEN)
# user_sig_handler=None è buona pratica con webhook per evitare che la libreria gestisca i segnali di terminazione
# che dovrebbero essere gestiti da Gunicorn/Render.
updater = Updater(bot=bot_instance, use_context=True, user_sig_handler=None)
dp = updater.dispatcher

# --- Funzioni Handler del Bot ---
def start_command_handler(update, context):
    user = update.effective_user
    update.message.reply_html(
        f"Ciao {user.mention_html()}! Sono il tuo bot delle barzellette (v2: webhook).\n"
        f"Usa il comando /barzelletta per ricevere una barzelletta!"
    )

def get_joke_from_api():
    try:
        response = requests.get(JOKE_API_URL)
        response.raise_for_status()
        joke_data = response.json()
        if 'setup' in joke_data and 'punchline' in joke_data:
            return f"{joke_data['setup']}\n\n...\n\n{joke_data['punchline']}"
        else:
            logger.error(f"Formato API inaspettato: {joke_data}")
            return "Spiacente, la barzelletta ricevuta non era nel formato corretto."
    except requests.exceptions.RequestException as e:
        logger.error(f"Errore nel recuperare la barzelletta dall'API: {e}")
        return "Spiacente, non sono riuscito a trovare una barzelletta al momento. Riprova più tardi!"
    except (KeyError, TypeError, ValueError) as e:
        logger.error(f"Errore nel formato della risposta dell'API o nel parsing JSON: {e}")
        return "Spiacente, c'è stato un problema con il formato della barzelletta. Riprova più tardi!"

def barzelletta_command_handler(update, context):
    joke_text = get_joke_from_api()
    update.message.reply_text(joke_text)

def unknown_command_handler(update, context):
    update.message.reply_text("Spiacente, non ho capito quel comando. Prova con /barzelletta!")

def telegram_error_handler(update, context):
    try:
        update_representation = str(update) if update else "Nessun update"
        error_representation = str(context.error) if context and context.error else "Nessun errore specifico"
        if update and hasattr(update, 'update_id'):
            update_representation = f"Update (ID: {update.update_id})"
        logger.warning(f"L'update (Telegram) \"{update_representation}\" ha causato l'errore \"{error_representation}\"")
    except Exception as log_formatting_error:
        logger.error(f"Errore critico durante la formattazione del messaggio di log per un errore Telegram: {log_formatting_error}")
        if context and context.error:
            logger.error(f"Errore Telegram originale non formattato: {context.error}")
        else:
            logger.error("Errore Telegram originale non disponibile o non formattabile.")

# --- Registrazione Handlers nel Dispatcher ---
dp.add_handler(CommandHandler("start", start_command_handler))
dp.add_handler(CommandHandler("barzelletta", barzelletta_command_handler))
dp.add_handler(CommandHandler("joke", barzelletta_command_handler)) # Alias
dp.add_handler(MessageHandler(Filters.command & (~Filters.update.edited_message), unknown_command_handler))
dp.add_error_handler(telegram_error_handler)

# --- Rotta Webhook per Flask ---
# Telegram invierà aggiornamenti a https://TUO_URL_RENDER/TUO_TOKEN_BOT
@app.route(f"/{TELEGRAM_BOT_TOKEN}", methods=['POST'])
def webhook_telegram_route():
    if request.is_json:
        json_data = request.get_json(force=True)
        update = telegram.Update.de_json(json_data, bot_instance)
        dp.process_update(update)
        return 'ok', 200
    else:
        logger.warning("Richiesta al webhook non JSON ricevuta")
        return 'Bad Request', 400

# --- Funzione per impostare il Webhook con Telegram (da chiamare una volta) ---
def set_actual_telegram_webhook(service_base_url_https):
    webhook_full_url = f"{service_base_url_https.rstrip('/')}/{TELEGRAM_BOT_TOKEN}"
    
    logger.info(f"Tentativo di impostare il webhook a: {webhook_full_url}")
    if bot_instance.set_webhook(url=webhook_full_url):
        logger.info(f"Webhook IMPOSTATO con successo a: {webhook_full_url}")
        webhook_info = bot_instance.get_webhook_info()
        logger.info(f"Info Webhook corrente: {webhook_info}")
        print(f"Webhook IMPOSTATO con successo a: {webhook_full_url}")
        print(f"Info Webhook corrente: {webhook_info}")
    else:
        logger.error(f"IMPOSTAZIONE Webhook FALLITA per URL: {webhook_full_url}")
        webhook_info = bot_instance.get_webhook_info()
        logger.info(f"Info Webhook corrente (dopo fallimento): {webhook_info}")
        print(f"IMPOSTAZIONE Webhook FALLITA per URL: {webhook_full_url}")
        print(f"Info Webhook corrente (dopo fallimento): {webhook_info}")

# --- Blocco Main per Utilità (Impostare/Cancellare Webhook) ---
# Gunicorn non eseguirà questo blocco __main__. Lo userà per trovare l'oggetto 'app' di Flask.
# Puoi eseguire questo script localmente (o nel Codespace) per gestire il webhook.
if __name__ == '__main__':
    valid_actions = ["setwebhook", "deletewebhook", "infowebhook"]
    
    # Controlla se lo script viene eseguito da Gunicorn (variabile d'ambiente tipica)
    # Se sì, non fare nulla qui, Gunicorn gestirà l'avvio dell'app Flask.
    if 'gunicorn' in os.environ.get('SERVER_SOFTWARE', ''):
        logger.info("Avviato da Gunicorn, nessuna azione da __main__.")
    elif len(sys.argv) > 1 and sys.argv[1] in valid_actions:
        action = sys.argv[1]
        
        if action == "setwebhook":
            # Usa l'URL di Render definito sopra
            if RENDER_APP_URL_BASE:
                if not RENDER_APP_URL_BASE.startswith("https://"):
                    print(f"ERRORE: L'URL di Render ({RENDER_APP_URL_BASE}) deve iniziare con https://")
                else:
                    set_actual_telegram_webhook(RENDER_APP_URL_BASE)
            else:
                print("ERRORE: RENDER_APP_URL_BASE non è definito nello script.")
                print("Se stai eseguendo questo comando manualmente e l'URL è diverso, passalo come argomento:")
                print(f"  python {sys.argv[0]} setwebhook https://ALTRO_TUO_URL_RENDER")

            # Permetti override da riga di comando se fornito
            if len(sys.argv) > 2 and sys.argv[2].startswith("https://"):
                 print(f"\nNOTA: L'URL di Render è stato fornito anche come argomento: {sys.argv[2]}.")
                 print("Se questo è l'URL corretto che vuoi usare, assicurati che RENDER_APP_URL_BASE nello script sia aggiornato,")
                 print("o riesegui il comando specificando l'URL corretto se diverso da quello hardcodato.")
                 print("Per ora, è stato usato l'URL hardcodato nello script se non hai modificato il codice per usare sys.argv[2].")


        elif action == "deletewebhook":
            if bot_instance.delete_webhook():
                logger.info("Webhook ELIMINATO con successo.")
                print("Webhook ELIMINATO con successo.")
            else:
                logger.error("Eliminazione webhook FALLITA.")
                print("Eliminazione webhook FALLITA.")
        
        elif action == "infowebhook":
            webhook_info = bot_instance.get_webhook_info()
            logger.info(f"Info Webhook corrente: {webhook_info}")
            print(f"Info Webhook corrente: {webhook_info}")

    else:
        print("Questo script è inteso per essere eseguito con Gunicorn su Render (per il bot operativo).")
        print("Per gestire il webhook manualmente, usa uno dei seguenti comandi:")
        print(f"  python {sys.argv[0]} setwebhook   (userà l'URL: {RENDER_APP_URL_BASE} hardcodato nello script)")
        print(f"  python {sys.argv[0]} deletewebhook")
        print(f"  python {sys.argv[0]} infowebhook")
        # Per testare Flask localmente (i webhook Telegram non funzioneranno senza HTTPS/tunneling come ngrok):
        # local_port = int(os.environ.get('PORT', 8080)) # Porta per test locali
        # logger.info(f"Avvio server Flask di sviluppo (solo per test locali) su http://0.0.0.0:{local_port}")
        # app.run(host='0.0.0.0', port=local_port, debug=True)