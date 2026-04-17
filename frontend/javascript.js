const formulari = document.getElementById('formulari-pelicules');
const llistaPelicules = document.getElementById('llista-pelicules');
const API_URL = 'http://127.0.0.1:8000/pelicules/'; // La URL del teu backend

// 1. Funció per carregar les pel·lícules de MongoDB quan obrim la pàgina
async function carregarPelicules() {
    try {
        const resposta = await fetch(API_URL);
        if (resposta.ok) {
            const pelicules = await resposta.json();
            llistaPelicules.innerHTML = ''; // Buidem la llista abans d'omplir-la

            // Per cada pel·lícula que ve de MongoDB, la pintem a la web
            pelicules.forEach(pelicula => {
                afegirPeliculaAlDOM(pelicula);
            });
        }
    } catch (error) {
        console.error("No s'ha pogut connectar amb el backend per carregar dades:", error);
    }
}

// 2. Funció auxiliar que reutilitza el teu codi per crear les targetes HTML
function afegirPeliculaAlDOM(pelicula) {
    const novaPelicula = document.createElement('div');
    novaPelicula.classList.add('pelicula-card');
    novaPelicula.innerHTML = `
        <h3>${pelicula.titol}</h3>
        <p><strong>Descripció:</strong> ${pelicula.descripcio}</p>
        <p><strong>Estat:</strong> ${pelicula.estat}</p>
        <p><strong>Puntuació:</strong> ${pelicula.puntuacio} / 5</p>
        <p><strong>Gènere:</strong> ${pelicula.genere}</p>
        <p><strong>Usuari:</strong> ${pelicula.usuari}</p>
    `;
    llistaPelicules.appendChild(novaPelicula);
}

// 3. Quan l'usuari clica "Guardar"
formulari.addEventListener('submit', async function (event) {
    event.preventDefault();

    // Recollim les dades dels inputs
    const novaPelicula = {
        titol: document.getElementById('titol').value,
        descripcio: document.getElementById('descripcio').value,
        estat: document.getElementById('estat').value,
        puntuacio: parseInt(document.getElementById('puntuacio').value), // Important: convertir a número
        genere: document.getElementById('genere').value,
        usuari: document.getElementById('usuari').value
    };

    try {
        // Enviem les dades al backend amb un POST
        const resposta = await fetch(API_URL, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(novaPelicula)
        });

        if (resposta.ok) {
            // Si el backend ens diu que tot bé (Codi 201), agafem la peli creada...
            const peliculaGuardada = await resposta.json();
            // ...la pintem a la llista...
            afegirPeliculaAlDOM(peliculaGuardada);
            // ...i buidem el formulari
            formulari.reset();
        } else {
            alert("Hi ha hagut un error guardant la pel·lícula. Revisa que les dades siguin correctes.");
        }
    } catch (error) {
        console.error("Error enviant les dades:", error);
        alert("Error de connexió. Recorda connectar el BACKEND");
    }
});

// 4. Executem la funció de càrrega només obrir la pàgina
carregarPelicules();
