# 📈 Investment Tracker

Un'applicazione web completa e sicura per monitorare i tuoi investimenti in tempo reale. Multi-utente, con supporto per import da Trade Republic, aggiornamento automatico dei prezzi e backup robusti.

## ✨ Caratteristiche Principali

- 🔐 **Multi-utente** - Sistema di autenticazione JWT sicuro
- 📊 **Portfolio multipli** - Gestisci più portafogli separati
- 💹 **Aggiornamento prezzi real-time** - Integrazione con Yahoo Finance
- 📥 **Import CSV** - Importa transazioni da Trade Republic o CSV generico
- 💾 **Backup automatici** - Sistema di backup robusto con retention configurabile
- 📱 **Responsive** - Interfaccia ottimizzata per desktop e mobile
- 🐳 **Docker-ready** - Deploy semplice con Docker Compose
- 🔒 **HTTPS support** - Configurazione SSL/TLS con Let's Encrypt

## 🏗️ Architettura

```
Backend:   FastAPI + PostgreSQL
Frontend:  React
Proxy:     Nginx
Container: Docker Compose
```

## 📋 Prerequisiti

- Docker & Docker Compose
- (Opzionale) Dominio per HTTPS
- (Opzionale) API keys per dati di mercato (Alpha Vantage, Twelve Data)

## 🚀 Installazione Rapida

### 1. Clona il repository

```bash
git clone <repository-url>
cd investments
```

### 2. Configura l'ambiente

```bash
cp .env.example .env
```

Modifica `.env` con i tuoi parametri:

```env
# Database
POSTGRES_USER=investmentuser
POSTGRES_PASSWORD=CAMBIAMI_PASSWORD_SICURA
POSTGRES_DB=investments

# Security
SECRET_KEY=CAMBIAMI_GENERA_CHIAVE_RANDOM
# Genera con: openssl rand -hex 32

# API Keys (opzionali ma consigliati)
ALPHA_VANTAGE_API_KEY=tua_chiave
TWELVE_DATA_API_KEY=tua_chiave
```

### 3. Avvia l'applicazione

```bash
# Build e start containers
docker-compose up -d

# Verifica lo stato
docker-compose ps

# Visualizza logs
docker-compose logs -f
```

### 4. Accedi all'applicazione

- **Frontend**: http://localhost:3000
- **API Docs**: http://localhost:8000/docs
- **API**: http://localhost:8000/api

## 📦 Deploy su Server Web (VPS)

### Configurazione per Production

1. **Prepara il server**

```bash
# Su server Ubuntu/Debian
apt update && apt upgrade -y
apt install docker.io docker-compose git -y
systemctl enable docker
systemctl start docker
```

2. **Clona e configura**

```bash
git clone <repository-url> /opt/investment-tracker
cd /opt/investment-tracker
cp .env.example .env
nano .env  # Configura con i tuoi parametri
```

3. **Configura HTTPS con Let's Encrypt**

Modifica `nginx/nginx.conf`:
- Decomment la sezione HTTPS server
- Sostituisci `your-domain.com` con il tuo dominio

```bash
# Ottieni certificato SSL
docker run -it --rm \
  -v $(pwd)/certbot/conf:/etc/letsencrypt \
  -v $(pwd)/certbot/www:/var/www/certbot \
  certbot/certbot certonly --webroot \
  -w /var/www/certbot \
  -d tuodominio.com \
  --email tua@email.com \
  --agree-tos
```

4. **Avvia in production**

```bash
# Modifica .env
ENVIRONMENT=production
DEBUG=false

# Start
docker-compose up -d

# Setup auto-renewal certificati
crontab -e
# Aggiungi: 0 0 * * * docker-compose run --rm certbot renew
```

## 🏠 Deploy su NAS (Synology/QNAP)

### Synology DSM 7+

1. **Installa Docker** da Package Center

2. **Upload progetto**

```bash
# Via SSH o FileStation
# Upload in /volume1/docker/investment-tracker/
```

3. **Configura**

```bash
cd /volume1/docker/investment-tracker
cp .env.example .env
vi .env  # Configura
```

4. **Avvia con Docker Compose**

- Apri Docker app in DSM
- Vai su Project
- Importa docker-compose.yml
- Start

### Accesso esterno

1. **Configura Port Forwarding** sul router:
   - Porta 80 → IP NAS:80
   - Porta 443 → IP NAS:443

2. **Configura DDNS** (es. Synology DDNS o NoIP)

3. **Ottieni certificato SSL** tramite DSM Control Panel

## 📊 Utilizzo

### Primo Accesso

1. Registra un nuovo account su `/register`
2. Login su `/login`
3. Crea il tuo primo portfolio

### Import da Trade Republic

1. Vai su **Import** nel menu
2. Seleziona il portfolio
3. Scegli "Trade Republic" come tipo
4. Upload del file CSV esportato da Trade Republic

**Come ottenere il CSV da Trade Republic:**
- Apri Trade Republic app
- Vai su Profilo → Documenti
- Scarica "Transazioni" in formato CSV

### Formato CSV Trade Republic

```csv
Date,Time,Type,Symbol,ISIN,Quantity,Price,Total,Currency,Notes
2024-01-15,10:30:00,BUY,AAPL,US0378331005,10,150.50,1505.00,USD,Purchase
```

