# 🚀 Quick Start Guide

Inizia in 5 minuti!

## Prerequisiti

- Docker e Docker Compose installati
- 4GB RAM liberi
- Porte 80, 443, 3000, 8000 disponibili

## Avvio Rapido

```bash
# 1. Copia e configura environment
cp .env.example .env

# 2. Genera una SECRET_KEY sicura
echo "SECRET_KEY=$(openssl rand -hex 32)" >> .env

# 3. Modifica password database (opzionale ma consigliato)
nano .env  # Cambia POSTGRES_PASSWORD

# 4. Avvia tutto
docker-compose up -d

# 5. Attendi che i servizi si avviino (30-60 secondi)
docker-compose logs -f backend

# Quando vedi "Application startup complete", premi Ctrl+C e continua
```

## Primo Accesso

1. Apri browser: **http://localhost:3000**
2. Clicca su "Register here"
3. Crea il tuo account:
   - Username: `admin`
   - Email: `admin@example.com`
   - Password: `password123` (cambiala dopo!)
4. Login automatico → Dashboard

## Crea il Primo Portfolio

1. Menu → **Portfolios**
2. Clicca **+ New Portfolio**
3. Nome: "Il mio portfolio principale"
4. Salva

## Import Transazioni

### Opzione A: Import da Trade Republic

1. Esporta CSV da Trade Republic app
2. Menu → **Import**
3. Seleziona il portfolio
4. Tipo: "Trade Republic"
5. Upload CSV → Import

### Opzione B: Dati di esempio

Crea file `test_transactions.csv`:

```csv
date,symbol,name,type,quantity,price,fees,currency
2024-01-15,AAPL,Apple Inc.,buy,10,150.50,1.99,USD
2024-01-20,MSFT,Microsoft Corp.,buy,5,380.75,1.99,USD
2024-02-01,AAPL,Apple Inc.,dividend,10,0.24,0,USD
```

Upload questo file con tipo "Generic CSV"

## Aggiorna Prezzi

1. Vai al tuo portfolio
2. Clicca **🔄 Update Prices**
3. Attendi 10-20 secondi
4. Ricarica pagina → Prezzi aggiornati!

## 🎉 Fatto!

Ora puoi:
- ✅ Vedere il valore totale del portfolio
- ✅ Monitorare gain/loss per asset
- ✅ Aggiungere nuove transazioni
- ✅ Esportare backup

## Comandi Utili

```bash
# Visualizza logs
docker-compose logs -f

# Restart applicazione
docker-compose restart

# Stop tutto
docker-compose down

# Reset completo (ATTENZIONE: cancella dati!)
docker-compose down -v
docker-compose up -d

# Backup manuale database
docker-compose exec db pg_dump -U investmentuser investments > backup.sql
```

## Troubleshooting Rapido

**Backend errore "database connection"**
```bash
docker-compose restart db
sleep 10
docker-compose restart backend
```

**Frontend non carica**
```bash
docker-compose logs frontend
# Se vedi errori di npm, rebuilda:
docker-compose build --no-cache frontend
docker-compose up -d frontend
```

**Porta già in uso**
```bash
# Modifica docker-compose.yml
# Cambia "3000:3000" in "3001:3000"
# Poi accedi a http://localhost:3001
```

## Prossimi Passi

1. Leggi [README.md](README.md) per configurazione completa
2. Configura HTTPS per production
3. Setup backup automatici
4. Ottieni API keys per dati di mercato migliori

**Buon tracking! 📈**
