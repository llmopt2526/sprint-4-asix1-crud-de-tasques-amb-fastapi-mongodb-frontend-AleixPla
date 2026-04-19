const formulari = document.getElementById('formulari-pelicules');
const llistaPelicules = document.getElementById('llista-pelicules');
const API_URL = 'http://127.0.0.1:8000/pelicules/';

let peliculesActuals = [];

// Comprovem si tenim connexió amb el servidor
async function carregarPelicules() {
    try {
        const resposta = await fetch(API_URL);
        if (resposta.ok) {
            peliculesActuals = await resposta.json();
            llistaPelicules.innerHTML = '';
            peliculesActuals.forEach(pelicula => afegirPeliculaAlDOM(pelicula));
        }
    } catch (error) {
        console.error("Error carregar dades:", error);
    }
}

// Comprovem les id que tenen les pel·lícules
function afegirPeliculaAlDOM(pelicula) {
    const peliId = pelicula.id || pelicula._id;
    const novaPelicula = document.createElement('div');
    novaPelicula.classList.add('pelicula-card');

// Funció per a crear una nova pel·lícula amb la seva respectiva infomració del seu respectiu camp + boton d'editar i esborrar
    novaPelicula.innerHTML = `
        <h3>${pelicula.titol}</h3>
        <p><strong> Descripció:</strong> ${pelicula.descripcio}</p>
        <p><strong> Estat:</strong> ${pelicula.estat}</p>
        <p><strong> Puntuació:</strong> ${pelicula.puntuacio} / 5</p>
        <p><strong> Gènere:</strong> ${pelicula.genere}</p>
        <p><strong> Usuari:</strong> ${pelicula.usuari}</p>

        <div class="accions-targeta">
            <button class="btn-editar" onclick="prepararEdicio('${peliId}')"> Editar</button>
            <button class="btn-esborrar" onclick="esborrarPelicula('${peliId}')"> Esborrar</button>
        </div>
    `;
    llistaPelicules.appendChild(novaPelicula);
}

// Funció per guardar o editar
formulari.addEventListener('submit', async function (e) {
    e.preventDefault();
    const idActiu = document.getElementById('pelicula-id').value;
    const dades = {
        titol: document.getElementById('titol').value,
        descripcio: document.getElementById('descripcio').value,
        estat: document.getElementById('estat').value,
        puntuacio: parseInt(document.getElementById('puntuacio').value),
        genere: document.getElementById('genere').value,
        usuari: document.getElementById('usuari').value
    };

    try {
        const method = idActiu ? 'PUT' : 'POST';
        const url = idActiu ? API_URL + idActiu : API_URL;

        const res = await fetch(url, {
            method: method,
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(dades)
        });

        if (res.ok) {
            cancelarEdicio();
            carregarPelicules();
        }
    } catch (e) { console.error(e); }
});

// Fem que esborri la pel·lícula, i que mostri un "alert" de que si estas segur d'esborrar-la
async function esborrarPelicula(id) {
    if (confirm("Estas segur?")) {
        await fetch(API_URL + id, { method: "DELETE" });
        carregarPelicules();
    }
}

// Omplim totes les caselles del formulari 
function prepararEdicio(id) {
    const p = peliculesActuals.find(p => (p.id === id || p._id === id));
    document.getElementById("pelicula-id").value = id;
    document.getElementById("titol").value = p.titol;
    document.getElementById("descripcio").value = p.descripcio;
    document.getElementById("estat").value = p.estat;
    document.getElementById("puntuacio").value = p.puntuacio;
    document.getElementById("genere").value = p.genere;
    document.getElementById("usuari").value = p.usuari;

// Cambiem l'aspecte del formulari per a que sigui més clar
    document.getElementById("titol-formulari").innerText = "Editar pel·lícula";
    document.getElementById("btn-guardar").innerText = "Actualitzar pel·lícula";
    document.getElementById("btn-guardar").style.backgroundColor = "#ffc107";
    document.getElementById("btn-guardar").style.color = "black";
    document.getElementById("btn-cancelar").style.display = "block";
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

// A l'hora d'editar una pel·lícula, fem que cancel·li l'edició
function cancelarEdicio() {
    formulari.reset();
    document.getElementById("pelicula-id").value = "";
    document.getElementById("titol-formulari").innerText = "Afegir pel·lícula";
    document.getElementById("btn-guardar").innerText = "Guardar la pel·lícula";
    document.getElementById("btn-guardar").style.backgroundColor = "#28a745";
    document.getElementById("btn-guardar").style.color = "white";
    document.getElementById("btn-cancelar").style.display = "none";
}

carregarPelicules();
