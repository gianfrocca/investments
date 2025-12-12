# 🚀 Guida al Deploy su Coolify

Ho preparato la tua applicazione per il deploy su Coolify. Ecco i passaggi per completare l'operazione.

## 1. Push delle Modifiche (GIÀ FATTO ✅)

I file aggiornati (`frontend/Dockerfile.production` e `docker-compose.coolify.yml`) sono già stati caricati sul tuo GitHub. Non devi fare nulla qui.

## 2. Configurazione su Coolify

1. **Crea Nuova Risorsa**: 
   - Vai su Coolify dashboard -> Seleziona il tuo server -> `+ New Resource`
   - Scegli `Git Repository` -> `Public Repository` (o Private se lo è).
   - Incolla l'URL del tuo repo GitHub.

2. **Configurazione Build Pack**:
   - Quando Coolify ti chiede il tipo di build, seleziona **Docker Compose**.
   - Nel campo "Docker Compose Location", inserisci: `/docker-compose.coolify.yml` (il file che ho creato apposta per Coolify).

3. **Variabili d'Ambiente (.env)**:
   Nell'interfaccia di Coolify, vai su **Environment Variables** e aggiungi queste chiavi (copia i valori dal tuo `.env` locale o generane di nuovi):

   ```env
   # Database
   POSTGRES_USER=investmentuser
   POSTGRES_PASSWORD=una_password_molto_sicura
   POSTGRES_DB=investments

   # Security
   SECRET_KEY=una_chiave_segreta_random_32_caratteri
   
   # App URL (IMPORTANTE: l'URL dove sarà raggiungibile la tua app)
   REACT_APP_API_URL=https://tua-app.tuo-dominio.com/api
   
   # Altre opzioni
   ENVIRONMENT=production
   BACKUP_ENABLED=true
   ```

4. **Network & Domains**:
   - Vai su **Settings** (o Configuration) del servizio su Coolify.
   - Nella sezione **Domains**, imposta il tuo dominio (es. `https://investments.tuodominio.com`).
   - Assicurati che "Port" sia impostato su `80`. Coolify girerà il traffico lì, e il nostro container `nginx` lo smisterà internamente.

5. **Deploy**:
   - Clicca su **Deploy**.

## 🚀 Cosa abbiamo migliorato?

*   **Dockerfile**: Ora accetta `REACT_APP_API_URL` durante la build. Questo significa che il frontend saprà esattamente dove trovare il backend in produzione, senza cercare `localhost`.
*   **Docker Compose**: Ho creato una versione specifica che rimuove i conflitti di porta 80/443 (che servono a Coolify) e rimuove Certbot (perché Coolify ci regala l'SSL automatico!).
