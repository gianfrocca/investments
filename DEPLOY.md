# 🚀 Guida Deployment - Investment Tracker

Guida completa al deployment dell'applicazione Investment Tracker su diverse piattaforme.

---

## 📋 Indice

1. [QNAP NAS](#-qnap-nas-deployment)
2. [Railway.app](#-railwayapp-deployment)
3. [VPS Server](#-vps-server-deployment)
4. [Synology NAS](#-synology-nas-deployment)
5. [Docker Desktop (Locale)](#-docker-desktop-locale)
6. [Troubleshooting](#-troubleshooting)

---

## 🏠 QNAP NAS Deployment

### Prerequisiti
- QNAP NAS con Container Station installato
- Almeno 4GB RAM disponibili
- QTS 5.0+ o QuTS hero

### Procedura

#### 1. Preparazione

**Via File Station:**
```
1. Crea cartella: /Container/investments
2. Carica tutti i file del progetto in questa cartella
3. Assicurati che la struttura sia:
   /Container/investments/
   ├── docker-compose.qnap.yml
   ├── backend/
   ├── frontend/
   ├── nginx/
   └── ...
```

#### 2. Configurazione

**Modifica `docker-compose.qnap.yml`:**

```yaml
# Trova e sostituisci questi valori:

# 1. Password database (2 posti)
POSTGRES_PASSWORD: MiaPasswordSicura123!
DATABASE_URL: postgresql://investmentuser:MiaPasswordSicura123!@db:5432/investments

# 2. Secret Key (genera con: openssl rand -hex 32)
SECRET_KEY: tua_chiave_random_32_caratteri

# 3. IP del NAS (2 posti)
BACKEND_CORS_ORIGINS: http://192.168.1.XXX:3000
REACT_APP_API_URL: http://192.168.1.XXX:8000
```

**Come trovare IP del NAS:**
```
QTS: Pannello Controllo → Rete → Interfacce
oppure
Router: Guarda i dispositivi connessi
```

#### 3. Deploy in Container Station

```
1. Apri Container Station
2. Click "Create" → "Create Application"
3. Nome: investment-tracker
4. Sorgente: Upload file
5. Seleziona: docker-compose.qnap.yml
6. Click "Validate" → Verifica nessun errore
7. Click "Create"
```

#### 4. Attendi Build

- Prima volta: **10-15 minuti**
- Container Station scaricherà le immagini
- Costruirà i container
- Attendi che tutti siano "Running" (verde)

#### 5. Accedi all'App

```
http://IP_DEL_NAS:3000

Esempio: http://192.168.1.50:3000
```

#### 6. Backup Automatici

I backup vengono salvati in: `/Container/investments/backups`

**Accedi via File Station** per scaricarli sul PC.

### Accesso Esterno (Opzionale)

**Per accedere da fuori casa:**

1. **Configura Port Forwarding sul router:**
   ```
   Porta esterna 8080 → IP_NAS:80
   Porta esterna 8443 → IP_NAS:443
   ```

2. **Configura DDNS:**
   - QTS: Pannello Controllo → Accesso Esterno → DDNS
   - Crea hostname: tuonome.myqnapcloud.com

3. **Accedi da fuori:**
   ```
   http://tuonome.myqnapcloud.com:8080
   ```

---

## 🚂 Railway.app Deployment

Railway è perfetto per test rapidi e deployment cloud.

### Prerequisiti
- Account GitHub con il repository
- Account Railway.app (gratis con $5 credito)

### Procedura

#### 1. Setup Repository

```bash
git clone <your-repo>
cd investments
```

#### 2. Deploy su Railway

**Via Dashboard:**

```
1. Vai su https://railway.app
2. Login con GitHub
3. "New Project" → "Deploy from GitHub repo"
4. Seleziona repository: investments
5. Railway rileva automaticamente i Dockerfile
```

#### 3. Aggiungi Database

```
1. Nel progetto Railway, click "+ New"
2. Seleziona "Database" → "PostgreSQL"
3. Railway genera automaticamente DATABASE_URL
```

#### 4. Configura Backend Service

```
1. Click sul servizio "backend"
2. Tab "Variables"
3. Aggiungi:

SECRET_KEY=<genera-con-openssl-rand-hex-32>
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
BACKEND_CORS_ORIGINS=https://<frontend-url-railway>
ALPHA_VANTAGE_API_KEY=demo
APP_NAME=Investment Tracker
ENVIRONMENT=production
DEBUG=false
```

#### 5. Configura Frontend Service

```
1. Click sul servizio "frontend"
2. Variables:

REACT_APP_API_URL=https://<backend-url-railway>
```

#### 6. Deploy

```
Railway fa auto-deploy ad ogni push su GitHub!
```

#### 7. Accedi

```
Railway genera URL pubblici tipo:
Backend:  https://investment-backend-production-xxxx.railway.app
Frontend: https://investment-frontend-production-xxxx.railway.app
```

### Note Railway

- **Storage**: Effimero (dati persi al restart) - Usa PostgreSQL Railway per persistenza
- **Backup**: Disabilitato di default, usa export manuale via UI
- **Costo**: ~$5-10/mese dopo credito gratuito
- **SSL**: Automatico ✅

---

## 🖥️ VPS Server Deployment

Deployment su server Linux (Ubuntu/Debian) - DigitalOcean, Linode, Hetzner, AWS EC2, etc.

### Prerequisiti
- VPS con Ubuntu 22.04+ o Debian 11+
- Almeno 2GB RAM (consigliato 4GB)
- Dominio (opzionale, per HTTPS)

### Procedura Completa

#### 1. Prepara Server

```bash
# SSH nel server
ssh root@your-server-ip

# Aggiorna sistema
apt update && apt upgrade -y

# Installa Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh

# Installa Docker Compose
apt install docker-compose -y

# Verifica installazione
docker --version
docker-compose --version
```

#### 2. Setup Progetto

```bash
# Crea directory
mkdir -p /opt/investment-tracker
cd /opt/investment-tracker

# Clona repository
git clone <your-repo-url> .

# Oppure upload via SFTP
```

#### 3. Configurazione

```bash
# Crea file .env
cp .env.example .env

# Modifica configurazione
nano .env
```

**Valori minimi da configurare:**

```env
# Database
POSTGRES_USER=investmentuser
POSTGRES_PASSWORD=<password-sicura-qui>
POSTGRES_DB=investments
DATABASE_URL=postgresql://investmentuser:<password>@db:5432/investments

# Security
SECRET_KEY=<genera-con-openssl-rand-hex-32>
ALGORITHM=HS256

# CORS - Usa il tuo dominio
BACKEND_CORS_ORIGINS=https://tuodominio.com,http://your-server-ip

# App
ENVIRONMENT=production
DEBUG=false
```

**Genera SECRET_KEY:**
```bash
openssl rand -hex 32
```

#### 4. Deploy Applicazione

```bash
# Usa il docker-compose per VPS
docker-compose -f docker-compose.vps.yml up -d

# Verifica status
docker-compose -f docker-compose.vps.yml ps

# Vedi logs
docker-compose -f docker-compose.vps.yml logs -f
```

#### 5. Configura Firewall

```bash
# Ubuntu UFW
ufw allow 22/tcp    # SSH
ufw allow 80/tcp    # HTTP
ufw allow 443/tcp   # HTTPS
ufw enable
```

#### 6. Setup HTTPS con Let's Encrypt

**Se hai un dominio:**

```bash
# 1. Punta il dominio al server (DNS A record)
# Dominio: tuodominio.com → IP: your-server-ip

# 2. Ottieni certificato SSL
docker-compose -f docker-compose.vps.yml run --rm certbot certonly \
  --webroot \
  -w /var/www/certbot \
  -d tuodominio.com \
  -d www.tuodominio.com \
  --email tua@email.com \
  --agree-tos \
  --no-eff-email

# 3. Modifica nginx/nginx.conf
nano nginx/nginx.conf

# Decomment la sezione HTTPS server
# Sostituisci "your-domain.com" con "tuodominio.com"

# 4. Restart nginx
docker-compose -f docker-compose.vps.yml restart nginx
```

#### 7. Backup Automatico

```bash
# Setup cron per backup giornaliero
crontab -e

# Aggiungi questa riga (backup ogni giorno alle 2 AM)
0 2 * * * cd /opt/investment-tracker && docker-compose -f docker-compose.vps.yml exec -T db pg_dump -U investmentuser investments | gzip > /opt/investment-tracker/backups/backup_$(date +\%Y\%m\%d).sql.gz
```

#### 8. Accedi

```
http://your-server-ip        # HTTP
https://tuodominio.com       # HTTPS (dopo setup SSL)
```

### Manutenzione VPS

**Aggiorna applicazione:**
```bash
cd /opt/investment-tracker
git pull
docker-compose -f docker-compose.vps.yml down
docker-compose -f docker-compose.vps.yml build
docker-compose -f docker-compose.vps.yml up -d
```

**Backup manuale:**
```bash
docker-compose -f docker-compose.vps.yml exec db pg_dump -U investmentuser investments > backup.sql
```

**Restore database:**
```bash
docker-compose -f docker-compose.vps.yml exec -T db psql -U investmentuser investments < backup.sql
```

**Vedi logs:**
```bash
docker-compose -f docker-compose.vps.yml logs -f backend
docker-compose -f docker-compose.vps.yml logs -f frontend
```

---

## 💾 Synology NAS Deployment

### Prerequisiti
- Synology NAS con DSM 7.0+
- Docker package installato
- Almeno 4GB RAM

### Procedura

#### 1. Installa Docker

```
1. Apri Package Center
2. Cerca "Docker"
3. Installa
```

#### 2. Prepara File

```
1. Apri File Station
2. Crea cartella: /docker/investments
3. Upload tutti i file del progetto
```

#### 3. Modifica Configurazione

**File da modificare: `docker-compose.yml`**

Via File Station → Edit, oppure SSH:

```bash
ssh admin@synology-ip
sudo -i
cd /volume1/docker/investments
nano .env
```

Modifica password e SECRET_KEY come per QNAP.

#### 4. Deploy con Docker Compose

**Via Terminal/SSH:**

```bash
cd /volume1/docker/investments
docker-compose up -d
```

**Via Docker UI:**

```
1. Apri Docker app
2. Tab "Container"
3. Import docker-compose.yml
4. Start
```

#### 5. Port Mapping

```
Verifica in Docker → Container che le porte siano mappate:
3000 → Frontend
8000 → Backend
5432 → PostgreSQL (opzionale)
```

#### 6. Accesso Esterno

**Reverse Proxy Synology:**

```
1. Pannello Controllo → Portale Applicazioni → Reverse Proxy
2. Crea nuova regola:
   - Nome: Investment Tracker
   - Protocollo: HTTP
   - Porta: 80
   - Backend: localhost:3000
```

---

## 🐳 Docker Desktop (Locale)

Per sviluppo o test in locale su Windows/Mac.

### Procedura

```bash
# 1. Clona repository
git clone <repo-url>
cd investments

# 2. Configura .env
cp .env.example .env
nano .env  # Modifica password

# 3. Avvia
docker-compose up -d

# 4. Accedi
# http://localhost:3000
```

**Windows**: Usa Docker Desktop
**Mac**: Usa Docker Desktop o Colima
**Linux**: Docker Engine nativo

---

## 🔧 Troubleshooting

### Errore: "env file not found"

**Soluzione 1 - QNAP/Synology:**
Usa `docker-compose.qnap.yml` con variabili hardcoded

**Soluzione 2:**
```bash
# Crea .env nella directory corretta
cd /path/to/investments
cp .env.example .env
nano .env
```

### Errore: "port already in use"

```bash
# Trova processo che usa la porta
lsof -i :3000
lsof -i :8000

# Killa il processo
kill -9 <PID>

# Oppure cambia porta in docker-compose.yml
ports:
  - "3001:3000"  # Usa 3001 invece di 3000
```

### Backend non si connette al database

```bash
# Verifica database running
docker ps | grep postgres

# Vedi logs database
docker logs investment_db

# Restart database
docker-compose restart db

# Attendi 10 secondi poi restart backend
docker-compose restart backend
```

### Frontend non carica

```bash
# Rebuild frontend
docker-compose build --no-cache frontend
docker-compose up -d frontend

# Vedi logs
docker logs -f investment_frontend
```

### Errore "Secret Key not set"

```bash
# Genera SECRET_KEY
openssl rand -hex 32

# Aggiungila al .env
echo "SECRET_KEY=<output-comando-sopra>" >> .env

# Restart backend
docker-compose restart backend
```

### Backup fallisce

```bash
# Verifica permessi directory
chmod 755 backups/

# Backup manuale
docker exec investment_db pg_dump -U investmentuser investments > backup.sql
```

### Reset completo (ATTENZIONE: cancella dati!)

```bash
docker-compose down -v
docker-compose up -d
# Attendi 30 secondi per inizializzazione database
```

---

## 📊 Confronto Piattaforme

| Piattaforma | Difficoltà | Costo/mese | HTTPS | Backup | Consigliato per |
|-------------|------------|------------|-------|--------|-----------------|
| **QNAP** | Media | €0 (hai NAS) | Manuale | Locale | Chi ha già NAS |
| **Synology** | Media | €0 (hai NAS) | Auto | Locale | Chi ha già NAS |
| **Railway** | Facile | $5-10 | Auto | Limitato | Test rapido |
| **VPS** | Media-Alta | $4-10 | Manuale | Completo | Production seria |
| **Locale** | Facile | €0 | No | No | Sviluppo |

---

## 🎯 Raccomandazioni Finali

**Per uso personale casa:**
→ QNAP o Synology NAS

**Per test rapido online:**
→ Railway.app

**Per production seria:**
→ VPS con HTTPS

**Per sviluppo:**
→ Docker Desktop locale

---

## 📞 Supporto

**Problemi comuni:** Consulta README.md sezione Troubleshooting

**Documentazione API:** http://your-url:8000/docs

**Logs in real-time:**
```bash
docker-compose logs -f
```

---

**Buon deployment! 🚀**
