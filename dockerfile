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

# Comando per eseguire l'applicazione con Gunicorn.
# Gunicorn si aspetta il formato modulo:variabile_app (il nostro file è bot.py, la variabile Flask app è 'app').
# Render imposta la variabile d'ambiente PORT. Gunicorn la userà.
# Aumentato il timeout per dare più tempo alle richieste iniziali o a quelle più lente.
CMD ["gunicorn", "--bind", "0.0.0.0:$PORT", "--workers", "1", "--timeout", "120", "bot:app"]