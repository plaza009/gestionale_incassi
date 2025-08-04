// Script personalizzato per Gestionale Incassi

// Funzione per inizializzare il sistema
document.addEventListener('DOMContentLoaded', function() {
    console.log('🚀 Gestionale Incassi - Sistema inizializzato');
    
    // Inizializza tutti i componenti
    initMobileSidebar();
    initFormValidation();
    initCalculations();
    initCharts();
    initTooltips();
    initAnimations();
});

// Gestione sidebar mobile
function initMobileSidebar() {
    const sidebarToggle = document.querySelector('.sidebar-toggle');
    const sidebar = document.querySelector('.sidebar');
    
    if (sidebarToggle && sidebar) {
        sidebarToggle.addEventListener('click', function() {
            sidebar.classList.toggle('show');
        });
        
        // Chiudi sidebar quando si clicca fuori
        document.addEventListener('click', function(e) {
            if (!sidebar.contains(e.target) && !sidebarToggle.contains(e.target)) {
                sidebar.classList.remove('show');
            }
        });
    }
}

// Validazione form
function initFormValidation() {
    const forms = document.querySelectorAll('form');
    
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            const requiredFields = form.querySelectorAll('[required]');
            let isValid = true;
            
            requiredFields.forEach(field => {
                if (!field.value.trim()) {
                    field.classList.add('is-invalid');
                    isValid = false;
                } else {
                    field.classList.remove('is-invalid');
                }
            });
            
            if (!isValid) {
                e.preventDefault();
                showAlert('⚠️ Compila tutti i campi obbligatori', 'warning');
            }
        });
    });
}

// Calcoli automatici
function initCalculations() {
    // Calcolo totale incasso
    const cashTotaleInput = document.getElementById('cash_totale');
    const fondoCassaInput = document.getElementById('fondo_cassa');
    const incassoPosInput = document.getElementById('incasso_pos');
    const prelievoInput = document.getElementById('prelievo_importo');
    const totaleDisplay = document.getElementById('totale_incasso');
    
    if (cashTotaleInput && fondoCassaInput && incassoPosInput && totaleDisplay) {
        function calcolaTotale() {
            const cashTotale = parseFloat(cashTotaleInput.value) || 0;
            const fondoCassa = parseFloat(fondoCassaInput.value) || 0;
            const incassoPos = parseFloat(incassoPosInput.value) || 0;
            const prelievo = parseFloat(prelievoInput?.value) || 0;
            
            const incassoCashEffettivo = cashTotale - fondoCassa;
            const totale = incassoPos + incassoCashEffettivo - prelievo;
            
            totaleDisplay.textContent = `€${totale.toFixed(2)}`;
            
            // Cambia colore se negativo
            if (totale < 0) {
                totaleDisplay.classList.add('text-danger');
            } else {
                totaleDisplay.classList.remove('text-danger');
            }
        }
        
        [cashTotaleInput, fondoCassaInput, incassoPosInput, prelievoInput].forEach(input => {
            if (input) {
                input.addEventListener('input', calcolaTotale);
            }
        });
        
        // Calcolo iniziale
        calcolaTotale();
    }
    
    // Calcolo banconote per movimenti cassaforte
    const importoInput = document.getElementById('importo');
    const moneteInput = document.getElementById('monete_importo');
    const banconoteInput = document.getElementById('banconote_importo');
    
    if (importoInput && moneteInput && banconoteInput) {
        function calcolaBanconote() {
            const importo = parseFloat(importoInput.value) || 0;
            const monete = parseFloat(moneteInput.value) || 0;
            const banconote = importo - monete;
            
            banconoteInput.value = banconote.toFixed(2);
        }
        
        importoInput.addEventListener('input', calcolaBanconote);
        moneteInput.addEventListener('input', calcolaBanconote);
    }
}

// Inizializzazione grafici
function initCharts() {
    const chartCanvas = document.getElementById('incomeChart');
    
    if (chartCanvas) {
        const ctx = chartCanvas.getContext('2d');
        
        // Dati del grafico (esempio)
        const chartData = {
            labels: ['Gen', 'Feb', 'Mar', 'Apr', 'Mag', 'Giu'],
            datasets: [{
                label: 'Incassi Mensili',
                data: [12000, 19000, 15000, 18000, 22000, 25000],
                backgroundColor: 'rgba(102, 126, 234, 0.2)',
                borderColor: 'rgba(102, 126, 234, 1)',
                borderWidth: 2,
                tension: 0.4
            }]
        };
        
        new Chart(ctx, {
            type: 'line',
            data: chartData,
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        position: 'top',
                    },
                    title: {
                        display: true,
                        text: 'Andamento Incassi'
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        ticks: {
                            callback: function(value) {
                                return '€' + value.toLocaleString();
                            }
                        }
                    }
                }
            }
        });
    }
}

