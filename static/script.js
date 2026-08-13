// 1. Initialisation des variables avec sauvegarde locale (localStorage)
let depenses = JSON.parse(localStorage.getItem('depenses')) || [];
let totalDepenses = 0;
let chartInstance = null;

// Éléments du DOM
const form = document.getElementById('expense-form');
const descriptionInput = document.getElementById('description');
const montantInput = document.getElementById('montant');
const categorieSelect = document.getElementById('categorie');
const expenseList = document.getElementById('expense-list');
const totalAmountDisplay = document.getElementById('total-amount');
const exportBtn = document.getElementById('export-btn');

// 2. Sauvegarde dans localStorage
function sauvegarderDonnees() {
    localStorage.setItem('depenses', JSON.stringify(depenses));
}

// 3. Ajouter une dépense
function ajouterDepense(description, montant, categorie) {
    depenses.push({ description, montant: parseFloat(montant), categorie });
    sauvegarderDonnees();
    mettreAJourPage();
}

// 4. Supprimer une dépense
function supprimerDepense(index) {
    depenses.splice(index, 1);
    sauvegarderDonnees();
    mettreAJourPage();
}

// 5. Afficher la liste et calculer le total
function afficherDepenses() {
    expenseList.innerHTML = '';
    totalDepenses = 0;

    depenses.forEach((depense, index) => {
        totalDepenses += depense.montant;

        const li = document.createElement('li');
        li.innerHTML = `
            <span><strong>${depense.description}</strong> (${depense.categorie}) : ${depense.montant.toFixed(2)} RON</span>
            <button class="delete-btn" onclick="supprimerDepense(${index})">X</button>
        `;
        expenseList.appendChild(li);
    });

    totalAmountDisplay.textContent = totalDepenses.toFixed(2);
}

// 6. Mise à jour du graphique (Chart.js)
function mettreAJourGraphique() {
    const ctx = document.getElementById('expenseChart').getContext('2d');

    // Regroupement des montants par catégorie
    const categoriesTotaux = {};
    depenses.forEach(d => {
        categoriesTotaux[d.categorie] = (categoriesTotaux[d.categorie] || 0) + d.montant;
    });

    const labels = Object.keys(categoriesTotaux);
    const data = Object.values(categoriesTotaux);

    if (chartInstance) {
        chartInstance.destroy();
    }

    chartInstance = new Chart(ctx, {
        type: 'pie',
        data: {
            labels: labels,
            datasets: [{
                data: data,
                backgroundColor: ['#3498db', '#e74c3c', '#2ecc71', '#f1c40f', '#9b59b6']
            }]
        }
    });
}

// 7. Exportation au format CSV
function exporterCSV() {
    if (depenses.length === 0) return alert("Aucune dépense à exporter.");

    let csvContent = "data:text/csv;charset=utf-8,Description,Montant (RON),Categorie\n";
    depenses.forEach(d => {
        csvContent += `"${d.description}",${d.montant},"${d.categorie}"\n`;
    });

    const encodedUri = encodeURI(csvContent);
    const link = document.createElement("a");
    link.setAttribute("href", encodedUri);
    link.setAttribute("download", "depenses.csv");
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
}

// Fonction globale de rafraîchissement
function mettreAJourPage() {
    afficherDepenses();
    mettreAJourGraphique();
}

// Événements
form.addEventListener('submit', (e) => {
    e.preventDefault();
    ajouterDepense(descriptionInput.value, montantInput.value, categorieSelect.value);
    form.reset();
});

exportBtn.addEventListener('click', exporterCSV);

// Initialisation au chargement de la page
mettreAJourPage();
