# Bot Telegram Barzellette (Jokebot) - Versione Webhook

Questo è un semplice bot Telegram che racconta barzellette recuperandole da un'API esterna ([Official Joke API](https://official-joke-api.appspot.com/)).
Questa versione è configurata per utilizzare **webhook** con Telegram e per essere deployata su piattaforme come Render.

**ATTENZIONE:** Il token del bot Telegram è attualmente inserito direttamente nel file `bot.py`. Questa pratica non è sicura per repository pubblici o per ambienti di produzione. Si consiglia vivamente di utilizzare variabili d'ambiente per gestire i token in scenari reali.

L'URL del servizio Render per questo bot è (esempio): `https://jokebot-47zu.onrender.com`

## Prerequisiti

*   Python 3.9+
*   Docker (per il build dell'immagine)
*   Un account Telegram e un token per il bot (ottenibile da @BotFather su Telegram)

## Configurazione (Token e URL di Render)

*   **Token Telegram:** Hardcodato nel file `bot.py` come `TELEGRAM_BOT_TOKEN`.
*   **URL Base di Render:** Hardcodato nel file `bot.py` come `RENDER_APP_URL_BASE`. Assicurati che corrisponda all'URL effettivo del tuo servizio su Render (es. `https://jokebot-47zu.onrender.com`).

## Flusso di Deployment e Configurazione Webhook

1.  **Aggiorna i file sorgente** (`bot.py`, `Dockerfile`, `requirements.txt`, `README.md`) nel tuo repository GitHub.
2.  **Commit e Push** delle modifiche su GitHub.
3.  **Render rileverà le modifiche** e avvierà un nuovo build e deploy del servizio. Assicurati che il servizio su Render sia configurato come "Web Service".
4.  **Attendi il completamento del deploy su Render.** L'applicazione Flask (servita da Gunicorn) sarà in ascolto sull'URL fornito da Render (es. `https://jokebot-47zu.onrender.com`).
5.  **Imposta il Webhook con Telegram (una tantum):**
    *   Dopo che il deploy su Render è attivo e funzionante, apri un terminale nel tuo ambiente di sviluppo (es. GitHub Codespace o il tuo PC locale, con l'ultima versione di `bot.py`).
    *   Esegui il comando:
        ```bash
        python bot.py setwebhook
        ```
    *   Questo comando utilizzerà la variabile `RENDER_APP_URL_BASE` definita in `bot.py` per costruire l'URL completo del webhook (es. `https://jokebot-47zu.onrender.com/TUO_TOKEN_BOT`) e lo registrerà con Telegram.
    *   Controlla l'output per messaggi di successo o errore.

## Gestione del Webhook (Comandi da Terminale)

Puoi gestire il webhook eseguendo `bot.py` localmente con i seguenti argomenti:

*   **Impostare il webhook:**
    ```bash
    python bot.py setwebhook
    ```
    (Usa l'URL `RENDER_APP_URL_BASE` hardcodato in `bot.py`)

*   **Ottenere informazioni sul webhook corrente:**
    ```bash
    python bot.py infowebhook
    ```

*   **Eliminare il webhook:**
    ```bash
    python bot.py deletewebhook
    ```
    (Se elimini il webhook, il bot smetterà di ricevere aggiornamenti tramite webhook. Dovresti ripristinare il polling o reimpostare il webhook).

## Creazione dell'Immagine Docker e Push su Docker Hub (Opzionale se Render builda da GitHub)

Se Render builda direttamente dal tuo repository GitHub (opzione consigliata), non hai bisogno di fare build e push manuali su Docker Hub. Se invece il tuo servizio Render è configurato per usare un'immagine da un registry Docker:

1.  **Build dell'immagine Docker:**
    (Sostituisci `terceros` con il tuo username Docker Hub e `jokebot` con il nome della tua immagine)
    ```bash
    docker build -t terceros/jokebot:latest .
    ```

2.  **Login su Docker Hub:**
    ```bash
    docker login -u terceros
    ```

3.  **Push dell'immagine su Docker Hub:**
    ```bash
    docker push terceros/jokebot:latest
    ```

## Comandi del Bot

*   `/start` - Messaggio di benvenuto.
*   `/barzelletta` (o `/joke`) - Invia una barzelletta casuale.

## Struttura dei File

```
.
├── bot.py            # Logica principale del bot Telegram (Flask, webhook, token hardcodato)
├── Dockerfile        # Istruzioni per costruire l'immagine Docker (con Gunicorn)
├── requirements.txt  # Dipendenze Python (Flask, Gunicorn, etc.)
└── README.md         # Questo file
```