// Inizializzazione tooltip
function initTooltips() {
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
}

// Animazioni
function initAnimations() {
    // Aggiungi classe fade-in agli elementi
    const elements = document.querySelectorAll('.card, .alert, .table');
    elements.forEach(element => {
        element.classList.add('fade-in');
    });
}

// Funzione per mostrare alert
function showAlert(message, type = 'info') {
    const alertContainer = document.createElement('div');
    alertContainer.className = `alert alert-${type} alert-dismissible fade show`;
    alertContainer.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    const container = document.querySelector('.container') || document.body;
    container.insertBefore(alertContainer, container.firstChild);
    
    // Auto-remove dopo 5 secondi
    setTimeout(() => {
        if (alertContainer.parentNode) {
            alertContainer.remove();
        }
    }, 5000);
}

// Funzione per conferma eliminazione
function confirmDelete(message = 'Sei sicuro di voler eliminare questo elemento?') {
    return confirm(message);
}

// Funzione per formattare numeri come valuta
function formatCurrency(amount) {
    return new Intl.NumberFormat('it-IT', {
        style: 'currency',
        currency: 'EUR'
    }).format(amount);
}

// Funzione per validare date
function isValidDate(dateString) {
    const date = new Date(dateString);
    return date instanceof Date && !isNaN(date);
}

// Funzione per calcolare differenza giorni
function daysDifference(date1, date2) {
    const oneDay = 24 * 60 * 60 * 1000;
    return Math.round(Math.abs((date1 - date2) / oneDay));
}

// Funzione per aggiornare badge notifiche
function updateNotificationBadge(count) {
    const badge = document.querySelector('.notification-badge');
    if (badge) {
        badge.textContent = count;
        badge.style.display = count > 0 ? 'inline' : 'none';
    }
}

// Funzione per toggle sidebar su mobile
function toggleSidebar() {
    const sidebar = document.querySelector('.sidebar');
    if (sidebar) {
        sidebar.classList.toggle('show');
    }
}

// Funzione per export dati
function exportData(format = 'csv') {
    const table = document.querySelector('table');
    if (!table) return;
    
    let csv = '';
    const rows = table.querySelectorAll('tr');
    
    rows.forEach(row => {
        const cols = row.querySelectorAll('td, th');
        const rowData = [];
        cols.forEach(col => {
            rowData.push('"' + col.textContent.trim() + '"');
        });
        csv += rowData.join(',') + '\n';
    });
    
    const blob = new Blob([csv], { type: 'text/csv' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'export_' + new Date().toISOString().split('T')[0] + '.csv';
    a.click();
    window.URL.revokeObjectURL(url);
}

// Funzione per ricerca in tempo reale
function initRealTimeSearch() {
    const searchInput = document.getElementById('searchInput');
    const tableRows = document.querySelectorAll('tbody tr');
    
    if (searchInput) {
        searchInput.addEventListener('input', function() {
            const searchTerm = this.value.toLowerCase();
            
            tableRows.forEach(row => {
                const text = row.textContent.toLowerCase();
                if (text.includes(searchTerm)) {
                    row.style.display = '';
                } else {
                    row.style.display = 'none';
                }
            });
        });
    }
}

// Funzione per ordinamento tabelle
function initTableSorting() {
    const sortableHeaders = document.querySelectorAll('th[data-sort]');
    
    sortableHeaders.forEach(header => {
        header.addEventListener('click', function() {
            const column = this.dataset.sort;
            const table = this.closest('table');
            const tbody = table.querySelector('tbody');
            const rows = Array.from(tbody.querySelectorAll('tr'));
            
            rows.sort((a, b) => {
                const aValue = a.querySelector(`td[data-${column}]`)?.textContent || '';
                const bValue = b.querySelector(`td[data-${column}]`)?.textContent || '';
                return aValue.localeCompare(bValue);
            });
            
            // Rimuovi righe esistenti
            rows.forEach(row => row.remove());
            
            // Aggiungi righe ordinate
            rows.forEach(row => tbody.appendChild(row));
        });
    });
}

// Inizializzazione completa
document.addEventListener('DOMContentLoaded', function() {
    initRealTimeSearch();
    initTableSorting();
    
    // Aggiungi event listener per export
    const exportBtn = document.getElementById('exportBtn');
    if (exportBtn) {
        exportBtn.addEventListener('click', () => exportData());
    }
});

// Utility per debug
window.debugGestionale = {
    showAlert,
    formatCurrency,
    isValidDate,
    daysDifference,
    updateNotificationBadge,
    toggleSidebar,
    exportData
}; 