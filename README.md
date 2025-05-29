# Bot Telegram Barzellette

Questo è un semplice bot Telegram che racconta barzellette recuperandole da un'API esterna ([Official Joke API](https://official-joke-api.appspot.com/)).

## Prerequisiti

*   Python 3.7+
*   Docker (per il build dell'immagine)
*   Un account Telegram e un token per il bot (ottenibile da @BotFather su Telegram)

## Configurazione

### Token del Bot

Il bot necessita di un token per autenticarsi con l'API di Telegram.

**Per lo sviluppo locale:**
Puoi modificare temporaneamente il file `bot.py` e inserire il token nella variabile `TELEGRAM_BOT_TOKEN`.

**Per il deployment (Docker & Render - CONSIGLIATO):**
NON inserire il token direttamente nel codice o nel Dockerfile. Invece, imposta una variabile d'ambiente chiamata `TELEGRAM_BOT_TOKEN` sulla tua piattaforma di hosting (es. Render).

Il file `bot.py` è già predisposto per leggere questa variabile d'ambiente se la riga `TELEGRAM_BOT_TOKEN = "IL_TUO_TOKEN_FORNITO"` viene commentata e le righe per `os.environ.get` vengono decommentate.

## Esecuzione Locale (Senza Docker)

1.  **Clona il repository (o crea i file):**
    ```bash
    # Se hai clonato un repo
    # git clone <url_del_tuo_repo>
    # cd <nome_del_repo>
    ```
    Assicurati di avere `bot.py` e `requirements.txt` nella stessa directory.

2.  **Crea un ambiente virtuale (consigliato):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # Su Windows: venv\Scripts\activate
    ```

3.  **Installa le dipendenze:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Imposta il token del bot (se non l'hai hardcodato per il test):**
    ```bash
    export TELEGRAM_BOT_TOKEN="IL_TUO_TOKEN_QUI" # Su Linux/macOS
    # set TELEGRAM_BOT_TOKEN="IL_TUO_TOKEN_QUI" # Su Windows (prompt dei comandi)
    # $env:TELEGRAM_BOT_TOKEN="IL_TUO_TOKEN_QUI" # Su Windows (PowerShell)
    ```

5.  **Avvia il bot:**
    ```bash
    python bot.py
    ```

## Creazione dell'Immagine Docker e Push su Docker Hub

1.  **Assicurati che Docker sia in esecuzione.**

2.  **Naviga nella directory del progetto** (dove si trovano `Dockerfile`, `bot.py`, `requirements.txt`).

3.  **Build dell'immagine Docker:**
    Sostituisci `tuoutentedockerhub` con il tuo username di Docker Hub e `nomeimmaginebot` con un nome per la tua immagine (es. `telegram-joke-bot`).
    ```bash
    docker build -t tuoutentedockerhub/nomeimmaginebot:latest .
    ```
    Ad esempio:
    ```bash
    docker build -t stefaterce/telegram-joke-bot:latest .
    ```

4.  **Login su Docker Hub (se non l'hai già fatto):**
    ```bash
    docker login
    ```
    Ti verranno chiesti username e password.

5.  **Push dell'immagine su Docker Hub:**
    ```bash
    docker push tuoutentedockerhub/nomeimmaginebot:latest
    ```
    Ad esempio:
    ```bash
    docker push stefaterce/telegram-joke-bot:latest
    ```

## Deployment su Render

Render può deployare direttamente da un'immagine Docker ospitata su Docker Hub.

1.  **Crea un account su [Render](https://render.com/) se non ne hai uno.**

2.  **Nel dashboard di Render, clicca su "New +" e seleziona "Web Service".**

3.  **Scegli "Deploy an existing image from a registry".**
    *   **Image Path:** Inserisci il percorso della tua immagine su Docker Hub (es. `tuoutentedockerhub/nomeimmaginebot:latest` o `stefaterce/telegram-joke-bot:latest`).

4.  **Dai un nome al tuo servizio** (es. `telegram-joke-bot`).

5.  **Variabili d'Ambiente:**
    *   Vai alla sezione "Environment".
    *   Clicca su "Add Environment Variable".
    *   **Key:** `TELEGRAM_BOT_TOKEN`
    *   **Value:** Incolla il token del tuo bot Telegram.

6.  **Instance Type:** Per un bot semplice come questo, il piano gratuito ("Free") dovrebbe essere sufficiente.

7.  **Impostazioni Avanzate (Opzionale ma utile):**
    *   **Health Check Path:** Render potrebbe provare a fare richieste HTTP al tuo servizio. Poiché questo è un bot e non un server web tradizionale, potresti non avere un endpoint HTTP. Se Render richiede un Health Check Path e il deploy fallisce, potresti dover configurare un semplice endpoint HTTP nel bot o vedere se Render permette di disabilitare/configurare diversamente l'health check per i "Background Worker" o servizi non HTTP. Per ora, prova a lasciare vuoto o con `/`. Se non funziona, Render potrebbe avere opzioni per "Background Worker" invece di "Web Service", che sono più adatti per bot che non espongono porte HTTP. *Aggiornamento: Per Render, se usi un "Web Service", si aspetta che qualcosa risponda sulla porta. Se il bot è solo un worker, potresti doverlo configurare come "Background Worker". Se lo configuri come "Web Service" e non hai un server HTTP, il deploy potrebbe avere problemi con gli health check. Il codice fornito non avvia un server HTTP.*
    *   **Start Command:** Di solito Render prende il `CMD` dal Dockerfile. Se necessario, puoi sovrascriverlo qui (es. `python bot.py`).

8.  **Clicca su "Create Web Service".**

Render inizierà il processo di pulling dell'immagine da Docker Hub e avvierà il container. Potrai vedere i log del deployment e dell'applicazione nel dashboard di Render.

## Comandi del Bot

*   `/start` - Messaggio di benvenuto.
*   `/barzelletta` (o `/joke`) - Invia una barzelletta casuale.

## Struttura dei File

```
.
├── bot.py            # Logica principale del bot Telegram
├── Dockerfile        # Istruzioni per costruire l'immagine Docker
├── requirements.txt  # Dipendenze Python
└── README.md         # Questo file
```

---

Spero che questo ti aiuti a mettere online il tuo bot!