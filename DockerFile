# Usa un'immagine Python ufficiale come base
FROM python:3.9-slim

# Imposta la directory di lavoro nel container
WORKDIR /app

# Copia il file delle dipendenze nella directory di lavoro
COPY requirements.txt .

# Installa le dipendenze
RUN pip install --no-cache-dir -r requirements.txt

# Copia il resto del codice dell'applicazione nella directory di lavoro
COPY bot.py .

# --- IMPORTANTE PER IL DEPLOYMENT ---
# Non includere il token direttamente qui.
# Su Render, imposterai TELEGRAM_BOT_TOKEN come variabile d'ambiente.
# ENV TELEGRAM_BOT_TOKEN="IL_TUO_TOKEN_QUI" # NON FARE QUESTO PER LA PRODUZIONE

# Comando per eseguire l'applicazione quando il container si avvia
CMD ["python", "bot.py"]