### Import Generico

Formato CSV supportato:

```csv
date,symbol,name,type,quantity,price,fees,currency
2024-01-15,AAPL,Apple Inc.,buy,10,150.50,1.99,USD
```

### Aggiornamento Prezzi

- **Manuale**: Clicca "🔄 Update Prices" nella pagina portfolio
- **Automatico**: Configura `PRICE_UPDATE_INTERVAL_MINUTES` in `.env`

API supportate:
- Yahoo Finance (default, gratuito)
- Alpha Vantage (richiede API key)
- Twelve Data (richiede API key)

### Backup & Restore

#### Export dati

```bash
# Via interfaccia web
Dashboard → Backup → Download Backup

# Via API
curl -X GET http://localhost:8000/api/backup/export/all \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -o backup.json
```

#### Backup automatico database

Configurato automaticamente tramite cron in `.env`:

```env
BACKUP_ENABLED=true
BACKUP_SCHEDULE=0 2 * * *  # Ogni giorno alle 2 AM
BACKUP_RETENTION_DAYS=30
```

#### Restore manuale

```bash
# Restore da file JSON
Dashboard → Backup → Restore Backup

# Restore database
docker-compose exec db psql -U $POSTGRES_USER -d $POSTGRES_DB < backup.sql
```

## 🔧 Configurazione Avanzata

### Variabili Ambiente

```env
# Application
APP_NAME=Investment Tracker
ENVIRONMENT=production
DEBUG=false

# Database
DATABASE_URL=postgresql://user:pass@db:5432/investments

# Security
SECRET_KEY=your-secret-key-32-chars-min
ACCESS_TOKEN_EXPIRE_MINUTES=30

# CORS
BACKEND_CORS_ORIGINS=http://localhost:3000,https://yourdomain.com

# Price Updates
PRICE_UPDATE_INTERVAL_MINUTES=15
PRICE_UPDATE_ENABLED=true

# Backup
BACKUP_ENABLED=true
BACKUP_RETENTION_DAYS=30
```

### API Endpoints Principali

- `POST /api/auth/register` - Registrazione utente
- `POST /api/auth/login` - Login
- `GET /api/portfolios/` - Lista portfolios
- `GET /api/assets/portfolio/{id}` - Assets di un portfolio
- `POST /api/import/trade-republic/{id}` - Import Trade Republic
- `POST /api/prices/update-portfolio/{id}` - Update prezzi
- `GET /api/backup/export/all` - Export dati

Documentazione completa: http://localhost:8000/docs

## 🔒 Sicurezza

### Best Practices Implementate

- ✅ Password hashing con bcrypt
- ✅ JWT token authentication
- ✅ HTTPS/TLS support
- ✅ Rate limiting su Nginx
- ✅ SQL injection protection (SQLAlchemy ORM)
- ✅ XSS protection
- ✅ CORS configuration
- ✅ Environment variables per secrets

### Raccomandazioni

1. **Cambia SEMPRE le password di default**
2. **Usa password robuste** (min 12 caratteri)
3. **Genera SECRET_KEY random**: `openssl rand -hex 32`
4. **Abilita HTTPS in production**
5. **Backup regolari** (automatici + manuali periodici)
6. **Aggiorna regolarmente** le dipendenze
7. **Limita accesso database** solo da backend

## 🐛 Troubleshooting

### Backend non si avvia

```bash
# Controlla logs
docker-compose logs backend

# Verifica database connection
docker-compose exec backend python -c "from app.database import engine; engine.connect()"
```

### Frontend non carica

```bash
# Rebuild frontend
docker-compose build frontend
docker-compose up -d frontend

# Verifica proxy Nginx
docker-compose logs nginx
```

### Database connection failed

```bash
# Verifica stato database
docker-compose ps db

# Reset database
docker-compose down -v
docker-compose up -d db
# Aspetta 10 secondi
docker-compose up -d backend
```

### Import CSV fallisce

- Verifica formato CSV
- Controlla encoding (deve essere UTF-8)
- Verifica separatori (virgola)
- Controlla logs backend per errori specifici

## 📈 Roadmap Futuro

Funzionalità pianificate per sviluppi futuri:

- [ ] Analisi ML/AI per raccomandazioni
- [ ] Notifiche push (email/mobile)
- [ ] App mobile (React Native)
- [ ] Grafici avanzati (Chart.js)
- [ ] Multi-currency support avanzato
- [ ] Tax reporting
- [ ] Social features (condivisione portfolio)
- [ ] API pubbliche per integrazioni

## 🤝 Contribuire

Contributi benvenuti! Per maggiori funzionalità:

1. Fork del progetto
2. Crea feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push al branch (`git push origin feature/AmazingFeature`)
5. Apri Pull Request

## 📝 Licenza

Questo progetto è open source. Usalo come preferisci!

## 📧 Supporto

Per domande o problemi:
- Apri una Issue su GitHub
- Consulta la documentazione API: http://localhost:8000/docs

---

**Disclaimer**: Questo software è fornito "as is" per scopi educativi e personali. Non fornisce consulenza finanziaria. Usa a tuo rischio e pericolo.
