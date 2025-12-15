import React, { createContext, useState, useContext } from 'react';

const translations = {
    en: {
        dashboard: 'Dashboard',
        portfolios: 'Portfolios',
        import: 'Import',
        backup: 'Backup',
        logout: 'Logout',
        totalPortfolioValue: 'Total Portfolio Value',
        totalInvested: 'Total Invested',
        totalGainLoss: 'Total Gain/Loss',
        yourPortfolios: 'Your Portfolios',
        managePortfolios: 'Manage Portfolios',
        noPortfolios: 'No portfolios yet. Create your first portfolio to get started!',
        createPortfolio: 'Create Portfolio',
        loading: 'Loading...',
        assets: 'Assets',
        value: 'Value',
        actions: 'Actions',
        newPortfolio: '+ New Portfolio',
        cancel: 'Cancel',
        createNewPortfolio: 'Create New Portfolio',
        portfolioName: 'Portfolio Name',
        description: 'Description (optional)',
        backToPortfolios: '← Back to Portfolios',
        updatePrices: '🔄 Update Prices',
        updating: 'Updating...',
        addAsset: '+ Add Asset',
        addNewAsset: 'Add New Asset',
        symbol: 'Symbol (Ticker)',
        name: 'Name',
        type: 'Type',
        quantity: 'Quantity',
        avgPrice: 'Average Buy Price (€)',
        currentPrice: 'Current Price',
        gainLoss: 'Gain/Loss',
        noAssets: 'No assets in this portfolio. Import transactions or add assets manually.',
        priceUpdateStarted: 'Price update started! Refresh the page in a few moments.',
        failedToLoad: 'Failed to load',
        delete: 'Delete',
        areYouSureDelete: 'Are you sure you want to delete this portfolio?',
        successCreated: 'Portfolio created successfully!',
        successDeleted: 'Portfolio deleted successfully',
    },
    it: {
        dashboard: 'Dashboard',
        portfolios: 'Portafogli',
        import: 'Importa',
        backup: 'Backup',
        logout: 'Esci',
        totalPortfolioValue: 'Valore Totale Portafoglio',
        totalInvested: 'Totale Investito',
        totalGainLoss: 'Totale Gu/Pe',
        yourPortfolios: 'I tuoi Portafogli',
        managePortfolios: 'Gestisci Portafogli',
        noPortfolios: 'Nessun portafoglio. Creane uno per iniziare!',
        createPortfolio: 'Crea Portafoglio',
        loading: 'Caricamento...',
        assets: 'Asset',
        value: 'Valore',
        actions: 'Azioni',
        newPortfolio: '+ Nuovo Portafoglio',
        cancel: 'Annulla',
        createNewPortfolio: 'Crea Nuovo Portafoglio',
        portfolioName: 'Nome Portafoglio',
        description: 'Descrizione (opzionale)',
        backToPortfolios: '← Torna ai Portafogli',
        updatePrices: '🔄 Aggiorna Prezzi',
        updating: 'Aggiornamento...',
        addAsset: '+ Aggiungi Asset',
        addNewAsset: 'Aggiungi Nuovo Asset',
        symbol: 'Simbolo (Ticker)',
        name: 'Nome',
        type: 'Tipo',
        quantity: 'Quantità',
        avgPrice: 'Prezzo Medio Acquisto (€)',
        currentPrice: 'Prezzo Attuale',
        gainLoss: 'Gu/Pe',
        noAssets: 'Nessun asset. Importa transazioni o aggiungi manualmente.',
        priceUpdateStarted: 'Aggiornamento prezzi avviato! Aggiorna la pagina tra poco.',
        failedToLoad: 'Caricamento fallito',
        delete: 'Elimina',
        areYouSureDelete: 'Sei sicuro di voler eliminare questo portafoglio?',
        successCreated: 'Portafoglio creato con successo!',
        successDeleted: 'Portafoglio eliminato con successo',
    }
};

const LanguageContext = createContext();

export const LanguageProvider = ({ children }) => {
    const [language, setLanguage] = useState('it'); // Default to Italian

    const t = (key) => {
        return translations[language][key] || key;
    };

    return (
        <LanguageContext.Provider value={{ language, setLanguage, t }}>
            {children}
        </LanguageContext.Provider>
    );
};

export const useLanguage = () => useContext(LanguageContext);
