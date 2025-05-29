# Bot Telegram Barzellette (Jokebot)

Questo è un semplice bot Telegram che racconta barzellette recuperandole da un'API esterna ([Official Joke API](https://official-joke-api.appspot.com/)).

**ATTENZIONE:** Il token del bot Telegram è attualmente inserito direttamente nel file `bot.py`. Questa pratica non è sicura per repository pubblici o per ambienti di produzione. Si consiglia vivamente di utilizzare variabili d'ambiente per gestire i token in scenari reali.

## Prerequisiti

*   Python 3.7+
*   Docker (per il build dell'immagine)
*   Un account Telegram e un token per il bot (ottenibile da @BotFather su Telegram)

## Configurazione del Token

Il token del bot è hardcodato nel file `bot.py`:
```python
TELEGRAM_BOT_TOKEN = "IL_TUO_TOKEN_QUI" # Sostituito con il token reale
```
Se devi cambiarlo, modifica questa riga direttamente nel file `bot.py`.

## Esecuzione Locale (Senza Docker)

1.  **Clona il repository (o crea i file):**
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

4.  **Avvia il bot:**
    ```bash
    python bot.py
    ```

## Creazione dell'Immagine Docker e Push su Docker Hub

1.  **Assicurati che Docker sia in esecuzione.**

2.  **Naviga nella directory del progetto** (dove si trovano `Dockerfile`, `bot.py`, `requirements.txt`).

3.  **Build dell'immagine Docker:**
    Sostituisci `tuoutentedockerhub` con il tuo username di Docker Hub (es. `terceros`) e `nomeimmaginebot` con il nome della tua immagine (es. `jokebot`).
    ```bash
    docker build -t tuoutentedockerhub/nomeimmaginebot:latest .
    ```
    Esempio per te:
    ```bash
    docker build -t terceros/jokebot:latest .
    ```

4.  **Login su Docker Hub (se non l'hai già fatto):**
    ```bash
    docker login -u tuoutentedockerhub
    ```
    Esempio per te:
    ```bash
    docker login -u terceros
    ```
    Ti verranno chiesti username e password.

5.  **Push dell'immagine su Docker Hub:**
    ```bash
    docker push tuoutentedockerhub/nomeimmaginebot:latest
    ```
    Esempio per te:
    ```bash
    docker push terceros/jokebot:latest
    ```

## Deployment su Render

Render può deployare direttamente da un'immagine Docker ospitata su Docker Hub.

1.  **Crea un account su [Render](https://render.com/) se non ne hai uno.**

2.  **Nel dashboard di Render, clicca su "New +" e seleziona "Web Service".**

3.  **Scegli "Deploy an existing image from a registry".**
    *   **Image Path:** Inserisci il percorso della tua immagine su Docker Hub (es. `terceros/jokebot:latest`).

4.  **Dai un nome al tuo servizio** (es. `jokebot-service`).

5.  **Variabili d'Ambiente:**
    *   Con il token hardcodato nel codice, **non è più necessario impostare** `TELEGRAM_BOT_TOKEN` nelle variabili d'ambiente di Render.

6.  **Instance Type:** Per un bot semplice come questo, il piano gratuito ("Free") dovrebbe essere sufficiente.

7.  **Start Command:** Render dovrebbe prendere il `CMD` dal Dockerfile (`python bot.py`). Non dovrebbe essere necessario modificarlo.

8.  **Clicca su "Create Web Service".**

Render inizierà il processo di pulling dell'immagine da Docker Hub e avvierà il container. Potrai vedere i log del deployment e dell'applicazione nel dashboard di Render.

## Comandi del Bot

*   `/start` - Messaggio di benvenuto.
*   `/barzelletta` (o `/joke`) - Invia una barzelletta casuale.

## Struttura dei File

```
.
├── bot.py            # Logica principale del bot Telegram (con token hardcodato)
├── Dockerfile        # Istruzioni per costruire l'immagine Docker
├── requirements.txt  # Dipendenze Python
└── README.md         # Questo file
```