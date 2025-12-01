const music = document.getElementById('bg-music');
const btn = document.getElementById('music-btn');
music.volume = 0.3;

function toggleMusic() {
    if (music.paused) {
        music.play().then(() => {
            btn.innerText = "PAUSE";
            btn.style.color = "#00f3ff";
            btn.style.textShadow = "0 0 5px #00f3ff";
        }).catch(e => console.log("Interacción requerida para audio"));
    } else {
        music.pause();
        btn.innerText = "PLAY";
        btn.style.color = "white";
        btn.style.textShadow = "none";
    }
}

function setVolume(val) {
    music.volume = val;
}

// Intentar reproducir al primer click en la página
document.body.addEventListener('click', () => {
    if(music.paused && btn.innerText.includes("PLAY")) {
        toggleMusic();
    }
}, { once: true });

// Exponer funciones al scope global para que funcionen los onclick del HTML
window.toggleMusic = toggleMusic;
window.setVolume = setVolume;
